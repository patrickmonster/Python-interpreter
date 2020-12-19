#-*- coding: utf-8 -*-
#파이썬 인터프리터 언어
#어휘분석 프로그램 




from Token import Token , GrammerError, Keyword
from buffer import Buffer
from polish import Memory
from stack import Stack


#역폴란드 표기법
def transformExpr(expr):
    op = [] #연산자들을 담아두는 stack
    newExpr = ''
    for ch in expr:
        if ch == '(': #여는 괄호가 나올 경우 다음 글자로 진행합니다.
            continue
        elif ch >= 'a' and ch <= 'z': #피연산자가 등장하면 그대로 결과 표현에 붙여줍니다.
            newExpr += ch
        elif ch == ')': #닫는 괄호가 나올 경우 표현이 끝난 것이므로 마지막으로 stack에 넣어놨던 연산자를 빼서 붙여줍니다.
            newExpr += op.pop()
        else: #연산자가 등장할 경우 stack에 넣어줍니다.
            op.append(ch)
    return newExpr
def code(token,mm,index = 0):#식처리
    tmp = None
    size = len(token)
    if index > size:
        print("잘못된 크기의 출력")
        return
    i = 0
    while i < size:
        t,k = token[i]
        if t == Keyword.LINE:
            i+=1
            continue
        print(t)
        if t in [Keyword.If,Keyword.While]:# if / while
            '''
            print("조건식 처리")
            t2,k2 = token[i+1]
            if t2 != Keyword.LPAREN:
                raise GrammerError("잘못된 조건식이 작성되었습니다." + str(index))
            if len(token) <= i+2:
                raise GrammerError("잘못된 조건식이 작성되었습니다." + str(index))
            t3,k3 = token[i+2]
            token[i] =[token[i+1],token[i+2]]
            del token[i+1]
            del token[i+2]
            i+=2
            '''
            pass
        if t == Keyword.TEXT:
            if size<=i+1:
                mm[k]='' #빈 메모리
                return
            t2,k2 = token[i+1]
            if t2 == Keyword.EQUAL or t2 in [Keyword.If,Keyword.While]:
                tmp = Stack()
                j = 2
                while True:
                    if size <= i+j:
                        break
                    t2,k2 = token[i+j]
                    if t2 == Keyword.EQUAL:
                        del tmp[len(tmp)-1]
                        break
                    tmp.append(token[i+j])
                    j += 1
                mm[k] = tmp
                i+= j
        i+=1
        
             
def run(tkns,mm,tkn = None):
    size = len(tkns)
    index = 0
    while index < size:
        i,j = tkns[index]
        if i == Keyword.TEXT and j in mm.keys():
            print(transformExpr(j))
        index +=1
            
class MM(dict):
    #기본 자료형 상속
    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, attr, value):
        return self.__setitem__(attr, value)

    def __delattr__(self, attr):
        return self.__delitem__(attr)
    
    def __repr__(s):
        out = '\n메모리 상태 ----' + str(len(s)) + '\n'
        for k in s.keys():
            out += str(k) +('='*30)+'\n'+ str(s[k]) + '\nEnd of M to ' + str(k) + '\n'
        out += '\n'
        return out

a = Token(log = False)
gBuffer = Buffer('문법.txt')
gBuffer.read()

a.addBuffer(gBuffer)
a.sort()
a.setFixing()#고정
print('메모리')
mm = MM()#문법테이블
code(a,mm)
print(mm)

gBuffer = Buffer('문법2.txt')
gBuffer.read()
a.addBuffer(gBuffer)
a.sort()
code(a,mm)
print(mm)
print("출력",'='*30)
print(a)

#c = Code()
#c.pushs(a)
#a.setFixing()      #인덱스 고
#print(c)
