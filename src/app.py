''''
Sample REST API using Flask and MongoDB
'''
import json
from http import HTTPStatus
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
db = None


@app.route('/api/v1/resources/countries/<string:country_code>', methods=['GET'])
def countries(country_code=None):
    resp = db.countries.find_one({'_id': country_code})
    if not resp:
        return jsonify({'timestamp': datetime.now(timezone.utc).isoformat(),
                        'status': HTTPStatus.NOT_FOUND.value,
                        'error': 'country_code not found'})
    return jsonify(resp)


@app.route('/api/v1/resources/countries/<string:country_code>', methods=['DELETE'])
def delete_country(country_code=None):
    resp = db.countries.delete_one({'_id': country_code})
    if resp.deleted_count == 0:
        return jsonify({'timestamp': datetime.now(timezone.utc).isoformat(),
                        'status': HTTPStatus.NOT_FOUND.value,
                        'error': 'country_code not found'})

    return jsonify({'timestamp': datetime.now(timezone.utc).isoformat(),
                    'status': HTTPStatus.OK.value})


@app.route('/api/v1/resources/countries', methods=['POST', 'PUT'])
def country():
    payload = request.get_json()

    if '_id' not in payload:
        return jsonify({'timestamp': datetime.now(timezone.utc).isoformat(),
                        'status': HTTPStatus.BAD_REQUEST.value,
                        'error': '_id not found'})

    if request.method == 'PUT':
        resp = db.countries.update_one({'_id': payload['_id']},
                                       {'$set': payload})
        if resp.modified_count == 0:
            return jsonify({'timestamp': datetime.now(timezone.utc).isoformat(),
                            'status': HTTPStatus.BAD_REQUEST.value,
                            'error': 'Data not updated'})
    elif request.method == 'POST':
        count = db.countries.count({'_id': payload['_id']})
        if count > 0:
            return jsonify({'timestamp': datetime.now(timezone.utc).isoformat(),
                            'status': HTTPStatus.BAD_REQUEST.value,
                            'error': 'Country already exists'})

        db.countries.insert_one(payload)

    return jsonify({'timestamp': datetime.now(timezone.utc).isoformat(),
                    'status': HTTPStatus.OK.value})


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client['mydb']

    with open(r'countries.json') as json_file:
        data = json.load(json_file)
    db.drop_collection('countries')
    db.countries.insert_many(data)
    app.run(host='localhost', port=5000, debug=True)
