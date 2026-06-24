#N-solver



A = ["a","b","c","d","e","f"] 

R = {}

pi = {}

for i in range(len(A)):
    R[A[i]]=i
    if i == 0:
        R["-"+A[i]]=1
    else:
        R["-"+A[i]]=0

        
            

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
                if a[0]=="-":
                    return self.pi["-"+a[2]]
                else:
                    return self.pi[a[1]]
        #Assuming that formulae are already in negation normal form. Will maybe impliment later nnf function. Assuming also that parameter variables do not appear bounded by a quantifier.
        if a[0] == "D": #Disjunction is handled as addition
            b,c = self.subs(a)
            return self.evaluate(b,{})+self.evaluate(c,{})
        
        if a[0] == "C": #Conjunction is handled as multipliation
            b,c = self.subs(a)
            return self.evaluate(b,{})*self.evaluate(c,{})
        
        if a[0]=="E": 
            y,b = self.subs(a)
            sum = 0
            for i in self.A:
                sum+= self.evaluate(self.substitution(b,y,i),{})
            return sum
        
        if a[0]=="F": 
            y,b = self.subs(a)
            prod = 1
            for i in self.A:
                prod*= self.evaluate(self.substitution(b,y,i),{})
            return prod

    def is_literal(self,a):
        return "(" not in a
    
    def ground(self,a,x): #grounds the variables in a with a valuation function x
        if len(x)==0:
            return a
        newformula = a
        for i in x.keys():
            newformula = self.substitution(newformula,i,x[i])
        return newformula

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
    solver = Nsolver(A,R)
    psi1 = "D(Rb,Rc)"
    psi2 = "E(x,R(x))"
    psi3 = "x=y"
    psi4 = "C(Rb,Rc)"
    psi4 = "C(D(Rb,Rc),C(Rb,Rc))"
    psi5 = "E(x,x=x)"
    psi6 = "F(x,E(y,C(-x=y,Ry)))"
    psi7 = "E(x,E(y,C(C(-x=y,Ry),Rx)))"
    print(solver.subs(psi1))
    print(solver.subs(psi2))
    print(solver.substitution(psi2,"x","a"))
    print(solver.ground(psi3,{"x":"a","y":"a"}))
    print(solver.evaluate("a=a",{}))
    print(solver.evaluate("-a=b",{}))
    print(solver.evaluate("Rx",{"x":"d"}))
    print(solver.evaluate("Rb",{}))
    print(solver.evaluate("Rc",{}))
    print(solver.evaluate(psi1,{}))
    print(solver.evaluate(psi4,{}))
    print(solver.evaluate(psi5,{}))
    print(solver.evaluate(psi6,{}))
    print(solver.evaluate(psi7,{}))
        




