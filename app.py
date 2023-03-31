from flask import Flask, render_template, request, url_for, send_from_directory
#from flask import Flask,render_template,request
#from flask_ngrok import run_with_ngrok
import json
#from PIL import Image
import base64
import io
from bert import bert_search
app = Flask(__name__)

@app.route('/')
def msg():
    return render_template('index.html')


# @app.route('/static/<path:path>')
# def serve_static(path):
#     return send_from_directory('static', path)

@app.route("/bert", methods=['POST','GET'])
def bert():
    search_term = request.form["input"]
    res,res1= bert_search(search_term)
    #print(res)
    #print(res1)
    return render_template('bert.html',res=res,res1=res1)
                           
@app.route("/pylucene", methods=['POST','GET'])
def pylucene():
    search_term = request.form["input"]
    res,res1= bert_search(search_term)
    print(res)
    print(res1)
    return render_template('pylucene.html',res=res,res1=res1)

# main driver function
if __name__ == '__main__':
	app.run()