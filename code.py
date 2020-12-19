#-*- coding: utf-8 -*-

'''
코드 분류
'''
from token import Keyword
from stack import Stack
from polish import Memory

'''
메모리 테이블
메모리 주소 | 토큰 |

메모리주소 = 값
조건문 (참/거짓) 식
'''




class Code:

    def __init__(s):
        s.ltkn = Keyword.Non #마지막 토큰
        s.mm = Memory()
        
    def parsing(tok):#구문분석  / 토큰객체
        try:
        for i in range(len(tok)):
            k,v = tok[i]
            if k == Keyword.TEXT:
                k2,v2 = tok[i+1]
                if k2 == Keyword.EQUAL: # = 일경우 처리
                    s.ltkn = k2
                    
                    
        
    #현재 실행데이터 가져옴
    def getIndex(s):
        pass
    
    #문법데이터
    def getTokenG(s,str=0,keyword=False):
        pass
