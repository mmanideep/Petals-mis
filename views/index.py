from flask import Flask, render_template

from petals_mis.app import app


@app.route("/")
def index_view():
    return render_template("index.html")
