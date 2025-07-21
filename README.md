
# 🎵 FastAPI Authentication + Transpose API

This project provides a secure FastAPI backend that supports user signup, login using JWT authentication, and a note transposition service for Hindustani music notation.

---

## 🚀 Features

- ✅ User Signup and Login (with hashed passwords)
- ✅ JWT-based Authentication
- ✅ Protected Transpose API (only for logged-in users)
- ✅ SQLAlchemy + SQLite Integration
- ✅ Pydantic for Input Validation

---

## 📦 Project Structure

```
.
├── main.py                 # FastAPI app entrypoint
├── logic.py                # Transposition logic
├── models.py               # SQLAlchemy models
├── JWTtoken.py             # JWT creation and verification
├── users.py                # Auth-related route handlers
├── transpose.py            # Transpose-related route handlers
├── schemas/
│   ├── users.py            # Pydantic schemas for auth
│   └── transpose.py        # Schema for transpose input
├── crud.py                 # Database logic
├── database.py             # DB session setup
└── README.md               # This file
```

---

## ⚙️ Setup Instructions

1. **Clone the repo**
```bash
git clone https://github.com/your-username/fastapi-transpose-app.git
cd fastapi-transpose-app
```

2. **Create a virtual environment and activate it**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
uvicorn main:app --reload
```

App will be live at:  
👉 `http://127.0.0.1:8000/docs`

---

## 🛠 API Usage

### 🔐 Signup
```http
POST /signup
```
```json
{
  "name": "Kedar",
  "email": "kedar@example.com",
  "password": "yourpassword"
}
```

### 🔐 Signin
```http
POST /signin
```
Returns JWT token.

### 🎵 Transpose Notes (Protected)
```http
POST /transpose
Authorization: Bearer <your-token>
```
```json
{
  "notes": "S R G M P D N S",
  "shift": 2
}
```

---

## 🧪 Testing with Postman

1. Use `/signup` to create an account.
2. Use `/signin` to get your JWT token.
3. Add the token to Authorization tab → Bearer Token.
4. Call `/transpose` with a note string.

---

## 🔐 Environment Variables (Optional)
Set a custom secret key in your `.env`:
```
JWT_SECRET=your_custom_secret_key
```

---

## 📜 License

MIT License. Free to use for educational and commercial purposes.

---

## 👨‍💻 Author

**Kedar Jevargi**  
Aspiring Backend Developer | CSE @2027  

