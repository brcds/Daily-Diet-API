from flask import Flask, request, jsonify
from models.user import User
from models.meal import Meal
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mysqladmin:mysqladmin123@localhost:3306/mydailydiet'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticação realizada com sucesso!"}), 200
    return jsonify({"message": "Credenciais inválidas"}), 400


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"}), 400


@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    exist_user = User.query.filter_by(username=username).first()
    if exist_user:
        return jsonify({"message": "Usuário já cadastrado!"}), 401

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso!"}), 200
    return jsonify({"message": "Dados inválidos!"}), 400


@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"message": "Operação não permitida!", }), 403

    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} atualizado com sucesso"})
    return jsonify({"message": "Usuário não encontrado!", }), 404


# Meal
@app.route('/meal', methods=['POST'])
@login_required
def create_meal():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    is_in_diet = bool(data.get('is_in_diet'))

    if name and description and is_in_diet:
        meal = Meal(name=name, description=description, is_in_diet=is_in_diet, user_id=current_user.id)
        db.session.add(meal)
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": "Refeição cadastrada com sucesso!"}), 200
    return jsonify({"message": "Dados inválidos para registrar a refeição!"}), 400


@app.route('/meal', methods=['GET'])
@login_required
def list_meals():
    meals = Meal.query.filter_by(user_id=current_user.id).all()

    if not meals:
        return jsonify({"message": "Não existem Refeições cadastradas!"}), 404

    meal_list = []
    for meal in meals:
        meal_list.append({
            "id": meal.id,
            "name": meal.name,
            "description": meal.description,
            "date_time": meal.date_time.strftime("%d/%m/%Y %H:%M"),
            "is_in_diet": meal.is_in_diet,
        })
    return jsonify({"meals": meal_list}), 200


@app.route('/meal/<int:id_meal>', methods=['GET'])
@login_required
def get_meal(id_meal):
    meal = Meal.query.filter_by(id=id_meal, user_id=current_user.id).first()

    if not meal:
        return jsonify({"message": "Refeição não encontrada!"}), 404

    meal_obj = {
        "id": meal.id,
        "name": meal.name,
        "description": meal.description,
        "date_time": meal.date_time.strftime("%d/%m/%Y %H:%M"),
        "is_in_diet": meal.is_in_diet,
    }
    return jsonify({"meal": meal_obj}), 200


@app.route('/meal/<int:id_meal>', methods=['PUT'])
@login_required
def update_meal(id_meal):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    is_in_diet = bool(data.get('is_in_diet'))

    meal = Meal.query.filter_by(id=id_meal, user_id=current_user.id).first()
    if not meal:
        return jsonify({"message": "Refeição não encontrada!"}), 404

    if not name and not description and not is_in_diet:
        return jsonify({"message": "Operação não permitida!"}), 404

    if name:
        meal.name = name
    if description:
        meal.description = description
    if is_in_diet:
        meal.is_in_diet = is_in_diet
    db.session.commit()
    return jsonify({"message": f"Refeição {meal.name} atualizada com sucesso"})


@app.route('/meal/<int:id_meal>', methods=['DELETE'])
@login_required
def delete_meal(id_meal):
    meal = Meal.query.filter_by(id=id_meal, user_id=current_user.id).first()

    if not meal:
        return jsonify({"message": "Refeição não encontrada!"}), 404

    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": "Refeição deletada com sucesso!"}), 200


if __name__ == '__main__':
    app.run(debug=True)
