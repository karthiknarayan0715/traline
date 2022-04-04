from flask import Flask, render_template, redirect, request, flash, url_for, session
from flask_weasyprint import HTML, render_pdf
from models import *
import math
import os

cur_path = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = "key"


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/short_line_model")
def short_line_model():
    return render_template('short_line.html')

@app.route("/medium_line_model")
def medium_line_model():
    return render_template('medium_line.html')

@app.route("/long_line_model/")
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
        
        data = form_to_float(form)

        for key in data.keys():
            result[key] = data[key]
        if verify_data(data, same_page):
            return redirect(url_for(same_page))
        
        mgmd = MGMD(data['d'], data['d'], data['d'])
        r = radius(data['d_strand'], data['n_s_c'])
        sgmd = SGMD(data['n_s_c'], data['l'], r)
        ind_str = result['Inductance per Km'] = f"{inductance(mgmd, sgmd)} H/km"
        ind = float(ind_str[0:-5])

        cap = result['Capacitance per Km'] = f"{capacitance(mgmd, sgmd)} F/km"
        Vr = data['Vr']
        Ir = IR(data['Pr'], data['pf'], Vr)
        A, B, C, D = shortline_ABCD(ind, r*data['l'])
        Vs, Is = sending_end(A, B, C, D, Vr, Ir)
        ind_reac = result['Inductive reactace'] = f"{(2*math.pi*ind*data['f'])} ohms"
        cap_reac = result['Capacitive reactace'] = f"{1/(2*math.pi*ind*data['f'])} ohms"
        CC = result['Charging Current'] = f"{abs(cc(Is, Ir))}∠{phase(cc(Is, Ir))} A"
        result['A'], result['B'], result['C'], result['D'] = f"{abs(A)}{phase(A)}", f"{abs(B)}{phase(B)}", f"{abs(C)}{phase(C)}", f"{abs(D)}{phase(D)}"
        ploss, eff = powerLoss_eff(Vr, Vs, Ir, Is)

        result['Sending End Voltage'] = f"{abs(Vs)}∠{phase(Vs)} V"
        result['Sending End Current'] = f"{abs(Is)}∠{phase(Vs)} A"
        result['Voltage Regulation'] = f"{VR(Vs, Vr)} %"
        result['Power Loss'] = f"{ploss/100000} MW"
        result['Effeciency'] = f"{eff}"
        result['Shunt Compensation'] = f"{shuntcomp(Vs, Is)}"

        session['result'] = result
        return render_template('result.html', result=result)   

    return render_template('shortline_symmetrical.html')


@app.route("/short_line_model/unsymmetrical", methods = ['GET', 'POST'])
def shortline_unsymmetrical():
    same_page = 'shortline_unsymmetrical'
    if request.method == "POST":
        form = request.form
        result = {}
        
        if not check_form(form):
            flash('Invalid input!')
            return redirect(url_for(same_page))

        data = form_to_float(form)
        if not verify_data(data):
            flash('Error')
            return redirect(url_for(same_page))

        mgmd = MGMD(data['d_a'], data['d_b'], data['d_c'])
        r = radius(data['d_strand'], data['n_s_c'])
        sgmd = SGMD(data['n_s_c'], data['l'], r)
        ind_str = result['Inductance per Km'] = f"{inductance(mgmd, sgmd)} H/km"
        ind = float(ind_str[0:-5])

        cap = result['Capacitance per Km'] = f"{capacitance(mgmd, sgmd)} F/km"
        Vr = data['Vr']
        Ir = IR(data['Pr'], data['pf'], Vr)
        A, B, C, D = shortline_ABCD(ind, r*data['l'])
        Vs, Is = sending_end(A, B, C, D, Vr, Ir)
        ind_reac = result['Inductive reactace'] = f"{(2*math.pi*ind*data['f'])} ohms"
        cap_reac = result['Capacitive reactace'] = f"{1/(2*math.pi*ind*data['f'])} ohms"
        CC = result['Charging Current'] = f"{abs(cc(Is, Ir))}∠{phase(cc(Is, Ir))} A"
        result['A'], result['B'], result['C'], result['D'] = f"{abs(A)}{phase(A)}", f"{abs(B)}{phase(B)}", f"{abs(C)}{phase(C)}", f"{abs(D)}{phase(D)}"
        ploss, eff = powerLoss_eff(Vr, Vs, Ir, Is)

        result['Sending End Voltage'] = f"{abs(Vs)}∠{phase(Vs)} V"
        result['Sending End Current'] = f"{abs(Is)}∠{phase(Vs)} A"
        result['Voltage Regulation'] = f"{VR(Vs, Vr)} %"
        result['Power Loss'] = f"{ploss/100000} MW"
        result['Effeciency'] = f"{eff}"
        result['Shunt Compensation'] = f"{shuntcomp(Vs, Is)}"

        session['result'] = result
        return render_template('result.html', result=result)        
        
    return render_template('shortline_unsymmetrical.html')

