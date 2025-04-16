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

class Agent(db.Model):
    __tablename__ = 'agents'
    __table_args__ = {'schema': 'mooninsurance_db'}

    agent_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    uname = db.Column(db.String(20), nullable=False)
    branch_id = db.Column(db.Integer, nullable=False)


agents = {}


@app.route('/agent')
def hello_world():  # put application's code here
    return 'Hello World! - from AGENT'


@app.route('/agent/post_agent', methods=['POST'])
def create_agent():
    data = request.form

    username = f'{data["first_name"]}_{data["last_name"]}'

    new_agent = Agent(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        uname=username,
        phone=data.get('phone'),
        branch_id=data.get('branch_id')
    )

    db.session.add(new_agent)
    db.session.commit()

    return jsonify(
        {"message": "Agent created successfully",
         "agent": new_agent.agent_id,
         "username": username,
         }), 201


@app.route('/agent/get_agent/<agent_id>', methods=['GET'])
@app.route('/agent/get_agent', defaults={'agent_id': None}, methods=['GET'])
def get_agent(agent_id):
    if agent_id:
        agent = Agent.query.get(agent_id)
        if not agent:
            return jsonify({"message": "Agent not found"}), 404
        agent_data = {
            "agent_id": agent.agent_id,
            "first_name": agent.first_name,
            "last_name": agent.last_name,
            "username": agent.uname,
            "email": agent.email,
            "phone": agent.phone,
            "branch_id": agent.branch_id
        }
        return jsonify({"agent": agent_data}), 200
    else:
        agents_all = Agent.query.all()
        result = [{
            "agent_id": a.agent_id,
            "first_name": a.first_name,
            "last_name": a.last_name,
            "username": a.uname,
            "email": a.email,
            "phone": a.phone,
        } for a in agents_all]

        return jsonify({
            "message": "Agents fetched successfully",
            "agents": result
        }), 200


# Delete agent (DELETE)
@app.route('/agent/delete_agent/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    agent = Agent.query.get(agent_id)
    if not agent:
        return jsonify({"message": "agent not found"}), 404

    db.session.delete(agent)
    db.session.commit()

    return jsonify({"message": f"Agent: {agent.uname} deleted successfully"}), 200


@app.route('/', methods=['GET'])
def hello_world_get():  # put application's code here
    return 'Hello World! - from AGENT /'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
