from flask import Response
from dicttoxml import dicttoxml
import csv, io

def api_response(dicts_list, content_type):
    if content_type == 'application/json':
        return dicts_list
    elif content_type == 'application/xml':
        xml = dicttoxml(dicts_list)
        return Response(xml, content_type=content_type)
    elif content_type == 'text/csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(dicts_list[0].keys())
        for violation in dicts_list:
            writer.writerow([value for value in violation.values()])
        return Response(output.getvalue(), content_type=content_type)

def post_request_arguments(request):
    content_type = request.content_type
    if content_type == 'application/json':
        return request.get_json()
    elif content_type == 'application/x-www-form-urlencoded':
        return request.form
