"""
Definition of logic gates
"""

def Order(Times=[30,20,20]): 
    """
        Gets a list of numbers and returns a list of two sublists.
                
                 Parameters:
                     Times (list): a list of numbers
        
        The first one contains the ranks corresponding to the 
        expected position of each numbers in the inputed list 
        if it was sorted from the smallest to the highest.
        
        The second sublist is the sorted version of the inputed
        list.
        
        Examples:
        -------
        1)
        Input: [30,20,20]
        Output: [[3,1,2],[20,20,30]]
        2)
        Order([30,20,10])=[[3,2,1],[10,20,30]]
    """
    res=[[],[]]
    for i in range(len(Times)):
        j=1
        for k in range(len(Times)):
            if (Times[k]<Times[i]):
                j=j+1
        while (j in res[0]):
            j=j+1
        res[0].append(j) # res[0][i] Order of index i
        res[1].append(0) # res[1][i] Index of the order i
    for i in range(len(Times)):
        res[1][int(res[0][i])-1]=Times[i]
    return res
#print(Order.__doc__)
#print(Order())
#print(Order([30,20,10]))
    
def InOrder(Orders=[1,3,2],Times=[10,20,30]): 
    """
        Gets two lists of numbers and returns a boolean.
        The first list contains ordinal numbers.
        
        The answer is true if the second list is ordered 
        according to the respective orders given in the
        first list.
            
               Parameters:
                     Times (list): a list of numbers
                     Orders (list): a list of numbers
          
        
        Examples:
        -------
        1)
        Input: 
            Orders=[1,3,2]
            Times=[10,20,30]
        Output: False
        2)
        InOrder([1,3,2],[10,30,20])=True
    """
    Temp=[Times[int(Orders[i])-1] for i in range(len(Orders))]
    res=True
    for i in range(len(Orders)-1):
        res=(res and (Temp[i]<=Temp[i+1]))
    return res
#print(InOrder.__doc__)
#print(InOrder())
#print(InOrder([1,3,2],[10,30,20]))
    
def RemoveEmpty(ValuesIn=[[],[1],[],[5]],Orders=None,\
                Times=None,IndicesPrincipal=None):
    """
        Takes as input four arguments:
            
             Parameters:
                 ValuesIn: a list of list
                 Orders (default=None): a list of ordinal values
                 Times (default=None): a list of numbers
                 IndicesPrincipal (default=None): a list of numbers
        
        When the lists 'Orders', 'Times' and 'IndicesPrincipal' are
        non-zero they must be of the same length as the 'ValuesIn' list.

        
        RemoveEmpty removes sub-lists of 'ValuesIn' and items with the same index in 
        index in the 'Orders', 'Times' and 'IndicesPrincipal' lists.
        
        Examples:
        -------
        1)
        Input: 
            ValuesIn=[[],[1],[],[5]]
            Orders=None
            Times=None
            IndicesPrincipal=None
            
        Output: [[[1],[5]],None,None,None]
        2)
        RemoveEmpty([[],[1],[],[5]],[1,2,3,4],[1,2,3,4],[1,0,1,1])=
        [[[1], [5]], [1], [2, 4], [0, 1]]
    """
    i=0
    n=len(ValuesIn)
    while (i<n):
        if (ValuesIn[i]==[]):
            del(ValuesIn[i])
            if (Orders!=None):
                del(Orders[i])
            if (Times!=None):
                del(Times[i])
            if (IndicesPrincipal!=None):
                del(IndicesPrincipal[i])
            i=i-1
            n=n-1
        i=i+1
    return [ValuesIn,Orders,Times,IndicesPrincipal]
#print(RemoveEmpty.__doc__)
#print(RemoveEmpty([[],[1],[],[5]],[1,2,3,4],[1,2,3,4],[1,0,1,1]))      

   
def Reducible(x=[1,0,1],y=[1,1,0]):
    """
        Gets in input two lists of numbers having the same length
        and return True if they are different on exactly one term.
                Parameters:
                    x: a list of numbers
                    y: a list of numbers
         
        Examples:
        -------
        1)
            Input: ([1,0,1],[1,1,0])    
            Output: False  
        2) 
            Reducible([1,0,1],[1,0,0])=True
    """
    res=False
    #Temp1=[x[i]-y[i] for i in range(len(x))]
    Temp2=sum([abs(x[i]-y[i]) for i in range(len(x))])
    if (Temp2==1):  #x est reducible par y
        res=True
        #for i in range(len(x)):
            #res.append(max(x[i],y[i])) 
    return res
