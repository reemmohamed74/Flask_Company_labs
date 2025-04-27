from flask import Flask, render_template, request
app = Flask(__name__)

app.debug = True
jobs =[
    {
            "id": 1,
            "title": "Software Engineer",
            "company": "Vodafon",
            "location": "Smart Village"
            
        },
        {
            "id": 2,
            "title": "FrontEnd Engineer",
            "company": "DXC",
            "location": "Smart Village"
            
        },
        {
            "id": 3,
            "title": "BackEnd Engineer",
            "company": "PWC",
            "location": "Tagamoa"
            
        },
        {
            "id": 4,
            "title": "Mob`ile App `Developer",
            "company": "b_labs",
            "location": "Qattamia"
            
        },
]
@app.route('/jobs', methods=['GET'])
def get_jobs():
    return render_template('jobs.html', jobs=jobs)


@app.route('/jobs/<int:job_id>' ,methods=['GET'])
def job_detail(job_id):
    for job in jobs:
        if job ['id'] == job_id:
            return render_template('job_detail.html', job=job)
    return "Job not found", 404

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