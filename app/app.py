from flask import Flask, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

# @app.route('/<name>',methods = ['POST', 'GET'])
# def request():
#    if request.method == 'POST':
#       user = request.form['nm']
#       return redirect(url_for('success',name = user))
#    else:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))


if __name__ == '__main__':
    app.run()