#print(Reducible.__doc__)
#print(Reducible([1,0,1],[1,1,0]))
#print(Reducible([1,0,1],[1,0,0]))

    
def G_ID(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None): #Identité

    """
        Gets in input 
                 Parameters:
                     ValuesIn: a list of list
                     Orders (default=None): a list of ordinal values
                     Times (default=None): a list of numbers
                     IndicesPrincipal (default=None): a list of numbers
        Examples:
        -------
        1)
            Input: ([1,0,1],[1,1,0])    
            Output: False  
        2) 
            

    """
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal) 
    return ValuesIn
#print(G_ID())

"""
def G_OR(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None):
    res=[]
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)
    Temp=ValuesIn.copy()
    for i in range(len(Temp)):
        for j in range(len(Temp[i])):
            if not(Temp[i][j] in res):
                res.append(Temp[i][j])
    return [res]
"""
def G_OR(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None):
    """
        Gets in input 
        
        Takes as input four arguments:
        
                Parameters:
                    ValuesIn: a list of list
                    Orders (default=None): a list of ordinal values
                    Times (default=None): a list of numbers
                    IndicesPrincipal (default=None): a list of numbers
        
        When the lists 'Orders', 'Times' and 'IndicesPrincipal' are
        non-zero they must be of the same length as the 'ValuesIn' list.

        
        RemoveEmpty removes sub-lists of 'ValuesIn' and items with the same index in 
        index in the 'Orders', 'Times' and 'IndicesPrincipal' lists and 

          Examples:
        -------
       
            Input: [1,0,1],[1,1,0]],[[0,1,0]]   
            Output: G_OR= ([[[1,0,1],[1,1,0]],[[1,0,0]]]))
       
       
    """
    res=[]
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)    #Suppression des portes vides
    Temp=ValuesIn.copy()
    if (len(Temp)>0):
        res=Temp[0].copy()
        if (len(Temp)>1):
            for i in range(1,len(Temp)): 
                n=len(res)
                Temp1=[]
                for j in range(len(Temp[i])):    
                    for l in range(n):
                        if (Reducible(Temp[i][j],res[l])):
                            Temp2=[]
                            for k in range(len(Temp[i][j])):
                                if (Temp[i][j][k]*res[l][k]==0):
                                    Temp2.append(0)
                                else:
                                    Temp2.append(max(-1,min(1,Temp[i][j][k]+res[l][k])))
                            if not(Temp2 in Temp1):
                                Temp1.append(Temp2)
                        else:
                            if not(res[l] in Temp1):
                                Temp1.append(res[l])
                            if not(Temp[i][j] in Temp1):
                                Temp1.append(Temp[i][j])
                res=Temp1
    return [res]
#print(G_OR())
#print(G_OR([[[1,0,1],[1,1,0]],[[1,0,0]]]))
    
def G_AND(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None): #AND
    """summary G_AND

    Args:
        ValuesIn (list, optional): _description_. Defaults to [[[1,0,1],[1,1,0]],[[0,1,0]]].
        Orders (list, optional): a list of ordinal values. Defaults to None.
        Times (list, optional): a list of numbers. Defaults to None.
        IndicesPrincipal (list, optional): a list of numbers. Defaults to None.

    Returns:
        liste: _description_
    
          Exemples:
        -------
       
            Input:ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]]  
            Output: G_OR= ([[[1,0,1],[1,1,0]],[[1,0,0]]]))
   

    """
    res=[]  #res=[[1,0,0],[0,1,0]]
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)   #Suppression des portes vides
    Temp=ValuesIn.copy() #Temp=[[[1,0,1],[1,1,0]],[[0,1,0]]]
    if (len(Temp)>0):   #Temp=[[[1,0,1],[1,1,0]],[[0,1,0]]]
        res=Temp[0].copy()  #res=[[1,0,1],[1,1,0]]
        if (len(Temp)>1):   
            for i in range(1,len(Temp)): 
                n=len(res)
                Temp1=[]
                for j in range(len(Temp[i])):    
                    for l in range(n):
                        Temp2=[]
                        for k in range(len(Temp[i][j])):
                            if (Temp[i][j][k]*res[l][k]!=-1):
                                 Temp2.append(max(-1,min(1,Temp[i][j][k]+res[l][k])))
                            else:
                                print("Bad")
                        if ((len(Temp2)==len(Temp[i][j])) and (not(Temp2 in Temp1))):
                            Temp1.append(Temp2)
                res=Temp1
    return [res]
