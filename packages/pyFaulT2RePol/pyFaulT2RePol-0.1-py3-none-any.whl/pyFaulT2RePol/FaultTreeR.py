"""
Bibliothèques utiles
"""

#import plotly.graph_objects as go

import sympy
import networkx as nx
import  matplotlib.pyplot  as  plt

from pyFaulT2RePol.LogicGate import *
from pyFaulT2RePol.FaultTree import *
from pyFaulT2RePol.HasseDiagramLib import *

"""
Construction of the fault tree
"""

FaultTreeRs={}
class FaultTreeR:
    NFaultTreeR=0       
    def __init__(self,n,IndivReliabilityVal=[[1]],IndivReliabilityFunc=[One],t=[0],Option=1):
        self.id=id(self)
        FaultTreeRs[str(self.id)]=self
        self.__class__.NFaultTreeR+=1
        self.Option=Option
        self.IndFiabVal=IndivReliabilityVal
        self.IndFiabFunc=IndivReliabilityFunc
        self.Time=t
        if (self.Option==1):
            self.NComponent=len(self.IndFiabVal) # The number of component(s) of the system
        else:
            self.NComponent=len(self.IndFiabFunc)
        #print("\n self.NComponent Start in FaultTreeR")
        #print(self.NComponent)
        self.NNode=n # Le système a moins de composant que n
        self.Node=[]
        self.SubTree={}
        
        for i in range(self.NNode):
            self.SubTree[i]=None
            
        self.Reliability={}
        self.Label=[]
        self.AdjMat={}#matlib.zeros((n, n))
        self.RelMat=[[],[],[],[],[],[]] 
        #[[Door],[NodeIn],[NodeOut],[Orders],[Times],[IndicesPrincipal]]
        self.IdxTable=[[],[],[]] 
        #[[NumRel],[Node i],[Node j]]
    
    def __del__(self):
        self.__class__.NFaultTreeR-=1
    
    def IdxNode(self,Indices=None):
        """summary IdxNode

        Args:
            Indices (list, optional): _description_. Defaults to None.

        Returns:
           list: contain the id of the nodes
        """
        res=None
        if (Indices in self.Node):
            res=0
            while (self.Node[res]!=Indices):
                res=res+1
        return res
    
    def InOrder2(self,xx=[1,3,2],yy=[1,2,30]):
        i=min(len(xx),len(yy))-1
        while ((xx[i]==yy[i]) and (i>=0)):
            #print((xx,yy))
            i=i-1
        if (i<0):
            res=True
        else:
            res=(xx[i]<yy[i])
        return res

    """
    def InOrder2(self,xx=[1,3,2],yy=[1,2,30]):
        res=True
        i=0
        while ((res==True) and (i<min(len(xx),len(yy)))):
            #print((xx,yy))
            res=(res and (xx[i]<=yy[i]))
            i=i+1
        return res
    
    print(InOrder2())
    """
    
    def Leaves(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        res=[]
        for j in range(len(self.AdjMat)):
            Temp=0
            for i in range(len(self.AdjMat)):
                if (i!=j):
                    Temp+=self.AdjMat[i][j]
                    if (self.InOrder2(self.Node[i],self.Node[j])):
                        Temp+=1
            if (Temp==0):#((Temp==0) and (self.RelMat[0][j]==1)):
                res.append(j)
        return res
    
    def Root(self):
        res=[]
        for i in self.AdjMat.keys():
            Temp=0
            for j in range(len(self.AdjMat)):
                if (i!=j):
                    Temp+=self.AdjMat[i][j]
                    if (self.InOrder2(self.Node[i],self.Node[j])):
                        Temp+=1
            if (Temp==0):#((Temp==0) and (self.RelMat[0][j]==1)):
                res.append(i)
        return res
    
    def Update(self):
        n=len(self.RelMat[0])
        if (n>0):
            Test=(len(self.Node)<=self.NNode-2)
            Test=Test or ((self.RelMat[1][-1] in self.Node) and (self.RelMat[2][-1] in self.Node))
            Test=Test or ((not(self.RelMat[1][-1] in self.Node) or not(self.RelMat[2][-1] in self.Node)) and (len(self.Node)<=self.NNode-1))
            if not(Test):
                #print("Update Test No")
                del(self.RelMat[0][-1])
                del(self.RelMat[1][-1])
                del(self.RelMat[2][-1])
                del(self.RelMat[3][-1])
                del(self.RelMat[4][-1])
                del(self.RelMat[5][-1])
            else:
                if not(self.RelMat[1][-1] in self.Node):
                    self.Node.append(self.RelMat[1][-1])
                    self.Label.append(ID_P(1))
                    for i in range(len(self.Node)-1):
                        self.AdjMat[i].append(0)
                    self.AdjMat[len(self.Node)-1]=[0 for i in range(len(self.Node))]
                if not(self.RelMat[2][-1] in self.Node):
                    self.Node.append(self.RelMat[2][-1])
                    self.Label.append(ID_P(self.RelMat[0][-1]))
                    for i in range(len(self.Node)-1):
                        self.AdjMat[i].append(0)
                    self.AdjMat[len(self.Node)-1]=[0 for i in range(len(self.Node))]
                if (self.RelMat[0][-1]>=0):
                    self.IdxTable[0].append(n-1)
                    self.IdxTable[1].append(self.IdxNode(self.RelMat[1][-1]))
                    self.IdxTable[2].append(self.IdxNode(self.RelMat[2][-1]))
                    self.AdjMat[self.IdxTable[1][-1]][self.IdxTable[2][-1]]=1
                #print("Update Test Ok")
                #print(self.Node)
   
    def Sort(self):     
        Temp1=[]
        Temp2=[]
        for i in range(len(self.IdxTable[0])):
            j=0
            for k in range(len(self.IdxTable[0])):           
                #if (self.InOrder2(self.RelMat[2][k],self.RelMat[1][i]) and (self.IdxTable[2][k]!=self.IdxTable[1][i])):
                Test=(self.AdjMat[self.IdxNode(self.RelMat[2][k])][self.IdxNode(self.RelMat[1][i])]==1)
                Test=Test or (self.InOrder2(self.RelMat[2][k],self.RelMat[1][i]))
                Test=Test and (self.IdxTable[2][k]!=self.IdxTable[1][i])
                if Test:
                    j=j+1
            while (j in Temp1):
                j=j+1
            Temp1.append(j)
            Temp2.append(0)
        for i in range(len(self.IdxTable[0])):
            Temp2[int(Temp1[i])]=i
        Temp3=[[],[],[]]
        Temp4=[[],[],[],[],[],[]]
        for i in range(len(self.IdxTable[0])):
            Temp3[0].append(i)
            Temp3[1].append(self.IdxTable[1][int(Temp2[i])])
            Temp3[2].append(self.IdxTable[2][int(Temp2[i])])
            Temp4[0].append(self.RelMat[0][int(Temp2[i])])
            Temp4[1].append(self.RelMat[1][int(Temp2[i])])
            Temp4[2].append(self.RelMat[2][int(Temp2[i])])
            Temp4[3].append(self.RelMat[3][int(Temp2[i])])
            Temp4[4].append(self.RelMat[4][int(Temp2[i])])
            Temp4[5].append(self.RelMat[5][int(Temp2[i])])
        self.IdxTable=Temp3.copy()
        self.RelMat=Temp4.copy()
        #print("\n Sort Called in FaultTreeR")
        #print(self.RelMat)
        
    def NewRelation(self,Port=1,IndicesIn=None,IndicesOut=None,Orders=None,Times=None,IndicesPrincipal=None):
        """summary NewRelation

        Args:
            Port (int, optional): _description_. Defaults to 1.
            IndicesIn (list, optional): _description_. Defaults to None.
            IndicesOut (list, optional): _description_. Defaults to None.
            Orders (list, optional): _description_. Defaults to None.
            Times (list, optional): _description_. Defaults to None.
            IndicesPrincipal (list, optional): _description_. Defaults to None.
        """
        if (IndicesIn!=None) and (IndicesOut!=None): 
            if (len(IndicesIn)<=self.NNode) and (len(IndicesOut)<=self.NNode):
                self.RelMat[0].append(Port)
                self.RelMat[1].append(IndicesIn)
                self.RelMat[2].append(IndicesOut)
                self.RelMat[3].append(Orders)
                self.RelMat[4].append(Times)
                self.RelMat[5].append(IndicesPrincipal)
                #print("\n NewRelation Called in FaultTreeR")
                #print(self.RelMat)
                self.Update()
                self.Sort()
        #print(self.RelMat)
            
        
    def AutoCompletion(self):
        nn=len(self.Node)
        for i in range(nn):
            #print("yeah !")
            #print(self.Node[i])
            for j in range(nn):
                if (i!=j) and self.InOrder2(self.Node[i],self.Node[j]):
                    self.NewRelation(1,self.Node[i],self.Node[j],None,None,None)
        """
        mm=self.NNode
        for i in range(nn):
            for j in range(mm):
                Temp=[0 for k in range(mm)]
                Temp[j]=1
                if (self.InOrder2(Temp,self.Node[i])) and (Temp!=self.Node[i]):
                    if not(Temp in self.Node):
                        if (len(self.Node)==self.NNode):
                            self.NNode+=1
                    self.NewRelation(1,Temp,self.Node[i],None,None,None)
        """
               
    def RecursiveStruturation(self):
        ##self.AutoCompletion()
        #print("\n RecursiveStruturation in FaultTreeR")
        #print("\n Nodes in RecursiveStruturation in FaultTreeR")
        #print(self.Node)
        for i in range(len(self.IdxTable[0])):
            Temp=self.IdxTable[2][i]
            #print("\n AdjMat: ")
            #print(self.AdjMat)
            nSon=0
            #print("\n Sons: ")
            for j in range(len(self.IdxTable[0])): #in range(len(self.Node)):
                if ((self.IdxTable[1][j]!=Temp) and (self.IdxTable[2][j]==Temp)):
                    nSon+=1#self.AdjMat[j][Temp]
                    #print((self.IdxTable[1][j],self.IdxTable[2][j]))
            #print(nSon)
            self.SubTree[Temp]=FaultTree(nSon+1)
            for j in range(len(self.IdxTable[0])):
                if (self.IdxTable[2][j]==Temp):
                    Temp1=self.RelMat[0][self.IdxTable[0][j]]
                    Temp2=self.RelMat[1][self.IdxTable[0][j]]
                    Temp3=self.RelMat[2][self.IdxTable[0][j]]
                    Temp4=self.RelMat[3][self.IdxTable[0][j]]
                    Temp5=self.RelMat[4][self.IdxTable[0][j]]
                    Temp6=self.RelMat[5][self.IdxTable[0][j]]
                    self.SubTree[Temp].NewRelation(Temp1,Temp2,Temp3,Temp4,Temp5,Temp6)
                    #print("\n NewRelation ")
                    #print(Temp1,Temp2,Temp3,Temp4,Temp5,Temp6)
                    #print("SubTree's Nodes ")
                    #print(self.SubTree[Temp].Node)
        
    def Generation(self):
        """_summary_
        """
        #print("\n Generation called in FaultTreeR")
        Temp1={i:self.Node[i] for i in range(len(self.Node))}
        Temp2={}
        res=[self.Leaves().copy()]
        #print("\n New generation")
        #print(res[-1])
        for i in res[0]:
            Temp2[i]=self.Node[i].copy()
            del(Temp1[i])
        while (Temp1!={}):
            Leaves=[]
            for j in Temp1.keys():
                Cond=True
                for  i in range(len(self.Node)):
                    if (((self.AdjMat[i][j]==1) or (self.InOrder2(self.Node[i],\
                         self.Node[j]))) and (i!=j)):
                        Cond=Cond and (i in Temp2.keys())
                if Cond :
                    Leaves.append(j)
            for k in Leaves:
                Temp2[k]=self.Node[k].copy()
                del(Temp1[k])
            res.append(Leaves)
            #print("\n New generation")
            #print(res[-1])
        #print("\n All cuts generated")
        return(res)
    
    def RecursiveReliability(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        #print("\n RecursiveReliability called in FaultTreeR")
        self.RecursiveStruturation()
        Temp=self.Generation()
        #print("\n All generations")
        #print(Temp)
        
        def LeafReliability(Generation,i,Option):
            #print("\n LeafReliability called in DefautTreeR")
            R=[]
            R2=[]
            for j in range(self.NComponent):
                if (self.Node[Generation[i]][j]==1):
                    R.append(sympy.Symbol("R"+str(j)))
                    if (Option==1):
                        """
                        print("\n self.NComponent")
                        print(self.NComponent)
                        print("\n Le node 1" )
                        print(self.Node[Genreration[i]])
                        """
                        
                        R2.append([self.IndFiabVal[j][k] for k in range(len(self.Time))])
                    else:
                        """
                        print("\n self.NComponent")
                        print(self.NComponent)
                        print("\n Le node 2" )
                        print(self.Node[Genreration[i]])
                        """
                        #print("\ Reliability steps")
                        #print([len(self.IndFiabFunc),j])
                        R2.append([self.IndFiabFunc[j](self.Time[k]) for k in range(len(self.Time))])
            self.Reliability[Generation[i]]={}
            #self.Reliability[Genreration[i]][0]=sympy.Symbol("R"+str(Genreration[i]))
            self.Reliability[Generation[i]][0]=R
            #self.Reliability[Genreration[i]][1]=[self.IndFiabVal[i][j] for j in range(len(self.Time))]
            self.Reliability[Generation[i]][1]=R2
            #self.Reliability[Genreration[i]][1]=[self.IndFiabFunc[i](self.Time[j]) for j in range(len(self.Time))]
            self.Reliability[Generation[i]][1]=R2
            #print(self.Reliability[Genreration[i]][0])
            #print(self.Reliability[Genreration[i]][1])
            #print(R)
            #print(R2)
        
        def BranchReliability(Generations,i,Option):
            #print("\n BranchReliability called in DefautTreeR")
            for k in range(len(Generations[i])):
                j=Generations[i][k]
                if (self.SubTree[j]==None):
                    LeafReliability(Generations[i],k,Option)
                    #print("Here")
                    #print(j)
                    #print(self.Reliability[j])
                    #print("Ok")

                else:
                    Temp1=self.SubTree[j]
                    #print("\n The subTree "+str([i,j]))
                    #print(Temp1.RelMat)
                    #print(Temp1.Node)
                    #print([Temp1.NNode,len(Temp1.Node)])
                    Temp2=[]
                    Temp3=[]
                    Temp4=[]
                    #print("\n Temp1.NNode 1")
                    #print(Temp1.NNode)
                    
                    for kk in range(Temp1.NNode):
                        if (Temp1.Node[kk]!=self.Node[j]): 
                            Temp2=[]
                            Temp3=[]
                            Temp4=[]
                            """
                            print("\n Les fiabilités connues :")
                            print(self.Reliability)
                            
                            print("\n Le node 3")
                            print(Temp1.Node[kk])
                            """
                            
                            for l in range(len(Temp1.Node[kk])):#range(self.NComponent):
                                if (Temp1.Node[kk][l]==1):
                                    Temp2.append(l)
                                    if (l<self.NComponent):
                                        Temp3.append(sympy.Symbol("R"+str(l)))
                                        if (Option==1):
                                            #print("\n Here 1 !")
                                            #print(self.IndFiabVal[l])
                                            Temp4.append([self.IndFiabVal[l][kkk] for kkk in range(len(self.Time))])
                                        else:
                                            #print("\n Here 2 !")
                                            #print(self.IndFiabFunc[l])
                                            Temp4.append([self.IndFiabFunc[l](self.Time[kkk]) for kkk in range(len(self.Time))])
                                    else:
                                        Node=[0 for kkk in range(len(Temp1.Node[kk]))]
                                        Node[l]=1
                                        ll=self.IdxNode(Node)
                                        #print("\n Les fiabilités connues :")
                                        #print(self.Reliability)
                                        #print("\n Here 30 !")
                                        #print(ll)
                                        #print(self.Reliability[ll])
                                        #print("Ok")
                                        
                                        Temp3.append(self.Reliability[ll][0][0])
                                        Temp4.append(self.Reliability[ll][1][0])
                            
                            #print(Temp3)
                            #print("\n Index 1")
                            #print(Temp2)
                            #print(Temp4)
                            #print(k)
                            #print(Temp2)
                            Temp5=self.Time
                            #print("\n Here 3 !")
                            #print(Temp2)
                            #print(Temp4)
                            #print(len(Temp4))
                            #print((Temp1,Temp2,Temp3,Temp4,None,Temp5,1))
                            print("Here")
                            print(j)
                            MyUpHasseDiagram=UpHasseDiagram(Temp1,Temp2,Temp3,Temp4,None,Temp5,1)
                            ##(Tree=FaultTree(2),IndivIndex=[0],IndivLabel=[0],IndivReliabilityVal=[[1]],IndivReliabilityFunc=[One],t=[0],Option=1)
                            
                            MyPolyFiab=MyUpHasseDiagram.GetPolyFiab()
                            
                            self.Reliability[j]={}
                            self.Reliability[j][0]=[MyPolyFiab[0]]
                            self.Reliability[j][1]=[MyPolyFiab[1]]
                            #print("\n Current Reliability :")
                            #print(self.Reliability[j][1])
                    #print("Here")
                    #print(j)
                    #print(self.Reliability[j])
                    #print("Ok")
      
        for i in range(len(Temp[0])):
            LeafReliability(Temp[0],i,self.Option)
            #print(i)
        
        if (len(Temp)>1):
            for i in range(1,len(Temp)):
                #print("In")
                #print(i)
                BranchReliability(Temp,i,self.Option)
                #print("Out")
                #print(i)
            
        res=[]
        for j in Temp[-1]:
            res.append(self.Reliability[j])
        
        #print("\n In BranchReliability ")
        #print("\n Reliability polynomial R= ")
        #print(res)
        return [self.Time,res]

    def ViewGraph(self,Dir=None):

        self.AutoCompletion()
        G=nx.DiGraph()
        GNode={}
        nn=len(self.Node)
        for i in self.AdjMat.keys():
            for j in range(len(self.AdjMat[i])):
                if (self.AdjMat[i][j]==1):
                    GNode[nn-1-self.IdxNode(self.Node[i])]=str(nn-1-self.IdxNode(self.Node[i]))+':'+self.Label[i]
                    GNode[nn-1-self.IdxNode(self.Node[j])]=str(nn-1-self.IdxNode(self.Node[j]))+':'+self.Label[j]
                    G.add_edge(GNode[nn-1-self.IdxNode(self.Node[i])],GNode[nn-1-self.IdxNode(self.Node[j])])
                    #G.add_edge(str(nn-1-self.IdxNode(self.Node[i]))+':'+self.Label[i],str(nn-1-self.IdxNode(self.Node[j]))+':'+self.Label[j])
                    #G.add_edge(str(self.Node[j]),str(self.Node[i]))
        #CompleteNode=self.Node.copy()
        
        mm=nn
        for i in range(nn):
            #print("yeah !")
            #print(self.Node[i])
            for j in range(nn):
                if (i!=j) and self.InOrder2(self.Node[i],self.Node[j]):
                    G.add_edge(GNode[nn-1-self.IdxNode(self.Node[i])],GNode[nn-1-self.IdxNode(self.Node[j])])
            for j in range(self.NNode):
                Temp=[0 for k in range(self.NNode)]
                Temp[j]=1
                if (self.InOrder2(Temp,self.Node[i])) and (Temp!=self.Node[i]):
                    #print(Temp)
                    if not(Temp in self.Node):
                        GNode[mm]=str(mm)+':'+ID_P(1)
                        G.add_edge(GNode[mm],GNode[nn-1-self.IdxNode(self.Node[i])])
                        mm+=1
                        #G.add_edge(str(self.Node[i]),str(Temp))
                    #CompleteNode.append(Temp)
        
        #print(G.adj)
        #fig=plt.figure(figsize=(5,5))
        plt.subplots(figsize=(10, 10))
        plt.clf() # Efface le contenu de la figure courante
        nx.draw_networkx(G,pos=nx.circular_layout(G),node_size=(10**4)/2)
        #nx.draw(G)
        #nx.draw(G,pos=nx.circular_layout(G),node_color='r',edge_color='b')
        plt.axis('off')
        #plt.grid(False)
        if (Dir!=None):
            plt.savefig(Dir+"AD.png")
            plt.savefig(Dir+"AD.pdf",format="pdf")
        plt.show()
        
"""
Dir="E:/Pedagogie/Encadrement/EncadrementEnsai/MasterRThese/20192020/TadieBenjaulys/"

MyTree=FaultTreeR(3,[[1],[1]],[One,One],[0],1)
MyTree.NewRelation(3,[1,1,0],[0,0,1])
print(MyTree.RecursiveReliability())
#MyTree.ViewGraph(Dir)

#MyUpHasseDiagram=UpHasseDiagram(MyTree,[0,1],[[1],[1]],[One,One],[0],1)

"""