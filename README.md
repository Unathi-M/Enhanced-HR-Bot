Proof-of-Concept Bot Built in Python

📚 ENHANCED HR BOT

An intelligent HR assistant chatbot built with Flask and SQLite. The bot helps employees and HR teams manage queries, log knowledge base entries, and streamline HR operations. It uses a modular architecture with Flask Blueprints, supports API-based interaction, and provides a static UI.

The project is container-ready, can be deployed to cloud platforms, and integrates a simple database layer for persistence.

🚀 Features

HR-Focused Q&A

Modular routes for HR and user operations

Knowledge base logging & query tracking

Employee management endpoints

Flask Backend

RESTful API built with Flask

Blueprint-based modular architecture

CORS-enabled for cross-origin requests

Database Integration

SQLite for local persistence

SQLAlchemy ORM models for easy schema management

UI Layer

Static HTML (extendable to frontend frameworks later)

Ready for integration with chat UIs

Scalable & Portable

Virtual environment support

Container-ready for Docker deployment

Runs locally or on cloud free tiers

🛠️ Tech Stack

Language: Python 3.10

Libraries:

Flask → web framework

Flask-CORS → cross-origin support

SQLAlchemy → ORM/database management

Infrastructure:

SQLite → lightweight database

Docker → containerization (optional)

📂 Project Structure
enhanced_hr_bot/
├── src/
│   ├── database/
│   │   └── app.db               # SQLite database
│   ├── models/
│   │   └── user.py              # User model
│   │   └── employee.py          # Employee model
│   │   └── knowledgebase.py     # KnowledgeBase model (future-ready)
│   ├── routes/
│   │   └── user.py              # User-related API routes
│   │   └── hr_bot.py            # HR bot API routes
│   ├── static/
│   │   └── index.html           # Static UI page
│   └── main.py                  # Flask app entry point
├── requirements.txt             # Python dependencies
├── .gitignore                   # Ignored files (venv, db, secrets, etc.)
└── README.md                    # Project documentation

⚙️ Setup & Usage
1️⃣ Local Setup

Clone repo:

git clone https://github.com/Unathi-M/Enhanced-HR-Bot.git
cd Enhanced-HR-Bot


Create virtual environment:

python -m venv .venv
# Activate
.venv\Scripts\activate   # (Windows)
source .venv/bin/activate  # (Linux/Mac)


Install dependencies:

pip install -r requirements.txt

2️⃣ Run Locally

Start Flask app:

cd src
python main.py


Access API/UI at 👉 http://localhost:5000

3️⃣ Docker Deployment (optional)

Add a Dockerfile and run:

docker build -t enhanced-hr-bot .
docker run -p 5000:5000 enhanced-hr-bot

📊 Monitoring

For now:

Simple logging is enabled.

Extendable with Prometheus & Grafana in the future.

🌍 Real-World Use Cases

HR Helpdesk → Employees ask HR-related questions before escalating to HR staff

Knowledge Management → Store & retrieve HR FAQs

Employee Self-Service → Query leave policies, benefits, procedures

Training & Onboarding → Assist new employees with HR processes

🚧 Roadmap

Add authentication & role-based access

Integrate with HR platforms (e.g., Workday, SAP SuccessFactors)

Expand knowledge base with document ingestion

Add conversational UI with React/Streamlit frontend

Enable container orchestration with Docker Compose

🤝 Contributing

PRs are welcome! For major changes, please open an issue first.

📜 License

MIT License – free to use, modify, and distribute.

📬 Contact

LinkedIn: www.linkedin.com/in/unathi-manana

Email: unathimanana77@gmail.com
