import flask
from flask import jsonify


books = [
    {
        'id': 0,
        'title': 'Il nome della Rosa',
        'author': 'Umberto Eco',
        'year_published': '1890'
    },

    {
        'id': 1,
        'title': 'Il problema dei tre corpi',
        'author': 'Liu Cixin',
        'year_published': '2008'
    },

    {
        'id': 2,
        'title': 'Fondazione',
        'author': 'Isaac Osimov',
        'year_published': '1951'
    }
]

app = flask.Flask(__name__)
app.config['DEBUG'] = True

@app.route('/',methods=['GET'])
def home():
    return "<h1>Un API, così, giusto per provare</h1>"

@app.route('/api/v1/resouces/books/all', methods=["GET"])
def api_all():
    return jsonify(books) #prova a trasformare in json

app.run()

