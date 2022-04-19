from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by().all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/product/<int:id>')
def product(id):
    product_detail = Item.query.get(id)
    return render_template('product.html', product_detail=product_detail)


@app.route('/buy/<int:id>')
def item_buy(id):
    return str(id)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']

        item = Item(title=title, price=price, text=text)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Что-то пошло не так!'
    else:
        return render_template('create.html')


@app.route('/product/<int:id>/update', methods=['POST', 'GET'])
def product_detail(id):
    prod = Item.query.get(id)
    if request.method == 'POST':
        prod.title = request.form['title']
        prod.price = request.form['price']
        prod.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'При редактировании товара произошла ошибка!'
    else:
        return render_template('product_update.html', prod=prod)


@app.route('/product/<int:id>/del')
def product_del(id):
    prod = Item.query.get_or_404(id)

    try:
        db.session.delete(prod)
        db.session.commit()
        return redirect('/')
    except:
        return 'При удалении товара произошла ошибка!'


if __name__ == '__main__':
    app.run(debug=True)

