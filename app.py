from flask import Flask, request, jsonify
from agent.agent import ask_llm,debug_agent

app = Flask(__name__)

@app.route("/")
def home():
    return "Server is running!"

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("query")
    response = ask_llm(user_input)
    return jsonify({"response": response})

@app.route("/debug", methods=["POST"])
def debug():
    user_input = request.json.get("input")
    return jsonify({"response": debug_agent(user_input)})

if __name__ == "__main__":
    app.run(debug=True)