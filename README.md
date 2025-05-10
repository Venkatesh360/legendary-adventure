# 📚 Library Management System API

A simple library management system built using **FastAPI** and **SQLAlchemy**, featuring JWT-based authentication, user roles (admin/user), book inventory management, and borrowing system.

---

## 🚀 Features

- User Signup & Login with JWT Authentication
- Admin-only routes for:
  - Adding new books
  - Granting admin access
  - Lending books to users
- Users can:
  - View all available books
  - View their borrowed books
- Passwords hashed securely using bcrypt

---

## 🛠 Tech Stack

- **FastAPI**
- **SQLAlchemy**
- **SQLite** (or any SQL DB via SQLAlchemy)
- **bcrypt** for password hashing
- **JWT (PyJWT)** for secure token-based authentication
- **Pydantic** for request/response validation

---

## 📂 Project Structure

```
.
├── app/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── utils/
│   └── database/
├── requirements.txt
└── README.md
```

---

## 🧪 Installation & Running

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/library-api.git
cd library-api
```

### 2. Create & activate a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file in the root with:

```env
JWT_SECRET=your_jwt_secret
ALOGRITHM=HS256
KEY=admin_access_key
TOKEN_URL= api/auth/login
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

---

## 🔐 Authentication

Use `api/auth/signup` and `api/auth/login` to generate a JWT token.

Include the token in the Authorization header for protected routes:

```http
Authorization: Bearer <your_token_here>
```

---

## 📫 API Endpoints

### User Routes

- `POST api/auth/signup` – Create new user  
- `POST api/auth/login` – Login and get JWT token

### Admin Routes

- `GET api/admin/get_all_user` – List all users  
- `POST api/admin/create_admin/{access_key}` – Grant admin access  
- `PUT api/admin/add_book` – Add new book  
- `POST api/admin/request_book` – Lend book to user

### Book Routes

- `GET api/books/get_all` – View available books  
- `GET api/books/get_borrowed_books` – View books borrowed by user
