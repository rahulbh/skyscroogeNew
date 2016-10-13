# -*- coding: UTF-8 -*-
"""jinja_app1.py: Get start with Jinja2 templates"""
from flask import Flask, render_template, request
from locale import currency
import SkyScrooge_git
import urllib.request as urllib
import json 

application = Flask(__name__)

@application.route('/')
def index():
    return render_template("index.html")

@application.route('/submit', methods=['POST'])
def submit():
    # Read the HTTP POST request parameter from request.form
    _from = request.form['_from']
    _to = request.form['to']
    _datetime = request.form['datetime']
    _pax = request.form['pax']
    _currency = request.form['currency']
    
    SkyScrooge_git.get_csv(_from,_to,_datetime,_pax,_currency)
        
    
    aFile = open("./templates/Results.html","a+")
    aFile.seek(0, 0)
    aFile.write('''<html lang='en'>\
<span class="prev">Previous</span><span class="next">Next</span><head>\
<title>SkyScrooge - Find Cheapest Fare</title>\
<meta charset='utf-8'>\
<link rel='stylesheet' href='{{ url_for("static", filename='table.css') }}' /><script src="https://code.jquery.com/jquery-3.1.1.js"   integrity="sha256-16cdPddA6VdVInumRGo6IbivbERE8p7CQR3HzTBuELA="   crossorigin="anonymous"></script><script src="http://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.9.1/jquery.tablesorter.min.js"></script><script type='text/javascript' src="{{ url_for('static', filename='table.js') }}"></script>\
</head>\
<body>''')
    aFile.seek(0,2)
    aFile.write("</body></html>")
    aFile.close()
    
    # Validate and send response
    if _from:
        print(_from,_to,_datetime,_pax,_currency)
        return render_template('Results.html', _from=_from,to=_to,_datetime=_datetime,_pax=_pax,_currency=_currency)
    else:
        return 'Please go back and enter the details...'
        
if __name__ == '__main__':
    application.run()
    
