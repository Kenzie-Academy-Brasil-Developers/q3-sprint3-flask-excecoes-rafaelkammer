from flask import Flask, request
import os
from json import load, dump

app = Flask(__name__)
if(__name__=='__main__'):
    app.run()

@app.get('/user')
def get_users():
    try:
        if not os.path.exists("./app/database.json"):
            os.system('touch app/database.json')
            with open(f"./app/database.json", "a") as f:
                f.write('{"data": []}')
            with open(f"./app/database.json", "r") as r:
                read = r.read()
            return read, 200
        else:
            raise FileExistsError
    except FileExistsError:
        with open(f"./app/database.json", "r") as r:
            read = r.read()            
        if(read == ''):
            with open(f"./app/database.json", "a") as f:
                f.write('{"data": []}')
            with open(f"./app/database.json", "r") as r:                
                return r.read(), 200
        elif(read == '[]'):
            return read, 200
        else:
            with open(f"./app/database.json", "r") as r:
                read = load(r)                
                return read, 200


@app.post('/user')
def post_user():
    try:
        with open("./app/database.json", "r") as r:
            read = load(r)
    except FileNotFoundError:
        os.system('touch app/database.json')
        with open(f"./app/database.json", "a") as f:
            f.write('{"data": []}')
        with open("./app/database.json", "r") as r:
            read = load(r)

    if (type(request.get_json()['nome']) != str or 
        type(request.get_json()['email']) != str):
        return {"wrong fields": 
        [
            {"nome": f"{type(request.get_json()['nome'])}"},
            {"email": f"{type(request.get_json()['email'])}"}
        ]}, 400

    formated_name = request.get_json()['nome'].title()
    formated_email = request.get_json()['email'].lower()
    new_id = len(read['data']) + 1 if len(read['data']) else 1

    formated_user_data = {'nome': f'{formated_name}', 'email': f'{formated_email}', '_id': f'{new_id}'}

    for data in read['data']:
        if(data['email'] == formated_email):
            return {"error": "User already exists."}, 409
            
    with open("./app/database.json", "w") as w:
        read['data'].append(formated_user_data)
        dump(read, w ,indent=4)
        return {"data": formated_user_data}, 201