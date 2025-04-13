from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

uname = 'admin'
password = 'root#123'
host = 'mooninsurancedb.cxoameg6ycbo.us-east-1.rds.amazonaws.com'
port = 3306
dbname = 'mooninsurance_db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{uname}:{password}@{host}:{port}/{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Integration(db.Model):
    __tablename__ = 'integrations'
    __table_args__ = {'schema': 'mooninsurance_db'}

    integration_id = db.Column(db.Integer, primary_key=True)
    agent_code = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    sales_amount = db.Column(db.String(10), nullable=False)
    sales_date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)


integrations = {}


@app.route('/integration')
def hello_world():  # put application's code here
    return 'Hello World! - from integration'


@app.route('/integration/post_integration', methods=['POST'])
def create_integration():
    data = request.form

    new_integration = Integration(
        agent_code=data.get('agent_code'),
        product_id=data.get('product_id'),
        sales_amount=data.get('sales_amount'),
        sales_date=data.get('sales_date'),
        status=data.get('status')
    )

    db.session.add(new_integration)
    db.session.commit()

    return jsonify(
        {"message": "integration created successfully",
         "integration": new_integration.integration_id,
         "username": new_integration.status,
         }), 201


@app.route('/integration/get_integration/<integration_id>', methods=['GET'])
@app.route('/integrations/get_integration', defaults={'integration_id': None}, methods=['GET'])
def get_integration(integration_id):
    if integration_id:
        integration = Integration.query.get(integration_id)
        if not integration:
            return jsonify({"message": "integration not found"}), 404
        integration_data = {
            "integration_id": integration.integration_id,
            "agent_code": integration.agent_code,
            "product_id": integration.product_id,
            "sales_amount": integration.sales_amount,
            "sales_date": integration.sales_date,
            "status": integration.status
        }
        return jsonify({"integration": integration_data}), 200
    else:
        integrations_all = Integration.query.all()
        result = [{
            "integration_id": a.integration_id,
            "agent_code": a.agent_code,
            "product_id": a.product_id,
            "sales_amount": a.sales_amount,
            "sales_date": a.sales_date,
            "status": a.status,
        } for a in integrations_all]

        return jsonify({
            "message": "integrations fetched successfully",
            "integrations": result
        }), 200


# Delete integration (DELETE)
@app.route('/integrations/delete_integration/<integration_id>', methods=['DELETE'])
def delete_integration(integration_id):
    integration = Integration.query.get(integration_id)
    if not integration:
        return jsonify({"message": "integration not found"}), 404

    db.session.delete(integration)
    db.session.commit()

    return jsonify({"message": f"integration: {integration.integration_id} deleted successfully"}), 200


@app.route('/', methods=['GET'])
def hello_world_get():  # put application's code here
    return 'Hello World! - from integration /'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
