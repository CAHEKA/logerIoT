from flask import  request, jsonify, json
from app import app, db
from app.model.bdModel import SensorData, Config

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
