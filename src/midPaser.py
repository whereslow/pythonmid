import re
from xml.dom import minidom #仅适用于可信环境
from dataclasses import dataclass,field
from typing import List,Dict
import json5

@dataclass
class fragment:
    line:int
    sonfrag:list[any] = field(default_factory=List)
    code:dict[str] = field(default_factory=Dict)

class midPaser:
    @staticmethod
    def loadPyTableFromPython(pythonPath):
        pass
    @staticmethod
    def dumpFragmentToXml(mainfragment:fragment,xmlPath) -> None:
        def createcontext(node:minidom.Element,percentfragment:fragment):
            linenode=root.createElement("line")
            node.appendChild(linenode)
            linenode.appendChild(root.createTextNode(str(percentfragment.line)))
            codenode = root.createElement("code")
            node.appendChild(codenode)
            for i in percentfragment.code:
                codenode.appendChild(codetextnode:=root.createElement(i))
                codetextnode.appendChild(root.createTextNode(percentfragment.code[i]))
        def createnode(node:minidom.Element,percentfragment:fragment):
            createcontext(node,percentfragment)
            fq = []
            nodeq = []
            while True:
                for i in percentfragment.sonfrag:
                    fq.append(i)
                    pnode = root.createElement("fragment")
                    nodeq.append(pnode)
                    node.appendChild(pnode)
                    createcontext(pnode,i)
                if nodeq == []:#即fq == []
                    break
                else:
                    node = nodeq.pop(0)
                    percentfragment = fq.pop(0)
                
        root = minidom.Document()
        fragmentnode=root.createElement("fragment")
        createnode(fragmentnode,mainfragment)
        root.appendChild(fragmentnode)
        
        with open(xmlPath,'w',encoding='utf-8') as f:
            root.writexml(f,encoding='utf-8',addindent='\t',newl='\n')
    @staticmethod
    def dumpFragmentToJson(pyTable,jsonPath) -> None:
        pass
    @staticmethod
    def dumpFragmentToPython(pyTable,pythonPath) -> None:
        pass
    @staticmethod
    def changeFragments(pyTable,changeDict):
        pass
    @staticmethod
    def diffFragment(pyTable1,pyTable2):
        pass
    @staticmethod
    def vectorize(filename:str) ->list[str]:
        with open(filename,'r',encoding='utf-8') as f:
            strings = f.read().replace('    ',"^TAB")
            token_vector = list(filter(None,re.split(r'(\n)|(\^TAB)',strings)))
            return token_vector
    @staticmethod
    def parseFragmentToMap():
        pass
    @staticmethod
    def parsePythonToFragment(tokenVec:list[str]) -> fragment:
        percent_line = 0
        tab_state = -1
        tab_count = 0
        father_fragment = []
        mainFragment = fragment(line=percent_line,sonfrag=[],code={})
        percent_line +=1
        percent_fragment = mainFragment
        for token in tokenVec:
            if token == "\n":
                tab_count = 0
                percent_fragment.code[str(percent_line-1)] += token
            elif token == "^TAB":
                tab_count += 1
            else:
                tab_diff = tab_count - tab_state
                tab_state = tab_count
                if tab_diff > 0:
                    father_fragment.append(percent_fragment)
                    
                    percent_fragment.sonfrag.append(fragment(line=percent_line,sonfrag=[],code={}))
                    percent_line += 1
                    
                    percent_fragment = percent_fragment.sonfrag[-1]
                    percent_fragment.code[str(percent_line-1)] = tab_count*"    "+token
                elif tab_diff == 0:
                    father_fragment[-1].sonfrag.append(fragment(line=percent_line,sonfrag=[],code={}))
                    percent_line += 1
                    percent_fragment = father_fragment[-1].sonfrag[-1]
                    percent_fragment.code[str(percent_line-1)] = tab_count*"    "+token
                elif tab_diff < 0:
                    percent_fragment = father_fragment[tab_diff-1]
                    temp_fragment = father_fragment[tab_diff-1]
                    if tab_count != (temp_fragment.code[min(temp_fragment.code)].count('    ') if temp_fragment.code !={} else tab_count):
                        percent_fragment.code[str(percent_line)] = tab_count*'    '+token
                    percent_line += 1
                    #父对象作用量
                    father_fragment = father_fragment[:tab_diff]
                    if tab_count == (temp_fragment.code[min(temp_fragment.code)].count('    ') if temp_fragment.code !={} else -tab_count):
                        percent_fragment = fragment(line=percent_line,sonfrag=[],code={})
                        percent_fragment.code[str(percent_line-1)] = tab_count*'    '+ token
                        father_fragment[-1].sonfrag.append(percent_fragment)
                        father_fragment.append(percent_fragment)
        return mainFragment
if __name__ == '__main__':
    vec=midPaser.vectorize('C:/Users/whereslow/Desktop/b.py')
    midPaser.dumpFragmentToXml(midPaser.parsePythonToFragment(vec),'C:/Users/whereslow/Desktop/b.xml')