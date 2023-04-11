from flask import Flask, render_template, request
from wtforms import Form, StringField, SelectField
from wtforms.validators import InputRequired, Optional


app = Flask(__name__)


class CafeForm(Form):
    c_coffee = StringField('Coffee Rating')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = CafeForm(request.form)
    if request.method == 'POST' and form.validate():
        print(form.c_coffee.data)
    return render_template('test.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
