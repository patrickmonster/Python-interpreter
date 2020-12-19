#-*- coding: utf-8 -*-

from stack import Stack
from enum import Enum
from buffer import Buffer


# 키워드 테이블 - 바이너리 데이터 변환작업시 필요
"""
바이너리 데이터 저장
키워드 테이블 기반 데이터를 사용하여
메모리 테이블에 기입
문법 테이블용 데이터 처리
"""

# 프로그램 실행문법 eval

class Keyword(Enum):
    Non = ' '
    #공백을 지정하는 문자 (처리 X)
    If = 'if'
    While = 'while'
    Print = 'print'
    # ------------------------
    # 가변
    Var	 = 'Var'
    Ep	= 'Ep'
    Con	='Con'
    Pass = 'Pass'
    Fun = 'Fun'
    # ------------------------
    DbQt = '"'
    PLUS = '+'
    MINUS = '-'
    STAR = '*'
    SLASH = '/'
    PERCENT = '%'
    GREATER = '>'
    LESS = '<'
    EQUAL = '='
    VBAR = '|'
    AMPER = '&'
    TILDE = '~'
    TAB = '\t'
    LINE = '\n'
    SHARP = '#'
    LBRACE = '{'
    RBRACE = '}'
    LPAREN = '('
    RPAREN = ')'
    LMOTH = '['
    RMOTH = ']'
    TEXT = 1
    MTEXT = 2
    #Text = re.compile('[a-zA-Z0-9]+')
    #num = re.compile('[0-9]')
    
    """
    
    Space    #공백 ' '
    If = 1		#if
    While = 2	#while
    Var	 = 3	#변수
    Ep	= 4		#식
    
    Con	= 5		#조건
    DbQt = 6	#"      #고유명사 지정하
    PLUS = 7	#+
    MINUS = 8	#-
    STAR =9		#*
    SLASH = 10		#/
    PERCENT = 11	#%
    GREATER = 12 	# > - 조건식
    EQGREATER = 13	#>=
    LESS = 14		#<
    EQLESS = 15		#<=
    EQEQUAL = 16	#==
    EQUAL = 17 		#= 우항 연산 결과를 좌항에 넣음 | 좌항에 변수가 없을경우 출력문
    VBAR = 18		#| - or연산
    AMPER = 19		#& - and 연산
    TILDE = 20		#~
    Tab = '\t'          #줄바꿈 문자
    Remark = '*='       #주석처리
    { } = L/R BRACE - 그룹지정자 
    """

class OverFilterError(Exception):
    pass

class GrammerError(Exception):
    pass

#베이직 문법 클래스
class Grammar:
    
    def __init__(s,keyword = Keyword,process=[['{','}'],['[',']'],['(',')'],['#','\n'],['"']],space=[' ','\ufeff','\n',''],name=['Ep','Con','Var']):
        s.keyword = keyword
        s.processes = [s.getToken(i[0],keyword=True) for i in process]
        s.space = space
        s.process = process
        #s.multiple = [i for i in s.getToken(All=True) if type(i.value)==str and i.value.isalpha()]
        s.multiple = [i for i in keyword if type(i.value)==str and i.value in name]

    #키워드만 가져옴
    def getTokenKeyword(s,str):
        for j in Keyword:
            if str == j.value:
                return j
        return Keyword.Non
    def isMutiple(s,name):
        for i in s.multiple:
            if i.value in name:
                index = name[len(i.value):]
                if not index.isdigit():
                    break
                return (s.getTokenKeyword(i.value),int(index))
        return (Keyword.TEXT, name)

    #문법데이터
    # ((Keyword,str/int )/ Keyword / [Keyword])
    def getToken(s,str=0,keyword=False,All=False):
        if All:
            return Keyword
        tkn = s.getTokenKeyword(str)
        if tkn == Keyword.Non:
            #for i in s.multiple:
            #    if str in 
            #    return (tkn,)
            i,j = s.isMutiple(str)
            if not keyword:
                if i != Keyword.Non:
                    return (i,j)
                else :
                    return (Keyword.TEXT, -1)
            else:
                if i != Keyword.Non:
                    return (i,j)
                else :
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

