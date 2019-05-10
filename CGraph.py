# -*- coding: utf-8 -*-
'''
Xavi Coret Mayoral
'''
#!/usr/bin/python
import time
import os
import numpy as np
import math
import random
import sys
import Queue

###############################################################################################
#		Class Vertex 																	  
#	Parametres: - x: Coordenada x sobre el pla
#				- y: Coordenada y sobre el pla
#
#	Camps: 		- m_x: Valor x del vertex, obte el valor del parametre x
#				- m_y: Valor y del vertex, obte el valor del parametre y
#				- m_Neighbords: Llista de nodes veins
###############################################################################################
class Vertex():
	def __init__(self,x=0,y=0):
		self.m_X = int(x)
		self.m_Y = int(y)
		self.m_Neighbords = []
		self.m_DijkstraDistance=0
		self.m_DijkstraVisit=False
		self.m_DijstraPrevious=None

	def __str__(self):
		name = '('+str(self.m_X)+', '+str(self.m_Y)+')'
		return name

###############################################################################################
	''' Funcio NeighbordP(v)
	Parametres: - v: Vertex
	Retorna: True si v forma part de la llista de veins del vertex tractat(self)
			 False en cas contrari
	'''
	def NeighbordP(self,v):
		for vi in self.m_Neighbords:
			if v.m_X == vi.m_X and v.m_Y == vi.m_Y:
				return True
		return False


###############################################################################################
#		Class Visits 																	  
#	Camps: - m_Vertices: Llista de vertex a visitar
###############################################################################################
class Visits():
	def __init__(self,filename=None,graph=None,nVisits=0,cicle=False):
		self.pGraph = graph
		self.m_Vertices = []
		if filename ==None:
			self.createRandomVisits(nVisits,cicle)
		else:
			self.read(filename)

	def __str__(self):
		data = ''
		for v in self.m_Vertices:
			data+=str(v)+'\n'
		return data

###############################################################################################
	''' Funcio read(filename)
	Parametres: - filename: Nom del fitxer de Visits a llegir
	Retorna: Guarda a m_Vertices els vertex que hi ha al fitxer
	'''
	def read(self, filename):
		f = open(filename,"r")
		filetype = f.readline().replace('\n','')
		#print filetype
		if filetype == 'VISITS':
			for line in f:
				line=line.replace('\n','')	
				coords = line.split(' ')
				temp = Vertex(coords[0],coords[1])
				self.m_Vertices.append(temp)
		else:
			print 'Error: Not a Visits file detected'
		f.close()
###############################################################################################
	''' Funcio createRandomVisits(nVisits,cicle)
	Parametres: - nVisits: Nombre de visits a crear
				- cicle: boolea que determina si es un cicle o no
	Retorna: Crea una llista de vertex a visitar
	'''		
	def createRandomVisits(self,nVisits, cicle):		
		i=0
		while i<nVisits:
			k=random.randint(0,len(self.pGraph.m_Vertices)-1)
			if self.pGraph.m_Vertices[k] not in self.m_Vertices:
				self.m_Vertices.append(self.pGraph.m_Vertices[k])
				i+=1
		if cicle:
			self.m_Vertices[nVisits-1]=self.m_Vertices[0]

		
###############################################################################################
	''' Funcio EuclideDistance(v1,v2)
	Parametres: - v1,v2: Vertex
	Retorna: La distancia euclidiana entre els dos vertex
	'''
def EuclideDistance(v1,v2):
	return math.sqrt((math.pow(v1.m_X-v2.m_X,2))+(math.pow(v1.m_Y-v2.m_Y,2)))

###############################################################################################
#		Class Track 																	  
#	Parametres: - filename: Nom del fitxer amb els vertex que formen el graf
#				- graph: Coordenada y sobre el pla
#				- visits: Llista de nodes veins
###############################################################################################
class Track():
	def __init__(self,filename=None,graph=None):
		self.pGraph = graph
		self.m_Vertices=[]
		if filename:
			self.read(filename)
	def AddFirst(self,v):
		self.m_Vertices.insert(0, v)
	def AddLast(self,v):
		self.m_Vertices.append(v)
	def Clear(self):
		self.m_Vertices=[]
	def length(self):
		return len(self.m_Vertices)
	
	def read(self,filename):
		f = open(filename,"r")
		filetype = f.readline().replace('\n','')
		for line in f:
			line=line.replace('\n','')	
			coords = line.split(' ')
			temp = Vertex(coords[0],coords[1])
			self.m_Vertices.append(temp)
		f.close()		
		

	def __str__(self):
		out='['
		for v in self.m_Vertices:
			if i < len(self.m_Vertices)-1:
				out+=str(v)+"->"
			else:
				out+=str(v)+"]"
			i+=1
		return out

