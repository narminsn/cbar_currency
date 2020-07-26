from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shadyshady@localhost:5432/currencyapp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
class BaseModel(db.Model):
    __abstract__=True
    # id=db.Column(db.INT, primary_key=True, autoincrement=True)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def filter(cls):
        return cls.query.filter_by().first()

    def save(self):
        db.session.add(self)
        db.session.commit()


class Currency_time(BaseModel):
    id=db.Column(db.INT,  primary_key=True, autoincrement=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

class Currency_diff(BaseModel):
    id = db.Column(db.INT, primary_key=True,  autoincrement=True)
    name = db.Column(db.String(150))
    code = db.Column(db.String(80))
    value = db.Column(db.Float)
    difference = db.Column(db.String(70))
    # time = db.Column(db.Integer, db.ForeignKey('currency_time.id'))

if __name__ == '__main__':
    manager.run()

