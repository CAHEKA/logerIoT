import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, jsonify, json
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
scheduler = APScheduler()


class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(50), db.ForeignKey('config.uid', ondelete="CASCADE"), nullable=False)
    data = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"<sensorData {self.id}>"
class Config(db.Model):
    uid = db.Column(db.String(50), primary_key=True)
    model = db.Column(db.String(50), nullable=False)
    ip = db.Column(db.String(50), nullable=False)
    setting = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<config {self.uid}>"

def create_tables():
    with app.app_context():
        if not database_exists():
            print("create bd")
            db.create_all()
def database_exists():
    return os.path.exists("instance/temp.db")

@app.route("/config", methods=("POST", "GET", "DELETE"))
def config():
    if request.method == "POST":
        # здесь должна быть проверка корректности введенных данных
        try:
            data = request.get_json()
            u = Config(uid=data['uid'],
                       model=data['model'],
                       ip=data['ip'],
                       setting=json.dumps(data['setting']))
            db.session.add(u)
            db.session.flush()
            db.session.commit()
            return jsonify({'uid': u.uid})
        except Exception as e:
            db.session.rollback()
            print("error",str(e))
            return jsonify({'error': str(e)})

    elif request.method == "GET":
        configs = Config.query.all()
        result = []
        for config in configs:
            result.append({'uid': config.uid, 'model': config.model, 'ip': config.ip, 'setting': config.setting})
        return jsonify(result)

    elif request.method == "DELETE":
        parameter = request.args.get('uid')
        if parameter:
            uid = Config.query.filter_by(uid=parameter).first()
            if uid:
                db.session.delete(uid)
                db.session.commit()
                return jsonify({'uid': parameter})
            else:
                return jsonify({'error': 'Uid not found'}), 404
        else:
            return jsonify({'error': 'Missing uid parameter'}), 400


@app.route("/sensorData")
def sensorData():
    if request.method == "GET":
        parameter = request.args.get('uid')
        if parameter:
            datas = SensorData.query.filter_by(uid=parameter).all()
            if datas:
                return jsonify([{'id': data.id, 'data': data.data} for data in datas])
            else:
                return jsonify({'error': 'Uid not found'}), 404
        else:
            return jsonify({'error': 'Missing uid parameter'}), 400


def scheduleTask():
    print("This test runs every 30 seconds")

if __name__ == "__main__":
    create_tables()  # Создание таблиц перед запуском приложения
    scheduler.add_job(id = 'Scheduled Task', func=scheduleTask, trigger="interval", seconds=30) # Настройки шедулера
    scheduler.start()
    app.run(debug=False)