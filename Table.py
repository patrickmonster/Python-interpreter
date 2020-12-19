#-*- coding: utf-8 -*-
#데이터 테이블
class Array:
	l = []
	def __init__(self):
		l = []
		print("부모초기화")
		
	def push(i):
		l.append(i)
	def pop(i):
		return l.pop()
	def get(i):
		return l[i]

#심볼 테이블 - 데이터 저장 메모리 관리
class SymbolTable(Array):
	
	def __init__(self): #
		parent_class.__init__()
		
a = Array()