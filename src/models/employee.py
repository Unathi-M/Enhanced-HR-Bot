from src.models.user import db
from datetime import datetime


class Employee(db.Model):
    employee_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    hire_date = db.Column(db.String(20), nullable=False)
    manager = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    annual_leave = db.Column(db.Integer, default=20)
    sick_leave = db.Column(db.Integer, default=10)
    personal_leave = db.Column(db.Integer, default=5)
    profile_image = db.Column(db.String(200), default='')
    phone = db.Column(db.String(20), default='')
    emergency_contact = db.Column(db.String(100), default='')

    def __repr__(self):
        return f'<Employee {self.employee_id}: {self.name}>'

    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'name': self.name,
            'department': self.department,
            'role': self.role,
            'hire_date': self.hire_date,
            'manager': self.manager,
            'email': self.email,
            'salary': self.salary,
            'leave_balance': {
                'annual': self.annual_leave,
                'sick': self.sick_leave,
                'personal': self.personal_leave
            },
            'profile_image': self.profile_image,
            'phone': self.phone,
            'emergency_contact': self.emergency_contact
        }


class QueryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), db.ForeignKey('employee.employee_id'), nullable=False)
    query = db.Column(db.Text, nullable=False)
    query_type = db.Column(db.String(50), nullable=False)
    intent = db.Column(db.String(50), nullable=False)
    controversy_score = db.Column(db.Float, default=0.0)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    escalated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<QueryLog {self.id}: {self.employee_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'query': self.query,
            'query_type': self.query_type,
            'intent': self.intent,
            'controversy_score': self.controversy_score,
            'response': self.response[:200] + '...' if len(self.response) > 200 else self.response,
            'timestamp': self.timestamp.isoformat(),
            'escalated': self.escalated
        }


class KnowledgeBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.Text, nullable=False)  # JSON string of keywords
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<KnowledgeBase {self.id}: {self.category}>'

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'question': self.question,
            'answer': self.answer,
            'keywords': self.keywords,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }