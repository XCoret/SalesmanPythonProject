# -*- coding: utf-8 -*-
'''
Xavi Coret Mayoral
'''
#!/usr/bin/python
import os
import sys
import ScrolledText
from tkinter import *
import tkMessageBox
import tkSimpleDialog
from tkinter.filedialog import askopenfilename,asksaveasfilename
from CGraph import *

class RandomGraphDialog(tkSimpleDialog.Dialog):

	def body(self, master):

		Label(master, text="#Vertices:").grid(row=0, sticky="W")
		Label(master, text="#Edges:").grid(row=1, sticky="W")

		self.e1 = Entry(master)
		self.e1.insert(END,'10')
		self.e2 = Entry(master)
		self.e2.insert(END,'20')

		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
	def validate(self):
		try:
			first =self.e1.get()
			second = self.e2.get()
			self.result = [int(first),int(second)]
			return 1
		except ValueError:
			tkMessageBox.showwarning("Bad input", "Illegal values, please entry again")
			self.result = [None,None]
			return 0
	def apply(self):
		return self.result

class RandomVisitsDialog(tkSimpleDialog.Dialog):
	
	def body(self, master):
		self.var = IntVar()
		Label(master, text="#Visits:").grid(row=0, sticky="W")	
		self.e1 = Entry(master)	
		self.e1.insert(END,'5')	
		self.cb = Checkbutton(master, text="Cicle",variable=self.var)

		self.e1.grid(row=0, column=1)
		self.cb.grid(row=1, columnspan=2, sticky=W)

	def validate(self):
		try:
			first =self.e1.get()
			second=self.var.get()
			self.result=[first,second]
			return 1
		except ValueError:
			tkMessageBox.showwarning("Bad input", "Illegal values, please entry again")
			self.result = [None,None]
			return 0
	def apply(self):
		return self.result


