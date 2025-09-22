import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.employee import Employee, QueryLog, KnowledgeBase
from src.routes.user import user_bp
from src.routes.hr_bot import hr_bot_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(hr_bot_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def init_sample_data():
    """Initialize sample employee data if database is empty"""
    if Employee.query.count() == 0:
        employees = [
            Employee(
                employee_id="EMP001",
                name="John Doe",
                department="Engineering",
                role="Senior Developer",
                hire_date="2020-01-15",
                manager="Jane Smith",
                email="john.doe@company.com",
                salary=75000,
                annual_leave=15,
                sick_leave=8,
                personal_leave=3,
                phone="(555) 123-4567",
                emergency_contact="Jane Doe - (555) 987-6543"
            ),
            Employee(
                employee_id="EMP002",
                name="Sarah Wilson",
                department="HR",
                role="HR Manager",
                hire_date="2019-03-10",
                manager="Mike Johnson",
                email="sarah.wilson@company.com",
                salary=65000,
                annual_leave=20,
                sick_leave=10,
                personal_leave=5,
                phone="(555) 234-5678",
                emergency_contact="Tom Wilson - (555) 876-5432"
            ),
            Employee(
                employee_id="EMP003",
                name="Mike Chen",
                department="Sales",
                role="Sales Representative",
                hire_date="2021-06-01",
                manager="Lisa Brown",
                email="mike.chen@company.com",
                salary=55000,
                annual_leave=12,
                sick_leave=6,
                personal_leave=2,
                phone="(555) 345-6789",
                emergency_contact="Amy Chen - (555) 765-4321"
            ),
            Employee(
                employee_id="EMP004",
                name="Emma Davis",
                department="Marketing",
                role="Marketing Specialist",
                hire_date="2020-09-20",
                manager="Tom Wilson",
                email="emma.davis@company.com",
                salary=58000,
                annual_leave=18,
                sick_leave=9,
                personal_leave=4,
                phone="(555) 456-7890",
                emergency_contact="Robert Davis - (555) 654-3210"
            ),
            Employee(
                employee_id="EMP005",
                name="Alex Rodriguez",
                department="Finance",
                role="Financial Analyst",
                hire_date="2022-03-01",
                manager="Carol Smith",
                email="alex.rodriguez@company.com",
                salary=60000,
                annual_leave=20,
                sick_leave=10,
                personal_leave=5,
                phone="(555) 567-8901",
                emergency_contact="Maria Rodriguez - (555) 543-2109"
            )
        ]
        
        for emp in employees:
            db.session.add(emp)
        
        db.session.commit()
        print("✅ Sample employee data initialized")

with app.app_context():
    db.create_all()
    init_sample_data()

@app.route('/', defaults={'path': ''}) 
@app.route('/<path:path>') 
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)