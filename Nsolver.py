#N-solver



A = ["a","b","c","d","e","f"] 

R = {}

Q = {}

for i in range(len(A)):
    R[A[i]]=i
    if i == 0:
        R["-"+A[i]]=1
    else:
        R["-"+A[i]]=0

for i in A:
    for j in A:
        Q[i+j]=1
        Q["-"+i+j]=0



pi = {"R":R,"Q":Q} #Example interpretation. Interpretation is a dir of predicates, which are themselves directories of the values for literals
        
            

class Nsolver:

    def __init__(self,A,pi):
        self.A = A
        self.pi = pi
    
    def evaluate(self,a,x):
        a = self.ground(a,x)
        if self.is_literal(a):
            if "=" in a:
                if a[0]=="-": # x!=y return 1 if true, 0 else
                    if a[1]==a[3]:
                        return 0
                    else:
                        return 1
                else:   #x=y return 1 if true, 0 else
                    if a[0]==a[2]:
                        return 1
                    else:
                        return 0
            else: #a is a predicate literal
                L,v=self.literal_args(a)
                return self.pi[L][v]
        # Assuming that quantified variables do not appear as free variables.
        if a[0] == "D": #Disjunction is handled as addition
            b,c = self.subs(a)
            return self.evaluate(b,{})+self.evaluate(c,{})
        
        if a[0] == "C": 
            #Conjunction is handled as multipliation
            b,c = self.subs(a)
            return self.evaluate(b,{})*self.evaluate(c,{})
        
        if a[0]=="E": 
            #Exists sums over the domain
            y,b = self.subs(a)
            sum = 0
            for i in self.A:
                sum+= self.evaluate(self.substitution(b,y,i),{})
            return sum
        
        if a[0]=="F": 
            #For all multiplies over domain
            y,b = self.subs(a)
            prod = 1
            for i in self.A:
                prod*= self.evaluate(self.substitution(b,y,i),{})
            return prod
        
        if a[0]=="-":
            #Push negation down eventually to literals
            return self.evaluate(self.push_negation(a),{})

    def is_literal(self,a):
        return "(" not in a
    
    def literal_args(self,a):
        # returns the relation symbol and variables of a literal. If negated literal, then returns "-" in front of variables
        start = 0
        for i in range(len(a)):
            if a[i].islower():
                start = i
                break
        if a[0]=="-":
            return a[1:start],"-"+a[start:]
        else:
            return a[:start],a[start:]
    
    def ground(self,a,x): 
        #grounds the variables in a with a valuation function x
        if len(x)==0:
            return a
        newformula = a
        for i in x.keys():
            newformula = self.substitution(newformula,i,x[i])
        return newformula
    
    def push_negation(self,a):
        #Push negation down one subformula using De Morgan's laws. -D(A,B)<->C(-A,-B), -C(A,B)<->D(-A,-B), -E(x,A)<->F(x,-A) , -F(x,A)<->E(x,-A)
        A,B = self.subs(a)
        if B[0]=="-":
            B=B[1:]
        else:
            B="-"+B
        if A[0].isupper():
            A = "-"+A
        elif A[0]=="-":
            A = A[1:]

        if a[1]=="D":
            return "C("+A+","+B+")"
        if a[1]=="C":
            return "D("+A+","+B+")"
        if a[1]=="E":
            return "F("+A+","+B+")"
        if a[1]=="F":
            return "E("+A+","+B+")"

    def substitution(self,a,x,b):
        # substitute all instances of x in formula a with b
        newformula = ""
        for i in a:
            if i ==x:
                newformula+=b
            else:
                newformula+=i
        return newformula

    def subs(self,a):
        # returns subformulae
        for i in range(len(a)):
            if a[i]=="(":
                start=i
                break
        
        if a[start-1] in ["E","F"]:
            return (a[start+1],a[start+3:-1])

        count = 0
        end = None
        for i in range(start+1,len(a)):
            if a[i]=="(":
                count+=1
            if a[i]==")":
                count-=1
                if count == 0:
                    end = i
                    break
        if not end:
            b,c = a.split(",")
            return (b[start+1:],c[:-1])
        return (a[start+1:end+1],a[end+2:-1])
    





if __name__ == "__main__":
    solver = Nsolver(A,pi)
    psi1 = "D(Rb,Rc)"
    psi2 = "E(x,R(x))"
    psi3 = "D(-Qxy,Ry)"
    psi4 = "C(D(Rb,Rc),C(Rb,Rc))"
    psi5 = "E(x,x=x)"
    psi6 = "F(x,E(y,C(-x=y,Ry)))"
    psi7 = "E(x,E(y,C(C(-x=y,Ry),Rx)))"
    print(solver.evaluate(psi3,{"x":"a","y":"b"}))
    print(solver.evaluate(psi4,{}))
    print(solver.evaluate(psi5,{}))
    print(solver.evaluate(psi6,{}))
    print(solver.evaluate(psi7,{}))
