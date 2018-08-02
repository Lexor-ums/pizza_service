import os
from datetime import datetime

from flask import Flask, render_template, json, jsonify, request, make_response
from flask_bootstrap import Bootstrap

list_of_pizza = []

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
Bootstrap(app)

objects_in_line = 4

top_bar = {'Меню': '/', 'О нас': '/', 'Меню администратора': '/admin', 'Корзина': '/bracket'}


@app.context_processor
def init_navbar():
    if request.cookies.get('total_cost') is None or request.cookies.get('total_items') is None:
        return dict(top_bar=top_bar,
                    total_cost=0,
                    total_items=0,
                    client_address='',
                    client_name='',
                    get_pizza_by_id=lambda x: get_pizza_by_id(x))
    else:
        return dict(top_bar=top_bar,
                    total_cost=request.cookies.get('total_cost'),
                    total_items=request.cookies.get('total_items'),
                    client_address=request.cookies.get('address'),
                    client_name=request.cookies.get('name'),
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
    list_of_pizza = json.load((open(os.path.abspath(os.curdir) + '/static/menu.json')))
    return render_template('index.html', get_menu=lambda row: get_pizza(row))


@app.route('/confirm')
def confirm_page():
    return render_template('confirm.html')


@app.route('/add_to_list', methods=['POST',])
def add_to_list():
    try:
        data = json.load((open(os.path.abspath(os.curdir) + '/static/list.json')))
    except:
        data = []
    data.append(int(request.values.get('id')))
    with open('static/list.json', 'w') as f:
        json.dump(data, f, indent=2)


@app.route('/admin')
def page_admin():
    try:
        data = json.load((open(os.path.abspath(os.curdir) + '/static/order.json')))
    except:
        data = []
    return render_template('admin.html', orders=data)


@app.route('/generate_order', methods=['POST',])
def generate_order():
    try:
        data = json.load((open(os.path.abspath(os.curdir) + '/static/list.json')))
    except:
        data = []
    try:
        order = json.load((open(os.path.abspath(os.curdir) + '/static/order.json')))
    except:
        order = []
    used = dict()
    for i in data:
        if used.__contains__(i):
            used.__setitem__(i, used[i] + 1)
        else:
            used.__setitem__(i, 1)
    items = ''
    for k, v in used.items():
        items += '{0}({1}),'.format(get_pizza_by_id(k)['name'], str(v))
    items = items[:-1]
    print('items ', items)
    order.append(dict(id=len(order) + 1,
                      items=items,
                      address=request.cookies.get('address'),
                      name=request.cookies.get('name'),
                      time=datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"),
                      state='В обработке'
                      ))
    print('order', order)
    with open(os.path.abspath(os.curdir) + '/static/order.json', 'w') as f:
        json.dump(order, f, indent=2)
    with open('static/list.json', 'w') as f:
        f.close()


@app.route('/remove_from_list', methods=['POST',])
def remove_from_list():
    try:
        data = json.load((open(os.path.abspath(os.curdir) + '/static/list.json')))
    except:
        data = []
    data.remove(int(request.values.get('id')))
    with open(os.path.abspath(os.curdir) + '/static/list.json', 'w') as f:
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
    data = json.load((open(os.path.abspath(os.curdir) + '/static/list.json')))
    return render_template('bracket.html', list=data)


@app.route('/set_cookies', methods=['POST'])
def set_cookies():
    res = make_response('')
    for k, v in request.values.items():
        res.set_cookie(k, v)
    return res


if __name__ == '__main__':
    app.run(debug=True)
