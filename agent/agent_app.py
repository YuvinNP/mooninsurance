from flask import Flask
app = Flask(__name__)

@app.route('/agent')
def hello_world():  # put application's code here
    return 'Hello World! - from AGENT'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
