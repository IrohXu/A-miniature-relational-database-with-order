#!/usr/bin/env python3
# import pandas as pd
from sly import Lexer,Parser
from table import Table, inputfromfile, outputtable
from operation import project, select, sort, concat, column_sum, column_avg, sumgroup, avggroup, join, movsum, movavg

class MyLexer(Lexer):
    tokens = { INPUT,OUTPUT,SELECT,PROJECT,AVGGROUP,AVG,SUMGROUP,SUM,SORT,JOIN,MOVAVG,MOVSUM,CONCAT,BTREE,HASH,COMP,OR,AND,NAME,NUMBER,DEFINE }
    literals = {'(',')', ',','"'} 
    ignore = ' \t'
   
    # Tokens
    INPUT = r'[iI][nN][pP][uU][tT][fF][rR][oO][mM][fF][iI][lL][eE]'
    OUTPUT = r'[oO][uU][tT][pP][uU][tT][tT][oO][fF][iI][lL][eE]'
    SELECT = r'[sS][eE][lL][eE][cC][tT]'
    PROJECT = r'[pP][rR][oO][jJ][eE][cC][tT]'
    AVGGROUP = r'[aA][vV][gG][gG][rR][oO][uU][pP]'
    AVG = r'[aA][vV][gG]'
    SUMGROUP = r'[sS][uU][mM][gG][rR][oO][uU][pP]'
    SUM = r'[sS][uU][mM]'
    SORT = r'[sS][oO][rR][tT]'
    JOIN = r'[jJ][oO][iI][nN]'
    MOVAVG = r'[mM][oO][vV][aA][vV][gG]'
    MOVSUM = r'[mM][oO][vV][sS][uU][mM]'
    CONCAT = r'[cC][oO][nN][cC][aA][tT]'
    BTREE = r'[bB][Tt][rR][eE][eE]'
    HASH = r'[hH][Aa][Ss][Hh]'
    COMP = r'[!><=]+'
    OR = r'or'
    AND = r'and'
    NAME = r'[\']?[a-zA-Z_][a-zA-Z0-9_.]*[\']?'
    NUMBER = r'\d+'
    DEFINE = r':='
    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class MyParser(Parser):
    ''' 
    @_('statements statements')
    def statements(self, p):
        return p.statement + [ p.statememts ]
    '''
    tokens = MyLexer.tokens

    def __init__(self):
        self.names = { }
    
    @_('NAME DEFINE expr')
    def statement(self, p):
        self.names[p.NAME.upper()] = p.expr  # all of the table name will be changed to upper version.
    
    @_('expr')
    def statement(self, p):
        expr = p.expr.upper()
        print(expr)
        if expr in self.names:
            outputtable(self.names[expr])
            # print(self.names[expr])

    @_('HASH "(" NAME "," expr ")"')
    @_('BTREE "(" NAME "," expr ")"')
    def statement(self, p):
        self.names[p.NAME] = self.names[p.NAME].reset_index()
        self.names[p.NAME] = self.names[p.NAME].set_index(p.expr)
        self.names[p.NAME] = self.names[p.NAME].sort_index() 
    
    @_('OUTPUT "(" NAME ")"')
    def statement(self, p):
        name = p.NAME.upper()
        outputtable(self.names[name])
        # self.names[p.NAME0].to_csv(p.NAME1,sep='|',index=False)

    # @_('OUTPUT "(" NAME "," NAME ")"')
    # def statement(self, p):
    #     self.names[p.NAME0].to_csv(p.NAME1,sep='|',index=False)

    @_('INPUT "(" NAME ")"')
    def expr(self, p):
        return inputfromfile(p.NAME)  # all column will be set to upper version

    @_('SELECT "(" NAME "," expr ")"')
    def expr(self, p):
        return select(self.names[p.NAME.upper()], p.expr.upper())

    @_('JOIN "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        df0 = self.names[p.NAME0.upper()]
        df1 = self.names[p.NAME1.upper()]
        query = p.expr.replace(".","_").upper()
        return join(df0, p.NAME0.upper(), df1, p.NAME1.upper(), query)

    @_('PROJECT "(" NAME "," expr ")"')
    def expr(self, p):
        l = p.expr
        if type(l) != list:
            l = [p.expr]
        out = []
        for i in range(0, len(l)): out.append(l[i].upper())
        return project(self.names[p.NAME.upper()], out)

    @_('SUM "(" NAME "," NAME ")"')
    def expr(self, p):
        return column_sum(self.names[p.NAME0.upper()], p.NAME1.upper())
    
    @_('AVG "(" NAME "," NAME ")"')
    def expr(self, p):
        return column_avg(self.names[p.NAME0.upper()], p.NAME1.upper())

    @_('SUMGROUP "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        l = p.expr
        if type(l) != list:
            l = [p.expr]
        out = []
        for i in range(0, len(l)): out.append(l[i].upper())
        return sumgroup(self.names[p.NAME0.upper()], p.NAME1.upper(), out)
    
    @_('AVGGROUP "(" NAME "," NAME "," expr ")"')
    def expr(self, p):
        l = p.expr
        if type(l) != list:
            l = [p.expr]
        out = []
        for i in range(0, len(l)): out.append(l[i].upper())
        return avggroup(self.names[p.NAME0.upper()], p.NAME1.upper(), out)
    
    @_('SORT "(" NAME "," expr ")"')
    def expr(self, p):
        return sort(self.names[p.NAME.upper()], p.expr.upper())

    @_('MOVAVG "(" NAME "," NAME "," NUMBER ")"')
    def expr(self, p):
        return movavg(self.names[p.NAME0.upper()], p.NAME1.upper(), int(p.NUMBER))
    
    @_('MOVSUM "(" NAME "," NAME "," NUMBER ")"')
    def expr(self, p):
        return movsum(self.names[p.NAME0.upper()], p.NAME1.upper(), int(p.NUMBER))

    @_('CONCAT "(" NAME "," NAME ")"')
    def expr(self, p):
        return concat(self.names[p.NAME0.upper()],self.names[p.NAME1.upper()])

    @_('"(" expr ")" OR "(" expr ")"')
    def expr(self, p):
        return p.expr0+" or "+p.expr1;

    @_('"(" expr ")" AND "(" expr ")"')
    def expr(self, p):
        return p.expr0+" and "+p.expr1;

    @_('NAME COMP NAME')
    def expr(self, p):
        if p.COMP == "=":
            return p.NAME0+"=="+p.NAME1
            #return p.NAME0+"=="+"\""+p.NAME1+"\""
        else:
            return p.NAME0+p.COMP+p.NAME1
            #return p.NAME0+p.COMP+"\""+p.NAME1+"\""
    
    @_('NAME COMP "\"" NAME "\""')
    def expr(self, p):
        if p.COMP == "=":
            return p.NAME0+"=="+"\""+p.NAME1+"\""
        else:
            return p.NAME0+p.COMP+"\""+p.NAME1+"\""
    
    @_('NAME COMP NUMBER')
    def expr(self, p):
        if p.COMP == "=":
            return p.NAME+"=="+p.NUMBER
        else:
            return p.NAME+p.COMP+p.NUMBER
     
    @_('NAME "," expr')
    def expr(self, p):
        l = [p.NAME]
        if type(p.expr) == list:
            l.extend(p.expr)  
        else:
            l.append(p.expr)
        return l;

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr;

    @_('NAME')
    def expr(self, p):
        return p.NAME.upper()

if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    while True:
        try:
            text = input('pd >> ')
        except EOFError:
            break
        if text:
            #for tok in lexer.tokenize(text):
            #    print(tok)
            parser.parse(lexer.tokenize(text)) 
