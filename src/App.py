from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
#import test_AlertSystem as AlertSys  # Uncomment when you have it

app = Flask(__name__)

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passworddevops3321@localhost/firefighters'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passworddevops3321@192.168.18.74/firefighters'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Firefighters model
class Firefighter(db.Model):
    __tablename__ = 'firefighters_info'
    name = db.Column(db.String(50), primary_key=True)
    area = db.Column(db.String(50))
    status = db.Column(db.String(20))
    password = db.Column(db.String(10))

# Mock alert system function
def get_fire_status():
    return 1  # Replace with AlertSys.alert() once implemented

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/page2.html')
def page2():
    return render_template('page2.html')

@app.route('/api/fire-status')
def fire_status_api():
    try:
        fire_value = get_fire_status()
        print(f"Fire status requested: {fire_value}")
        return jsonify({'value': fire_value, 'status': 'success'})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'value': 0, 'status': 'error', 'message': str(e)})

@app.route('/page3.html')
def page3():
    return render_template('page3.html')

@app.route('/page4.html')
def page4():
    return render_template('page4.html')

@app.route('/page5.html')
def page5():
    on_duty = Firefighter.query.filter(Firefighter.status.ilike('On-Duty')).all()
    return render_template('page5.html', data=on_duty)

@app.route('/page6.html') 
def page6():
    off_duty = Firefighter.query.filter(Firefighter.status.ilike('Off-Duty')).all()
    return render_template('page6.html', data=off_duty)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
