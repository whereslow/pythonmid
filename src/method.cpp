#include "method.h"

Parser::Parser(){
    this->table = nullptr;
    this->keywords = nullptr;
}
Parser::~Parser(){
    delete this->table;
    delete this->keywords;
    this->table = nullptr;
    this->keywords = nullptr;
}
bool Parser::loadKeywords(string& filename){
    if(filename.empty()) return false;
    else{
        
    }
}

pyTable* Parser::getTableFromPy(string& filename){
    if(filename.empty()) return nullptr;
    else{
        
    }
}
pyTable* Parser::getTableFromXML(string& filename){
    if(filename.empty()) return nullptr;
    else{
        
    }
}
bool Parser::dumpTableToPy(string& filename){
    if(filename.empty()) return false;
    else{
        
    }
}
bool Parser::dumpTableToXMl(string& filename){
    if(filename.empty()) return false;
    else{
        
    }
}

bool Parser::changeTable(auto&& Func){
    if(table == nullptr) return nullptr;
    else{
        
    }
}