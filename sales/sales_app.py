from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

uname = 'admin'
password = 'root#123'
host = 'moonagentdb.cxoameg6ycbo.us-east-1.rds.amazonaws.com'
port = 3306
dbname = 'mooninsurance_db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{uname}:{password}@{host}:{port}/{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Sales(db.Model):
    __tablename__ = 'sales'
    __table_args__ = {'schema': 'mooninsurance_db'}

    sale_id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.String(50), nullable=False)
    sales_amount = db.Column(db.String(100), nullable=False)
    sales_date = db.Column(db.String(10), nullable=False)


sales = {}


@app.route('/sales')
def hello_world():  # put application's code here
    return 'Hello World! - from sale'


@app.route('/sales/post_sales', methods=['POST'])
def create_sale():
    data = request.form

    new_sale = Sales(
        agent_id=data.get('agent_id'),
        product_id=data.get('product_id'),
        sales_amount=data.get('sales_amount'),
        sales_date=data.get('sales_date')
    )

    db.session.add(new_sale)
    db.session.commit()

    return jsonify(
        {"message": "sale created successfully",
         "sale": new_sale.sale_id
         }), 201


@app.route('/sales/get_sales/<sale_id>', methods=['GET'])
@app.route('/sales/get_sales', defaults={'sales_id': None}, methods=['GET'])
def get_sale(sale_id):
    if sale_id:
        sale = Sales.query.get(sale_id)
        if not sale:
            return jsonify({"message": "sale not found"}), 404
        sale_data = {
            "sale_id": sale.sales_id,
            "agent_id": sale.agent_id,
            "product_id": sale.product_id,
            "sales_amount": sale.sales_amount,
            "sales_date": sale.sales_date
        }
        return jsonify({"sale": sale_data}), 200
    else:
        sales_all = Sales.query.all()
        result = [{
            "sale_id": a.sales_id,
            "agent_id": a.agent_id,
            "product_id": a.product_id,
            "sales_amount": a.sales_amount,
            "sales_date": a.sales_date
        } for a in sales_all]

        return jsonify({
            "message": "sales fetched successfully",
            "sales": result
        }), 200


# Delete sale (DELETE)
@app.route('/sales/delete_sales/<sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    sale = Sales.query.get(sale_id)
    if not sale:
        return jsonify({"message": "sale not found"}), 404

    db.session.delete(sale)
    db.session.commit()

    return jsonify({"message": f"sale: {sale.sales_id} deleted successfully"}), 200


@app.route('/', methods=['GET'])
def hello_world_get():  # put application's code here
    return 'Hello World! - from sale /'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
