from flask import Flask, render_template
import pymysql
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

app = Flask(__name__)
# Ensure the URI is correct with your MySQL user, password, host, port, and database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/team2'
db = SQLAlchemy(app)

# Define the People model
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # Updated to 255 characters for the name
    desc = db.Column(db.String(5000))  # New field for the description with 5000 characters

# Create the database tables and perform other startup tasks
with app.app_context():
    # Create tables
    db.create_all()
    # Accessing and printing the database URI for confirmation
    print(app.config['SQLALCHEMY_DATABASE_URI'])

@app.route('/')
def index():
    # Example of querying People data to pass to the template (optional)
    people = People.query.all()
    # return render_template('index.html', people=people)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