###############################################################################################
#		Class Graph 																	  
#	Parametres: - filename: Nom del fitxer amb els vertex que formen el graf
#				- m_y: Coordenada y sobre el pla
#				- m_Neighbords: Llista de nodes veins
###############################################################################################
class Graph():
	def __init__(self,filename = None,nVertices=0,nEdges=0):
		self.m_Vertices = []
		if(filename==None):
			self.createRandomGraph(nVertices,nEdges)
		else:
			self.read(filename)
		#self.m_Visits = []
		#self.distMatrix = None
		#self.read(filename)

###############################################################################################
	''' Funcio FindVertex(x,y)
	Parametres: - x,y Coordenades
	Retorna: El vertex corresponent a les coordenaes si existeix 
			 None en cas que no existeixi
	'''
	def FindVertex(self,x,y):
		for v in self.m_Vertices:
			if float(v.m_X) == float(x) and float(v.m_Y) ==float(y):
				return v
		return None

###############################################################################################
	''' Funcio AddEdge(x1,y1,x2,y2)
	Parametres: - x1,y1,x2,y2 Coordenades
	Retorna: Afegeix el vertex corresponent a les coordenades x1,y1 a la llista de veins del vertex de les 
			 coordenades x2,y2 i al reves
	'''
	def AddEdge(self,x1,y1,x2,y2):
		v1 = self.FindVertex(x1,y1)
		v2 = self.FindVertex(x2,y2)

		if v1==None:
			v1 = Vertex(x1,y1)
			self.m_Vertices.append(v1)
		if v2==None:
			v2 = Vertex(x2,y2)
			self.m_Vertices.append(v2)
		if not v1.NeighbordP(v2) and not v2.NeighbordP(v1):
			v1.m_Neighbords.append(v2)
			v2.m_Neighbords.append(v1)


###############################################################################################
	''' Funcio read(filename)
	Parametres: - filename: Nom del fitxer de Graf a llegir
	Retorna: Per a cada vertex que llegeix hi afegeix el vei corresponent
	'''
	def read(self, filename):
		f = open(filename,"r")
		filetype = f.readline().replace('\n','')
		tuples=[]
		if filetype == 'GRAPH':
			for line in f:
				line=line.replace('\n','')				
				coords = line.split(' ')
				if not [[coords[0],coords[1]],[coords[2],coords[3]]] in tuples and not [[coords[2],coords[3]],[coords[0],coords[1]]] in tuples:
					tuples.append( [[coords[0],coords[1]],[coords[2],coords[3]]])
			for t in tuples:
				self.AddEdge(t[0][0],t[0][1],t[1][0],t[1][1])
		else:
			print 'Error: Not a Graph file detected'
		f.close()

###############################################################################################
	''' Funcio GetNVertices()
	Retorna: El nombre de vertex que te el graf
	'''
	def GetNVertices(self):
		return len(self.m_Vertices)

###############################################################################################
	''' Funcio GetNEdges()
	Retorna: El nombre de arestes que te el graf
	'''
	def GetNEdges(self):
		n=0
		for v in self.m_Vertices:
			n+=len(v.m_Neighbords)
		return n/2
###############################################################################################
	''' Funcio GetNEdges()
	Parametres: -x: Coordenada x en el pla
				-y: Coordenada y en el pla
	Retorna: El vertex que es troba enaquestes coordenades
			 False en cas que no es trobi
	'''		
	def GetVertex(self,x,y):
		for v in self.m_Vertices:
			if v.m_X == x and v.m_Y == y:
				return v
		return False
