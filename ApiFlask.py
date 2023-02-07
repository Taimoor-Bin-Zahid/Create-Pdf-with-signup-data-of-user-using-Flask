from flask import Flask, render_template
from flask import request
import pdfkit
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sqlalchemy'

db = SQLAlchemy(app)
class Pdf(db.Model):


    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    age = db.Column(db.Integer)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name


@app.route('/')
def index():
    return render_template('FormApi.html')

@app.route('/', methods=['POST'])
def getvalue():
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    password = request.form['password']
    entry = Pdf(name=name, email=email, age=age, password=password)
    db.session.add(entry)
    db.session.commit()
    newHtml = render_template("PassApi.html",  n=name, e=email, a=age, p=password)
    print(newHtml)
    file = open("newHtml.html", 'w')
    file.write(newHtml)
    file.close()
    config = pdfkit.configuration(wkhtmltopdf = path_to_wkhtmltopdf)
    pdfkit.from_file("newHtml.html", output_path = 'sample.pdf', configuration = config)
    return render_template('PassApi.html', n=name, e=email, a=age, p=password)



if __name__ == '__main__':
    app.run(debug=True)