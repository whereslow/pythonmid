import json

from dataclasses import dataclass,field
from typing import List
@dataclass
class frag:
    Id:int      #1,2,3...
    fragType:str = ""  #一个N个结构的头用-分隔,剩余用_分隔的描述串,N-frag#1_frag#2_frag#3_...,上n级节点用n个^分隔
    propertys:dict[str] =field(default_factory=dict)
    sonfrag:list[any] = field(default_factory=list)
    code:str = ""
    
PyTable=List[frag]

@dataclass
class keywords:
    keywordMap:dict #keyword To {frag 或 in 或 out}

class midPaser:
    """代理keywords和做方法载体"""
    def __init__(self,jsonPath) -> None:
        with open(jsonPath) as f:
            self.keywords = keywords(json.load(f))
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
    def diffPyTable(pyTable1,pyTable2):
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
                    i,token_vector = symbolDivideHeighLightSemicolon(i,token_vector,':')
                if '(' in token_vector[i]:
                    i,token_vector = symbolHeighLightDivideBracket(i,token_vector,'(')
                if ')' in token_vector[i]:
                    i,token_vector = symbolHeighLightDivideBracket(i,token_vector,')')
            return token_vector
    def parse(self,tokenVec:list[str]) -> PyTable:
        divideSymbols = {'^TAB','(',')',':'}
        state = None
        #转移容器
        pytable = []
        fragtoken = []
        #~
        #状态容器
        fatherfrag:list[frag]
        fatherfrag = []
        fatherbracket = 0
        tab_state = 0
        tab_count = 0
        #~
        for token in tokenVec:
            if token != '^TAB' and tab_count != 0: #TAB状态终止,同时决定是否切换状态
                if tab_state == tab_count:#不改变状态
                    tab_count=0
                elif tab_state < tab_count: #产生子结构 状态标志'sonfrag'
                    state ='sonfrag'
                    tab_state = tab_count
                    tab_count=0
                elif tab_state > tab_count: #结束子结构,并进入父结构'fatherfrag'
                    state = 'fatherfrag'
                    tab_diff = tab_state - tab_count
                    tab_state = tab_count
                    tab_count=0
            if token in self.keywords.keywordMap or token in divideSymbols:
                if token in self.keywords.keywordMap and self.keywords.keywordMap[token] == 'frag':
                    match state:
                        case 'frag':
                            state = 'frag'
                            percentfrag.fragType = f"{len(fatherfrag)+1}-{percentfrag.fragType}"
                            fatherfrag.clear()
                            
                            fragtoken.append(token)
                            percentfrag = frag(Id=len(fatherfrag)+1,fragType=token+"#"+str(fragtoken.count(token)+1))
                            pytable.append(percentfrag)
                            percentfrag.code+=token+' '
                        case 'in':
                            percentfrag.code+=token+' '
                            percentfrag.propertys.update({percentfrag.propertys["IN"]:percentfrag.propertys["IN"]+' '+token})
                        case '(': #中间作为无结构语义的代码段
                            percentfrag.code+=token+' '
                        case 'sonfrag':
                            state = 'frag'
                            #添加当前结构的子结构
                            fatherfrag.append(percentfrag)
                            percentfrag.sonfrag.append(percentfrag:=frag(Id=len(fatherfrag)+1,fragType=token+"#"+str(fragtoken.count(token)+1)))
                            percentfrag.code+=token+' '
                        case 'fatherfrag':
                            state = 'frag'
                            #添加父结构的子结构
                            fatherfrag=fatherfrag[0:-(tab_diff-1) if tab_diff>0 else -1]
                            fatherfrag[-1].fragType = f"{fatherfrag[-1].fragType}_{percentfrag.fragType}"
                            percentfrag = fatherfrag[-1]
                            percentfrag.sonfrag.append(percentfrag:=frag(Id=len(fatherfrag)+1,fragType=token+"#"+str(fragtoken.count(token)+1)))
                            percentfrag.code+=token+' '
                        case None: #第一次产生状态
                            state = 'frag'
                            pytable.append(percentfrag:=frag(Id=len(fatherfrag)+1,fragType=token))
                            percentfrag.code+=token+' '
                        case _ :
                            raise Exception(f"error frag to {token} symbol in {state} state")
                elif token in self.keywords.keywordMap and self.keywords.keywordMap[token] == 'in': #in也是frag
                    match state:
                        case 'frag':
                            state = 'in'
                            percentfrag.fragType = f"{len(fatherfrag)+1}-{percentfrag.fragType}"
                            fatherfrag.clear()
                            
                            fragtoken.append(token)
                            percentfrag = frag(Id=len(fatherfrag)+1,fragType=token+"#"+str(fragtoken.count(token)+1))
                            pytable.append(percentfrag)
                            percentfrag.code+=token+' '
                            percentfrag.propertys.update({"IN":' '+token})
                        case '(':
                            percentfrag.code+=token+' '
                        case 'in':
                            percentfrag.code+=token+' '
                            percentfrag.propertys.update({"IN":percentfrag.propertys["IN"]+' '+token})
                        case 'sonfrag':
                            state = 'in'
                            fatherfrag.append(percentfrag)
                            percentfrag.sonfrag.append(percentfrag:=frag(Id=len(fatherfrag)+1,fragType=token+"#"+str(fragtoken.count(token)+1)))
                            percentfrag.code+=token+' '
                            percentfrag.propertys.update({"IN":' '+token})
                        case 'fatherfrag':
                            state = 'in'
                            fatherfrag=fatherfrag[0:-(tab_diff-1) if tab_diff>0 else -1]
                            fatherfrag[-1].fragType = f"{fatherfrag[-1].fragType}_{percentfrag.fragType}"
                            percentfrag = fatherfrag[-1]
                            percentfrag.sonfrag.append(percentfrag:=frag(Id=len(fatherfrag)+1,fragType=token+"#"+str(fragtoken.count(token)+1)))
                            percentfrag.code+=token+' '
                            percentfrag.propertys.update({"IN":' '+token})
                        case None:
                            state = 'in'
                            pytable.append(percentfrag:=frag(Id=len(fatherfrag)+1,fragType=token))
                            percentfrag.code+=token+' '
                            percentfrag.propertys.update({"IN":' '+token})
                        case _ :
                            raise Exception(f"error in to {token} symbol {state} state")
                elif token in self.keywords.keywordMap and self.keywords.keywordMap[token] == 'out':
                    match state:
                        case '(':
                            percentfrag.code+=token+' '
                        case 'sonfrag':
                            state = 'frag'
                            percentfrag.code+=token+' '
                            percentfrag.propertys.update({"OUT":percentfrag.propertys["IN"]})
                            percentfrag.propertys.pop("IN")
                        case 'fatherfrag':
                            state = 'frag'
                            fatherfrag=fatherfrag[0:-(tab_diff-1) if tab_diff>0 else -1]
                            fatherfrag[-1].propertys.update({"OUT":fatherfrag[-1].propertys["IN"]})
                            fatherfrag[-1].propertys.pop("IN")
                            fatherfrag[-1].propertys.update({"OUTPOS":len(percentfrag.code)})
                            percentfrag.code+=token+' '
                        case _ :
                            raise Exception(f"error out to {token} symbol in {state} state")
                elif token == ':':
                    match state:
                        case 'frag':
                            percentfrag.code+=token+' '
                            tab_state =0 if tab_state==0 else tab_state-1 # 替代换行
                        case 'in':
                            state = 'frag'
                            percentfrag.code+=token+' '
                        case '(':
                            percentfrag.code+=token+' '
                        case _ :
                            raise Exception(f"error : symbol to {state} state")
                elif token == '^TAB':
                    if tab_count == 0:
                        percentfrag.code = percentfrag.code[:-1]
                        percentfrag.code+='\n'
                    tab_count+=1
                    percentfrag.code+="    "
                elif token == '(':
                    match state:
                        case 'frag':
                            state = '('
                            percentfrag.code+=token+' '
                        case 'in':
                            state = 'in'
                            percentfrag.code+=token+' '
                            percentfrag.propertys.update({"IN":percentfrag.propertys['IN']+' '+token})
                        case '(':
                            state = '('
                            fatherbracket+=1
                            percentfrag.code+=token+' '
                        case None:
                            pass
                elif token == ')':
                    match state:
                        case '(':
                            if fatherbracket == 0:
                                state = 'frag'
                            else:
                                fatherbracket-=1
                            percentfrag.code+=token+' '
                        case 'in':
                            state = 'in'
                            percentfrag.code+=token+' '
                            percentfrag.propertys.update({"IN":percentfrag.propertys['IN']+' '+token})
                        case _ :
                            raise Exception(f"error ) symbol to {state} state")
            else: #是普通的token字段
                match state:
                        case 'frag':
                            percentfrag.code+=token+' '
                        case 'in':
                            percentfrag.code+=token+' '
                            if(token !=':'):
                                percentfrag.propertys.update({"IN":percentfrag.propertys['IN']+' '+token})
                        case '(':
                            percentfrag.code+=token+' '
                        case 'sonfrag':
                            state = 'frag'
                            fatherfrag.append(percentfrag)
                            percentfrag.sonfrag.append(percentfrag:=frag(Id=len(fatherfrag)+1,fragType=token+"#"+str(fragtoken.count(token)+1)))
                            percentfrag.code+=token+' '
                        case 'fatherfrag':
                            state = 'frag'
                            fatherfrag=fatherfrag[0:-(tab_diff-1) if tab_diff>0 else -1]
                            fatherfrag[-1].fragType = f"{fatherfrag[-1].fragType}_{percentfrag.fragType}"
                            percentfrag = fatherfrag[-1]
                            percentfrag.sonfrag.append(percentfrag:=frag(Id=len(fatherfrag)+1,fragType=token+"#"+str(fragtoken.count(token)+1)))
                            percentfrag.code+=token+' '
                        case _ :
                            raise Exception(f"error {token} symbol to {state} state")
        return pytable
#特殊字符处理的工具函数,后期重写
def symbolDivideHeighLightSemicolon(index:int,token_vector:list[str],symbol=':'):
    #apear once
    assert symbol == ':'
    temp = token_vector[index].split(symbol)
    if temp[0] != "" and temp[1] != "":
        del token_vector[index]
        token_vector.insert(index,temp[1])
        token_vector.insert(index,symbol)
        token_vector.insert(index,temp[0])
        index+=2
    elif temp[0] != "" and temp[1] == "":
        token_vector[index] = token_vector[index].replace(symbol, '')
        token_vector.insert(index+1,symbol)
    elif temp[0] == "" and temp[1]!= "":
        token_vector[index] = token_vector[index].replace(symbol, '')
        token_vector.insert(index-1,symbol)
    elif temp[0] == "" and temp[1] == "":
        pass
    else:
        raise ValueError
    return index,token_vector
def symbolHeighLightDivideBracket(index:int,token_vector:list[str],symbol:str):
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
    parser = midPaser("C:/Users/whereslow/Desktop/pythonmid/resource/keywords.json")
    vec=parser.vectorize('C:/Users/whereslow/Desktop/b.py')
    table = parser.parse(vec)
    print(table)