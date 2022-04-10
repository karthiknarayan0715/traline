from flask import Flask, render_template, redirect, request, flash, url_for, session
from flask_weasyprint import HTML, render_pdf
from models import *
import numpy as np
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
    same_page = 'shortline_unsymmetrical'
    if request.method == "POST":
        form = request.form
        result = {}

        if not check_form(form):
            flash("Invalid Inputs!!")
            return redirect(url_for(same_page))

        sys = "Symmetric"
        a = b = c = float(form.get('d'))

        subcon = int(form.get('n_sub_bundle'))
        subspa = float(form.get('spacing'))
        d = subspa*10
        nos = int(form.get('n_strands'))
        dia = float(form.get('d_strand'))
        line = float(form.get('l'))
        type = "short"
        r = float(form.get('R'))
        f = float(form.get('f'))
        V = float(form.get('Vr'))
        Pr = float(form.get('Pr'))
        pf = float(form.get('pf'))

        result, data = Compute(a, b, c, subcon, subspa, nos, dia, line, type, r, f, V, Pr, pf)
        return render_template('result.html', data=data)
    return render_template('shortline_symmetrical.html') 


@app.route("/short_line_model/unsymmetrical", methods = ['GET', 'POST'])
def shortline_unsymmetrical():
    same_page = 'shortline_unsymmetrical'
    if request.method == "POST":
        form = request.form
        result = {}

        if not check_form(form):
            flash("Invalid Inputs!!")
            return redirect(url_for(same_page))

        sys = "Unsymmetric"
        a = float(form.get('d_a'))
        b = float(form.get('d_b'))
        c = float(form.get('d_c'))

        subcon = int(form.get('n_sub_bundle'))
        subspa = float(form.get('spacing'))
        d = subspa*10
        nos = int(form.get('n_strands'))
        dia = float(form.get('d_strand'))
        line = float(form.get('l'))
        type = "short"
        r = float(form.get('R'))
        f = float(form.get('f'))
        V = float(form.get('Vr'))
        Pr = float(form.get('Pr'))
        pf = float(form.get('pf'))

        result, data = Compute(a, b, c, subcon, subspa, nos, dia, line, type, r, f, V, Pr, pf)
        return render_template('result.html', result=result, data=data)
        
    return render_template('shortline_unsymmetrical.html')

@app.route("/medium_line_model/symmetrical", methods=['GET', 'POST'])
def mediumline_symmetrical():
    same_page = 'mediumline_symmetrical'
    if request.method == "POST":
        form = request.form
        result = {}

        if not check_form(form):
            flash("Invalid Inputs!!")
            return redirect(url_for(same_page))

        sys = "Symmetric"
        a = b = c = float(form.get('d'))

        subcon = int(form.get('n_sub_bundle'))
        subspa = float(form.get('spacing'))
        d = subspa*10
        nos = int(form.get('n_strands'))
        dia = float(form.get('d_strand'))
        line = float(form.get('l'))
        type = "nominal pi"
        r = float(form.get('R'))
        f = float(form.get('f'))
        V = float(form.get('Vr'))
        Pr = float(form.get('Pr'))
        pf = float(form.get('pf'))

        result, data = Compute(a, b, c, subcon, subspa, nos, dia, line, type, r, f, V, Pr, pf)
        return render_template('result.html', result=result, data=data)
    return render_template('medium_line_symmetrical.html') 


@app.route("/medium_line_model/unsymmetrical", methods=['GET', 'POST'])
def mediumline_unsymmetrical():
    same_page = 'shortline_unsymmetrical'
    if request.method == "POST":
        form = request.form
        result = {}

        if not check_form(form):
            flash("Invalid Inputs!!")
            return redirect(url_for(same_page))

        sys = "Unsymmetric"
        a = float(form.get('d_a'))
        b = float(form.get('d_b'))
        c = float(form.get('d_c'))

        subcon = int(form.get('n_sub_bundle'))
        subspa = float(form.get('spacing'))
        d = subspa*10
        nos = int(form.get('n_strands'))
        dia = float(form.get('d_strand'))
        line = float(form.get('l'))
        type = "nominal pi"
        r = float(form.get('R'))
        f = float(form.get('f'))
        V = float(form.get('Vr'))
        Pr = float(form.get('Pr'))
        pf = float(form.get('pf'))

        result, data = Compute(a, b, c, subcon, subspa, nos, dia, line, type, r, f, V, Pr, pf)
        return render_template('result.html', result=result, data=data)        
        
    return render_template('medium_line_unsymmetrical.html')


@app.route("/long_line_model/unsymmetrical", methods=['GET', 'POST'])
def longline_unsymmetrical():
    same_page = 'longline_unsymmetrical'
    if request.method == "POST":
        form = request.form
        result = {}

        if not check_form(form):
            flash("Invalid Inputs!!")
            return redirect(url_for(same_page))

        sys = "Unsymmetric"
        a = float(form.get('d_a'))
        b = float(form.get('d_b'))
        c = float(form.get('d_c'))

        subcon = int(form.get('n_sub_bundle'))
        subspa = float(form.get('spacing'))
        d = subspa*10
        nos = int(form.get('n_strands'))
        dia = float(form.get('d_strand'))
        line = float(form.get('l'))
        type = "long"
        r = float(form.get('R'))
        f = float(form.get('f'))
        V = float(form.get('Vr'))
        Pr = float(form.get('Pr'))
        pf = float(form.get('pf'))

        result, data = Compute(a, b, c, subcon, subspa, nos, dia, line, type, r, f, V, Pr, pf)
        return render_template('result.html', result=result, data=data)        
        
    return render_template('long_line_unsymmetrical.html')

@app.route("/long_line_model/symmetrical", methods=['GET', 'POST'])
def longline_symmetrical():
    same_page = 'longline_symmetrical'
    if request.method == "POST":
        form = request.form
        result = {}

        if not check_form(form):
            flash("Invalid Inputs!!")
            return redirect(url_for(same_page))

        sys = "Symmetric"
        a = b = c = float(form.get('d'))

        subcon = int(form.get('n_sub_bundle'))
        subspa = float(form.get('spacing'))
        d = subspa*10
        nos = int(form.get('n_strands'))
        dia = float(form.get('d_strand'))
        line = float(form.get('l'))
        type = "long"
        r = float(form.get('R'))
        f = float(form.get('f'))
        V = float(form.get('Vr'))
        Pr = float(form.get('Pr'))
        pf = float(form.get('pf'))

        result, data = Compute(a, b, c, subcon, subspa, nos, dia, line, type, r, f, V, Pr, pf)
        return render_template('result.html', result=result, data=data)
    return render_template('long_line_symmetrical.html') 

@app.route("/pdf", methods=['GET', 'POST'])
def pdf():
    html = render_template("pdf.html",output=session['result'])
    return render_pdf(HTML(string=html))

if __name__ == "__main__":
    app.run(debug=True, port=8080)