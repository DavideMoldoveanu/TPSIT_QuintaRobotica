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
app.config["DEBUG"] = True

@app.route('/', methods = ['GET'])
def home():
    return "<h1>Biblioteca online</h1><p>Prototipo di web API</p> <p> <button onclick='window.location.href='http://127.0.0.1:5000/api/v1/resources/books/all';'>Click Here</button></p>"

@app.route('/api/v1/resources/books/all', methods = ['GET'])
def api_all():
    return jsonify(books)

app.run()

