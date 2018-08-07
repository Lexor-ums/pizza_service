import os
from datetime import datetime

from flask import Flask, render_template, json, jsonify, request, make_response
from flask_bootstrap import Bootstrap

from sqlalchemy import Integer, Text
import models
from models import Table

list_of_pizza = []

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
Bootstrap(app)

objects_in_line = 4

top_bar = {'Меню': '/', 'О нас': '/about', 'Меню администратора': '/admin', 'Корзина': '/bracket'}

menu_tab = Table("table_menu", models.engine)
menu_tab.add_columns(('id', Integer),
                    ('name', Text),
                    ('alt', Text),
                    ('image', Text),
                    ('ingredients', Text),
                    ('price', Integer))
order_tab = Table("table_order", models.engine)
order_tab.add_columns(('id', Integer),
                      ('items', Text),
                      ('address', Text),
                      ('name', Text),
                      ('state', Text),
                      ('time', Text))


@app.context_processor
def init_navbar():
    glob_dict = dict()
    glob_dict['top_bar'] = top_bar
    glob_dict['get_pizza_by_id'] = lambda x: get_pizza_by_id(x)
    if request.cookies.get('total_cost') is None or request.cookies.get('total_cost') == 0:
        glob_dict['total_cost'] = 0
    else:
        glob_dict['total_cost'] = request.cookies.get('total_cost')
    if request.cookies.get('total_items') is None or request.cookies.get('total_items') == 0:
            glob_dict['total_items'] = 0
    else:
        glob_dict['total_items'] = request.cookies.get('total_items')
    if request.cookies.get('address') is None:
        glob_dict['client_address'] = ''
    else:
        glob_dict['client_address'] = request.cookies.get('address')
    if request.cookies.get('name') is None:
        glob_dict['client_name'] = ''
    else:
        glob_dict['client_name'] = request.cookies.get('name')
    return glob_dict


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
    res = menu_tab.do_select()
    list_of_pizza = [dict(r) for r in res]
    return render_template('index.html', get_menu=lambda row: get_pizza(row))


@app.route('/about')
def home_about():
    global list_of_pizza
    return render_template('about.html')


@app.route('/confirm')
def confirm_page():
    return render_template('confirm.html')


@app.route('/add_to_list', methods=['POST', ])
def add_to_list():
    cookie = request.cookies.get('bracket')
    if cookie is None or cookie == '':
        data = []
    else:
        data = json.loads(cookie)
    data.append(int(request.values.get('id')))
    res = make_response('')
    res.set_cookie('bracket', json.dumps(data, indent=2))
    print('add to list ' + json.dumps(data, indent=2))
    return res


@app.route('/admin')
def page_admin():
    data = order_tab.do_select()
    return render_template('admin.html', orders=[dict(r) for r in data])


@app.route('/generate_order', methods=['POST', ])
def generate_order():
    cookie = request.cookies.get('bracket')
    if cookie is None or cookie == '':
        data = []
    else:
        data = json.loads(cookie)
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
    order_tab.do_insert(items=items,
                        address=request.cookies.get('address'),
                        name=request.cookies.get('name'),
                        time=datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"),
                        state='В обработке'
                        )
    res = make_response('')
    res.set_cookie('bracket', '')
    return res


@app.route('/remove_from_list', methods=['POST', ])
def remove_from_list():
    cookie = request.cookies.get('bracket')
    if cookie is None or cookie == '':
        data = []
    else:
        data = json.loads(cookie)
    data.remove(int(request.values.get('id')))
    res = make_response('')
    res.set_cookie('bracket', json.dumps(data, indent=2))
    return res


@app.route('/remove_from_orders', methods=['POST', ])
def remove_from_orders():
    order_tab.do_delete(int(request.values.get('id')))


@app.route('/cost', methods=['GET'])
def get_cost():
    pizza_id = request.values.get('data')
    for pizza in list_of_pizza:
        if pizza['id'] == int(pizza_id):
            return jsonify({'id': pizza_id, 'cost': pizza['price']})
    return None


@app.route('/bracket')
def bracket_page():
    cookie = request.cookies.get('bracket')
    if cookie is None or cookie == '':
        data = []
    else:
        data = json.loads(cookie)
    return render_template('bracket.html', list=data)


@app.route('/set_cookies', methods=['POST'])
def set_cookies():
    res = make_response('')
    for k, v in request.values.items():
        res.set_cookie(k, v)
    return res


if __name__ == '__main__':
    app.run(debug=True)
