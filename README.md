# 🧪 Test Doc Server

A backend system for managing test documentation including test plans, test cases, coverage, defect tracking, and report generation. Designed to support QA engineers and software teams in maintaining structured testing workflows.

---

## 🚀 Features

- 📋 Manage Test Plans & Test Cases
- 🧩 Track Test Coverage
- 🐞 Record and View Defects
- 📤 Export Reports
- 🔐 Basic User Authentication

---

## 🏗️ Tech Stack

- **Backend**: Python (Django)
- **Database**: PostgreSQL (configurable)
- **API Testing**: Postman Collection

---

## 📦 Installation

### ✅ Requirements

- Python 3.8+
- pip
- Git

### ⬇️ Clone Repository
```bash
git clone https://github.com/watcoconutareyousaying/test-doc-server.git

cd test-doc-server
```

### 📥 Install Dependencies
```bash
pip install -r requirements.txt
```
### 🔧 Environment Setup
Create a .env file (if needed) and configure your database or secret keys.

### 🔌 Run the Server
```bash
python manage.py runserver
```
The server will be live at http://localhost:8000/ or http://127.0.0.1:5000/, depending on the framework used.

## 🔍 API Usage
Use the included Postman collection for testing endpoints:
``` Test Documentation.postman_collection.json ```

Import it into Postman and run predefined requests.

## 🙌 Contributing
We welcome contributions!

Fork the repository

- Create a feature branch: ``` git checkout -b my-feature ```

- Commit your changes: ```git commit -m "Add my feature"```

- Push to the branch: ```git push origin my-feature```

- Open a Pull Request

## 📄 License
This project is licensed under the MIT License.
