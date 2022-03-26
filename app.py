from flask import Flask, render_template, redirect, request
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
    if request.method == "POST":
        form = request.form


        #Inductance per phase
        L_ph = None
        #Capacitance per phase
        C_ph = 0
        
    return render_template('shortline_symmetrical.html')

if __name__ == "__main__":
    app.run(debug=True, port=8080)