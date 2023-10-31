from typing import List, Dict, Union, Callable
from abc import ABC, abstractmethod
import mystring, uuid, threading, os, sys, splych

try: #Python2
    import __builtin__ as builtins
except:
    import builtins

class RepoSifting(object):
    def __init__(self):
        self.uuid = mystring.string.of(str(uuid.uuid4()))
        self.stage = None

    def staticKeyTypeMap(self) -> Dict[str, type]:
        return {
            **{
                "uuid": mystring.string,
                "stage": mystring.string,
            },
            **self._internal_staticKeyTypeMap()
        }

    @staticmethod
    @abstractmethod
    def _internal_staticKeyTypeMap() -> Dict[str, type]:
        pass

    def toMap(self) -> Dict[str, Union[str, int, bool]]:
        #https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python
        #return {a:getattr(self,a) for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))}
        output:Dict[str, Union[str, int, bool]] = {}
        for key in self.staticKeyTypeMap().keys():
            output[key] = getattr(self,key)
        return output

    @property
    def frame(self):
        return mystring.frame.from_arr([self.toMap()])

    @property
    def jsonString(self):
        import json
        return json.dumps(self.toMap())

    @property
    def base64JsonString(self):
        import json
        return mystring.string.of(json.dumps(self.toMap())).tobase64(prefix=True)

    @property
    def csvString(self):
        #https://stackoverflow.com/questions/9157314/how-do-i-write-data-into-csv-format-as-string-not-file
        import csv,io
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(self.toMap().values())
        return output.getvalue()
    
    @property
    def csvHeader(self):
        #https://stackoverflow.com/questions/9157314/how-do-i-write-data-into-csv-format-as-string-not-file
        import csv,io
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(self.staticKeyTypeMap.keys())
        return output.getvalue()

    @property
    def csvStrings(self):
        #https://stackoverflow.com/questions/9157314/how-do-i-write-data-into-csv-format-as-string-not-file
        import csv,io
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        for value in self.toMap().values():
            writer.writerow(value)
        return output.getvalue()


class RepoObject(RepoSifting):
    def __init__(self, path: mystring.string, hash: mystring.string, content: mystring.string, hasVuln: bool, cryVulnId: int, langPattern: mystring.string = None, file_scan_lambda: mystring.string = None):
        super().__init__()
        self.path = path
        self.file_scan_lambda = file_scan_lambda
        self.hash = hash
        self._content = content
        self.hasVuln = hasVuln
        self.cryVulnId = cryVulnId
        self.langPattern = langPattern

    @property
    def is_dir(self):
        return os.path.isdir(self.path)

    @staticmethod
    def str_type(self):
        return "dir" if self.is_dir else "file"

    @staticmethod
    def _internal_staticKeyTypeMap() -> Dict[str, type]:
        return {
            "path": mystring.string,
            "hash": mystring.string,
            "_content": mystring.string,
            "hasVuln": bool,
            "cryVulnId": int,
            "langPattern": mystring.string,
            "file_scan_lambda": Callable[str, bool]
        }

    def updateContent(self, newContent:mystring.string):
        self._content = newContent
        return self._content

    @property
    def content(self):
        return self._content
    
    @property
    def contentb64(self):
        return self._content.tobase64()