###############################################################################################
	''' Funcio createRandomGraph(nVertices,nEdges)
	Parametres: - nVertices: Nombre de vertex que ha de conternir el graf
				- nEdges: Nombre de arestes que ha de conternir el graf
	Retorna: Per a cada vertex que dins el rang de vertex donar hi afegeix el vei corresponent
	'''
	def createRandomGraph(self,nVertices,nEdges):
		tuples=[]
		vertices = np.zeros((nVertices,2))
		for i in range(nVertices):
			x,y = 0,0
			found=False
			minDist = 10240000.0			
			x= random.randint(0,16000)
			y= random.randint(0,16000)
			found = False
			for j in range(i):
				dx = vertices[j][0] - x
				dy = vertices[j][1] - y
				if ((dx*dx)+(dy*dy))<minDist:
					found = True
					break
			minDist *= 0.75
			while found==True:
				x= random.randint(0,16000)
				y= random.randint(0,16000)
				found = False
				for j in range(i):
					dx = vertices[j][0] - x
					dy = vertices[j][1] - y
					if ((dx*dx)+(dy*dy))<minDist:
						found = True
						break
				minDist *= 0.75
			vertices[i]=[x,y]
			if i>0:				
				j = random.randint(0,i-1)
				if not[[x,y],[vertices[j][0],vertices[j][1]]]in tuples:
					tuples.append([[vertices[j][0],vertices[j][1]],[x,y]])
					#self.AddEdge(vertices[j][0],vertices[j][1],x,y)
					nEdges-=1
		pos = 0
		for t in tuples:
			self.AddEdge(t[0][0],t[0][1],t[1][0],t[1][1])
			pos+=1		
		rep = 0
		while nEdges>=0 and rep<100:
			i=random.randint(0,nVertices-1)
			j=random.randint(0,nVertices-1)
			vi = self.m_Vertices[i]
			vj = self.m_Vertices[j]
			if i!=j and not vi.NeighbordP(vj):
				if not [[vi.m_X,vi.m_Y],[vj.m_X,vj.m_Y]] in tuples or not [[vj.m_X,vj.m_Y],[vi.m_X,vi.m_Y]] in tuples:
					tuples.append([[vi.m_X,vi.m_Y],[vj.m_X,vj.m_Y]])
				#self.AddEdge(vi.m_X,vi.m_Y,vj.m_X,vj.m_Y)
					nEdges-=1
					rep=0
			else:
				rep+=1
		for i in range(len(tuples)):
			if i>pos:
				self.AddEdge(tuples[i][0][0],tuples[i][0][1],tuples[i][1][0],tuples[i][1][1])
###############################################################################################
###############################################################################################
###############################################################################################
	def distanciaTemptativa(self, vActual, vi):
		return float(float(vActual.m_DijkstraDistance)+float(math.sqrt((pow((vActual.m_X - vi.m_X),2))+pow((vActual.m_Y - vi.m_Y),2))))

	def Dijkstra(self, pStart):
		for v in self.m_Vertices:
			if v == pStart:
				v.m_DijkstraDistance=0.0
			else:
				v.m_DijkstraDistance = sys.maxint

			v.m_DijkstraVisit = False
		vActual = pStart
		while vActual != None:
			vNext = None
			for vi in vActual.m_Neighbords:
				if not vi.m_DijkstraVisit:
					distance = self.distanciaTemptativa(vActual,vi)
					if distance < vi.m_DijkstraDistance:
						vi.m_DijkstraDistance = distance
						vi.m_DijstraPrevious = vActual
			vActual.m_DijkstraVisit = True
			minDistance = sys.maxint
			for vi in self.m_Vertices:
				if not vi.m_DijkstraVisit and vi.m_DijkstraDistance<minDistance:
					minDistance = vi.m_DijkstraDistance
					vNext = vi
			vActual = vNext
	def DijkstraQueue(self, pStart):
		pass

		


		


###############################################################################################
	'''def DistanceMatrix(self):
		self.distMatrix=np.zeros((len(self.m_Visits.m_Vertices),len(self.m_Visits.m_Vertices)))
		for i,vi in enumerate(self.m_Visits.m_Vertices):
			for j,vj in enumerate(self.m_Visits.m_Vertices):
				self.distMatrix[i,j]=EuclideDistance(vi,vj)
		return self.distMatrix

	def printDistanceMatrix(self):
		mat=self.distMatrix
		if mat == None:
			mat = self.DistanceMatrix()
		dat=''
		for d in mat:
			for e in d:
				dat+=str(int(e))+'\t'
			dat+='\n'
		print dat
'''
###############################################################################################
