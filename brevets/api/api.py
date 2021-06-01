# Streaming Service
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from pymongo import MongoClient
import os

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.brevetsdb


app = Flask(__name__)
api = Api(app)


class listAll(Resource):
    def get(self, data="json"):
        k = int(request.args.get("top", default=-1))
        vals = list(db.vals.find({}, {'_id': 0, 'brevet_dist': 0, 'begin_date': 0, 'km': 0, 'miles': 0, 'location': 0}))
        if data == "json":
            return _json(k, vals)
        else:
            return _csv(k, vals)


class listOpenOnly(Resource):
    def get(self, data="json"):
        k = int(request.args.get("top", default=-1))
        vals = list(db.vals.find({}, {'_id': 0, 'brevet_dist': 0, 'begin_date': 0, 'km': 0, 'miles': 0, 'location': 0, 'close_time': 0}))
        if data == "json":
            return _json(k, vals)
        else:
            return _csv(k, vals)


class listCloseOnly(Resource):
    def get(self, data="json"):
        k = int(request.args.get("top", default=-1))
        vals = list(db.vals.find({}, {'_id': 0, 'brevet_dist': 0, 'begin_date': 0, 'km': 0, 'miles': 0, 'location': 0, 'open_time': 0}))
        if data == "json":
            return _json(k, vals)
        else:
            return _csv(k, vals)


def _json(k, vals):
    if k >= 0 and k <= len(vals):
        ret = []
        for i in range(k):
            ret.append(dict(vals[i]))
        return jsonify(ret)
    return jsonify(vals)


def _csv(k, vals):
    times = list(vals[0].keys())
    temp = []
    if k < 0 or k > len(vals):
        k = len(vals)
    for i in range(k):
        for time in times:
            if time == times[-1]:
                temp.append(str((vals[i]).get(time) + "\n"))
            else:
                temp.append(str((vals[i]).get(time)))
    return ",".join(times) + "\n" + ",".join(temp)


# Create routes
# Another way, without decorators
api.add_resource(listAll, '/listAll', '/listAll/', '/listAll/<string:data>')
api.add_resource(listOpenOnly, '/listOpenOnly', '/listOpenOnly/', '/listOpenOnly/<string:data>')
api.add_resource(listCloseOnly, '/listCloseOnly', '/listCloseOnly/', '/listCloseOnly/<string:data>')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