class RepoResultObject(RepoSifting):
    def __init__(self, projecttype: str, projectname: str, projecturl: str, qual_name: str, tool_name: str, Program_Lines: int, Total_Lines: int, Number_of_Imports: int, MCC: int, IsVuln: bool, ruleID: int, cryptolationID: int, CWEId: int, Message: str, Exception:str, llmPrompt:str, llmResponse:str, extraToolInfo:str, fileContent:str, Line: int, correctedCode:str, severity: str=None, confidence: str=None, context: str=None, TP: int=0, FP: int=0, TN: int=0, FN: int=0, dateTimeFormat:str="ISO 8601", startDateTime:str=None, endDateTime:str=None, stage:str=None):
        super().__init__()
        self.projecttype = projecttype
        self.projectname = projectname
        self.projecturl = projecturl

        self.qual_name = qual_name
        self.tool_name = tool_name

        self.Program_Lines = Program_Lines
        self.Total_Lines = Total_Lines
        self.Number_of_Imports = Number_of_Imports
        self.MCC = MCC
        self.fileContent = fileContent

        self.IsVuln = IsVuln
        self.ruleID = ruleID
        self.cryptolationID = cryptolationID
        self.CWEId =  CWEId
        self.Message = Message
        self.Line = Line
        self.correctedCode = correctedCode
        self.severity = severity
        self.confidence = confidence
        self.context = context

        self.Exception = Exception
        self.extraToolInfo = extraToolInfo

        self.llmPrompt = llmPrompt
        self.llmResponse = llmResponse
        self.TP = TP
        self.FP = FP
        self.TN = TN
        self.FN = FN

        self.dateTimeFormat=dateTimeFormat
        self.startDateTime = startDateTime
        self.endDateTime = endDateTime
        self.stage = stage

    @staticmethod
    def newEmpty(projecttype: str,projectname: str,projecturl: str,qual_name: str,tool_name: str,ExceptionMsg:str=None,stage:str=None,startDateTime:str=None,endDateTime:str=None):
        return RepoResultObject(
            projecttype=projecttype,
            projectname=projectname,
            projecturl=projecturl,
            qual_name=qual_name,
            tool_name=tool_name,
            Program_Lines=None,
            Total_Lines=None,
            Number_of_Imports=None,
            MCC=None,
            IsVuln=False,
            ruleID=None,
            cryptolationID=None,
            CWEId=None,
            Message=None,
            Exception=ExceptionMsg,
            llmPrompt=None,
            llmResponse=None,
            extraToolInfo=None,
            fileContent=None,
            Line=None,
            correctedCode=None,
            severity=None,
            confidence=None,
            context=None,
            TP=0,
            FP=0,
            TN=0,
            FN=0,
            dateTimeFormat="ISO 8601",
            startDateTime=startDateTime,
            endDateTime=endDateTime,
            stage=stage
        )

    @staticmethod
    def _internal_staticKeyTypeMap() -> Dict[str, type]:
        return {
            "projecttype": str,
            "projectname": str,
            "projecturl": str,
            "qual_name": str,
            "tool_name": str,
            "Program_Lines": int,
            "Total_Lines": int,
            "Number_of_Imports": int,
            "MCC": int,
            "IsVuln": bool,
            "ruleID": int,
            "cryptolationID": int,
            "CWEId": int,
            "Message": str,
            "Exception":str,
            "llmPrompt":str,
            "llmResponse":str,
            "extraToolInfo":str,
            "fileContent":str,
            "Line": int,
            "correctedCode":str,
            "severity": str,
            "confidence": str,
            "context": str,
            "TP": int,
            "FP": int,
            "TN": int,
            "FN": int,
            "dateTimeFormat":str,
            "startDateTime":str,
            "endDateTime":str,
            "stage":str
        };

    @staticmethod
    def fromCSVLine(line:mystring.string) -> Union[any,None]:
        numAttributes:int = len(RepoResultObject.staticKeyTypeMap().keys())
        splitLine:List[str] = [x.strip() for x in line.split(",")]

        if len(splitLine) != numAttributes:
            return None

        info:Dict[str, any] = {}
        for keyitr,key,value in enumerate(RepoResultObject.staticKeyTypeMap().items()):
            info[key] = getattr(builtins,value)(splitLine[keyitr])

        return RepoResultObject(**info)


class CoreObject(ABC):
    def __init__(self):
        self.imports = []
        import sys;self.executable = sys.executable

    def installImports(self) -> bool:
        if not hasattr(self, "imports"):
            setattr(self, "imports", [])

        cmd = mystring.string.of("{0} -m pip install {1}".format(sys.executable, ' '.join(self.imports)))
        try:
            if len(self.imports) > 0:
                cmd.exec()
            return True
        except:
            return False

    @abstractmethod
    def initialize(self)->bool:
        pass

    @abstractmethod
    def name(self) -> mystring.string:
        pass

    @abstractmethod
    def clean(self) -> bool:
        pass


class Runner(CoreObject):
    @abstractmethod
    def scan(self,filePath: str) -> List[RepoResultObject]:
        pass

class Envelop(CoreObject):
    @abstractmethod
    def per_next_repo_obj(self,repo_object: RepoObject):
        pass

    @abstractmethod
    def per_repo_obj_scan(self,repo_object: RepoObject, runner:Runner):
        pass

    @abstractmethod
    def per_repo_obj_scan_result(self,repo_object: RepoResultObject, runner:Runner):
        pass

class EnvelopSet(object):
    def __init__(self, envelops=[]):
        self.envelops = envelops

    def __len__(self):
        return len(self.envelops)

    def add(self, envelop:Envelop):
        envelop.initialize()
        self.envelops += [envelop]

    def per_next_repo_obj(self,repo_object: RepoObject):
        for envelop in self.envelops:
            try:
                envelop.per_next_repo_obj(repo_object)
            except:pass

    def per_repo_obj_scan(self,repo_object: RepoObject, runner:Runner):
        for envelop in self.envelops:
            try:
                envelop.per_repo_obj_scan(repo_object, runner)
            except:pass

    def per_repo_obj_scan_result(self,repo_object: RepoResultObject, runner:Runner):
        for envelop in self.envelops:
            try:
                envelop.per_repo_obj_scan_result(repo_object, runner)
            except:pass

