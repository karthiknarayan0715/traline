import math
from flask import flash, redirect, url_for

def mgmd(a, b, c):
    return (a*b*c)**(1/3)
def sgmd(r1, r2, r3):

    return 0
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

def check_form(form):
    for field in form.values():
        try:
            float(field)
        except:
            print(field)
            return False
    return True

def verify_data(data, same_page):
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
def form_to_float(form):
    data = {}
    for key in form.keys():
        data[key] = float(form[key])
    return data
