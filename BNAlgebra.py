# -*- coding: utf-8 -*-
# COPYRIGHT 2019 Gurkeerat Chhina, Claudius Zibrowius
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from fractions import Fraction
from itertools import groupby

import Cob

def ToExponent(exponent):
    return str(exponent).translate(str.maketrans("-0123456789.", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹·"))

def inverse(num,field): #this only works over a field
    if field == 0:
        return Fraction(1)/num
    elif field == 1:
        if num in [1, -1]:
            return num
        else: 
            raise Exception("Can't invert over Z")
    else: #taken from https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
        s = 0
        S = 1
        r = field
        R = num
        while r != 0:
            q = R // r
            R, r = r, R - q * r
            S, s = s, S - q * s
        #print((S*num)%self.field) # should be 1 if computed correctly
        return S

class obj(object):
    """An object is a pair [idempotent,q,h,delta(optional)], where idempotent is either 0 (b=solid dot) or 1 (c=hollow dot). 
    """
    __slots__ = 'idem','q','h','delta'
    
    def __init__(self,idempotent,q,h,delta="default"):
        self.idem = idempotent
        self.q = q
        self.h = h
        if delta=="default":
            self.delta = q/2-h
        else:
            self.delta = delta
    
    def idem2dot(self):
        if self.idem==0:
            return "●"#b (solid dot)
        else: 
            return "○"#c (hollow dot)
    
    def obj2string(self,switch="idem",index=-1):        
        
        if "idem" in switch:
            idem=self.idem2dot()
        else:
            idem = ""
        
        if (index == -1) or ("index" not in switch):
            index = ""
        else:
            index = str(index)
        if "q" in switch:
            q="q"+ToExponent(self.q)
        else:
            q=""
        if "h" in switch:
            h="h"+ToExponent(self.h)
        else:
            h=""
        if "delta" in switch:
            if 2*self.delta % 2 == 0: # delta is an integer
                delta="δ"+ToExponent(round(self.delta))
            else:
                #delta="δ"+ToExponent(round(2*self.delta))+"'²"
                delta="δ"+ToExponent(self.delta)
            
        else:
            delta=""
        
        grading=q+h+delta
        
        if (grading == "") or (index == ""):
            return index+grading+idem
        else:
            return index+":"+grading+idem
    
    def shift_q(self,shift): #shift q, keep h fixed; create new object
        return obj(self.idem,self.q+shift,self.h,self.delta+shift/2)
        
    def shift_h(self,shift): #shift h, keep q fixed; create new object
        return obj(self.idem,self.q,self.h+shift,self.delta-shift)
    
    def ToCob(self):
        arcs = []
        if self.idem == 0:
            arcs = [3,2,1,0]
        else:
            arcs = [1,0,3,2]
        return Cob.obj(1,3, arcs, self.h, self.q, self.delta)

def coeff_simplify(num,field):
    if field > 1:
        return num % field
    else: # This probably needs to be fixed for field=0
        return num 

class mor_alt(object):# work in progress
    """An element of Bar-Natan's algebra is a list of pairs [power,coeff]
    'power' is an integer, which determines the exponent of D (if positive) and the exponent of S (if negative)
    'coeff' is some non-zero integer (= coefficient in the base ring/field) # Alternatively, a Fraction object
    """
    import numpy as np # move this to the top of the file if used
    #__slots__ = 'pairs'
    
    def __init__(self,S,D,I):
        self.S = np.array(S) # list of coefficients
        self.D = np.array(D) # list of coefficients
        self.I = I #coefficient
    
    def simplify_mor(self,field):
        """simplify algebra elements by omitting superflous zeros."""
        self.S=[coeff_simplify(i,field) for i in self.S]
        self.D=[coeff_simplify(i,field) for i in self.D]
        self.I=coeff_simplify(self.I,field)
        while self.S[-1] ==0:
            del self.S[-1]
        while self.D[-1] ==0:
            del self.D[-1]
        return self
    
    def __add__(self, other):
        
        #newS = [a+b for a,b in zip_longest(self.S,other.S)]
        if len(self.S) < len(other.S):
            newS = other.S.copy()
            newS[:len(self.S)] += self.S
        else:
            newS = self.S.copy()
            newS[:len(other.S)] += other.S
        
        #newD = [a+b for a,b in zip_longest(self.D,other.D)]
        if len(self.D) < len(other.D):
            newD = other.D.copy()
            newD[:len(self.D)] += self.D
        else:
            newD = self.D.copy()
            newD[:len(other.D)] += other.D
        
        return mor(newS,newD,self.I+other.I).simplify_mor()

    def __mul__(self, other):
        newSmatrix = np.tensordot(self.S,other.S,axes=0)
        newS= [sum(np.diagonal(A[:, ::-1],len(other.S)-index)) for index in range(len(self.S)+len(other.S)-1)]
        
        newDmatrix = np.tensordot(self.D,other.D,axes=0)
        newD= [sum(np.diagonal(A[:, ::-1],len(other.D)-index)) for index in range(len(self.D)+len(other.D)-1)]
        
        return mor([[a1[0]+a2[0],a1[1]*a2[1]] for a1 in self.pairs for a2 in other.pairs if a1[0]*a2[0]>=0]).simplify_mor()
    
class mor(object):
    """An element of Bar-Natan's algebra is a list of pairs [power,coeff]
    'power' is an integer, which determines the exponent of D (if positive) and the exponent of S (if negative)
    'coeff' is some non-zero integer (= coefficient in the base ring/field) # Alternatively, a Fraction object
    """
    __slots__ = 'pairs','field'
    
    def __init__(self,pairs,field):
        self.pairs = pairs
        self.field = field
    
    def simplify_mor(self,field):
        """simplify algebra elements by adding all coeffients of the same power of D or S, omitting those with coefficient 0. This is very similar to simplify_decos"""
        def droplast(l):
            return l[:-1]
        def add_coeffs(iterable):
            coeff=0
            for x in iterable:
                coeff+=x[-1]
            return coeff_simplify(coeff,field)
        self.pairs = [power+[add_coeffs(grouped)] for power,grouped in groupby(sorted(self.pairs),droplast)]
        self.pairs = [x for x in self.pairs if x[-1]!=0]
        if self.pairs == []:
            return 0
        return self
    
    def __add__(self, other):
        if other == 0:
            return self
        return mor(self.pairs+other.pairs,self.field).simplify_mor(self.field)
    
    def __radd__(self, other):
        if other == 0:
            return self
        return mor(self.pairs+other.pairs,self.field).simplify_mor(self.field)

    def __mul__(self, other):
        if other == 0:
            return 0
        if isinstance(other,mor):
            return mor([[a1[0]+a2[0],a1[1]*a2[1]] for a1 in self.pairs for a2 in other.pairs if a1[0]*a2[0]>=0],self.field).simplify_mor(self.field)
        # 'other' is assumed to be a non-zero integer
        return mor([[pair[0],other*pair[1]] for pair in self.pairs],self.field).simplify_mor(self.field)
        
    def __rmul__(self, other):
        if other == 0:
            return 0
        return mor([[a1[0]+a2[0],a1[1]*a2[1]] for a1 in self.pairs for a2 in other.pairs if a1[0]*a2[0]>=0],self.field).simplify_mor(self.field)
    
    def is_identity(self):
        if len(self.pairs)!=1:
            return False
        elif self.pairs[0][0]!=0:
            return False
        elif self.pairs[0][1] in [1,-1]:
            return True
        else:
            return False
            
    def is_isomorphism(self):
        if len(self.pairs)!=1:
            return False
        elif self.pairs[0][0]!=0:
            return False
        elif self.pairs[0][1]==0:
            return False
        return True
    
    def contains_D(self):
        return all([pair[0]<=0 for pair in self.pairs])==False
    
    def contains_S(self):
        return all([pair[0]>=0 for pair in self.pairs])==False
    
    def __neg__(self):
        return mor([[pair[0],(-1)*pair[1]] for pair in self.pairs],self.field)
    
    def __str__(self):
        string=""
        for pair in self.pairs:
            coeff = pair[1]
            if (string != "") & (coeff > 0):# add plus sign if the next coefficient is positive, except for the first summand
                string += "+"
            if coeff < 0: # add minus sign in any case
                string += "-"
                coeff = abs(coeff)
            
            if coeff != 0:# omit any summands with coefficient 0
            
                exponent=abs(pair[0])
                if exponent==1: # omit exponent 1 from the notation
                    exponent = ""
                else:
                    exponent= ToExponent(exponent)
                
                if coeff==1: # omit coefficients 1 and -1 from the notation
                    coeff = ""
                else:
                    coeff = str(coeff) + "·"
                
                if pair[0] > 0:# powers of D
                    string += coeff + "D" + exponent
                if pair[0] < 0:
                    string += coeff + "S" + exponent
                if pair[0] == 0:
                    string += coeff + "id"
        return string
    
    def ToCob(self, sourceCLT, targetCLT):# does not work yet, since Z is not implemented over BNAlgebra and Cob is only implemented over Z.
        if self.field != 1:
            raise Exception("You are converting a morphism in BNalgebra with coefficients in field={} into a morphism in Cob. However, the category Cob is only implemented over integers, ie for field=1.".format(field))
        decos = []
        
        for pair in self.pairs:
            if pair[0] > 0 : 
                decos.append([pair[0]-1, 0, 1, pair[1]])
            elif pair[0] == 0: 
                decos.append([0, 0, 0, pair[1]])
            elif pair[0] %2 == 0:
                power = int(Fraction(-1*pair[0], 2))
                decos.append([power, 0, 0, ((-1)** power) *pair[1]]) #(-H)^(n/2)
                decos.append([power - 1, 0, 1, ((-1)** (power -1)) *pair[1]]) #(-H)^(n/2-1) D
            elif pair[0] %2== 1: 
                power = int(Fraction(-1*pair[0] -1, 2))
                decos.append([power, 0, ((-1)** power)*pair[1] ])#(-H)^((n-1)/2) S
            else: 
                raise Exception("pair is not an integer?")
        mor = Cob.mor(sourceCLT, targetCLT, decos)
        mor.ReduceDecorations()
        return mor

