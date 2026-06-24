# 📄 AI Document Summarizer

An AI-powered web application that enables users to upload PDF or text documents, generate concise summaries, and interact with their documents through natural language conversations. Built with **FastAPI**, **Google Gemini**, and **PostgreSQL**, the application provides context-aware answers by identifying the most relevant information from uploaded documents.

---

## ✨ Features

* 🔐 User Authentication
* 📄 Upload PDF & TXT Documents
* 🤖 AI-Powered Document Summarization
* 💬 Context-Aware Document Q&A
* 🔍 Intelligent Section-Specific Information Retrieval
* 🧠 Interactive Chat Interface
* 🗄️ PostgreSQL Database Integration
* ⚡ FastAPI Backend with Jinja2 Templates
* 🐳 Docker Support

---

## 🛠️ Tech Stack

**Backend**

* FastAPI
* SQLAlchemy
* PostgreSQL
* Uvicorn

**Frontend**

* HTML
* CSS
* Jinja2

**AI**

* Google Gemini 2.5 Flash

**Document Processing**

* PyPDF

**Containerization**

* Docker
* Docker Compose

---

## 📁 Project Structure

```text
AI-Document-Summarizer/
│
├── templates/
        ├── dashboard.html
        ├── login.html
        ├── register.html
├── main.py
├── models.py
├── database.py
├── init_db.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/AI-Document-Summarizer.git
cd AI-Document-Summarizer
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure PostgreSQL and create a database named:

```text
summary_app
```

Initialize the database:

```bash
python init_db.py
```

Run the application:

```bash
uvicorn main:app --reload
```

## 🐳 Running with Docker

```bash
docker compose up --build
```

---

## 🔮 Future Enhancements

* Password hashing (bcrypt)
* JWT Authentication
* Multi-document support
* Persistent chat history
* OCR support for scanned PDFs
* Semantic search with vector embeddings
* Streaming AI responses
* Dark mode
* File upload history

---
