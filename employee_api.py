import os
from flask import Flask, request
from flask_restful import Resource, Api

UPLOAD_FOLDER = os.environ.get("EMPLOYEE_API_UPLOAD_FOLDER", "tmp")
supported_data_types = [ "department", "job", "employee" ]

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

class CSVEndpoint(Resource):
    def post(self, data_type):
        print(data_type)
        if data_type not in supported_data_types:
            return { "message": "Data type is not supported"}, 400
        if request.files:
            try:
                csv_file = request.files['csv_file']
                file_path = f"{UPLOAD_FOLDER}/{csv_file.filename}"
                csv_file.save(file_path)
                return { "message": f"uploaded {csv_file.filename} to {data_type}"}, 200
            except Exception  as e:
                return { "message": "No file"}, 400
        elif request.is_json:
            file_path = request.json["csv_path"]
            return { "message": f"uploading {file_path} to {data_type}"}, 200

api.add_resource(CSVEndpoint, '/csv/<string:data_type>')

if __name__ == '__main__':
    app.run(debug=True)