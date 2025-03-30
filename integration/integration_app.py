from flask import Flask
app = Flask(__name__)

@app.route('/integration')
def hello_world():  # put application's code here
    return 'Hello World! - From Integration'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
