from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foods.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for storing food names and timers
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False)  # in minutes

    def __repr__(self):
        return f"<Food {self.name}>"

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manage_foods', methods=['GET', 'POST'])
def manage_foods():
    if request.method == 'POST':
        food_name = request.form['food_name']
        cooking_time = int(request.form['cooking_time'])
        
        new_food = Food(name=food_name, cooking_time=cooking_time)
        db.session.add(new_food)
        db.session.commit()
        return redirect(url_for('manage_foods'))
    
    foods = Food.query.all()
    return render_template('manage_foods.html', foods=foods)

@app.route('/delete_food/<int:id>')
def delete_food(id):
    food = Food.query.get(id)
    db.session.delete(food)
    db.session.commit()
    return redirect(url_for('manage_foods'))

@app.route('/start_timer/<int:id>')
def start_timer(id):
    food = Food.query.get(id)
    return render_template('timer_page.html', food=food)

if __name__ == '__main__':
    app.run(debug=True)
