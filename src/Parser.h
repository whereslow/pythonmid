#ifndef _METHOD_H
    #define _METHOD_H
    #include <string>
    #include <map>
    #include <vector>
    #include <xmllite.h>
    #include <fstream>



/*关键字 ->| 对应处理方式状态值*/
typedef std::map<std::string,std::string> keywordMap;

typedef std::string string;
/*xml对应的链表,代替AST*/
struct CodeStruction
{
    int Id;
    string Type;
    std::vector<string> property;
    string code;
    CodeStruction* child;

    CodeStruction():child(0),code(0),property(0),Type(0),Id(0){}
};

typedef std::vector<CodeStruction> pyTable;



class Parser
{
private:
    pyTable* table;
    keywordMap* keywords;

    std::vector<string> vectorize(std::fstream& file);
    void parse(std::vector<string>& vector);
public:
    Parser();
    ~Parser();
    bool loadKeywords(string& filename);
    pyTable* getTableFromXML(string& filename);
    pyTable* getTableFromPy(string& filename);
    bool dumpTableToPy(string& filename);
    bool dumpTableToXMl(string& filename);
    bool changeTable(auto&& ChangeMap);
};

#endif