from cmath import pi
from textwrap import indent

from flask import Flask, render_template, json, jsonify, request, make_response
from flask_bootstrap import Bootstrap

list_of_pizza = []

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
Bootstrap(app)

objects_in_line = 4

top_bar = {'Меню': '/', 'О нас': '/', 'Корзина': '/bracket'}


@app.context_processor
def init_navbar():
    if request.cookies.get('total_cost') is None or request.cookies.get('total_items') is None:
        return dict(top_bar=top_bar,
                    total_cost=0,
                    total_items=0,
                    get_pizza_by_id=lambda x: get_pizza_by_id(x))
    else:
        return dict(top_bar=top_bar,
                    total_cost=request.cookies.get('total_cost'),
                    total_items=request.cookies.get('total_items'),
                    get_pizza_by_id=lambda x: get_pizza_by_id(x))


def get_pizza(row):
    if row * objects_in_line + objects_in_line > len(list_of_pizza):
        return list_of_pizza[row * objects_in_line:]
    else:
        return list_of_pizza[row * objects_in_line: objects_in_line]


def get_pizza_by_id(pizza_id):
    for pizza in list_of_pizza:
        if int(pizza['id']) == pizza_id:
            return pizza
    return None


@app.route('/')
def home_page():
    global list_of_pizza
    list_of_pizza = json.load((open('static/menu.json')))
    return render_template('index.html', get_menu=lambda row: get_pizza(row))


@app.route('/add_to_list', methods=['POST',])
def add_to_list():
    try:
        data = json.load((open('static/list.json')))
    except:
        data = []
    data.append(int(request.values.get('id')))
    with open('static/list.json', 'w') as f:
        json.dump(data, f, indent=2)


@app.route('/cost', methods=['GET'])
def get_cost():
    pizza_id = request.values.get('data')
    for pizza in list_of_pizza:
        if pizza['id'] == int(pizza_id):
            return jsonify({'id': pizza_id, 'cost': pizza['price']})
    return None


@app.route('/bracket')
def bracket_page():
    data = json.load((open('static/list.json')))
    return render_template('bracket.html', list=data)


@app.route('/set_cookies', methods=['POST'])
def set_cookies():
    res = make_response('')
    res.set_cookie('total_cost', request.values.get('total_cost'))
    res.set_cookie('total_items', request.values.get('total_items'))
    return res


if __name__ == '__main__':
    request.cookies.clear()
    app.run(debug=True)
