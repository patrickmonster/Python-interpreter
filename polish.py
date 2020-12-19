#-*- coding: utf-8 -*-

from stack import Stack
from Token import Keyword
from Token import Token
from Token import Grammar
from Token import GrammerError
'''
void polish(char *s);
int execute();
int getvalue(int ch);
int order(int ch);
void push(int n);
int pop();
'''

#코드 테이블 - 변수/함수를 별도 구분 - 딕셔너리 자료형으로 탐색
#메모리
class Memory(dict):
    def __init__(s,grammar=None):
        s._grammar = grammar
        if not s.grammar :
            s.grammar = Grammar()
        s._lastTkn = None

    #기본 자료형 상속
    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, attr, value):
        if attr in self.keys():
            if type(value) == Token:#토큰 내부에 다른 옵젝 존재
                pass
            else :
                
                if attr == Keyword.TEXT or s._lastTkn == None:
                    s.__setitem__(data,[])#배열형 자료형을 넣어 담들어올 데이터
                else :
                    s.__setitem__(attr, data)
        else :
            return self.__setitem__(attr, value)

    def __delattr__(self, attr):
        return self.__delitem__(attr)
# 구문을 확인하여 분류
def polish(s):
    
    pass

def main():
    
    print('test')
if __name__ in '__main__':
    main()

