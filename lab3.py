from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Define the models

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    employees_count = db.Column(db.Integer)
    location = db.Column(db.String(100))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    hashed_password = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

# Register route
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Login route
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({"token": token}), 200

    return jsonify({"message": "Invalid credentials"}), 401

# CRUD Operations for Company

# Create a new company (Only authenticated users)
@app.route('/api/companies', methods=['POST'])
@jwt_required()
def create_company():
    data = request.get_json()
    current_user = get_jwt_identity()  # Get current logged-in user

    new_company = Company(
        name=data['name'],
        description=data['description'],
        employees_count=data['employees_count'],
        location=data['location']
    )

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "Company created successfully", "company": new_company.name}), 201

# Get all companies
@app.route('/api/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    result = [{"id": company.id, "name": company.name, "description": company.description, 
               "employees_count": company.employees_count, "location": company.location} 
              for company in companies]

    return jsonify(result), 200

# Get a single company by ID
@app.route('/api/companies/<int:id>', methods=['GET'])
def get_company(id):
    company = Company.query.get(id)
    if not company:
        return jsonify({"message": "Company not found"}), 404

    result = {
        "id": company.id,
        "name": company.name,
        "description": company.description,
        "employees_count": company.employees_count,
        "location": company.location
    }

    return jsonify(result), 200

# Update company details (Only authenticated users)
@app.route('/api/companies/<int:id>', methods=['PUT'])
@jwt_required()
def update_company(id):
    data = request.get_json()
    company = Company.query.get(id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    # Optionally: check if the current user is the owner of the company (not implemented here)

    company.name = data.get('name', company.name)
    company.description = data.get('description', company.description)
    company.employees_count = data.get('employees_count', company.employees_count)
    company.location = data.get('location', company.location)

    db.session.commit()

    return jsonify({"message": "Company updated successfully"}), 200

# Delete a company (Only authenticated users)
@app.route('/api/companies/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_company(id):
    company = Company.query.get(id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    db.session.delete(company)
    db.session.commit()

    return jsonify({"message": "Company deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
