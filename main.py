from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from dataGrabber import PoLine

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET', 'POST'])
def form():

    po = ''
    line = ''

    if request.method=='POST':
        po = request.form['po']
        line = request.form['line']

        if not po or not line:
            flash('Please enter a PO number and line!', 'error')
        else:
            return redirect('/label?po={}&line={}'.format(po, line))

    return render_template('form.html', title='Material Stickers', po=po, line=line)

@app.route('/label')
def label():
    args = request.args

    if 'po' and 'line' in args:
        po = str(args['po'])
        line = str(args['line'])
        poLine = PoLine(po, line)

        return render_template('label.html', poLine = poLine)
    else:
        flash('Invalid URL parameters', 'error')
        return redirect('/')

if __name__ == "__main__":
    app.run()
