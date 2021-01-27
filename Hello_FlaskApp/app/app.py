from flask import Flask, redirect, url_for, request, render_template
import random
app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return "Hello Phani !!!"

@app.route('/<dice>')
def dice_roller(dice):
    if dice == 'dice':
        mydice = random.randint(1, 6)
    else:
        mydice = "Invalid Option."
    return "Dice rolled on --> {}".format(mydice)

@app.route('/success/<username>')
def successLogin(username):
    return render_template('hello.html', uname=username, uname2=username)


@app.route('/login', methods=['POST', 'GET'])
def logintest():
    if request.method == 'POST':
        user = request.form['uname']
        return redirect(url_for('successLogin', username=user))
    else:
        user = request.args.get('uname')
        return redirect(url_for('successLogin', username=user))

app.add_url_rule('/','/hello', hello_world)
if __name__ == '__main__':
    app.run()