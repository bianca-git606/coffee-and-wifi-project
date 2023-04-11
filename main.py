from flask import Flask, render_template, request
from wtforms import StringField, SelectField, Form
from wtforms.validators import InputRequired
import csv

app = Flask(__name__)


class CafeForm(Form):
    c_name = StringField('Cafe Name', validators=[InputRequired()])
    c_location = StringField('Location', validators=[InputRequired()])
    c_open = StringField('Open Time e.g. 8AM', validators=[InputRequired()])
    c_close = StringField('Close Time e.g. 5:30PM', validators=[InputRequired()])
    c_coffee = SelectField('Coffee Rating', choices=['✘', '☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'])
    c_wifi = SelectField('Wifi Rating', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
    c_power = SelectField('Power Rating', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])


@app.route('/')
def home():
    return render_template('index.html')


def get_cafe_list():
    cafe_objs = []
    with open('cafe-data.csv', encoding='utf-8') as file:
        csv_data = csv.reader(file)
        for row in csv_data:
            cafe_objs.append(row)
    return cafe_objs


@app.route('/cafes', methods=['GET', 'POST'])
def cafes():
    cafe_objs = get_cafe_list()
    return render_template('cafes.html', cafe_objs=cafe_objs)


def add_to_file(f):
    with open('cafe-data.csv', 'a', newline='', encoding='UTF-8') as file:
        new_obj = [f.c_name.data, f.c_location.data, f.c_open.data, f.c_close.data, f.c_coffee.data,
                   f.c_wifi.data, f.c_power.data]
        w = csv.writer(file)
        w.writerow(new_obj)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = CafeForm(request.form)
    if request.method == 'POST':

        form.validate()

        if not form.c_name.data[0].isalpha():
            # checks if valid name
            form.c_name.errors.append('Name cannot start with a number.')
            return render_template('add.html', form=form)

        if not form.c_location.data.startswith('https://'):
            # checks if valid url
            form.c_location.errors.append('Invalid URL')
            return render_template('add.html', form=form)

        add_to_file(form)
        cafe_objs = get_cafe_list()
        return render_template('cafes.html', cafe_objs=cafe_objs)

    return render_template('add.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
