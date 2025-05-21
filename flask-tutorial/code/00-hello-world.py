from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hello world"

if __name__ == '__main__':
    app.run(debug=True)
    # you can make the server publicly available simply by adding --host=0.0.0.0 
    # app.run(debug=True, host='0.0.0.0')
