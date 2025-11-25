# 📚 Online Library Management System (Django)

![Repository screenshot](/mnt/data/60a9be1d-f6fc-4057-9752-3fe78aaee5dd.png)

A professional, full‑stack web application built with **Django** and **SQLite** to manage library operations (books, members, and issue/return records). The app demonstrates authentication, role-based access, CRUD operations, search, pagination, and an admin interface — ideal for a university SIP / portfolio.

---

## 🚀 Live demo

*(If deployed, add the public URL here)*

---

## ✨ Key Features

* **Authentication & Authorization** — secure login/logout; staff-only actions protected.
* **Book & Member Management (CRUD)** — add, view, edit, delete records with validation.
* **Issue & Return Module** — issue books to members, return flow, and automatic availability updates.
* **Dashboard** — quick statistics for total books, available books, members, and currently issued books.
* **Search & Pagination** — search books by title/author/ISBN and paginated lists for large datasets.
* **Admin Panel** — manage models via Django admin.
* **Responsive UI** — built with Bootstrap for clean, mobile-friendly pages.
* **Version Control** — Git & GitHub for history and collaboration.

---

## 🧰 Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, Bootstrap
* **Database:** SQLite
* **Other:** Git, GitHub, Pillow (optional for cover images)

---

## 📁 Project Structure (simplified)

```
library_management/
├── library_management/        # project settings & urls
├── libraryapp/                # app: models, views, templates, static
├── db.sqlite3                 # local database (not in repo if ignored)
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup (local development)

1. **Clone the repository**

```bash
git clone https://github.com/AvishiShrivastava/Library-Management-System-Django.git
cd Library-Management-System-Django
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
# Windows (PowerShell)
venv\Scripts\activate
# macOS / Linux
# source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply migrations**

```bash
python manage.py migrate
```

5. **Create a superuser**

```bash
python manage.py createsuperuser
```

6. **Run the development server**

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

---

## 🔧 Important URLs

* `/` — Home / Dashboard
* `/login/` — Login
* `/logout/` — Logout
* `/view-books/` — Browse books (search + pagination)
* `/add-book/` — Add a new book
* `/view-members/` — Members list
* `/add-member/` — Add member
* `/issue-book/` — Issue a book
* `/view-issued/` — Issued records
* `/admin/` — Django admin panel

---

## ✅ Deployment (brief)

Suggested: **Render** or **PythonAnywhere** for simple Django deployments. Create a `Procfile` containing:

```
web: gunicorn library_management.wsgi
```

Push to GitHub, connect the repo to the hosting provider, configure environment variables and static/media handling, then deploy. I can provide a step‑by‑step Render guide when you're ready.

---

## 🧾 Notes

* `db.sqlite3` and `media/` are recommended to be in `.gitignore` (not pushed). If DB is in the repo temporarily for demo, remove it before production.
* To enable book cover images, install Pillow and configure `MEDIA_ROOT`/`MEDIA_URL`.

---

## 📌 Contribution / Contact

If you’d like enhancements, features, or help deploying this project, open an issue or contact:

**Avishi Shrivastava** — GitHub: `@AvishiShrivastava`

---

*Prepared for portfolio / SIP demonstration. Feel free to copy this README into your repository root and push.*
