from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from dataGrabber import LabelBuilder

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "6r$QDzDI6fL$"

builder = LabelBuilder()


@app.route('/', methods=['GET', 'POST'])
def form():

    po = ''
    line = ''

    if request.method=='POST':
        po = request.form['po']
        line = request.form['line']

        if not po:
            flash('Please enter a PO number!', 'error')
        elif not line:
            return redirect('/label?po={}'.format(po))
        else:
            return redirect('/label?po={}&line={}'.format(po, line))

    return render_template('form.html', title='Material Stickers', po=po, line=line)

@app.route('/label')
def label():
    args = request.args

    if 'po' and 'line' in args:
        po = str(args['po'])
        line = str(args['line'])
        poLine = builder.buildSingleLabel(po, line)
        #print(poLine)

        return render_template('label.html', poLine = poLine)

    elif 'po' and not 'line' in args:
        po = str(args['po'])
        poLines = builder.buildAllLabels(po)

        if len(poLines) > 1:
            return render_template('lines.html', lines = poLines)
        else:
            return render_template('label.html', poLine = poLines[0])

    else:
        flash('Invalid URL parameters', 'error')
        return redirect('/')

if __name__ == "__main__":
    app.run()
