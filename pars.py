#-*- coding: utf-8 -*-

'''
구문분석
'''
from Token import Keyword
from Token import Grammar
from stack import Stack
from enum import Enum

'''
코드
실행 코드
내용 / 종류
////묶음 정보 처리

변수명 / 값
'''

class Var(Stack):
    pass
class Code(Stack):
    pass

class Pars(Stack):
    

    def __init__(s,process=[['{','}'],['[',']'],['(',')'],['#'],['"']],log=False):
        s.process = process
        s.log = log
    
    #구문 푸싱
    def push(s,d):
        pass
    
    #문법데이터
    def getTokenG(s,str=0,keyword=False):
        
        pass

    #키워드만 가져옴
    def getTokenKeyword(s,str):
        for j in Keyword:
            if str == j.value:
                return j
        return Keyword.Non
    #문법데이터
    # ((Keyword,str/int )/ Keyword / [Keyword])
    def getToken(s,str=0,keyword=False,All=False):
        if All:
            return Keyword
        tkn = s.getTokenKeyword(str)
        if tkn == Keyword.Non:
            if not keyword:
                return (Keyword.TEXT, -1)
            else:
                return Keyword.TEXT
        if not keyword:
            for k in s.process:
                #필터 적용 테그들
                if len(k) > 2:
                    raise OverFilterError()
                if str in k:
                    return (tkn,(s.process.index(k)+1,k))
            return (tkn,0)
        else :
            return tkn
        #처리 하지 못했을때에 -1
        #print("처리하지 못함(키워드 처리)", end='\t')