class _Salesmangui:
	def __init__(self,master):
		frame = Tk()
		self.windowW = frame.winfo_screenwidth()*0.75
		self.windowH = frame.winfo_screenheight()*0.75
		frame.destroy()
		#WINDOW DEFINITION
		frame = Frame(master,width = self.windowW,height = self.windowH)
		frame.pack()

		self.master = master
		self.x,self.y,self.w,self.h = -1,-1,-1,-1
		self.master.title("SALESMAN")
		self.master.iconbitmap(r'tsp.ico')
		self.font = 'Ubuntu'
		self.nVertices=0
		self.nEdges = 0
		self.graph = None
		self.visits = None
		self.track = None
		self.CanvasVisits = []
		self.CanvasTrackV = []
		self.CanvasTrackE = []
		self.CanvasVertices = []
		self.CanvasEdges = []
		self.CanvasTrackIndexes = []
		self.CanvasVerticesIndexes = []
		self.indexed=False
		#SIZES
		''' buttonW:14.25%
			buttonH:7.75%
			canvasW:65%
			canvasH:80%
			self.padding:1.5%
		'''
		self.buttonWidth = self.windowW*0.15
		self.buttonHeight = self.windowH*0.0775
		self.canvasWidth = self.windowW*0.65
		self.canvasHeight = self.windowH*0.8
		self.padding = self.windowW*0.015
		self.marginW = self.windowW*0.006
		self.marginH =self.windowH*0.0035
		#POSITIONS
		'''
		RIGHT COL BUTTONS:
			x: self.windowW-(self.padding+self.buttonWidth)
		LEFT COL BUTTONS:
			x:
		y:= self.padding+((self.marginH*nButtons) +(self.buttonHeight*nButtons) )
		'''
		nButtons=0
		rightColBtnX = self.windowW-(self.padding+self.buttonWidth)
		leftColBtnX = rightColBtnX-(self.padding+self.buttonWidth)

		#1st ROW
		self.btn_ReadGraph = Button(self.master,text='Read Graph', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=leftColBtnX,y=self.padding+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonReadGraph)

		self.btn_ReadGraph = Button(self.master,text='Dijkstra', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=rightColBtnX,y=self.padding+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonDijkstra)
		nButtons+=1

		#2nd ROW
		self.btn_ReadGraph = Button(self.master,text='Random Graph', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=leftColBtnX,y=self.padding+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonRandomGraph)

		self.btn_ReadGraph = Button(self.master,text='Dijkstra Queue', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=rightColBtnX,y=self.padding+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonDijkstraQueue)
		nButtons+=1

		#3rd ROW -- Right Col self.padding
		self.btn_ReadGraph = Button(self.master,text='Save Graph', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=leftColBtnX,y=self.padding+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonSaveGraph)

		self.btn_ReadGraph = Button(self.master,text='Greedy', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=rightColBtnX,y=(2*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonGreedy)
		nButtons+=1

		#4th ROW -- Right Col self.padding
		self.btn_ReadGraph = Button(self.master,text='Read Distances', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=leftColBtnX,y=(2*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonReadDistances)

		self.btn_ReadGraph = Button(self.master,text='Pure Backtracking', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=rightColBtnX,y=(3*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonBacktracking)
		nButtons+=1

		#5th ROW -- Right Col self.padding
		self.btn_ReadGraph = Button(self.master,text='Save Distances', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=leftColBtnX,y=(2*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonSaveDistances)

		self.btn_ReadGraph = Button(self.master,text='Greedy Backtracking', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=rightColBtnX,y=(3*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonGreedyBacktracking)
		nButtons+=1

		#6th ROW -- Right Col self.padding
		self.btn_ReadGraph = Button(self.master,text='Read Visits', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=leftColBtnX,y=(3*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonReadVisits)

		self.btn_ReadGraph = Button(self.master,text='Branch&Bound 1', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=rightColBtnX,y=(4*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonBranchAndBound1)
		nButtons+=1

		#7th ROW -- Right Col self.padding
		self.btn_ReadGraph = Button(self.master,text='Random Visits', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=leftColBtnX,y=(3*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonRandomVisits)

		self.btn_ReadGraph = Button(self.master,text='Branch&Bound 2', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=rightColBtnX,y=(4*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonBranchAndBound2)
		nButtons+=1

		#8th ROW -- Right Col self.padding
		self.btn_ReadGraph = Button(self.master,text='Save Visits', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=leftColBtnX,y=(3*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonSaveVisits)

		self.btn_ReadGraph = Button(self.master,text='Branch&Bound 3', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=rightColBtnX,y=(4*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonBranchAndBound3)
		nButtons+=1		

		#9th ROW -- Right Col self.padding
		self.btn_ReadGraph = Button(self.master,text='Read Track', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=leftColBtnX,y=(4*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonReadTrack)

		self.btn_ReadGraph = Button(self.master,text='Vertex index', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=rightColBtnX,y=(5*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonVertexIndex)
		nButtons+=1	

		#10th ROW -- Right Col self.padding
		self.btn_ReadGraph = Button(self.master,text='Save Track', font=self.font, relief='raised')
		self.btn_ReadGraph.place(x=leftColBtnX,y=(4*self.padding)+((self.marginH*nButtons)+(self.buttonHeight*nButtons)),width = self.buttonWidth, height= self.buttonHeight)
		self.btn_ReadGraph.bind("<ButtonRelease-1>",self.OnButtonSaveTrack)	

		#CANVAS
		self.canvas = Canvas(self.master,bd=2 ,relief='groove',bg='#ffffff',width = self.canvasWidth, height = self.canvasHeight)
		self.canvas.place(x=self.padding,y=self.padding, width=self.canvasWidth, height=self.canvasHeight)


		#DRAWING AREA
		'''
		left = self.padding+50
		right = (self.padding + self.canvasW)-50
		top = self.padding+50
		bottom = (self.padding + self.canvasH)-50

		'''
		self.left = self.padding+50
		self.right = (self.padding + self.canvas.winfo_width())-50
		self.top = self.padding+50
		self.bottom = (self.padding + self.canvas.winfo_height())-50

	def updateTrack(self,viit):
		self.drawTrack(int(viit))
		
	#LEFT COLUMN FUNCTIONS
###############################################################################################
	def OnButtonReadGraph(self,event):
		print 'Read Graph'
		filename = askopenfilename(initialdir = "./test",title = "Open Graph file",filetypes=(("Graph file","*.txt"),))
		self.graph = Graph(filename)
		self.drawGraph()
		
###############################################################################################
	def OnButtonRandomGraph(self, event):
		print 'Random Graph'
		data = RandomGraphDialog(self.master)
		if data.result[0]!=None:
			self.nVertices = data.result[0]
			self.nEdges = data.result[1]
			self.graph = Graph(nVertices = self.nVertices, nEdges = self.nEdges)
			if self.graph!=None:
				self.drawGraph()			
###############################################################################################
	def OnButtonSaveGraph(self,event):
		print 'Save Graph'
		if self.graph:
			filename = asksaveasfilename(initialdir = "./test",title = "Save Graph as",filetypes = (("Graph file","*.txt"),))
			if filename!=None:
				if not '.txt' in filename:
					filename = filename+str('.txt')
				f = open(filename,'w')
				f.write("GRAPH\n")
				tuples=[]
				for v in self.graph.m_Vertices:
					for vi in v.m_Neighbords:
						if not [vi,v] in tuples:
							tuples.append([v,vi])
				for t in tuples:
					f.write(str(t[0].m_X)+" "+str(t[0].m_Y)+" "+str(t[1].m_X)+" "+str(t[1].m_Y)+"\n")
				f.close()
		else:
			tkMessageBox.showwarning("Graph Error", "The graph doesn't exists")
###############################################################################################
	def OnButtonReadDistances(self,event):
		print 'Read Distances'
		if self.graph:
			filename = askopenfilename(initialdir = "./test",title = "Open Distances file",filetypes=(("Distances file","*.txt"),))
			f = open(filename,"r")
			filetype = f.readline().replace('\n','')
			distances=[]
			if filetype == 'DISTANCES':
				for i,line in enumerate(f):
					line=line.replace('\n','')	
					distances.append(float(line))
				i=0
				for v in self.graph.m_Vertices:
					v.m_DijkstraDistance = distances[i]
					x,y = self.getPoint(v.m_X,v.m_Y)

					text = self.canvas.create_text(x+5,y+5,anchor="nw",fill="black",font="Consolas",text=round(v.m_DijkstraDistance,2))
					rectangle = self.canvas.create_rectangle(self.canvas.bbox(text), fill="white")
					self.canvas.tag_lower(rectangle,text)
					i+=1
			else:
				tkMessageBox.showwarning("File Error", "Not a Distances file detected")
			f.close()
		else:
			tkMessageBox.showwarning("Graph Error", "The graph doesn't exists")
###############################################################################################
	def OnButtonSaveDistances(self,event):
		print 'Save Distances'
		if self.graph:
			filename = asksaveasfilename(initialdir = "./test",title = "Save Distances as",filetypes = (("Distances file","*.txt"),))
			if filename!=None:
				if not '.txt' in filename:
					filename = filename+str('.txt')
				f = open(filename,'w')
				f.write("DISTANCES\n")
				for v in self.graph.m_Vertices:
					f.write(str(v.m_DijkstraDistance)+"\n")
				f.close()
		else:
			tkMessageBox.showwarning("Graph Error", "The graph doesn't exists")
###############################################################################################
	def OnButtonReadVisits(self,event):
		print 'Read Visits'
		if self.graph:
			filename = askopenfilename(initialdir = "./test",title = "Open Visits file",filetypes=(("Visits file","*.txt"),))
			f = open(filename,"r")
			filetype = f.readline().replace('\n','')			
			if filetype == 'VISITS':
				f.close()
				self.visits = Visits(filename=filename,graph=self.graph)
				self.drawVisits()
			else:
				f.close()
				tkMessageBox.showwarning("File Error", "Not a Visits file detected")
		else:
			tkMessageBox.showwarning("Graph Error", "The graph doesn't exists")

###############################################################################################
	def OnButtonRandomVisits(self,event):
		print 'Random Visits'
		data = RandomVisitsDialog(self.master)
		if int(data.result[0])>self.graph.GetNVertices():
			tkMessageBox.showwarning("Visits Error","Too many visits for this graph")
		else:
			self.visits = Visits(graph = self.graph,nVisits=int(data.result[0]),cicle = bool(data.result[1]))
			self.drawVisits()
		
###############################################################################################
	def OnButtonSaveVisits(self,event):
		print 'Save Visits'
		if self.graph:
			if self.visits:
				filename = asksaveasfilename(initialdir = "./test",title = "Save Visits as",filetypes = (("Visits file","*.txt"),))
				if filename!=None:
					if not '.txt' in filename:
						filename = filename+str('.txt')
					f = open(filename,'w')
					f.write("VISITS\n")
					tuples=[]
					for v in self.visits.m_Vertices:
						f.write(str(v.m_X)+" "+str(v.m_Y)+"\n")
					f.close()
			else:
				tkMessageBox.showwarning("Visits Error", "There are no visits to save")			
		else:
			tkMessageBox.showwarning("Graph Error", "The graph doesn't exists")		
###############################################################################################
	def OnButtonReadTrack(self,event):
		print 'Read Track'
		if self.graph:
			filename = askopenfilename(initialdir = "./test",title = "Open Track file",filetypes=(("Track file","*.txt"),))
			f = open(filename,"r")
			filetype = f.readline().replace('\n','')			
			if filetype == 'TRACK':
				f.close()
				self.track = Track(filename=filename)
				self.drawTrack(int(len(self.track.m_Vertices)))
				#TRACK INDEX
				#viit = VertexIndexInTrack
				
				viit = IntVar()
				self.trackIndex = Scale(self.master,variable = viit,command=self.updateTrack,orient="horizontal",length=self.canvasWidth-(self.padding*0.5),from_=0,to=len(self.track.m_Vertices)-1)
				self.trackIndex.place(x=self.padding,y=self.padding+self.canvasHeight)
				self.trackIndex.set(len(self.track.m_Vertices)-1)

			else:
				f.close()
				tkMessageBox.showwarning("File Error", "Not a Track file detected")
		else:
			tkMessageBox.showwarning("Graph Error", "The graph doesn't exists")		
###############################################################################################
	def OnButtonSaveTrack(self,event):
		print 'Save Track'
###############################################################################################


	#RIGHT COLUMN FUNCTIONS
	def OnButtonDijkstra(self,event):
		print 'Dijkstra'
		self.graph.Dijkstra(self.graph.m_Vertices[0])
		self.drawDistances()

	def OnButtonDijkstraQueue(self, event):
		print 'Dijkstra Queue'
	def OnButtonGreedy(self,event):
		print 'Greedy'
	def OnButtonBacktracking(self,event):
		print 'Bactracking'
	def OnButtonGreedyBacktracking(self,event):
		print 'Greedy backtracking'
	def OnButtonBranchAndBound1(self,event):
		print 'Branch and Bound 1'
	def OnButtonBranchAndBound2(self,event):
		print 'Branch and Bound 2'
	def OnButtonBranchAndBound3(self,event):
		print 'Branch and Bound 3'
	def OnButtonVertexIndex(self,event):
		print 'Vertex index'
		if self.indexed:
			for vi in self.CanvasVerticesIndexes:
				self.canvas.delete(vi[0])
				self.canvas.delete(vi[1])
			self.indexed=False
		else:
			for i,v in enumerate(self.graph.m_Vertices):
				x,y = self.getPoint(v.m_X,v.m_Y)
				tag = 'V:'+str(i)
				text = self.canvas.create_text(x+5,y+5,anchor="nw",fill="blue",font="Consolas",text=tag)
				rectangle = self.canvas.create_rectangle(self.canvas.bbox(text), fill="white",outline="white")
				self.canvas.tag_lower(rectangle,text)
				self.CanvasVerticesIndexes.append([text,rectangle])
				self.indexed=True

	def getPoint(self,x,y):
		maxWidth = self.canvas.winfo_width()-200
		maxHeight = self.canvas.winfo_height()-100
		tx = self.maxs[0]+self.mins[0]
		hx = (x*maxWidth)/tx
		ty = self.maxs[1]+self.mins[1]
		hy = (y*maxHeight)/ty
		return float(hx+100),float(hy+50)

	def drawVertices(self):
		for cv in self.CanvasVertices:
			self.canvas.delete(cv)
		self.CanvasVertices=[]
		self.mins = [sys.maxint,sys.maxint]
		self.maxs = [-sys.maxint,-sys.maxint]
		for v in self.graph.m_Vertices:
			self.mins[0] = min(self.mins[0],v.m_X)
			self.mins[1] = min(self.mins[1],v.m_Y)
			self.maxs[0] = max(self.maxs[0],v.m_X)
			self.maxs[1] = max(self.maxs[1],v.m_Y)
		for v in self.graph.m_Vertices:
			vx,vy = self.getPoint(v.m_X,v.m_Y)
			self.CanvasVertices.append(self.canvas.create_oval(vx-4,vy-4,vx+4,vy+4,outline="#000000",fill="#0080FF",width=1))
		for cv in self.CanvasVertices:
			self.canvas.tag_raise(cv)

	def drawEdges(self):
		for ce in self.CanvasEdges:
			self.canvas.delete(ce)
		self.CanvasEdges=[]
		self.mins = [sys.maxint,sys.maxint]
		self.maxs = [-sys.maxint,-sys.maxint]
		for v in self.graph.m_Vertices:
			self.mins[0] = min(self.mins[0],v.m_X)
			self.mins[1] = min(self.mins[1],v.m_Y)
			self.maxs[0] = max(self.maxs[0],v.m_X)
			self.maxs[1] = max(self.maxs[1],v.m_Y)
		for v in self.graph.m_Vertices:
			vx,vy = self.getPoint(v.m_X,v.m_Y)
			for vi in v.m_Neighbords:
				vix,viy = self.getPoint(vi.m_X,vi.m_Y)
				self.CanvasEdges.append(self.canvas.create_line(vx,vy,vix,viy, fill="#646464", width=1,dash=(2,2)))

	def drawGraph(self):
		for cv in self.CanvasVertices:
			self.canvas.delete(cv)
		self.CanvasVertices=[]
		for ce in self.CanvasEdges:
			self.canvas.delete(ce)
		self.CanvasEdges=[]

		self.drawEdges()
		self.drawVertices()


	def drawDistances(self):
		for v in self.graph.m_Vertices:
			x,y = self.getPoint(v.m_X,v.m_Y)
			text = self.canvas.create_text(x+5,y+5,anchor="nw",fill="black",font="Consolas",text=round(v.m_DijkstraDistance,2))
			rectangle = self.canvas.create_rectangle(self.canvas.bbox(text), fill="white")
			self.canvas.tag_lower(rectangle,text)

	def drawVisits(self):
		#Negre:0
		#Blanc: ultim
		#color:#FF8040
		for cv in self.CanvasVisits:
			self.canvas.delete(cv)
		self.CanvasVisits = []
		i=0
		for v in self.visits.m_Vertices:
			x,y = self.getPoint(v.m_X,v.m_Y)
			if i==0:
				self.CanvasVisits.append(self.canvas.create_rectangle(x-4,y-4,x+4,y+4,fill="#000000",width=1))
			elif i==len(self.visits.m_Vertices)-1:
				self.CanvasVisits.append(self.canvas.create_rectangle(x-4,y-4,x+4,y+4,outline="#000000",fill="#ffffff",width=1)) 
			else:
				self.CanvasVisits.append(self.canvas.create_oval(x-4,y-4,x+4,y+4,outline="#000000",fill="#FF8040",width=1)) 
			i+=1
		for cv in self.CanvasVisits:
			self.canvas.tag_raise(cv)
		
	def drawSingleEdge(self,v0,v1):
		#Calcul x
		x0,y0 = self.getPoint(v0.m_X,v0.m_Y)
		x1,y1 = self.getPoint(v1.m_X,v1.m_Y)
		vi = Vertex(0.0,0.0)
		if float(x0) > float(x1) :
			vi.m_X= float(float(v0.m_X)-float(float(v0.m_X-v1.m_X)/3))
		elif float(x0) < float(x1) :
			vi.m_X= float(float(v0.m_X)+float(float(v1.m_X-v0.m_X)/3))
		else:
			vi.m_X = float(v0.m_X)

		if float(y0) > float(y1) :
			vi.m_Y=float(float(v0.m_Y)-float(float(v0.m_Y-v1.m_Y)/3))
		elif float(y0) < float(y1) :
			vi.m_Y= float(float(v0.m_Y)+float(float(v1.m_Y-v0.m_Y)/3))
		else:
			vi.m_Y = float(v0.m_Y)

		xi,yi = self.getPoint(vi.m_X,vi.m_Y)
		if v0.NeighbordP(v1):
			trackColor = "#00C800"
		else:
			trackColor = "#C80000"
		
		self.CanvasTrackE.append(self.canvas.create_line(x0,y0,x1,y1, fill=trackColor, width=2,arrow="last", arrowshape=(16,20,6)))
		self.CanvasTrackE.append(self.canvas.create_line(x0,y0,xi,yi, fill=trackColor, width=2,arrow="last", arrowshape=(16,20,6)))


	def drawTrack(self,stop):
		#Wrong:#C80000
		#Right:#00C800
		#00CC66
		for tv in self.CanvasTrackV:
			self.canvas.delete(tv)
		self.CanvasTrackV = []
		for te in self.CanvasTrackE:
			self.canvas.delete(te)
		self.CanvasTrackE = []
		for cti in self.CanvasTrackIndexes:
			self.canvas.delete(cti[0])
			self.canvas.delete(cti[1])
		self.CanvasTrackIndexes=[]
		coordList=[]

		i=0
		for v in range(len(self.track.m_Vertices)):
			v = self.track.m_Vertices[i]
			if i<stop:				
				x,y = v.m_X,v.m_Y
				v= self.graph.FindVertex(x,y)
				x,y = self.getPoint(v.m_X,v.m_Y)
				if i <len(self.track.m_Vertices)-1:
					vi = self.track.m_Vertices[i+1]
					vx,vy =  self.getPoint(vi.m_X,vi.m_Y)
					if i== len(self.track.m_Vertices)-1:
						self.CanvasTrackV.append(self.canvas.create_rectangle(x-8,y-8,x+8,y+8,fill="#000000",width=1))
					else:
						if v.NeighbordP(vi):
							trackColor = "#00C800"
						else:
							trackColor = "#C80000"
						if i==0:
							self.CanvasTrackV.append(self.canvas.create_rectangle(x-8,y-8,x+8,y+8,fill="#ffffff",width=1))
							text = self.canvas.create_text(x+5,(y+15),anchor="nw",fill="red",font="Consolas",text=0)
							rectangle = self.canvas.create_rectangle(self.canvas.bbox(text), fill="white",outline='white')
							self.canvas.tag_lower(rectangle,text)
							self.CanvasTrackIndexes.append([text,rectangle])
						else:	
							self.CanvasTrackV.append(self.canvas.create_rectangle(x-8,y-8,x+8,y+8,fill=trackColor,width=1))
						#self.CanvasTrackE.append(self.canvas.create_line(x,y,vx,vy, fill=trackColor, width=4,arrow="last"))

						self.drawSingleEdge(v,vi)

				k=0
				for c in coordList:
					if [vx,vy]==c:
						k+=1
				coordList.append([x,y])

				text = self.canvas.create_text(vx+5,(vy+15)+(k*20),anchor="nw",fill="red",font="Consolas",text=i+1)
				rectangle = self.canvas.create_rectangle(self.canvas.bbox(text), fill="white",outline='white')
				self.canvas.tag_lower(rectangle,text)
				self.CanvasTrackIndexes.append([text,rectangle])

				
				i+=1
		
		for ce in self.CanvasTrackE:
			self.canvas.tag_raise(ce)
		for cv in self.CanvasTrackV:
			self.canvas.tag_raise(cv)
		for cti in self.CanvasTrackIndexes:
			self.canvas.tag_raise(cti[1])
			self.canvas.tag_raise(cti[0])
		self.drawVisits()

if __name__=='__main__':
	root = Tk()
	app = _Salesmangui(root)
	root.resizable(False,False)
	root.mainloop()
