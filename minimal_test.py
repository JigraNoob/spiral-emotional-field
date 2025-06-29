from flask import Flask
app = Flask(__name__)

@app.route('/minimal_test')
def minimal_test():
    print("Minimal test route called")
    return "Minimal Flask app working", 200

if __name__ == '__main__':
    app.run(port=5001)
