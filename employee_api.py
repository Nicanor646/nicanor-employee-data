import os
import json
from flask import Flask, request
from flask_restful import Resource, Api

from etl import CSVETL
from report import Report

UPLOAD_FOLDER = os.environ.get("EMPLOYEE_API_UPLOAD_FOLDER", "tmp")
supported_data_types = [ "department", "job", "employee" ]
supported_reports = [ "employees_by_q" ]

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

class CSVEndpoint(Resource):

    def _cleanup_files(self, folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    def post(self, data_type):
        print(data_type)
        if data_type not in supported_data_types:
            return { "message": "Data type is not supported"}, 400
        if request.files:
            try:
                csv_file = request.files['csv_file']
                file_path = f"{UPLOAD_FOLDER}/{csv_file.filename}"
                csv_file.save(file_path)
                csv_etl = CSVETL(file_path, data_type)
                csv_etl.etl()
                self._cleanup_files(UPLOAD_FOLDER)
                return { "message": f"uploaded {csv_file.filename} to {data_type}"}, 200
            except Exception  as e:
                print(e)
                return { "message": "No file"}, 400
        elif request.is_json:
            file_path = request.json["csv_path"]
            return { "message": f"uploading {file_path} to {data_type}"}, 200

api.add_resource(CSVEndpoint, '/csv/<string:data_type>')

class ReportEndpoint(Resource):
    def get(self,report_type):
        if report_type not in supported_reports:
            return { "message": "Report is not implemented"}, 400
        report = Report()
        match report_type:
            case "employees_by_q":
                year = int(request.args.get('year', 2021) )
                report_results = report.employees_by_q(year)
                return {"results": report_results}

api.add_resource(ReportEndpoint, '/reports/<string:report_type>')

if __name__ == '__main__':
    app.run(debug=True)