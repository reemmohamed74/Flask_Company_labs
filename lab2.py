from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SECRET_KEY'] = 'reem74mohamed'
job_db = SQLAlchemy(app)
migrate=Migrate(app, job_db)


class Company(job_db.Model):
    id = job_db.Column(job_db.Integer, primary_key=True)
    name = job_db.Column(job_db.String(80), nullable=False)
    description = job_db.Column(job_db.String(200))
    employees_count = job_db.Column(job_db.Integer)
    location = job_db.Column(job_db.String(100))


    def __repr__(self):
     return f'<Company {self.name}>'




class CompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    description = StringField('Description')
    employees_count = IntegerField('Employees Count')
    location = StringField('Location')
    submit = SubmitField('Create Company')




@app.route('/create_company', methods=['GET', 'POST'])
def create_company():
    form = CompanyForm()
    if form.validate_on_submit():
        new_company = Company(
            name=form.name.data,
            description=form.description.data,
            employees_count=form.employees_count.data,
            location=form.location.data
        )
        job_db.session.add(new_company)
        job_db.session.commit()
        return 'Company created successfully!'
    return render_template('create_company.html', form=form)


@app.route('/companies')
def show_companies():
    companies = Company.query.all()
    return render_template('companies.html', companies=companies)


@app.route('/company/<string:company_name>', methods=['GET'])
def company_detail(company_name):
    company_jobs = []
    for job in jobs:
        if job['company'].lower() == company_name.lower():
            company_jobs.append(job)
    if company_jobs:
        return render_template('company_detail.html', company_name=company_name, jobs=company_jobs)
    return "Company not found", 404

if __name__ == '__main__':
    app.run(debug=True)