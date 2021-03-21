from datetime import datetime

import flask
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dpd_test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    trust = db.Column(db.Float)
    initiative = db.Column(db.Float)
    competence = db.Column(db.Float)
    autonomy = db.Column(db.Float)
    identity = db.Column(db.Float)

    def __repr__(self):
        return self.id


class Answer(db.Model):
    stage_of_development = db.Column(db.String(30))
    result_1 = db.Column(db.Text, primary_key=True)
    result_2 = db.Column(db.Text, primary_key=True)
    result_3 = db.Column(db.Text, primary_key=True)


@app.route('/')
@app.route('/api/resultSave.php', methods=['GET', 'POST'])
def save_result():
    if request.method == "POST":
        user = User(
            name=flask.request.json['name'],
            surname=flask.request.json['surname'],
            email=flask.request.json['email'],
            trust=float(flask.request.json['result']['trust']),
            initiative=float(flask.request.json['result']['initiative']),
            competence=float(flask.request.json['result']['competence']),
            autonomy=float(flask.request.json['result']['autonomy']),
            identity=float(flask.request.json['result']['identity'])
        )
        try:
            db.session.add(user)
            db.session.commit()
            print('ok')
            return redirect('/')
        except Warning:
            return "Ops"
    else:
        output = dict()
        output_web = list()
        persons_web = User.query.all()
        answer_web = Answer.query.all()
        for person in persons_web:
            if person.trust < 3.5:
                output['trust'] = answer_web[0].result_1
            elif 3.5 <= person.trust <= 4.5:
                output['trust'] = answer_web[0].result_2
            elif person.trust > 4.5:
                output['trust'] = answer_web[0].result_3

            if person.initiative < 3.5:
                output['initiative'] = answer_web[1].result_1
            elif 3.5 <= person.initiative <= 4.5:
                output['initiative'] = answer_web[1].result_2
            elif person.initiative > 4.5:
                output['initiative'] = answer_web[1].result_3

            if person.competence < 3.5:
                output['competence'] = answer_web[2].result_1
            elif 3.5 <= person.competence <= 4.5:
                output['competence'] = answer_web[2].result_2
            elif person.competence > 4.5:
                output['competence'] = answer_web[2].result_3

            if person.autonomy < 3.5:
                output['autonomy'] = answer_web[3].result_1
            elif 3.5 <= person.autonomy <= 4.5:
                output['autonomy'] = answer_web[3].result_2
            elif person.autonomy > 4.5:
                output['autonomy'] = answer_web[3].result_3

            if person.identity < 3.5:
                output['identity'] = answer_web[4].result_1
            elif 3.5 <= person.identity <= 4.5:
                output['identity'] = answer_web[4].result_2
            elif person.identity > 4.5:
                output['identity'] = answer_web[4].result_3

            output_web.append(output)

        return render_template('index.html', output_web=output_web)


app.run()