class Logger(CoreObject):
    def __init__(self):
        super().__init__()
        self.stage:mystring.string = None
        self.general_prefix = None

    @abstractmethod
    def message(self, msg:mystring.string)->bool:
        pass

    @abstractmethod
    def emergency(self, msg:mystring.string)->bool:
        pass

    @abstractmethod
    def parameter(self,parameter:RepoObject)->bool:
        pass

    @abstractmethod
    def result(self,result:RepoResultObject)->bool:
        pass

    def file_size_limit_bytes(self)->float:
        return float('inf')

    def break_file_down(self, file_path:str)->List[str]:
        file_size = os.path.getsize(file_path)
        if file_size < self.file_size_limit_bytes:
            return [file_path]

        if not file_path.endswith(".zip"):
            import hugg
            zyp_container = hugg.zyp(file_path+".zip")
            zyp_container[file_path] = file_path
            file_path = zyp_container.location

        return splych.file_split(file_path, chunk_size=self.file_size_limit_bytes, delete_original=True)

    def file_name(self, result:RepoSifting, extraString:str='', prefix:str='', suffix:str=".txt", newFile:bool=True)->str:
        current_file = mystring.string.of("{0}_{1}_{2}_{3}".format(
            prefix,
            result.uuid,
            extraString,
            suffix
        ))
        if self.general_prefix:
            current_file = mystring.string.of("{0}_{1}".format(self.general_prefix, current_file))

        if newFile:
            ktr = 0
            while os.path.exists(current_file):
                current_file = current_file.replace(suffix, "_{0}{1}".format(ktr, suffix))
                ktr += 1

        return current_file

    def start(self, stage:mystring.string):
        self.stage = stage
        self.send(":>␍ Entering the stage: {0}".format(self.stage))
        return self

    def send(self, msg:Union[mystring.string, RepoObject, RepoResultObject])->bool:
        successful = True
        try:
            if isinstance(msg, RepoResultObject):
                self.result(msg)
            elif isinstance(msg, RepoObject):
                self.parameter(msg)
            else: #if isinstance(msg, mystring.string):
                self.message(msg)
        except Exception as e:
            print("Problem Sending Log From {0}; {1}".format(self.name(), msg.__class__.__name__))
            successful = False
        return successful

    def stop(self):
        self.send(":>␌ Exiting the stage: {0}".format(self.stage))
        return self


class LoggerSet(object):
    def __init__(self, loggers=[], stage:str=None,log_debug_messages=False):
        self.loggers = loggers
        self.stage = stage
        self.log_debug_messages = log_debug_messages

    def __len__(self):
        return len(self.loggers)

    def add(self, logger:Logger):
        self.loggers += [logger]

    def set_prefix(self, general_prefix:mystring.string):
        for logger in self.loggers:
            logger.general_prefix = general_prefix
        return self

    def start(self, stage:mystring.string):
        for logger in self.loggers:
            if self.log_debug_messages:logger.send(":>␋ sending to logger")
            logger.start(self.stage or stage)
            if self.log_debug_messages:logger.send(":>␋ ^^^^^ sending to logger")
        return self

    def send(self, msg:Union[mystring.string, RepoObject, RepoResultObject], is_debug:bool=False)->bool:
        if is_debug and self.log_debug_messages or not is_debug:
            for logger in self.loggers:
                if self.log_debug_messages:logger.send(":>␈ sending to logger")
                logger.send(msg)
                if self.log_debug_messages:logger.send(":>␈ end sending to logger")
        return self

    def emergency(self, msg:mystring.string)->bool:
        for logger in self.loggers:
            logger.emergency(msg)

    def stop(self):
        for logger in self.loggers:
            if self.log_debug_messages:logger.send(":>␇ sending to logger")
            logger.stop()
            if self.log_debug_messages:logger.send(":>␇ end sending to logger")
        return self

    def __enter__(self, stage:Union[mystring.string, None]=None):
        stage = self.stage or stage
        self.start(stage=stage)
        return self

    def __exit__(self, _type=None, value=None, traceback=None):
        self.stop()


class RepoObjectProvider(CoreObject):
    @property
    @abstractmethod
    def RepoObjects(self) -> List[RepoObject]:
        pass


