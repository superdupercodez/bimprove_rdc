from flask import Flask, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET','POST', 'OPTIONS'])
def home():
   return render_template('index.html')
if __name__ == '__main__':
   app.run(port=8081, host='0.0.0.0')