class Token(Stack):
    
    #컴파일데이터
    """
    파일을 읽어서 토큰처리를 하거나 혹은,
    바이너리 데이터를 토큰화 시켜 저장
    """

    #필터 함수
    def __init__(self,filter=None,log=False):
        if not filter:
            self.filter = Grammar()
        else :
            self.filter = filter
        if not hasattr(self.filter,'getToken'):
            raise GrammerError('토큰 처리 클래스가 아님!' + str(self.filter))
        self.flag = 0           #전에 처리한 index값이 들어감(튜플/index)
        self.kind = Keyword.Non #현재 처리중인 모드 Keyword
        self.tmp = Stack()      #모드 처리중 데이터
        self.line = 0           #현재 처리라인
        self.remark = 0         #6
        self.count=0
        #변환 하기 쉽도록 미리 변환

        self.log = log

        self.fixing = -1
    #데이터를 넣음
    """
    데이터 플레그
    -1 = 네이밍 변수
    0 = 일반처리 (스텍에 명령)
    1 = 동시처리 데이터
    """
    def addD(self,string):
        #공백 문자 판단해서 생략
        if self.tknSkip(string):
            return len(self)
        #튜플형 / 처리내용  |  키워드 값 Keyword.LBRACE (1, ['{', '}'])
        data,index = self.filter.getToken(string)

        #특수 키워드 처리 / 튜풀형 전제조건
        if type(self.flag) == tuple:
            #이전 키워드 가져오기
            i,j = self[len(self)-1]
            self.p("포괄문 데이터 처리" + str(index) + "\t" + str(data))
            #이전키워드와 현재 키워드 비교
            if self.flag == index:
                k,l = self.flag
                if len(l) != 1:
                    #이전 데이터하고 같은 토큰일 경우
                    self.p("토큰 비교" + str(data) + "\t" + str(self.filter.getToken(l[0],keyword=True)))
                    if data == self.filter.getToken(l[0],keyword=True):
                        self.count +=1
                        self.p("Count ++ \t" + str(self.count))
                    else:
                        if self.count == 0:
                            self.flag = 0
                            self.p("처리" + str(self.tmp) + '\t' + str(data))
                            self.p("="*80)
                            if len(self.tmp)>1:
                                sorts = self.sortArray(self.tmp)
                                self[self.tmp_i] = (i,sorts)
                            else :
                                if len(self.tmp) <= 0:
                                    print('Error' + ('='*50))
                                    print(self)
                                    raise GrammerError("문법에러["+ str(self.line) +"]: " + string + " (의)가 종단점이 잘못됨")
                                self[len(self)-1] = (i,self.tmp[0])
                            return len(self)
                        self.count -=1
                        self.p("Count -- \t" + str(self.count))
                        if self.count < 0:
                            raise GrammerError("[" + str(self.line) + "] :" + string)
                elif self.count > 1:
                    raise OverFilterError("카운터 에러" + str(self.count))
                else:
                    if len(self.tmp) <= 0:
                        print('Error' + ('='*50))
                        print(self)
                        raise GrammerError("문법에러["+ str(self.line) +"]: " + string + " (의)가 종단점이 잘못됨")
                    self.flag = 0
                    self.p("처리" + str(self.tmp))
                    self.p("="*80)
                    if len(self.tmp)>1:
                        self[lself.tmp_i] = (i,self.sortArray(self.tmp))
                    else :
                        for m in self.filter.process:
                            if self.tmp[0] in m:
                                self[self.tmp_i] = (i,self.tmp[0])
                                return len(self)

                        #검사
                        t,v = self.filter.getToken(self.tmp[0])
                        self.p('검사문'+str(self.tmp[0])+'\t검사식 '+str(t) + '\t' +  str(v))
                        if t != Keyword.TEXT:
                            self.p("할당",str(v))
                            s = Token()
                            s.addD(self.tmp[0])
                            s.sort()
                            self[len(self)-1] = (i,s)
                            return len(self)
                        self.p('검사문 무시' + str(self.tmp[0]))
                        self[len(self)-1] = (i,self.tmp[0])
                    return len(self)
                self[len(self)-1] = (i,self.tmp)
            self.tmp.push(string)
            return len(self)
        self.p(data,end='\t')
        self.p(str(index) + '\t' + str(string))
        self.tmp = Stack()
        #일반정의문법 처리
        #플레그 인덱스 지정
        #데이터 처리
        if type(index) == tuple:
            self.kind = data
            self.tmp_i = len(self)
            self.flag = index
            self.p("="*80)
            self.p("모드처리 시작" + str(data) + '\t'+ str(index))
            self.p("="*80)
        
        #데이터 기입 (사용 데이터이기 때문에)
        if index != -1:
            self.push((data,index))
        else :
            self.push((data,string))
        return len(self)
    def sortArray(s,arr):
        tmp = Token()
        for i in arr:
            if s.tknSkip:
                tmp.addD(i)
        return tmp
    #토큰 생략가능여부
    def tknSkip(s,str):
        if str in s.filter.space:
            return True
        return False
    #키워드만 가져옴
    def getTokenKeyword(s,str):
        for j in Keyword:
            if str == j.value:
                return j
        return Keyword.Non
    #문법데이터
    # ((Keyword,str/int )/ Keyword / [Keyword])
    def getTokenG(s,str=0,keyword=False,All=False):
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
        
    def addBuffer(s,buffer):
        for l in buffer:
            s.addLine(l)
    
        
    def addLine(s,line):
        tmp = ''
        s.line += 1
        s.p("line ("+ str(s.line) +") =" + line)
        for i in line:
            if i.isalnum() or i == '_':
                tmp += i
            else :
                if tmp != ' ':
                    s.addD(tmp)
                if len(s) >= 1:
                    v, o = s[len(s)-1]
                if i != ' ':
                    s.addD(i)
                tmp = ''
        s.p("="*80)
        if s.tmp:
            s.p("처리되지 않은 데이터 :" + str(s.tmp) + ' (을)를 ' + str(s.flag) + '에 기입요망')
        s.addD('\n')
        s.push((Keyword.LINE,s.line))        #명령 종단 선언
    #sort 정렬시켜 데이터를 재 정의 규칙을 탐색
    #skip = 재 탐색시, 스킵할 토큰
    def sort(s,skip=[Keyword.DbQt,Keyword.SHARP,Keyword.TEXT],delete=[Keyword.Non]):
        #탐색
        if len(s.tmp) >0:
            k,v = s[s.tmp_i]
            s[s.tmp_i] = (k,s.sortArray(s.tmp))
            s.tmp = Stack()
            
        for i,j in s:
            if type(j) == Stack :
                s.p("정렬시작 : " + str(j))
                T = Token(s.filter,s.log)
                for k in j:
                    T.addD(k)
                T.sort(skip=skip,delete=delete)
                s[s.index((i,j))] = (i,T)
            if i == Keyword.TEXT or i in s.filter.processes and i != Keyword.DbQt:
                s.p("재탐색"+str(i) + '\t' + str(j))
                if type(j) == Token:
                    j.sort()
                    continue
                i2,j2 = s.filter.getToken(j)
                if i2 == Keyword.TEXT:
                    continue
                tmp = s.index((i,j))
                s[tmp] = (i2,j2)
                s.p('변경 '+ str(tmp) + '\t' + str(s[tmp]))
            if type(j) == Token:
                s.p('sort 재정렬 시도' + ('*'*40))
                j.sort()
                s.p('sort 재정렬' +str(s))
            
    #토큰 인덱스 고정
    def setFixing(s):
        if s.fixing != -1:
            return s.fixing
        s.fixing = len(s)-1
        print("고정길이 :" + str(s.fixing))

    
    def print(s):
        for (i,j) in s:
            if i in s.filter.processes:
                k = s.filter.process[s.filter.processes.index(i)]
                print(k[0],end='')
                if type(j)==Token:
                    j.print()
                else:
                    print(j,end='')
                if len(k) > 1 :
                    print(k[1],end='')
                else :
                    print(k[0],end='')
                continue
            
            if i == Keyword.TEXT:
                print(j,end=' ')
            elif i == Keyword.LINE:
                print()
            elif type(i) == Token :
                i.print()
            else :
                print(i.value,end=' ')
    def getStr(s):
        out = ''
        for (i,j) in s:
            if i in s.filter.processes:
                k = s.filter.process[s.filter.processes.index(i)]
                s.p(k[0],end='')
                if type(j)==Token:
                    j.print()
                else:
                    print(j,end='')
                if len(k) > 1 :
                    print(k[1],end='')
                else :
                    print(k[0],end='')
                continue
            
            if i == Keyword.TEXT:
                out +=j
            elif i == Keyword.LINE:
                out+='\n'
            elif type(i) == Token :
                out+=i.value
            else :
                out += i.value
        return out
    def p(self,s=None,end='\n'):
        if not self.log:
           return
        if not s:
            print()
        else:
            print(s,end=end)

    #데이터 정규화
    def getNormalization(s):
        out = Token()
        for i,j in s:
            if type(j) == Token:
                #자식 정규화
                out += j.getNormalization()
            else:
                out.append((i,j))
        return out
    #str 출력
    def __repr__(s):#__repr__
        out = ''
        index = 0
        for i in s:
            out += str(index) + ' ' + str(i) + '\n'
            if s.fixing == index:
                out += ("="*50) +'\n'
            index+= 1
        return out
    '''
    #덧셈
    def __add__(s,o):
        if type(o) == Token:
            p = Token()
            for i in s:
                p.push(i )
            for i in o:
                p.push(i)
            return p
        return str(s) + "/" + str(o)
    '''
    
class TokenG(Token):
    def __init__(self,filter):
        super().__init__(filter)

def main():
    filter= Grammar()
    gBuffer = Buffer('문법.txt')
    gBuffer.read()
    a = Token(filter)
    a.addBuffer(gBuffer)
    a.sort()
    #a.setFixing()      #인덱스 고
    print("정렬완료 출력 -")
    print(a)
    a.print()
    
if __name__ in '__main__':
    main()



