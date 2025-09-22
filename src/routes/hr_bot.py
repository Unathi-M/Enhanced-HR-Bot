from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.models.employee import Employee, QueryLog, KnowledgeBase, db
from datetime import datetime

# Try NLTK but make it completely optional
try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
    nltk.download('vader_lexicon', quiet=True)
    HAS_NLTK = True
    print("✅ NLTK loaded successfully")
except:
    HAS_NLTK = False
    print("⚠️ NLTK not available - using basic processing")

hr_bot_bp = Blueprint('hr_bot', __name__)

class EnhancedControversialHandler:
    def __init__(self):
        self.controversial_keywords = [
            "harassment", "discriminat", "racist", "sexist", "bias", "unfair",
            "bullying", "hostile", "toxic", "retaliation", "lawsuit", "sue",
            "pay gap", "underpaid", "violation", "illegal", "abuse", "misconduct"
        ]
        
        self.escalation_keywords = [
            "threat", "violence", "harm", "attack", "kill", "murder", "suicide",
            "bomb", "weapon", "dangerous", "revenge", "assault", "hurt"
        ]
        
        # Try to use NLTK sentiment analyzer
        if HAS_NLTK:
            try:
                self.sentiment_analyzer = SentimentIntensityAnalyzer()
            except:
                self.sentiment_analyzer = None
        else:
            self.sentiment_analyzer = None
    
    def analyze_query(self, query):
        try:
            query_lower = query.lower()
            
            # Check for escalation
            for keyword in self.escalation_keywords:
                if keyword in query_lower:
                    return "escalation_required", 1.0
            
            # Check for controversial content
            controversy_score = 0
            for keyword in self.controversial_keywords:
                if keyword in query_lower:
                    controversy_score += 1
            
            # Get sentiment if available
            sentiment_score = 0
            if self.sentiment_analyzer:
                try:
                    sentiment = self.sentiment_analyzer.polarity_scores(query)
                    sentiment_score = abs(sentiment.get('neg', 0))
                except:
                    sentiment_score = 0
            
            # Determine classification
            total_score = controversy_score * 0.3 + sentiment_score
            
            if total_score > 0.7:
                return "escalation_required", min(total_score, 1.0)
            elif total_score > 0.3:
                return "controversial", min(total_score, 1.0)
            else:
                return "safe", total_score
                
        except Exception as e:
            print(f"Analysis error: {e}")
            return "safe", 0.0

class EnhancedIntentExtractor:
    def __init__(self):
        self.intents = {
            "leave_inquiry": ["leave", "vacation", "time off", "pto", "holiday", "absence", "days off"],
            "salary_inquiry": ["salary", "pay", "compensation", "wage", "income", "paycheck", "bonus"],
            "policy_inquiry": ["policy", "rule", "regulation", "procedure", "guideline", "handbook"],
            "benefits_inquiry": ["benefits", "insurance", "health", "dental", "401k", "retirement", "medical"],
            "contact_inquiry": ["contact", "phone", "email", "manager", "hr", "reach", "call"],
            "complaint_inquiry": ["complain", "report", "issue", "problem", "concern", "feedback"],
            "training_inquiry": ["training", "course", "learning", "development", "skill", "certification"],
            "performance_inquiry": ["performance", "review", "evaluation", "feedback", "rating", "goals"],
            "schedule_inquiry": ["schedule", "hours", "shift", "overtime", "flexible", "remote"]
        }
    
    def extract_intent(self, query):
        try:
            query_lower = query.lower()
            
            # Score each intent
            intent_scores = {}
            for intent, keywords in self.intents.items():
                score = 0
                for keyword in keywords:
                    if keyword in query_lower:
                        score += 1
                intent_scores[intent] = score
            
            # Return the intent with highest score
            if intent_scores:
                best_intent = max(intent_scores, key=intent_scores.get)
                if intent_scores[best_intent] > 0:
                    return best_intent
            
            return "general_info"
        except Exception as e:
            print(f"Intent extraction error: {e}")
            return "general_info"

