from flask import Flask
from flask import render_template 
app = Flask(__name__)


@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/page2.html')
def page2():
    return render_template('page2.html')

@app.route('/page3.html')
def page3():
    return render_template('page3.html')

@app.route('/page4.html')
def page4():
    return render_template('page4.html')

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0') 