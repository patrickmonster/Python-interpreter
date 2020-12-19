"""
처리
1.문법 파일을 읽어, 심볼테이블로 변환하여 테이블저장
2.컴파일 목표 파일을 함수형만 읽어들여 심볼데이터로 변환하여 테이블저장
3.컴파일 목표 파일의 나머지 코드를 읽어 실행

스텍

테이블의 데이터를 처
"""
class Stack(list):
    push = list.append

    def is_empty(self):
        if not self:
            return True
        else:
            return False

    def peek(self):
        return self[-1]

    #join # 맨 앞에 추가
    #출력 함수
    '''
    def print(s):#__repr__
        out = ''
        index = 0
        for i in s:
            out += str(index) + str(i) + '\n'
            index+= 1
        return out
    '''
    #비교 함수
    def __cmp__(s,o):
        return len(s) == len(o)
    #덧셈 함수
    #str 출력
    def __repr__(s):#__repr__
        out = ''
        index = 0
        for i in s:
            out += str(index) + str(i) + '\n'
            index+= 1
        return out
    '''
    def __add__(s,o):
        if type(o) == Stack:
            p = Stack()
            for i in s:
                p.push(i)
            for i in o:
                p.push(i)
            return p
        return str(s) + "/" + str(o)
            
    '''
        
        