#print(G_AND())
    
def G_NOT(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None): #NOT
    """summary G_NOT

    Args:
        ValuesIn (list, optional): _description_. Defaults to [[[1,0,1],[1,1,0]],[[0,1,0]]].
        Orders (list, optional): _description_. Defaults to None.
        Times (list, optional): _description_. Defaults to None.
        IndicesPrincipal (list, optional): _description_. Defaults to None.

    Returns:
        list: _description_
    Exemples:
    -------
       
            Input:ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]]  
            Output: G_NOT= [[1,0,1],[1,1,0]]
    """
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal) 
    res=ValuesIn.copy()
    l=len(res)
    for i in range(l): #res=[[1,0,1],[1,1,0]]
        ll=len(res[i])
        if (ll==1):
            lll=len(res[i][0])
            if (sum([abs(res[i][0][k]) for k in range(lll)])<=1):
                for j in range(lll):
                    res[i][0][j]=-res[i][0][j]
            else:
                Temp1=[]
                for j in range(lll):
                    if (res[i][0][j]!=0):
                        Temp2=[0 for k in range(lll)]
                        Temp2[j]=res[i][0][j]
                        Temp1.append(G_NOT([[Temp2]])[0])
                res=G_OR(Temp1)
        else:
            res[i]=G_AND([G_NOT([[res[i][j]]])[0] for j in range(ll)])[0]
    return res
#print(G_NOT())
    
def G_PAND(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=[0,0,0],Times=[0,0,0],IndicesPrincipal=None): #PAND
    """G_PAND

    Args:
        ValuesIn (list, optional): _description_. Defaults to [[[1,0,1],[1,1,0]],[[0,1,0]]].
        Orders (list, optional): _description_. Defaults to [0,0,0].
        Times (list, optional): _description_. Defaults to [0,0,0].
        IndicesPrincipal (list, optional): _description_. Defaults to None.

    Returns:
        list: nom du porte PAND appelle
    Exemples:
    -------
       
            Input:
                ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]] 
                Orders=[0,0,0] 
                Times=[0,0,0]
            Output: 
             1 Porte PAND appellee 1
             2 Porte PAND appellee 2
    """
    res=[[]]
    if InOrder(Orders,Times):
        res=G_AND(ValuesIn,Orders,Times,IndicesPrincipal)
        print("Porte PAND appellee 1")
    else:
        print("Porte PAND appellee 2") 
        if (len(ValuesIn)>0):
            n=len(ValuesIn[0][0])
            res[0]=[[0 for i in range(n)]]
            #print(Orders)
            #print(Times)
    return res
#print(G_AND())

def G_FDEP(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=None,IndicesPrincipal=None): #
    """G_FDEP

    Args:
        ValuesIn (list, optional): _description_. Defaults to [[[1,0,1],[1,1,0]],[[0,1,0]]].
        Orders (list, optional): _description_. Defaults to None.
        Times (list, optional): _description_. Defaults to None.
        IndicesPrincipal (list, optional): _description_. Defaults to None.

    Returns:
        list : _description_
    
    Exemples:
    -------
   
        Input:
            ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]] 

        Output: G_FDEP=[[1,0,1],[1,1,0]]

    """
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)    #Suppression des portes vides
    res=[[]]    #res=[[1,0,1],[1,1,0]]
    Temp=ValuesIn.copy()
    if (len(Temp)>0):
        res=[Temp[0].copy()]
        if (len(Temp)>1):
            res=G_OR(G_NOT(res)+[Temp[i] for i in range(1,len(Temp))]) 
    return res
#print(G_FDEP())
    
