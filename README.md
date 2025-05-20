# 🧠 KanMind – Aufgaben- und Nutzerverwaltung

KanMind ist ein Lernprojekt, das ein Django REST Framework Backend mit einem einfachen Vanilla JavaScript Frontend kombiniert. Es ermöglicht die Verwaltung von Aufgaben, Boards und Nutzern – mit Login- und Registrierungssystem.

---

## 🔧 Tech Stack

- **Backend:** Django 5.2 + Django REST Framework + Token Auth
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Datenbank:** SQLite (lokal)
- **API-Auth:** Token-basierte Authentifizierung (`TokenAuthentication`)

---

## 🚀 Schnellstart

### 📁 Backend starten

1. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

2. **Migrationen ausführen**
   ```bash
   python manage.py migrate
   ```

3. **Superuser erstellen (optional)**
   ```bash
   python manage.py createsuperuser
   ```

4. **Entwicklungsserver starten**
   ```bash
   python manage.py runserver
   ```

→ Die API läuft unter: `http://127.0.0.1:8000/`

---

### 🌐 Frontend starten

1. Öffne das Projekt im Editor (z. B. VS Code)
2. Öffne die Datei `index.html` im Hauptverzeichnis
3. Starte sie mit **Live Server** oder einem lokalen Server

> 🔁 Das Frontend leitet je nach Login-Status automatisch zu Login oder Dashboard weiter.

---

## 📬 API-Endpunkte

### 🔐 Authentifizierung

- `POST /api/register/` – Benutzer registrieren
- `POST /api/login/` – Benutzer einloggen (Token wird zurückgegeben)

### 👤 Nutzer

- `GET /api/email-check/?email=...` – prüft, ob ein Benutzer mit der E-Mail existiert

### 🗂️ Boards & Tasks (nur mit Token)

- `GET /api/boards/` – alle Boards, bei denen man Mitglied ist
- `GET /api/tasks/assigned-to-me/` – alle zugewiesenen Tasks
- `GET /api/tasks/reviewing/` – Tasks, bei denen man Reviewer ist

---

## 💾 Lokale Speicherung

Das Frontend nutzt `localStorage` zur Speicherung von:

- `auth-token`
- `auth-user-id`
- `auth-email`
- `auth-fullname`

> Hinweis: Probleme beim Login entstehen oft durch veraltete Tokens im localStorage → Konsole: `localStorage.clear()`.

---

## 🧪 Testen mit Postman

### Registrierung:
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

## 👥 Entwickler

Wenn du Änderungen am Backend machst:

- Achte darauf, die Serializers, Views und URL-Router synchron zu halten
- Das Frontend ist bewusst einfach gehalten – Anpassungen (Login, API-Calls) erfolgen in `api.js`, `login.js`, etc.

---

## 📝 Lizenz

Dieses Projekt ist ein internes Lernprojekt für die Developer Akademie. Es ist nicht für kommerzielle Nutzung oder Weitergabe bestimmt.

---