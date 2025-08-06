from flask import Flask
from flask import render_template 
from flask_mysqldb import MySQL
from flask import jsonify
import test_AlertSystem as AlertSys #replace with import test_AlertSystem as AlertSys

app = Flask(__name__)

app.config["MYSQL_HOST"] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'passworddevops3321'
app.config['MYSQL_DB'] = 'firefighters'

mysql = MySQL(app)

def get_fire_status():
    return AlertSys.alert()

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/page2.html')
def page2():
    return render_template('page2.html')

@app.route('/api/fire-status')
def fire_status_api():
    try:
        fire_value = get_fire_status()  # Gets value from your fire_alert.py
        print(f"Fire status requested: {fire_value}")  # Debug print
        return jsonify({'value': fire_value, 'status': 'success'})
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        return jsonify({'value': 0, 'status': 'error', 'message': str(e)})


@app.route('/page3.html')
def page3():
    return render_template('page3.html')

@app.route('/page4.html')
def page4():
    return render_template('page4.html')

@app.route('/page5.html')
def page5():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM firefighters_info WHERE status = 'On-Duty'")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template('page5.html', data=fetchdata)
@app.route('/page6.html')
def page6():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM firefighters_info WHERE status = 'Off-Duty'")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template('page6.html', data=fetchdata)

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0') 