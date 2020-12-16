from flask import Flask, render_template, url_for, request

app = Flask(__name__)


menu = [{'name': 'Головна сторінка', 'url': '/home'},
        {'name': 'Розрахунки', 'url': '/analize'},
        {'name': 'Контакти', 'url': '/about'}
        ]

@app.route('/')
@app.route('/home')
def index():
    print(url_for('index'))
    return render_template('index.html', title='Головна сторінка', menu = menu)

@app.route('/analize')
def analize():
    print(url_for('analize'))
    return render_template('analize.html', title='Розрахунки', menu = menu)


@app.route('/about')
def about():
    print(url_for('about'))
    return render_template('about.html', title='Про нас', menu = menu)


@app.route('/profile/<username>')
def user(username):
    return f'User profile: {username}'


if __name__ == '__main__':
    app.run(debug=True)