class contextString(object):
    def __init__(self, lines=List[str], vulnerableLine:str=None, imports:List[str] = []):
        self.lines:List[str] = lines
        self.vulnerableLine:str = vulnerableLine
        self.imports = imports

    @staticmethod
    def fromString(context:str) -> any:
        lines:List[str] = []
        vulnerableLine:str = None
        imports:List[str] = []

        for line in context.split("\n"):
            #001:       println("1")
            #002:       println("1") #!
            num:int = line.split(":")[0]
            content:str = line.split(":")[1]
            vulnerable:bool = content.endswith("#!")

            if vulnerable and vulnerableLine is None:
                vulnerableLine = content

            rawcontent:str = content.replace(line.strip(),'')
            whitespace:str = content.replace(rawcontent,'')
            isImport:bool = "import" in rawcontent
            if isImport:
                imports += [rawcontent]

            lines += [{
                "RawLine":line,
                "LineNum":num,
                "RawContent":rawcontent,
                "IsVulnerable":vulnerable,
                "Whitespace":whitespace,
                "IsImport":isImport
            }]
        
        return contextString(lines=lines, vulnerableLine=vulnerableLine, imports=imports)

    def toString(self) -> str:
        output = []

        for line in self.lines:
            output += "#{0}:{1}{2} {3}".format(
                line['LineNum'],
                line['Whitespace'],
                line['RawContent'],
                '#!' if line['IsVulnerable'] else ''
            )

        return '\n'.join(output)