class EnhancedResponseGenerator:
    def __init__(self):
        self.response_templates = {
            "controversial": """
<b>Sensitive Matter Detected</b>

I understand you have a concern that requires special attention. For sensitive matters like this, I recommend speaking directly with HR.

<b>Contact Information:</b>

• HR Email: hr@company.com

• HR Phone: (555) 123-4567

• Anonymous Hotline: (555) 999-TIPS

• Online Portal: ethics.company.com

Your query has been logged for HR review and you can expect a follow-up within 24 hours.
            """.strip(),
            
            "escalation": """
<b>URGENT - Immediate HR Attention Required</b>

Your query requires immediate HR attention and has been escalated to our emergency response team.

<b>Contact HR IMMEDIATELY:</b>

• Emergency HR: (555) 999-8888

• HR Director: (555) 123-4567

• Security (if needed): ext. 911

• Crisis Support: (555) 555-HELP

A member of the HR team will contact you within 2 hours. If this is an emergency, please call 911.
            """.strip()
        }
    
    def generate_response(self, employee, intent, query, knowledge_base_results=None):
        try:
            # Time-based greeting
            hour = datetime.now().hour
            greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"
            
            # Check knowledge base first
            if knowledge_base_results:
                return f"""
{greeting} {employee.name}! 👋


<b>Based on our knowledge base, here's what I found:</b>

{knowledge_base_results}


Is there anything else you'd like to know?
                """.strip()
            
            if intent == "leave_inquiry":
                total = employee.annual_leave + employee.sick_leave + employee.personal_leave
                return f"""
{greeting} {employee.name}! 👋


<b>Your Leave Balance:</b>

• 🏖️ Annual Leave: {employee.annual_leave} days

• 🏥 Sick Leave: {employee.sick_leave} days

• 👤 Personal Leave: {employee.personal_leave} days

• 📊 Total Available: {total} days


<b>To Request Leave:</b>

1. Contact your manager: {employee.manager}

2. Submit request through HR portal: portal.company.com

3. Allow 2 weeks notice for annual leave


<b>Leave Policies:</b>

• Annual leave: Use within calendar year

• Sick leave: Doctor's note required for 3+ consecutive days

• Personal leave: Manager approval required


Need help with anything else?
                """.strip()
            
            elif intent == "salary_inquiry":
                return f"""
{greeting} {employee.name}!


<b>Salary & Compensation Information</b>

For detailed salary information, please:

• Visit the employee portal: portal.company.com

• Contact HR: (555) 123-4567

• Email: payroll@company.com


<b>General Information:</b>

• Pay schedule: Bi-weekly (every other Friday)

• Direct deposit: Available

• Pay stubs: Available online

• Tax documents: W-2 available in January

Salary details require secure verification for privacy protection.
                """.strip()
            
            elif intent == "policy_inquiry":
                return f"""
{greeting} {employee.name}!


<b>Company Policies & Procedures</b>

<b>Key Policies:</b>

• <b>Remote Work:</b> Up to 3 days/week with manager approval

• <b>Leave Policy:</b> 20 annual days, submit 2 weeks advance notice

• <b>Code of Conduct:</b> Zero tolerance for harassment or discrimination

• <b>Performance Reviews:</b> Annual in December, mid-year check-in June

• <b>Dress Code:</b> Business casual, casual Fridays

• <b>Working Hours:</b> Core hours 9 AM - 3 PM, flexible start/end


<b>For detailed policies:</b>

• Employee handbook: portal.company.com/handbook

• HR: (555) 123-4567

• Policy updates: Check company newsletter
                """.strip()
            
            elif intent == "benefits_inquiry":
                return f"""
{greeting} {employee.name}!


<b>Your Benefits Package</b>

<b>Health & Wellness:</b>

• 🏥 Health Insurance: PPO/HMO options, company pays 80%

• 🦷 Dental & Vision: Full coverage for preventive care

• 🧘 Wellness Program: Gym membership discount, mental health support


<b>Financial Benefits:</b>

• 💰 401(k): 4% company match, immediate vesting

• 💼 Life Insurance: 2x annual salary

• 🏠 Disability: Short & long-term coverage


<b>Time Off:</b>

• 🏖️ Paid Time Off: 20 days annually

• 🎄 Holidays: 12 paid holidays

• 👶 Parental Leave: 12 weeks paid


<b>Contact:</b>

benefits@company.com | (555) 123-BENEFITS
                """.strip()
            
            elif intent == "contact_inquiry":
                return f"""
{greeting} {employee.name}!


<b>Your Key Contacts</b>

<b>Direct Contacts:</b>

• <b>Manager:</b> {employee.manager}

• <b>Department:</b> {employee.department} team

• <b>HR Representative:</b> Sarah Wilson (ext. 1234)


<b>General Contacts:</b>

• <b>HR:</b> hr@company.com | (555) 123-4567

• <b>IT Support:</b> it@company.com | (555) 123-TECH

• <b>Facilities:</b> facilities@company.com | (555) 123-BLDG

• <b>Emergency HR:</b> (555) 999-8888

• <b>Ethics Hotline:</b> (555) 999-TIPS


<b>Office Location:</b>

Building A, 2nd Floor


<b>Reception:</b>

(555) 123-0000
                """.strip()
            
            elif intent == "complaint_inquiry":
                return f"""
{greeting} {employee.name}!


<b>How to Report Issues & Concerns</b>

<b>Step 1: Direct Manager</b>

• Contact: {employee.manager}

• Best for: Team issues, work-related concerns


<b>Step 2: HR Department</b>

• Email: hr@company.com

• Phone: (555) 123-4567

• Best for: Policy violations, workplace issues


<b>Step 3: Anonymous Reporting</b>

• Ethics Hotline: (555) 999-TIPS

• Online Portal: ethics.company.com

• Best for: Sensitive matters, harassment


<b>Your Rights:</b>

• ✅ Confidentiality protection

• ✅ No retaliation policy

• ✅ Regular status updates

• ✅ Fair investigation process

All reports are taken seriously and investigated promptly.
                """.strip()
            
            elif intent == "training_inquiry":
                return f"""
{greeting} {employee.name}!


<b>Training & Development Opportunities</b>

<b>Available Training:</b>

• 💻 Technical Skills: LinkedIn Learning, Coursera

• 👥 Leadership Development: Monthly workshops

• 🎯 Professional Certifications: Company-sponsored

• 🗣️ Communication Skills: Quarterly sessions


<b>How to Access:</b>

• Training Portal: learning.company.com

• Request Form: Submit to HR

• Manager Approval: Required for external training


<b>Budget:</b>

$2,000 annual training allowance per employee


<b>Upcoming Sessions:</b>

• Project Management (Next week)

• Diversity & Inclusion (Monthly)

• Safety Training (Quarterly)


<b>Contact:</b>

training@company.com
                """.strip()
            
            elif intent == "performance_inquiry":
                return f"""
{greeting} {employee.name}!


<b>Performance & Career Development</b>

<b>Review Schedule:</b>

• 📅 Annual Review: December

• 🎯 Mid-Year Check-in: June

• 💬 Monthly 1-on-1s: With {employee.manager}


<b>Performance Goals:</b>

• Set annually with manager

• Tracked quarterly

• Aligned with company objectives


<b>Career Development:</b>

• Individual Development Plan (IDP)

• Mentorship Program available

• Internal job postings priority


<b>Resources:</b>

• Performance Portal: performance.company.com

• Career Planning Guide: Available in handbook

• HR Career Counseling: Schedule with HR


<b>Next Review:</b>

Check with {employee.manager}
                """.strip()
            
            elif intent == "schedule_inquiry":
                return f"""
{greeting} {employee.name}!


<b>Work Schedule & Flexibility</b>

<b>Standard Schedule:</b>

• Core Hours: 9:00 AM - 3:00 PM

• Flexible Start: 7:00 AM - 10:00 AM

• Flexible End: 3:00 PM - 6:00 PM

• Lunch Break: 1 hour (flexible timing)


<b>Remote Work:</b>

• Up to 3 days per week

• Manager approval required

• Home office setup support available


<b>Overtime:</b>

• Pre-approval required

• Time-and-a-half for non-exempt employees

• Comp time available for exempt employees


<b>Time Tracking:</b>

• Use company time system

• Submit weekly timesheets

• Manager approval required


<b>Contact:</b>

{employee.manager} for schedule changes
                """.strip()
            
            # Default response
            return f"""
{greeting} {employee.name}! 👋


I'm your enhanced HR Assistant! I can help with:

<b>Leave & Time Off</b> - Balances, requests, policies

<b>Benefits</b> - Health, dental, 401k, life insurance  

<b>Policies</b> - Company rules, procedures, handbook

<b>Contacts</b> - Find the right person or department

<b>Report Issues</b> - Complaints, concerns, feedback

<b>Training</b> - Professional development opportunities

<b>Performance</b> - Reviews, goals, career planning

<b>Schedule</b> - Work hours, remote work, flexibility


What would you like to know about? I'm here to help make your work life easier!
            """.strip()
            
        except Exception as e:
            print(f"Response generation error: {e}")
            return f"Hi {employee.name}! I'm having trouble generating a detailed response right now, but I'm here to help with HR questions. Please contact HR at (555) 123-4567 if you need immediate assistance."

