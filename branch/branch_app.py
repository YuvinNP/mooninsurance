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


class Branch(db.Model):
    __tablename__ = 'branches'
    __table_args__ = {'schema': 'mooninsurance_db'}

    branch_id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    total_sales = db.Column(db.String(100), nullable=False)


branches = {}


@app.route('/branch')
def hello_world():  # put application's code here
    return 'Hello World! - from branch'


@app.route('/branch/post_branch', methods=['POST'])
def create_branch():
    data = request.form

    new_branch = Branch(
        branch_name=data.get('branch_name'),
        location=data.get('location'),
        total_sales=data.get('total_sales')
    )

    db.session.add(new_branch)
    db.session.commit()

    return jsonify(
        {"message": "branch created successfully",
         "branch": new_branch.branch_id,
         "username": uname,
         }), 201


@app.route('/branch/get_branch/<branch_id>', methods=['GET'])
@app.route('/branch/get_branch', defaults={'branch_id': None}, methods=['GET'])
def get_branch(branch_id):
    if branch_id:
        branch = Branch.query.get(branch_id)
        if not branch:
            return jsonify({"message": "branch not found"}), 404
        branch_data = {
            "branch_id": branch.branch_id,
            "branch_name": branch.branch_name,
            "location": branch.location,
            "total_sales": branch.total_sales
        }
        return jsonify({"branch": branch_data}), 200
    else:
        branches_all = Branch.query.all()
        result = [{
            "branch_id": a.branch_id,
            "branch_name": a.branch_name,
            "location": a.location,
            "total_sales": a.total_sales
        } for a in branches_all]

        return jsonify({
            "message": "Branches fetched successfully",
            "branchs": result
        }), 200


# Delete branch (DELETE)
@app.route('/branch/delete_branch/<branch_id>', methods=['DELETE'])
def delete_branch(branch_id):
    branch = Branch.query.get(branch_id)
    if not branch:
        return jsonify({"message": "branch not found"}), 404

    db.session.delete(branch)
    db.session.commit()

    return jsonify({"message": f"branch: {branch.branch_name} deleted successfully"}), 200


@app.route('/', methods=['GET'])
def hello_world_get():  # put application's code here
    return 'Hello World! - from branch /'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
