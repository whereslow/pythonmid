import json
from dataclasses import dataclass

@dataclass
class pyTable:
    Id:int
    Type:str
    sonStruct:any
    propertys:list[str]
    code:str

@dataclass
class keywords:
    keyword:list[str]
    keywordMap:dict

def loadKeywordsFromJson(jsonPath):
    pass
def loadPyTableFromPython(pythonPath):
    pass
def loadPyTableFromJson(xmlPath):
    pass
def dumpPyTableToJson(pyTable,jsonPath):
    pass
def dumpPyTableToPython(pyTable,pythonPath):
    pass
def changePyTable(pyTable,changeDict):
    pass
def diffPyTable(pyTable1,pyTable2):
    pass