class GenProcedure(ABC):
    """
class operation(structure.GenProcedure):
	def __init__(self):
		super().__init__(
			fileProviders = [
				SingleFile.app(content="import os,sys;print('Hello World')")
			],
			runners = [
				simple.app(),
			],
			loggersset = [
				Printr.app(),
			],
			perScan = None,
			stage = None
		)

	def run_procedure(self):
		with structure.LoggerSet(loggers=self.loggerSet.loggers, stage="StageOne") as logggg:
			for runnerSvr in self.runners:
				with self.getRunnerProcedure(runnerSvr) as runner:
					for fileObj in self.RepoObjects:
						firstScanResults: List[RepoResultObject] = self.scan(fileObj, runner())
		return

operation().run_procedure()
# or operation()()
    """
    def __init__(self, fileProviders:List[RepoObjectProvider], runners:List[Runner], loggersset:List[Logger]=[], enveloperset:List[Envelop]=[], perScan:Union[Callable, None] = None, general_prefix:Union[str, None]=None, log_debug_messages:bool=False):
        self.fileProviders = fileProviders
        self.runners = runners

        self.perScan = perScan
        self.stage = None
        #https://superfastpython.com/asyncio-async-with/
        self.loggerSet = LoggerSet(log_debug_messages = log_debug_messages)
        for logger in loggersset:
            self.loggerSet.add(logger)
        
        self.envelopSet = EnvelopSet()
        for envelop in enveloperset:
            self.envelopSet.add(envelop)

        for big_list in (fileProviders + runners + loggersset + enveloperset):
            if isinstance(big_list, list):
                for core in big_list:
                    core.installImports()
            else:
                big_list.installImports()
        
        if general_prefix:
            self.loggerSet.set_prefix(general_prefix)

    def log(self, msg:Union[mystring.string, RepoObject, RepoResultObject]):
        self.loggerSet.send(msg)

    @property
    def RepoObjects(self) -> List[RepoObject]:
        for fileProvider in self.fileProviders:
            for RepoObj in fileProvider.RepoObjects:
                self.envelopSet.per_next_repo_obj(RepoObj)
                yield RepoObj

    def __enter__(self):
        if self.stage:
            self.loggerSet.start(stage=self.stage)
        return self

    def __exit__(self, _type=None, value=None, traceback=None):
        if self.stage:
            self.loggerSet.end()
        return self

    @property
    def getRunnerProcedure(self):
        class RunnerProcedure(object):
            def __init__(self, runner:Runner, loggerSet, scanr):
                self.runner = runner
                self.loggerSet = loggerSet
                self.scanFile = scanr

            def log(self, msg:Union[mystring.string, RepoObject, RepoResultObject]):
                self.loggerSet.send(":>␄ START LOG",is_debug=True)
                self.loggerSet.send(msg)
                self.loggerSet.send(":>␄ END LOG",is_debug=True)

            def __call__(self) -> Runner:
                return self.runner

            def scan(self, fileObj):
                self.scanFile(fileObj, self.runner)

            def __enter__(self):
                self.loggerSet.send(":>␅ START",is_debug=True)
                self.runner.initialize()
                self.loggerSet.send(":>␅ END START",is_debug=True)
                return self

            def __exit__(self, _type=None, value=None, traceback=None):
                self.loggerSet.send(":>␆ START",is_debug=True)
                self.runner.clean()

        return lambda runner:RunnerProcedure(runner=runner, loggerSet=self.loggerSet, scanr=self.scan)

    def process(self, isAliveMin:int=None):
        with LoggerSet(self.loggerSet.loggers, stage=":>. Starting the overall process") as logy:
            def alive(min:int=None, loggerSet=None):
                import time
                while True:
                    loggerSet.send(":> Still Alive")
                    time.sleep(60 * min)

            aliveThread = None
            if isAliveMin:
                aliveThread = threading.Thread(target=alive, args=(isAliveMin, self.loggerSet), daemon = True)
                aliveThread.start()

            try:
                logy.send(":> Starting the procedure",is_debug=True)
                self.run_procedure()
            except Exception as e:
                logy.emergency(":> Hit an unexpected error {0}".format(e))
            finally:
                logy.send(":> Closing the process",is_debug=True)
        sys.exit(0)

    def __call__(self):
        return self.run_procedure()

    @abstractmethod
    def run_procedure(self):
        pass

    def scan(self, repoObj:RepoObject, runner:Runner, stage:mystring.string=None, notHollow:bool=False)-> List[RepoResultObject]:
        self.envelopSet.per_repo_obj_scan(repoObj, runner)
        output:List[RepoResultObject] = []
        if repoObj.is_dir and repoObj.file_scan_lambda is not None:
            for root, dirs, files in os.walk(repoObj.path):
                for file in files:
                    full_file_path = os.path.join(root, file)
                    if repoObj.file_scan_lambda(full_file_path):
                        full_file_obj = foil(full_file_path, preload=True)
                        output += self.scanObj(obj = RepoObject(
                            path=full_file_path,
                            hash=full_file_obj.hash_content(),
                            content=full_file_obj.content,
                            hasVuln=None,
                            cryVulnId=-1,
                            langPattern=None,
                            file_scan_lambda=None
                        ), runner = runner, stage = stage, notHollow = notHollow)
        else:
            output = self.scanObj(obj = repoObj, runner = runner, stage = stage, notHollow = notHollow)
        
        for RepoResultObj in output:
            self.envelopSet.per_repo_obj_scan_result(repoObj, runner)
        
        return output

    def scanObj(self, obj:RepoObject, runner:Runner, stage:mystring.string=None, notHollow:bool=False)-> List[RepoResultObject]:
        from ephfile import ephfile

        exceptionString = None
        output:List[RepoResultObject] = []

        try:
            with LoggerSet(self.loggerSet.loggers, stage="␃ Scanning {0} with {1}".format(obj.path, runner.name())) as logy:
                logy.send("␀ Starting For Loop",is_debug=True)
                logy.send(obj)

                endTime=None

                if obj.content is None:
                    logy.send("␁ Started Scanning {0} {1}".format(obj.str_type, obj.path),is_debug=True)
                    try:
                        startTime:datetime.datetime = mystring.timestamp.now()
                        output = runner.scan(obj.path)
                        endTime:datetime.datetime = mystring.timestamp.now()
                    except Exception as e:
                        self.loggerSet.emergency(str(e))
                else:
                    with ephfile("{0}_stub.py".format(runner.name()), obj.content) as eph:
                        logy.send("␁ Started Scanning {0} {1}".format(obj.str_type, obj.path),is_debug=True)

                        try:
                            startTime:datetime.datetime = mystring.timestamp.now()
                            output = runner.scan(eph())
                            endTime:datetime.datetime = mystring.timestamp.now()
                        except Exception as e:
                            self.loggerSet.emergency(str(e))

                if endTime is None:
                    endTime = startTime

                resultObject: RepoResultObject
                for resultObject in output:
                    resultObject.startDateTime = startTime
                    resultObject.endDateTime = endTime
                    if stage:
                        resultObject.stage=stage
                    logy.send("␀ Starting Sending For Loop",is_debug=True)
                    logy.send(resultObject)
                    logy.send("␀ Ending Sending For Loop",is_debug=True)

                    logy.send("␂ Ended Scanning {0} {1}".format(str_type.is_dir, obj.path),is_debug=True)
        except Exception as e:
            exceptionString = str(e)

        if notHollow and len(output) == 0:
            output = [RepoResultObject.newEmpty(
                projecttype=obj.path,
                projectname=obj.path,
                projecturl=None,
                qual_name=None,
                tool_name=runner.name(),
                stage=stage,
                ExceptionMsg=exceptionString,
                startDateTime=None,
                endDateTime=None
            )]

        if self.perScan:
            self.perScan()
        return output