def G_SPARE(ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=None,Times=[30,20],IndicesPrincipal=[1,0]):   #SPARE
    """SPARE

    Args:
        ValuesIn (list, optional): _description_. Defaults to [[[1,0,1],[1,1,0]],[[0,1,0]]].
        Orders (_type_, optional): _description_. Defaults to None.
        Times (list, optional): _description_. Defaults to [30,20].
        IndicesPrincipal (list, optional): _description_. Defaults to [1,0].

    Returns:
        list : _description_
 
    Exemples:
    -------
   
        Input:
            ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]]
            Times=[30,20] 
            IndicesPrincipal=[1,0]

        Output: G_SPARE=[[1,0,1],[1,1,0]]

    """
    [ValuesIn,Orders,Times,IndicesPrincipal]=RemoveEmpty(ValuesIn,Orders,Times,IndicesPrincipal)    #Suppression des portes vides
    Temp1=[]
    Temp2=[]
    for i in range(len(IndicesPrincipal)):  #IndicesPrincipal=[1,0]
        if (IndicesPrincipal[i]==1):
            Temp1.append(i)
        elif (IndicesPrincipal[i]==0):
            Temp2.append(i)
    Orders=Order(Times)[1]  #Orders=[0,1]
    Temp3=[Orders[i] for i in Temp1]
    Temp4=[Orders[i] for i in Temp2]
    Temp5=ValuesIn.copy()
    res=[]
    for i in range(len(Temp3)): #Temp3=[0,1]
        if (i<len(Temp4)):
            res+=G_AND([Temp5[int(Temp3[i])]]+[Temp5[int(Temp4[i])]])
        else:
            res+=[Temp5[int(Temp3[i])]]
    return res
#print(G_SPARE())

def G_Gen(n=1,ValuesIn=[[[1,0,1],[1,1,0]],[[0,1,0]]],Orders=[0,0,0],Times=[30,20,40],IndicesPrincipal=[1,0]):

    
    """
            Gets in input 
                 Parameters:
                     n (int, optional): number of elements. The default value is 1.
                     ValuesIn (list, optional): _description_. The default value is [[[1,0,1], [1,1,0]], [[0,1,0]].
                     Orders (list, optional): _description_. Default value is [0,0,0].
                     Hours (list, optional): _description_. The default value is [30,20,40].
                     MainIndexes (list, optional): _description_. The default value is [1,0].
             
            Examples:
            -------
            1)
                Input: (2)    
                Output: "G_NOT"  
            2) 
                G_Gen(0)= G_ID()
                G_Gen(1)= G_ID()
                G_Gen(2)= G_NOT()
                G_Gen(3)= G_OR()
                G_Gen(4)= G_AND()
                G_Gen(5)= G_PAND()
                G_Gen(6)= G_FDEP()
                G_Gen(n)= G_SPARE, for any n>6

        """
    """G_Gen

    Args :
        n (int, optional): number of elements. The default value is 1.
        ValuesIn (list, optional): _description_. The default value is [[[1,0,1], [1,1,0]], [[0,1,0]].
        Orders (list, optional): _description_. Default value is [0,0,0].
        Hours (list, optional): _description_. The default value is [30,20,40].
        MainIndexes (list, optional): _description_. The default value is [1,0].

    Retourne :
       list: contains the list values of G_Input, G_ID, G_NOT, G_OR, G_AND, G_PAND, G_FDEP, G_SPARE
    """
    if n==0:
        return G_ID(ValuesIn,Orders,Times,IndicesPrincipal)  
    elif n==1:  
        return G_ID(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==2:
        return G_NOT(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==3:
        return G_OR(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==4:
        return G_AND(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==5:
        return G_PAND(ValuesIn,Orders,Times,IndicesPrincipal)
    elif n==6:
        return G_FDEP(ValuesIn,Orders,Times,IndicesPrincipal)
    else:
        return G_SPARE(ValuesIn,Orders,Times,IndicesPrincipal)

#print(G_Gen())
        
def ID_G(n=1):  #ID_G    
    
    """
            Gets in input n (int, optional): generates the IDs of the different inputs. Defaults to 1.
                 
                  Parameters:
                      n (int,optional): a positive integer
                      
                  returns: 
                      IDs of the different inputs
             
            Examples:
            -------
            1)
                Input: (2)    
                Output: "G_NOT"  
            2) 
                ID_G(0) = "G_Input"
                ID_G(1) = "G_ID"
                ID_G(2) = "G_NOT"
                ID_G(3) = "G_OR"
                ID_G(4) = "G_AND"
                ID_G(5) = "G_PAND"
                ID_G(6) = "G_FDEP"
                ID_G(n) = "G_SPARE", for any n>6

        """
    if n==0:
        return "G_Input"
    elif n==1:
        return "G_ID"
    elif n==2:
        return "G_NOT"
    elif n==3:
        return "G_OR"
    elif n==4:
        return "G_AND"
    elif n==5:
        return "G_PAND"
    elif n==6:
        return "G_FDEP"
    else:
        return "G_SPARE"
#print(ID_G())  #ID==