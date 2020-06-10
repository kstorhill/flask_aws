import json
import boto3
from flask_lambda import FlaskLambda
from flask import request

app = FlaskLambda(__name__)
ddb = boto3.resource('dynamodb')
table = ddb.Table('students')

@app.route('/hello')
def index():
    data = {
        "message": "Hello, world!"
    }
    return (
        json.dumps(data),
        200,
        {'Content-Type': "application/json"}
    )

@app.route('/students', methods=['GET', 'POST'])
def put_or_list_students():
    if request.method == 'GET':
        students = table.scan()['Items']
        return (
        json.dumps(students),
        200,
        {'Content-Type': "application/json"}
    )
    else:
        table.put_item(Item=request.form.to_dict())
        return (
        json.dumps({"message": "student entry created"}),
        200,
        {'Content-Type': "application/json"}
    )

@app.route('/students/<id>', methods=['GET', 'PATCH', 'DELETE'])
def get_patch_delete_student(id):
    key = {'id': id}
    if request.method == 'GET':
        student = table.get_item(Key=key).get('Item')
        if student:
            return (
                json.dumps(student),
                200,
                {'Content-Type': "application/json"}
            )
        else:
            return (
                json.dumps({"message": "student not found"}),
                200,
                {'Content-Type': "application/json"}
    )
    elif request.method == 'PATCH':
        attribute_updates = {key: {'Value': value, 'Action': 'PUT'} for key, value in request.form.items()}
        table.update_item(Key=key, AttributeUpdates=attribute_updates)
        return (
                json.dumps({"message": "student entry updated"}),
                200,
                {'Content-Type': "application/json"}
        )
    else:
        table.delete_item(Key=key)
        return (
                json.dumps({"message": "student entry deleted"}),
                200,
                {'Content-Type': "application/json"}
        )