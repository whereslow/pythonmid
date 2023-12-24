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
            token_vector=f.read().replace('    ','^TAB ').replace("\n"," ").split(" ")
            try:
                while True:
                    token_vector.remove('')
            except ValueError:
                pass
            # 控制流适配符号向量化处理
            i = 0
            while i!=len(token_vector)-1:
                i+=1
                if ':' in token_vector[i]:
                    i,token_vector = symbolDivide(i,token_vector,':')
                if '(' in token_vector[i]:
                    i,token_vector = symbolHeightLightDivide(i,token_vector,'(')
                if ')' in token_vector[i]:
                    i,token_vector = symbolHeightLightDivide(i,token_vector,')')
            return token_vector
    def parse(self,code:str):
        pass
#特殊字符处理工具函数
def symbolDivide(index:int,token_vector:list[str],symbol:str):
    temp = token_vector[index].split(symbol)
    if temp[0] != "" and temp[1] != "":
        token_vector.insert(index+1,temp[1])
        token_vector[index] = temp[0]
    elif temp[0] != "" and temp[1] == "":
        token_vector[index] = token_vector[index].replace(symbol, '')
    elif temp[0] == "" and temp[1]!= "":
        token_vector[index] = token_vector[index].replace(symbol, '')
    elif temp[0] == "" and temp[1] == "":
        del token_vector[index]
    else:
        raise ValueError
    return index,token_vector
def symbolHeightLightDivide(index:int,token_vector:list[str],symbol:str):
        temp = token_vector[index].split(symbol)
        if len(temp) > 2:
            multiflag = True
            for j in range(2,len(temp)):
                temp[j]=symbol+temp[j]
                temp[1]+=temp[j]
        else:
            multiflag = False
        if temp[0] != "" and temp[1] != "":
            del token_vector[index]
            token_vector.insert(index,temp[1])
            token_vector.insert(index,symbol)
            token_vector.insert(index,temp[0])
            if multiflag:
                index+=1
            else:
                index+=2
        elif temp[0] != "" and temp[1] == "":
            del token_vector[index]
            token_vector.insert(index,symbol)
            token_vector.insert(index,temp[0])
            index+=1
        elif temp[0] == "" and temp[1]!= "":
            del token_vector[index]
            token_vector.insert(index,temp[1])
            token_vector.insert(index,symbol)
            if multiflag:
                index+=0
            else:
                index+=1
        elif temp[0] == "" and temp[1] == "":
            pass
        else:
            raise ValueError
        return index,token_vector
if __name__ == '__main__':
    p=midPaser()
    print(p.vectorize('C:/Users/whereslow/Desktop/b.py'))