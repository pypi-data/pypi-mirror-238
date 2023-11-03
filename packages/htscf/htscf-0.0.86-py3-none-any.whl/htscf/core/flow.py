import re
from pathlib import Path
from subprocess import Popen, PIPE
from typing import Union
from uuid import uuid4

from htscf.db.mongo import connect
from htscf.utils.tools import writeScript, py2cmdline


class Workflow:
    def __init__(self,
                 rootPath: Union[Path, str],
                 stepIds: list[str],
                 dbName: str,
                 stepsCollectionName: str,
                 stepLogCollectionName: str,
                 settingsCollectionName: str,
                 host: str,
                 port: int,
                 flowId: str):
        self.stepsCollection = connect(dbName, stepsCollectionName, host, port)
        self.stepLogCollection = connect(dbName, stepLogCollectionName, host, port)
        self.settingsCollection = connect(dbName, settingsCollectionName, host, port)
        self.rootPath = Path(rootPath)
        self.rootPath.mkdir(exist_ok=True, parents=True)
        self.stepIds = stepIds
        self.flowId = flowId
        self.error = False
        self.logId = None

    def runStep(self, stepId: str):
        if self.logId and self.checkError():
            # 如果没有在上一步的日志中检测到"flow-exit-with-code-0",则退出
            raise Exception("上一步流程出错")
        stepsData = self.stepsCollection.find_one({
            "_id": stepId
        })
        settingsId = f"settings-{uuid4()}"  # 生成随机配置id
        self.settingsCollection.insert_one({
            "_id": settingsId,
            "data": stepsData["settings"]
        })
        programName = stepsData["program"]
        if programName in ["python", "python3"]:
            popen = Popen(
                py2cmdline(stepsData["script"], [
                    self.rootPath,  # 运行根目录
                    settingsId,  # 数据库中配置文件的ID
                    self.logId,  # 日志文件的ID
                    self.flowId  # 当前流程的ID
                ])
                , stdout=PIPE, stderr=PIPE, shell=True)
        else:
            popen = Popen([
                stepsData["program"],  # 运行的程序名
                writeScript(self.rootPath, stepsData["script"]),  # 执行的脚本路径
                self.rootPath,  # 运行根目录
                settingsId,  # 数据库中配置文件的ID
                self.logId,  # 日志文件的ID
                self.flowId  # 当前流程的ID
            ], stdout=PIPE, stderr=PIPE)
        popen.wait()
        self.logId = f"{stepId}-{uuid4()}"
        self.stepLogCollection.insert_one({
            "_id": self.logId,
            "data": popen.stdout.read().decode("utf-8"),
            "error": popen.stderr.read().decode("utf-8")
        })

    def checkError(self):
        prevLogData = self.stepLogCollection.find_one({
            "_id": self.logId,
        })["data"]
        if not re.search("flow-exit-with-code-0", prevLogData, re.S):
            return True
        return False

    def run(self):
        while self.stepIds:
            self.runStep(self.stepIds.pop(0))
