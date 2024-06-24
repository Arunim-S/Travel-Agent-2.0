from flask import Flask, request, jsonify
from flask_cors import CORS
from graph2 import generate_travel_plan

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query')
    response = generate_travel_plan(query)
    print(response)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
