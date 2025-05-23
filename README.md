# 🧠 KanMind – Task and User Management

KanMind is a learning project that combines a Django REST Framework backend with a simple Vanilla JavaScript frontend. It enables the management of tasks, boards, and users – with login and registration functionality.

---

## 🔧 Tech Stack

- **Backend:** Django 5.2 + Django REST Framework + Token Auth
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Database:** SQLite (local)
- **API Auth:** Token-based authentication (`TokenAuthentication`)

---

## 🚀 Quickstart

### 📁 Backend Setup

1. **Create and activate a virtual environment**  
   *(recommended for dependency isolation)*

   **On Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **On macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

→ The API is available at: `http://127.0.0.1:8000/`

---

### 🌐 Frontend Setup

1. Open the project in your editor (e.g. VS Code)
2. Open `index.html` from the project root
3. Launch it using **Live Server** or any local server

> 🔁 The frontend redirects automatically to login or dashboard based on the login state.

---

## 📬 API Endpoints

### 🔐 Authentication

- `POST /api/register/` – Register a user
- `POST /api/login/` – Log in a user (returns token)

### 👤 Users

- `GET /api/email-check/?email=...` – Check if a user exists by email

### 🗂️ Boards & Tasks (Token required)

- `GET /api/boards/` – All boards the user is a member of
- `GET /api/tasks/assigned-to-me/` – All tasks assigned to the user
- `GET /api/tasks/reviewing/` – Tasks where the user is a reviewer

---

## 💾 Local Storage

The frontend uses `localStorage` to store:

- `auth-token`
- `auth-user-id`
- `auth-email`
- `auth-fullname`

> Note: Login issues are often caused by outdated tokens in localStorage → fix via browser console: `localStorage.clear()`.

---

## 🧪 Testing with Postman

### Registration:
```json
POST /api/register/
{
  "email": "test@example.com",
  "fullname": "Max Mustermann",
  "password": "Testpass123",
  "repeated_password": "Testpass123"
}
```

### Login:
```json
POST /api/login/
{
  "email": "test@example.com",
  "password": "Testpass123"
}
```

---

## 👥 Developer Notes

If you're making changes to the backend:

- Keep serializers, views, and URL routing in sync
- The frontend is deliberately minimal – changes (e.g. login, API calls) are handled in `api.js`, `login.js`, etc.

---

## 📝 License

This project is an internal learning project for the Developer Akademie. It is not intended for commercial use or distribution.

---
