from flask import Flask, render_template, url_for, request
from make_pdf import MakePDF
from select_serial import SelectSerial
import time

app = Flask(__name__)


menu = [{'name': 'Головна', 'url': '/'},
        {'name': 'Розрахунки', 'url': '/calculation'},
        {'name': 'Контакти', 'url': '/about'}
        ]


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Головна сторінка', menu=menu)


requests_dict = dict()
number_mark = 1
position_mark = 'ПР'


@app.route('/calculation', methods=['GET', 'POST'])
def calculation():
    global number_mark
    if request.method == 'POST':
        type_of_wall = request.form['type_of_wall']
        type_of_construction_wall = request.form['type_of_construction_wall']
        height_of_bricks = request.form['height_of_bricks']
        width_of_opening = request.form['width_of_opening']
        width_of_wall = request.form['width_of_wall']
        requests_dict[f'{position_mark}-{number_mark}'] = [
            type_of_wall,
            type_of_construction_wall,
            height_of_bricks,
            width_of_opening,
            width_of_wall
        ]
        number_mark += 1
    print(requests_dict)
    return render_template('calculation.html', title='Розрахунки', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title='Про нас', menu=menu)


file_number = 0
file_name = ''


@app.route('/result', methods=['POST'])
def result():
    dict_for_pdf = dict()
    global file_number
    global file_name
    if request.method == 'POST':
        file_number += 1
        file_name = f'files/result_{file_number}.pdf'
        for mark, parameters in requests_dict.items():
            package = SelectSerial(parameters)
            dict_for_pdf[mark] = package.get_result()
    print(dict_for_pdf)
    # MakePDF(dict_for_pdf, file_name)
    return render_template('result.html', title='Результат', file=file_name)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Сторінка не знайдена', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)