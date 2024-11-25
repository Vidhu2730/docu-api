from flask import Flask, request, jsonify
from controller import handle_interaction
from confluence_interaction import confluence_bp
import json

app = Flask(__name__)

app.register_blueprint(confluence_bp)

@app.route('/interact', methods=['POST'])
def interact():
    # Get data from the request
    data = request.json
    user_prompt = data.get("query")

    # Call the controller function
    response = handle_interaction(
        user_prompt
    )

    return response

if __name__ == '__main__':
    app.run(debug=True)