@app.route("/medium_line_model/symmetrical", methods=['GET', 'POST'])
def mediumline_symmetrical():
    same_page = 'mediumline_symmetrical'
    if request.method == "POST":
        form = request.form
        result = {}
        
        if not check_form(form):
            flash('Invalid input!')
            return redirect(url_for(same_page))

        data = form_to_float(form)
        if not verify_data(data):
            flash('Error')
            return redirect(url_for(same_page))

        mgmd = MGMD(data['d_a'], data['d_b'], data['d_c'])
        r = radius(data['d_strand'], data['n_s_c'])
        sgmd = SGMD(data['n_s_c'], data['l'], r)
        ind_str = result['Inductance per Km'] = f"{inductance(mgmd, sgmd)} H/km"
        ind = float(ind_str[0:-5])

        cap = result['Capacitance per Km'] = f"{capacitance(mgmd, sgmd)} F/km"
        Vr = data['Vr']
        Ir = IR(data['Pr'], data['pf'], Vr)
        A, B, C, D = mediumline_ABCD(ind, r*data['l'])
        Vs, Is = sending_end(A, B, C, D, Vr, Ir)
        ind_reac = result['Inductive reactace'] = f"{(2*math.pi*ind*data['f'])} ohms"
        cap_reac = result['Capacitive reactace'] = f"{1/(2*math.pi*ind*data['f'])} ohms"
        CC = result['Charging Current'] = f"{abs(cc(Is, Ir))}∠{phase(cc(Is, Ir))} A"
        result['A'], result['B'], result['C'], result['D'] = f"{abs(A)}∠{phase(A)}", f"{abs(B)}∠{phase(B)}", f"{abs(C)}∠{phase(C)}", f"{abs(D)}∠{phase(D)}"
        ploss, eff = powerLoss_eff(Vr, Vs, Ir, Is)

        result['Sending End Voltage'] = f"{abs(Vs)}∠{phase(Vs)} V"
        result['Sending End Current'] = f"{abs(Is)}∠{phase(Vs)} A"
        result['Voltage Regulation'] = f"{VR(Vs, Vr)} %"
        result['Power Loss'] = f"{ploss/100000} MW"
        result['Effeciency'] = f"{eff}"

        session['result'] = result
        return render_template('result.html', result=result)  

    return render_template('mediumline_unsymmetrical.html')


@app.route("/medium_line_model/unsymmetrical", methods=['GET', 'POST'])
def mediumline_unsymmetrical():
    same_page = 'mediumline_unsymmetrical'
    if request.method == "POST":
        form = request.form
        result = {}
        
        if not check_form(form):
            flash('Invalid input!')
            return redirect(url_for(same_page))

        data = form_to_float(form)
        if not verify_data(data):
            flash('Error')
            return redirect(url_for(same_page))

        mgmd = MGMD(data['d_a'], data['d_b'], data['d_c'])
        r = radius(data['d_strand'], data['n_s_c'])
        sgmd = SGMD(data['n_s_c'], data['l'], r)
        ind_str = result['Inductance per Km'] = f"{inductance(mgmd, sgmd)} H/km"
        ind = float(ind_str[0:-5])

        cap = result['Capacitance per Km'] = f"{capacitance(mgmd, sgmd)} F/km"
        Vr = data['Vr']
        Ir = IR(data['Pr'], data['pf'], Vr)
        A, B, C, D = mediumline_ABCD(ind, r*data['l'])
        Vs, Is = sending_end(A, B, C, D, Vr, Ir)
        ind_reac = result['Inductive reactace'] = f"{(2*math.pi*ind*data['f'])} ohms"
        cap_reac = result['Capacitive reactace'] = f"{1/(2*math.pi*ind*data['f'])} ohms"
        CC = result['Charging Current'] = f"{abs(cc(Is, Ir))}∠{phase(cc(Is, Ir))} A"
        result['A'], result['B'], result['C'], result['D'] = f"{abs(A)}∠{phase(A)}", f"{abs(B)}∠{phase(B)}", f"{abs(C)}∠{phase(C)}", f"{abs(D)}∠{phase(D)}"
        ploss, eff = powerLoss_eff(Vr, Vs, Ir, Is)

        result['Sending End Voltage'] = f"{abs(Vs)}∠{phase(Vs)} V"
        result['Sending End Current'] = f"{abs(Is)}∠{phase(Vs)} A"
        result['Voltage Regulation'] = f"{VR(Vs, Vr)} %"
        result['Power Loss'] = f"{ploss/100000} MW"
        result['Effeciency'] = f"{eff}"

        session['result'] = result
        return render_template('result.html', result=result)  

    return render_template('mediumline_unsymmetrical.html')


@app.route("/pdf", methods=['GET', 'POST'])
def pdf():
    html = render_template("pdf.html",output=session['result'])
    return render_pdf(HTML(string=html))

if __name__ == "__main__":
    app.run(debug=True, port=8080)