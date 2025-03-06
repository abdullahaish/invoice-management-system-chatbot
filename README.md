# 📄 Invoice Management System with Chatbot Integration

## 📌 Project Overview
The **Invoice Management System** is a **FastAPI-based** application that integrates a **chatbot** for seamless invoice management. Users can insert, update, retrieve, and delete invoices, as well as generate reports using simple chatbot commands. The system utilizes a **SQLite database** for storage and provides structured API endpoints.

---

## 🚀 Features
- **Chatbot Interface** for intuitive invoice management
- **CRUD Operations**: Insert, update, retrieve, and delete invoices
- **SQLite Database** for efficient storage
- **FastAPI Endpoints** for invoice processing and reporting
- **Logging Support** for debugging and monitoring
- **Basic Reporting Functionality** to summarize invoices

---

## 🏗️ Project Structure
```
CVInsight/
│── app/
│   ├── routes/
│   │   ├── chatbot.py
│   │   ├── invoices.py
│   │   ├── reports.py
│   ├── services/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │── main.py
│── docs/
│   │── Invoice_Management_Deliverables.pdf
│── output-sample/
│   │── last_week_report.csv
│── requirements/
│   │── requirements.txt
│── README.md  # Project Documentation
```

---

## 🛠️ Setup & Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/abdullahaish/invoice-management-system-chatbot.git
cd CVInsight
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements/requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file and add:
```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=sqlite:///./invoices.db
```

---

## 🏃‍♂️ Running the API
```bash
uvicorn main:app --reload
```
API will be available at: `http://127.0.0.1:8000`

### 🔍 Interactive API Docs
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc UI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📬 Contributions & Issues
Feel free to submit issues or contribute via pull requests! 🚀
