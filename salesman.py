# -*- coding: utf-8 -*-
'''
Xavi Coret Mayoral
'''
#!/usr/bin/python
from CGraph import *



if __name__ == '__main__':
	graph = Graph('../test/Graph1.txt')
	visits = Visits('../test/Visits1.txt')

	for v in graph.m_Vertices:
		print v
	print ''
	for vi in visits.m_Vertices:
		print vi