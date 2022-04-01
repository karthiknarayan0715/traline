from flask import Flask, render_template, redirect, request, flash, url_for
from flask_weasyprint import HTML
import math
import os

cur_path = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = "key"

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
    for field in form.keys():
        try:
            float(field)
        except:
            return False
    return True

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/short_line_model")
def short_line_model():
    return render_template('short_line.html')


@app.route("/medium_line_model")
def medium_line_model():
    return render_template('medium_line.html')

@app.route("/long_line_model")
def long_line_model():
    return render_template('long_line.html')

@app.route("/short_line_model/symmetrical", methods = ['GET', 'POST'])
def shortline_symmetrical():
    same_page = 'shortline_symmetrical'
    if request.method == "POST":
        form = request.form
        result = {}

        if not check_form(form):
            flash('Invalid input!')
            return redirect(url_for(same_page))
        #form inputs
        spacing = float(form.get('spacing'))
        n_s_c = float(form.get('sub-cond'))
        d = float(form.get('sub_space'))
        d_strand = float(form.get('strand_dia'))
        l = float(form.get('length'))
        resistance_per_km = float(form.get('resistance'))
        frequency = float(form.get('frequency'))
        voltage_line = float(form.get('voltage'))
        load_3_ph = float(form.get('load'))
        pf = float(form.get('pf'))
        load_mva = load_3_ph/(3*pf)
        I = load_mva/(voltage_line/(3**0.5))



        # allowed = [1, 7, 19, 37, 61]
        # r = -1
        # if r==-1:
        #     return redirect(url_for('shortline_symmetrical'))
        # #Results
        # ind_per_ph = result['Inductance per Phase'] = f"{2*10**(-4)*(math.log(d/(0.7784*r)))} H/km"
        # cam_per_ph = result['Capacitance per Phase'] = f"{str(0)} F/km"
        # ind_reac = result['Inductive Reactance'] = f"{float(ind_per_ph[0:-5])*frequency} ohms/km"
        # cap_reac = result['Capacitance Reactance'] = f"Infinity ohms"
        # A_parameter = result['A Parameter'] = f"{1}"
        # B_parameter = result['B Parameter'] = f"{ind_per_ph[0:-5]}"
        # C_parameter = result['C Parameter'] = f"{0}"
        # D_parameter = result['D Parameter'] = f"{1}"
        # sending_end_vol = result['Sending End Voltage'] = f"{voltage_line+(I*(resistance_per_km+ind_per_ph)*l)/1000} V"
        # sending_end_cur = result['Sending End Current'] = f"{I} A"
        # voltage_regulation = result['Voltage Regulation'] = f"{(voltage_line - sending_end_vol)/sending_end_vol}"
        # power_loss = result['Power Loss'] = f"{(I**2)*resistance_per_km*l}"


        return render_template('result.html', result=result)

    return render_template('shortline_symmetrical.html')


@app.route("/short_line_model/unsymmetrical", methods = ['GET', 'POST'])
def shortline_unsymmetrical():
    if request.method == "POST":
        form = request.form
        result = {}

        for value in form.keys():
            result[value] = 10

        return render_template('result.html', result=result)
        
        
    return render_template('shortline_unsymmetrical.html')

if __name__ == "__main__":
    app.run(debug=True, port=8080)