from flask import Flask, render_template, redirect, request, flash, url_for
from flask_weasyprint import HTML
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

        data = form_to_float(form)
        if not verify_data(data, same_page):
            return redirect(url_for(same_page))
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


         # #form inputs
        # spacing = float(form.get('spacing'))
        # n_s_c = float(form.get('sub-cond'))
        # d = float(form.get('sub_space'))
        # d_strand = float(form.get('strand_dia'))
        # l = float(form.get('length'))
        # resistance_per_km = float(form.get('resistance'))
        # frequency = float(form.get('frequency'))
        # voltage_line = float(form.get('voltage'))
        # load_3_ph = float(form.get('load'))
        # pf = float(form.get('pf'))
        # load_mva = load_3_ph/(3*pf)   
        # I = load_mva/(voltage_line/(3**0.5))
        # 