# Initialize handlers
controversial_handler = EnhancedControversialHandler()
intent_extractor = EnhancedIntentExtractor()
response_generator = EnhancedResponseGenerator()

@hr_bot_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    try:
        # Parse JSON data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        employee_id = data.get('employee_id')
        query = data.get('query')
        
        if not employee_id or not query:
            return jsonify({"error": "Missing employee_id or query"}), 400
        
        print(f"Received chat request: {employee_id} - {query}")
        
        # Get employee
        employee = Employee.query.filter_by(employee_id=employee_id).first_or_404()
        
        # Analyze query
        query_type, controversy_score = controversial_handler.analyze_query(query)
        intent = intent_extractor.extract_intent(query)
        
        print(f"Query type: {query_type}, Intent: {intent}, Score: {controversy_score:.2f}")
        
        # Handle based on query type
        if query_type == "escalation_required":
            response = response_generator.response_templates["escalation"]
            escalated = True
        elif query_type == "controversial":
            response = response_generator.response_templates["controversial"]
            escalated = False
        else:  # Safe query
            response = response_generator.generate_response(employee, intent, query)
            escalated = False
        
        # Log the query
        log_entry = QueryLog(
            employee_id=employee_id,
            query=query,
            query_type=query_type,
            intent=intent,
            controversy_score=controversy_score,
            response=response[:500],  # Truncate for storage
            escalated=escalated
        )
        db.session.add(log_entry)
        db.session.commit()
        
        return jsonify({
            "response": response,
            "query_type": query_type,
            "controversy_score": controversy_score,
            "intent": intent,
            "escalated": escalated,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()  # Rollback on error to avoid partial commits
        return jsonify({
            "response": f"I encountered an error processing your request. Please try again or contact HR directly at (555) 123-4567.",
            "query_type": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@hr_bot_bp.route('/employees', methods=['GET'])
@cross_origin()
def get_employees():
    try:
        employees = Employee.query.all()
        return jsonify([emp.to_dict() for emp in employees])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@hr_bot_bp.route('/employees/<employee_id>', methods=['GET'])
@cross_origin()
def get_employee(employee_id):
    try:
        employee = Employee.query.filter_by(employee_id=employee_id).first()
        if not employee:
            return jsonify({"error": "Employee not found"}), 404
        return jsonify(employee.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@hr_bot_bp.route('/logs', methods=['GET'])
@cross_origin()
def get_logs():
    try:
        logs = QueryLog.query.order_by(QueryLog.timestamp.desc()).limit(100).all()
        return jsonify([log.to_dict() for log in logs])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@hr_bot_bp.route('/logs/<employee_id>', methods=['GET'])
@cross_origin()
def get_employee_logs(employee_id):
    try:
        logs = QueryLog.query.filter_by(employee_id=employee_id).order_by(QueryLog.timestamp.desc()).limit(50).all()
        return jsonify([log.to_dict() for log in logs])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@hr_bot_bp.route('/analytics', methods=['GET'])
@cross_origin()
def get_analytics():
    try:
        total_queries = QueryLog.query.count()
        escalated_queries = QueryLog.query.filter_by(escalated=True).count()
        controversial_queries = QueryLog.query.filter_by(query_type='controversial').count()
        
        # Intent distribution
        intent_counts = db.session.query(QueryLog.intent, db.func.count(QueryLog.intent)).group_by(QueryLog.intent).all()
        
        return jsonify({
            "total_queries": total_queries,
            "escalated_queries": escalated_queries,
            "controversial_queries": controversial_queries,
            "intent_distribution": dict(intent_counts),
            "safety_rate": ((total_queries - escalated_queries - controversial_queries) / max(total_queries, 1)) * 100
        })
    
    except Exception as e:
        print(f"Analytics error: {e}")
        return jsonify({"error": "Failed to generate analytics", "details": str(e)}), 500