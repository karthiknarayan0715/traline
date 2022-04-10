from fileinput import filename
from http.client import ImproperConnectionState
import math
from multiprocessing.connection import wait
from ssl import VerifyFlags
from flask import flash, redirect, url_for
import cmath
from cmath import phase
import numpy as np
from matplotlib.figure import Figure
import os
from io import BytesIO
import base64
from flask import session


def check_form(form):
    for field in form.values():
        try:
            float(field)
        except:
            print(field)
            return False
    allowed = [1, 7, 19, 37, 61]
    if float(form['pf'])>1 or float(form['pf'])<-1:
        flash('Invalid power factor!')
        return False
    try:
        if not int(form['n_strands']) in allowed:
            flash('Invalid input!')
            return False
    except ValueError:
        flash('Invalid input!')
        return False
    return True


def Compute(a, b, c, subcon, d, nos, dia, line, type, r, f, V, Pr, pf):
    result = {}
    l=(3+((12*nos)-3)**(1/2))/6
    rad=dia*(2*l-1)/2
    Pr = Pr*10**6
    h=0.7788*rad

    if subcon==1:
        SGMl=h
        SGMc=rad
    elif subcon==2:
        SGMl=(h*d)**(1/2)
        SGMc=(rad*d)**(1/2)
    elif subcon==3:
        SGMl=(h*d*d)**(1/3)
        SGMc=(rad*d*d)**(1/3)
    elif subcon==4:
        SGMl=(h*1.414*d*d*d)**(1/4)
        SGMc=(rad*1.414*d*d*d)**(1/4)
    elif subcon==6:
        SGMl=(6*h*d*d*d*d*d)**(1/6)
        SGMc=(6*rad*d*d*d*d*d)**(1/6)
    elif subcon==5:
        SGMl=(3.23606*d*d*d*d*h)**(1/5)
        SGMc=(3.23606*d*d*d*d*rad)**(1/5)
    GMD=(a*b*c)**(1/3)

    L=2*0.0001*math.log(GMD*1000/SGMl)
    Cap=(2*(10**-9)*8.854*3.14)/(math.log(GMD*1000/SGMc))
    R=r*line	
    X=line*L*2*3.14*f
    Z=R+(X)*1j
    Y=(2*3.14*Cap*line)*1j
    if type=="short":
        A=1
        C=0
        D=A
        B=Z
    elif type=="nominal pi":
        A=1+(Z*Y*0.5)
        B=Z
        C=Y*(1+(0.25*Y*Z))
        D=A
    elif type=="long":
        Zc=((Z/line)/(Y/line))**(1/2)
        Yc=((Z/line)*(Y/line))**(1/2)
        A=(2.71828**(Yc*line)+2.71828**(Yc*line*-1))*0.5
        B=(2.71828**(Yc*line)-2.71828**(Yc*line*-1))*0.5*Zc
        C=(2.71828**(Yc*line)-2.71828**(Yc*line*-1))*0.5*(1/Zc)
        D=A
    I=Pr/(pf*V*(3**(0.5)))
    Vr=V/(3**0.5)
    Ir=I*pf-(I*((1-(pf**2))**(0.5))*1j)
    Vs=A*Vr+B*Ir
    Is=C*Vr+D*Ir

    Vore=(abs(Vs)-abs(Vr))/abs(Vs)
    los=(abs(Vs)*abs(Is)*math.cos(cmath.phase(Vs/Is)))-(abs(Vr)*abs(Ir)*math.cos(cmath.phase(Vr/Ir)))
    loss=los*(3**0.5)

    eff=(abs(Vr)*abs(Ir)*math.cos(cmath.phase(Vr/Ir)))/(abs(Vs)*abs(Is)*math.cos(cmath.phase(Vs/Is)))
    
    result = {
        "Inductance per Km": f"{str(L)} H/km",
        "Capacitance per Km": f"{str(Cap)} F/km",
        "Inductive Reactance": f"{str(X)} ohms",
        "Capacitive Reactance": f"{str(abs(1j/Y))} ohms",
        "A Parameter": str(A),
        "B Parameter": str(B),
        "C Parameter": str(C),
        "D Parameter": str(D),
        "Charging Current": f"{str(abs(Is-Ir))} ohms",
        "Sending End Voltage": f"{str(abs(Vs*(3**0.5))/1000)} kV",
        "Sending End Current": f"{str(abs(Is))} A",
        "Voltage Regulation": f"{str(Vore*100)} %",
        "Losses": f"{str(loss)} W",
        "Effeciency": f"{str(eff*100)} %"
    }
    session['result'] = result
    a1=(abs(A)*abs(Vr)*abs(Vr)/abs(B))*math.cos(cmath.phase(B/A))*-1/1000000
    b1=(abs(A)*abs(Vr)*abs(Vr)/abs(B))*math.sin(cmath.phase(B/A))*-1/1000000
    a2=(abs(A)*abs(Vs)*abs(Vs)/abs(B))*math.cos(cmath.phase(B/A))/1000000
    b2=(abs(A)*abs(Vs)*abs(Vs)/abs(B))*math.sin(cmath.phase(B/A))/1000000
    r=abs(Vs)*abs(Vr)/abs(B)/1000000

    file = open('./static/images/graph.png', "w+")
    file.close()
    circle = np.linspace(0,360,500)
    x1 = []
    y1 = []
    x2 = []
    y2 = []

    for i in range(500):
        x1.append(a1 + r*math.sin(np.radians(circle[i])))
        y1.append(b1 + r*math.cos(np.radians(circle[i])))
        x2.append(a2 + r*math.sin(np.radians(circle[i])))
        y2.append(b2 + r*math.cos(np.radians(circle[i])))

    fig = Figure()
    ax = fig.subplots()
    ax.plot(x1, y1, x2, y2)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    if type=="short":
        P=Pr/3000000
        Ql=((1-(pf**2))**(0.5))*P/pf
        Qr=(((r**2)-((P-a1)**2))**(0.5))+b1
        Qc = Qr - Ql
        compensation = 3*(Qr-Ql)

        result["Compensation Required"] = compensation

        
    return result, data