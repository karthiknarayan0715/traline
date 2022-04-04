import math
from flask import flash, redirect, url_for
import cmath
from cmath import phase

def MGMD(a, b, c):
    return (a*b*c)**(1/3)
def SGMD(n, l, r):
    if n==1:
        return 0.7788*r
    elif n==2:
        return (r*0.7788*(l**(n-1)))**(1/n)
    elif n==3:
        return (0.7788*r*(l**(n-1)))**(1/n)
    elif n==4:
        return ((2**0.5)*0.7788*r*(l**(n-1)))**(1/n)
    elif n==5:
        return ((1.618**2)*0.7788*r*(l**(n-1)))**(1/n)
    elif n==6:
        return (3*2*0.7788*r*(l**(n-1)))**(1/n)
    elif n==7:
        return (16.39*0.7788*r*(l**(n-1)))**(1/n)
    else:
        return (9.2426*2.1631*0.7788*r*(l**(n-1)))**(1/n)
def inductance(mgmd, sgmd):
    return 2*(10**-7)*math.log(mgmd/sgmd)/1000
def capacitance(mgmd, sgmd):
    return (10**-9)/18*math.log(mgmd/sgmd)/1000
def capacitive_recatance(c, f):
    return 1/(2*math.pi*f*c)
def inductive_reactance(l, f):
    return 2*math.pi*f*l

def radius(d_strand, n_s_c):
    r = -1
    if int(n_s_c) == 1:
        r = d_strand/2
    elif int(n_s_c) == 7:
        r = 3*d_strand/2
    elif int(n_s_c) == 19:
        r = 5*d_strand/2
    elif int(n_s_c) == 37:
        r = 7*d_strand/2
    elif int(n_s_c) == 61:
        r = 9*d_strand/2
    else:
        flash("Invalid no. of strands")
    return r*10**-2

def check_form(form):
    for field in form.values():
        try:
            float(field)
        except:
            print(field)
            return False
    return True

def verify_data(data):
    allowed = [1, 7, 19, 37, 61]
    if data['pf']>1 or data['pf']<-1:
        flash('Invalid power factor!')
        return False
    try:
        if not int(data['n_s_c']) in allowed:
            flash('Invalid input!')
            return False
    except ValueError:
        flash('Invalid input!')
        return False
    return True

def cc(Is,Ir):
    return abs(Is) - abs(Ir)


def shortline_ABCD(L,R):
    return complex(1,0),complex(R,L),complex(0,0),complex(1,0)

def mediumline_ABCD(Z,Y):
    return Z*Y/2 +1,Z,Y*(Z*Y/4 +1),Z*Y/2 +1

def longline_ABCD(Z,Y):
    return cmath.cosh((Z*Y)**0.5), ((Z/Y)**0.5)*cmath.sinh((Z*Y)**0.5), cmath.cosh((Z*Y)**0.5), ((Y/Z)**0.5)*cmath.sinh((Z*Y)**0.5)

def IR(Pr,pf,Vr):
    return complex(Pr/(((3)**0.5)*Vr*pf)*pf, Pr/(((3)**0.5)*Vr*pf)*math.sin(math.acos(pf)))

def sending_end(A,B,C,D,Vr,Ir):
    Vs = A * Vr + B * Ir
    Is = C * Vr + D * Ir
    return Vs,Is

def VR(vs,vr):
    return (abs(vs) - abs(vr))*100/abs(vr)

def pf(V,I):
    return math.cos(phase(V/I))

def powerLoss_eff(vr,vs,Ir,Is):
    return abs(vs)*abs(Is)*pf(vs,Is) - abs(vr)*abs(Ir)*pf(vr,Ir),( abs(vr)*abs(Ir)*pf(vr,Ir))*100/(abs(vs)*abs(Is)*pf(vs,Is) )

def shuntcomp(Vs,Is):
    return abs(Vs)*abs(Is)*math.sin(phase(Vs/Is))/1000000

def form_to_float(form):
    data = {}
    for key in form.keys():
        data[key] = float(form[key])
    return data