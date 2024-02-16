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

    def __repr__(self):
        selfAll = (self.id, self.name, self.desc)
        return '<people %r>' % str(selfAll)

class Peopleinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))  # foreign key referencing People.id
    position = db.Column(db.String(255))
    image = db.Column(db.String(255))
    
    def __repr__(self):
        selfAll = (self.people_id, self.postion, self.image)
        return '<Peopleinfo %r>' % str(selfAll)
# Create the database tables and perform other startup tasks

class Person:
    def __init__(self, id, name, desc, position, image):
        self.id = id
        self.name = name
        self.desc = desc
        self.position = position
        self.image = image


def getListPeople():
    listOfPeople = []
    people = People.query.all()
    people_info = Peopleinfo.query.all()
    print(len(people_info), "hi")
    
    for person_data in people:
        # Find corresponding person_info data for the current person
        person_info = None
        for info in people_info:
            if info.people_id == person_data.id:
                person_info = info
                break
        
        if person_info:
            person = Person(
                id=person_data.id,
                name=person_data.name,
                desc=person_data.desc,
                position=person_info.position,
                image=person_info.image
            )
            listOfPeople.append(person)
            
    
    return listOfPeople


with app.app_context():
    # Create tables
    db.create_all()
    # Accessing and printing the database URI for confirmation
    print(app.config['SQLALCHEMY_DATABASE_URI'])

@app.route('/')
def index():
    # Example of querying People data to pass to the template (optional)
    people = getListPeople()
 
    # return render_template('index.html', people=people)
    return render_template('index.html', people = people)

if __name__ == '__main__':
    app.run(debug=True)


