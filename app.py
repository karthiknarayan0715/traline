from flask import Flask, render_template, redirect
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

if __name__ == "__main__":
    app.run(debug=True, port=8080)