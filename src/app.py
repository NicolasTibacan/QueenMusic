from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Datos iniciales: 10 canciones más conocidas de Queen
songs = [
    {"id": 1, "nombre": "Bohemian Rhapsody", "fecha_lanzamiento": "1975-10-31"},
    {"id": 2, "nombre": "Don't Stop Me Now", "fecha_lanzamiento": "1979-01-26"},
    {"id": 3, "nombre": "We Will Rock You", "fecha_lanzamiento": "1977-10-07"},
    {"id": 4, "nombre": "We Are the Champions", "fecha_lanzamiento": "1977-10-07"},
    {"id": 5, "nombre": "Another One Bites the Dust", "fecha_lanzamiento": "1980-08-22"},
    {"id": 6, "nombre": "Somebody to Love", "fecha_lanzamiento": "1976-11-12"},
    {"id": 7, "nombre": "Radio Ga Ga", "fecha_lanzamiento": "1984-01-23"},
    {"id": 8, "nombre": "Under Pressure", "fecha_lanzamiento": "1981-10-26"},
    {"id": 9, "nombre": "I Want to Break Free", "fecha_lanzamiento": "1984-04-02"},
    {"id": 10, "nombre": "Killer Queen", "fecha_lanzamiento": "1974-10-21"}
]

def find_song(song_id):
    return next((song for song in songs if song["id"] == song_id), None)

@app.route('/canciones', methods=['GET'])
def get_songs():
    return jsonify(songs)

@app.route('/canciones/<int:song_id>', methods=['GET'])
def get_song(song_id):
    song = find_song(song_id)
    if song is None:
        abort(404)
    return jsonify(song)

@app.route('/canciones', methods=['POST'])
def create_song():
    if not request.json or not all(k in request.json for k in ("nombre", "fecha_lanzamiento")):
        abort(400)
    new_id = max(song["id"] for song in songs) + 1 if songs else 1
    song = {
        "id": new_id,
        "nombre": request.json["nombre"],
        "fecha_lanzamiento": request.json["fecha_lanzamiento"]
    }
    songs.append(song)
    return jsonify(song), 201

@app.route('/canciones/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    song = find_song(song_id)
    if song is None or not request.json:
        abort(404)
    song["nombre"] = request.json.get("nombre", song["nombre"])
    song["fecha_lanzamiento"] = request.json.get("fecha_lanzamiento", song["fecha_lanzamiento"])
    return jsonify(song)

@app.route('/canciones/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    song = find_song(song_id)
    if song is None:
        abort(404)
    songs.remove(song)
    return jsonify({"result": True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')