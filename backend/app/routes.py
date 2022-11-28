from flask import render_template, jsonify, request
from app import service
from flask_api import status


from app import app,APP_ROOT

@app.route('/')
def home():
    return render_template('index.html',title='Home')


@app.route("/load_faces",  methods=['POST']) 
def register():
    if request.method == 'POST':
        model = request.get_json()
        service.save_faces(model['name'], model['images'])
        service.save_encodings(model['name'])
        return "Success", 201

@app.route("/find_face",  methods=['POST']) 
def login():
    if request.method == 'POST':
        model = request.get_json()
        image = model['image']
        userName = model['name']
        (status) = service.find_face(userName, image[22:])
        print(status, type(status))
        return status, 200
  