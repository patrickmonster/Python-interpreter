#_*_ coding:utf-8 _*_
"""
Buffer 클래스
파일을 읽고 처리함
"""
import os
from stack import Stack
class Buffer(Stack):
    
    def read(s):
        s.l = -1
        with open(s.name,'r',encoding='UTF-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                s.push(line)
        print("파일 버퍼 작업완료 - read")
        
    def __init__(self,name,datas=None):
        self.name = name
        self.isfile = os.path.isfile(name)
        self.l = -1
        if not self.isfile:
            f = open(name,'w')
            f.close()
            print('파일을 생성 - ' + name)
        if datas:
           for i in datas:
               self.push(i)
    
    def write(s,string='\n',index=-1):
        if index==-1:
            s.push(string)
        else :
            s.insert(index,string)

    def save(s,bin=False):
        with open(s.name,'w' +(bin and'b' or ''),encoding='UTF-8') as f:
            for i in s:
                if bin:
                    d = [hex(ord(x) for x in i.encode('UTF-8'))]
                    
                else:
                    f.write(i)
                    
    def close(s):
        with open(s.name,'w', encoding='UTF-8') as f:
            for i in s:
                f.write(i)
                f.write('\n')
