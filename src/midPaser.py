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
class midPaser:
    """代理keywords和做方法载体"""
    #def __init__(self,jsonPath) -> None:
    #    self.keywords = self.loadKeywordsFromJson(jsonPath)
    def loadKeywordsFromJson(jsonPath) -> keywords:
        keywordstruct = keywords()
        jsondict = json.load(jsonPath)
        for i in jsondict:
            keywordstruct.keyword.append(i['keyword'])
            keywordstruct.keywordMap.update({i['keyword']:i['Type']})
    def loadPyTableFromPython(pythonPath) -> pyTable:
        pass
    def loadPyTableFromJson(jsonPath) -> pyTable:
        pass
    def dumpPyTableToJson(pyTable,jsonPath) -> None:
        pass
    def dumpPyTableToPython(pyTable,pythonPath) -> None:
        pass
    def changePyTable(pyTable,changeDict) -> pyTable:
        pass
    def diffPyTable(pyTable1,pyTable2):#不太确定
        pass
    def vectorize(self,filename:str) ->list[str]:
        with open(filename,'r',encoding='utf-8') as f:
            fstrlist=f.read().replace('    ','^TAB ').replace("\n"," ").split(" ")
            try:
                while True:
                    fstrlist.remove('')
            except ValueError:
                pass
            # 控制流适配符号向量化处理
            i = 0
            while i!=len(fstrlist)-1:
                i+=1
                if ':' in fstrlist[i]:
                    temp = fstrlist[i].split(':')
                    if temp[0] != "" and temp[1] != "":
                        fstrlist.insert(i+1,temp[1])
                        fstrlist[i] = temp[0]
                    elif temp[0] != "" and temp[1] == "":
                        fstrlist[i] = fstrlist[i].replace(':', '')
                    elif temp[0] == "" and temp[1]!= "":
                        fstrlist[i] = fstrlist[i].replace(':', '')
                    elif temp[0] == "" and temp[1] == "":
                        del fstrlist[i]
                    else:
                        raise ValueError
                if '(' in fstrlist[i]:
                    temp = fstrlist[i].split('(')
                    if len(temp) > 2:
                        multiflag = True
                        for j in range(2,len(temp)):
                            temp[j]='('+temp[j]
                            temp[1]+=temp[j]
                    else:
                        multiflag = False
                    if temp[0] != "" and temp[1] != "":
                        del fstrlist[i]
                        fstrlist.insert(i,temp[1])
                        fstrlist.insert(i,'(')
                        fstrlist.insert(i,temp[0])
                        if multiflag:
                            i+=1
                        else:
                            i+=2
                    elif temp[0] != "" and temp[1] == "":
                        del fstrlist[i]
                        fstrlist.insert(i,'(')
                        fstrlist.insert(i,temp[0])
                        i+=1
                    elif temp[0] == "" and temp[1]!= "":
                        del fstrlist[i]
                        fstrlist.insert(i,temp[1])
                        fstrlist.insert(i,'(')
                        if multiflag:
                            i+=0
                        else:
                            i+=1
                    elif temp[0] == "" and temp[1] == "":
                        pass
                    else:
                        raise ValueError
                if ')' in fstrlist[i]:
                    temp = fstrlist[i].split(')')
                    if len(temp) > 2:
                        multiflag = True
                        for j in range(2,len(temp)):
                            temp[j]=')'+temp[j]
                            temp[1]+=temp[j]
                    else:
                        multiflag = False
                    if temp[0] != "" and temp[1] != "":
                        del fstrlist[i]
                        fstrlist.insert(i,temp[1])
                        fstrlist.insert(i,')')
                        fstrlist.insert(i,temp[0])
                        if multiflag:
                            i+=1
                        else:
                            i+=2
                    elif temp[0] != "" and temp[1] == "":
                        del fstrlist[i]
                        fstrlist.insert(i,')')
                        fstrlist.insert(i,temp[0])
                        i+=1
                    elif temp[0] == "" and temp[1]!= "":
                        del fstrlist[i]
                        fstrlist.insert(i,temp[1])
                        fstrlist.insert(i,')')
                        if multiflag:
                            i+=0
                        else:
                            i+=1
                    elif temp[0] == "" and temp[1] == "":
                        pass
                    else:
                        raise ValueError
            return fstrlist
    def parse(self,code:str):
        pass
    
if __name__ == '__main__':
    p=midPaser()
    print(p.vectorize('C:/Users/whereslow/Desktop/b.py'))