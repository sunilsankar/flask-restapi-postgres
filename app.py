import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@172.16.16.100:5432/inventories"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%s:%s@%s/%s' % (
    # ARGS.dbuser, ARGS.dbpass, ARGS.dbhost, ARGS.dbname
    os.environ['DBUSER'], os.environ['DBPASS'], os.environ['DBHOST'], os.environ['DBNAME']
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class InventoriesModel(db.Model):
    __tablename__ = 'inventories'

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String())
    environment = db.Column(db.String())
    ipaddress = db.Column(db.String())
    applicationname = db.Column(db.String())

    def __init__(self, hostname, environment, ipaddress, applicationname):
        self.hostname = hostname
        self.applicationname = applicationname
        self.environment = environment
        self.ipaddress = ipaddress

    def __repr__(self):
        return f"<Inventory {self.hostname}>"


@app.route('/')
def hello():
        db.create_all()
        db.session.commit()
        return {"message": "The is a inventory script"}


@app.route('/inventories', methods=['POST', 'GET'])
#def test_db():
#     db.create_all()    
#     db.session.commit() 
#     return {"message": f"tables created."}
def handle_inventories():
    if request.method == 'POST':
        db.create_all()
        db.session.commit()
        if request.is_json:
            data = request.get_json()
            new_inventory = InventoriesModel(hostname=data['hostname'], environment=data['environment'], ipaddress=data['ipaddress'], applicationname=data['applicationname'])

            db.session.add(new_inventory)
            db.session.commit()

            return {"message": f"inventory {new_inventory.hostname} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        inventories = InventoriesModel.query.all()
        results = [
            {
                "hostname": inventory.hostname,
                "environment": inventory.environment,
                "ipaddress": inventory.ipaddress,
                "applicationname": inventory.applicationname
            } for inventory in inventories]

        return {"count": len(results), "inventories": results, "message": "success"}


@app.route('/inventories/<inventory_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_inventory(inventory_id):
    inventory = InventoriesModel.query.get_or_404(inventory_id)

    if request.method == 'GET':
        response = {
            "hostname": inventory.hostname,
            "environment": inventory.environment,
            "ipaddress": inventory.ipaddress,
            "applicationname": inventory.applicationname
        }
        return {"message": "success", "inventory": response}

    elif request.method == 'PUT':
        data = request.get_json()
        inventory.hostname = data['hostname']
        inventory.environment = data['environment']
        inventory.ipaddress = data['ipaddress']
        inventory.applicationname = data['applicationname']

        db.session.add(inventory)
        db.session.commit()
        
        return {"message": f"inventory {inventory.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(inventory)
        db.session.commit()
        
        return {"message": f"Car {inventory.hostname} successfully deleted."}


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
