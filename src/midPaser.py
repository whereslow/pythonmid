import json

from dataclasses import dataclass
from typing import List

@dataclass
class frag:
    Id:int      #1,2,3...
    Type:str    #一个N个结构的头用-分隔,剩余用_分隔的描述串,N-frag1_frag2_frag3_...
    sonfrag:any
    propertys:list[str]
    code:str

PyTable=List[frag]

@dataclass
class keywords:
    keywordMap:dict #keyword To {frag 或 in 或 out}

class midPaser:
    """代理keywords和做方法载体"""
    def __init__(self,jsonPath) -> None:
        self.keywords:keywords = self.loadKeywordsFromJson(jsonPath)
    def loadKeywordsFromJson(jsonPath) -> keywords:
        keywordstruct = keywords()
        jsondict = json.load(jsonPath)
        for i in jsondict:
            keywordstruct.keyword.append(i['keyword'])
            keywordstruct.keywordMap.update({i['keyword']:i['Type']})
        return keywordstruct
    def loadPyTableFromPython(pythonPath) -> PyTable:
        pass
    def loadPyTableFromJson(jsonPath) -> PyTable:
        pass
    def dumpPyTableToJson(pyTable,jsonPath) -> None:
        pass
    def dumpPyTableToXml(pyTable,xmlPath) -> None:
        pass
    def dumpPyTableToPython(pyTable,pythonPath) -> None:
        pass
    def changePyTable(pyTable,changeDict) -> PyTable:
        pass
    def diffPyTable(pyTable1,pyTable2):#不太确定
        pass
    def vectorize(filename:str) ->list[str]:
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
                    i,token_vector = symbolDivideSemicolon(i,token_vector,':')
                if '(' in token_vector[i]:
                    i,token_vector = symbolHeightLightDivideBracket(i,token_vector,'(')
                if ')' in token_vector[i]:
                    i,token_vector = symbolHeightLightDivideBracket(i,token_vector,')')
            return token_vector
    def parse(self,code:str):
        tokenVec = self.vectorize(code)
        divideSymbols = {'^TAB','(',')'}
        state = None
        #转移容器
        pytable = []
        #~
        #临时容器
        fatherfrag=[]
        #~
        for token in tokenVec:
            if token in self.keywords.keywordMap:
                if self.keywords.keywordMap[token] == 'frag':
                    match state:
                        case 'frag':
                            pass
                        case 'in':
                            pass
                        case 'out':
                            pass
                        case None:
                            pass
                elif self.keywords.keywordMap[token] == 'in':
                    match state:
                        case 'frag':
                            pass
                        case 'in':
                            pass
                        case 'out':
                            pass
                        case None:
                            pass
                elif self.keywords.keywordMap[token] == 'out':
                    match state:
                        case 'frag':
                            pass
                        case 'in':
                            pass
                        case 'out':
                            pass
                        case None:
                            pass
            elif token in divideSymbols:
                if token == '^TAB':
                    pass
                elif token == '(':
                    pass
                elif token == ')':
                    pass
            else: #是普通的token字段
                pass
#特殊字符处理的工具函数
def symbolDivideSemicolon(index:int,token_vector:list[str],symbol=':'):
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
def symbolHeightLightDivideBracket(index:int,token_vector:list[str],symbol:str):
    assert symbol in {'(',')'}
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
    print(midPaser.vectorize('C:/Users/whereslow/Desktop/b.py'))