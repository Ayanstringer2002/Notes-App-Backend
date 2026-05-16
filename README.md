# 📝 Multi-User Notes Service API

A production-ready REST API backend for a multi-user notes service, similar to Google Keep or Apple Notes. Built with Flask, SQLAlchemy, and JWT authentication.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

---

## ✨ Features

### Core Features
- ✅ **User Registration & Authentication** - Secure JWT-based authentication
- ✅ **Note Management** - Full CRUD operations (Create, Read, Update, Delete)
- ✅ **Note Sharing** - Share notes with other registered users
- ✅ **Note Unsharing** - Revoke access to shared notes
- ✅ **Full-Text Search** - Search notes by title and content
- ✅ **Pagination** - Efficient data retrieval with customizable page size
- ✅ **OpenAPI Documentation** - Auto-generated API specification
- ✅ **Input Validation** - Comprehensive validation for all inputs

### Security Features
- 🔒 **JWT Authentication** - Secure token-based authentication
- 🔒 **Password Hashing** - PBKDF2-SHA256 password hashing with Werkzeug
- 🔒 **Access Control** - User-based access controls and authorization checks
- 🔒 **SQL Injection Prevention** - SQLAlchemy ORM prevents SQL injection
- 🔒 **Email Validation** - Regex-based email format validation
- 🔒 **CORS Support** - Cross-origin resource sharing enabled

### Deployment Options
- 🚀 **Docker Support** - Included Dockerfile for containerization
- 🚀 **Cloud Ready** - Deploy to Render, Heroku, Fly.io, Railway.app
- 🚀 **Database Flexible** - Support for SQLite, PostgreSQL, MySQL

---

## 📋 Table of Contents

- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [API Endpoints](#-api-endpoints)
- [Testing with Postman](#-testing-with-postman)
- [Deployment](#-deployment)
- [Environment Variables](#-environment-variables)
- [Database Models](#-database-models)
- [Error Handling](#-error-handling)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Flask 2.3.3 |
| **Database** | SQLAlchemy with SQLite/PostgreSQL |
| **Authentication** | JWT (PyJWT 2.8.0) |
| **Password Hashing** | Werkzeug 2.3.7 |
| **Web Server** | Gunicorn 21.2.0 |
| **Server Framework** | WSGI |
| **Language** | Python 3.8+ |

---

## 📁 Project Structure

```
notes-service/
├── app.py                          # Application factory and main entry point
├── config.py                       # Configuration for dev/prod/test
├── database.py                     # SQLAlchemy database setup
├── models.py                       # Database models (User, Note, SharedNote)
├── auth.py                         # JWT token management
├── utils.py                        # Utility functions (validation, hashing)
│
├── routes/
│   ├── __init__.py                # Blueprint initialization
│   ├── auth_routes.py             # POST /register, POST /login
│   ├── notes_routes.py            # CRUD operations & search
│   ├── share_routes.py            # POST /notes/{id}/share, unshare
│   └── system_routes.py           # GET /about, GET /openapi.json
│
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker compose setup
├── README.md                      # This file
└── COMPLETE_GUIDE.md             # Detailed setup and testing guide
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)
- Virtual environment (recommended)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/notes-service.git
cd notes-service
```

### Step 2: Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# Minimum required: JWT_SECRET_KEY
nano .env
```

Example `.env` file:
```env
FLASK_ENV=development
FLASK_APP=app.py
PORT=5000
DATABASE_URL=sqlite:///notes.db
JWT_SECRET_KEY=your-secret-key-change-in-production
DEBUG=False
```

### Step 5: Create Routes Directory
```bash
mkdir -p routes
touch routes/__init__.py
```

### Step 6: Run Application
```bash
python app.py
```

The API will be available at: `http://localhost:5000`

---

## ⚡ Quick Start

### 1. Register a User
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### 2. Login to Get Token
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. Create a Note
```bash
curl -X POST http://localhost:5000/notes \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Note", "content": "This is my first note"}'
```

### 4. Get All Notes
```bash
curl -X GET http://localhost:5000/notes \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 5. View API Documentation
```bash
curl http://localhost:5000/openapi.json | jq
```

---

## 📚 API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```
**Response:** `201 Created`
```json
{
  "message": "User registered successfully",
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Login
```http
POST /login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```
**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Notes Endpoints

#### Get All Notes (with Pagination)
```http
GET /notes?page=1&per_page=10
Authorization: Bearer <jwt-token>
```
**Response:** `200 OK`
```json
{
  "notes": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Meeting Notes",
      "content": "Discussed project roadmap...",
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ],
  "total": 5,
  "page": 1,
  "per_page": 10
}
```

#### Get Specific Note
```http
GET /notes/{note-id}
Authorization: Bearer <jwt-token>
```
**Response:** `200 OK`

#### Create Note
```http
POST /notes
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "title": "My Note",
  "content": "Note content here"
}
```
**Response:** `201 Created`

#### Update Note
```http
PUT /notes/{note-id}
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content"
}
```
**Response:** `200 OK`

#### Delete Note
```http
DELETE /notes/{note-id}
Authorization: Bearer <jwt-token>
```
**Response:** `204 No Content`

---

### Sharing Endpoints

#### Share Note
```http
POST /notes/{note-id}/share
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "share_with_email": "friend@example.com"
}
```
**Response:** `200 OK`
```json
{
  "message": "Note shared successfully",
  "shared_with": "friend@example.com",
  "note_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Unshare Note
```http
POST /notes/{note-id}/unshare
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "unshare_with_email": "friend@example.com"
}
```
**Response:** `200 OK`

---

### Search Endpoint

#### Search Notes
```http
GET /search?q=keyword
Authorization: Bearer <jwt-token>
```
**Response:** `200 OK`
```json
{
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Shopping List",
      "content": "Buy keyword items...",
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ],
  "total": 1,
  "query": "keyword"
}
```

---

### System Endpoints

#### Get API Information
```http
GET /about
```
**Response:** `200 OK`
```json
{
  "name": "Your Name",
  "email": "your@email.com",
  "my_features": {
    "Note Sharing": "Users can share notes with other registered users...",
    "Full-Text Search": "Search notes by keyword...",
    "Note Pagination": "GET /notes supports pagination...",
    "Unshare Notes": "Users can revoke access to shared notes..."
  }
}
```

#### Get OpenAPI Specification
```http
GET /openapi.json
```
**Response:** `200 OK` (Full OpenAPI 3.0 specification)

---

## 🧪 Testing with Postman

### Import Collection
1. Download the Postman collection from the project
2. Click "Import" in Postman
3. Select the collection file
4. Set up your environment variables

### Create Environment Variables
```
base_url = http://localhost:5000
token = (auto-populated after login)
email_user1 = user1@example.com
email_user2 = user2@example.com
```

### Test Workflow

#### 1. Authentication Flow
- [ ] Register User 1
- [ ] Register User 2
- [ ] Login User 1 (save token)
- [ ] Login User 2 (save token as token_user2)

#### 2. Note Management
- [ ] Create Note 1
- [ ] Create Note 2
- [ ] Get All Notes
- [ ] Get Specific Note
- [ ] Update Note
- [ ] Search Notes

#### 3. Sharing & Collaboration
- [ ] Share Note from User 1 to User 2
- [ ] User 2 Access Shared Note
- [ ] Unshare Note

#### 4. Cleanup
- [ ] Delete Note
- [ ] Test Error Cases (missing auth, invalid token, etc.)

See `COMPLETE_GUIDE.md` for detailed Postman setup instructions with screenshots and examples.

---

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t notes-service:latest .
```

### Run Container
```bash
docker run -p 5000:5000 \
  -e JWT_SECRET_KEY=your-secret-key \
  -e FLASK_ENV=production \
  notes-service:latest
```

### Using Docker Compose
```bash
docker-compose up -d
```

---

## ☁️ Cloud Deployment

### Deploy to Render.com (Recommended for Free)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Render Service**
   - Go to https://render.com
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn --bind 0.0.0.0:$PORT app:create_app()`

3. **Set Environment Variables**
   - JWT_SECRET_KEY: (generate strong random string)
   - FLASK_ENV: production
   - DATABASE_URL: (if using PostgreSQL)

4. **Deploy**
   - Click "Deploy"
   - Your app will be live at: `https://your-app-name.onrender.com`



---

## 🔧 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Environment mode | development | No |
| `FLASK_APP` | Application entry point | app.py | No |
| `PORT` | Server port | 5000 | No |
| `DATABASE_URL` | Database connection string | sqlite:///notes.db | No |
| `JWT_SECRET_KEY` | Secret key for JWT signing | (unsafe default) | **Yes (Production)** |
| `DEBUG` | Debug mode | False | No |

### Production Setup
```env
FLASK_ENV=production
FLASK_APP=app.py
PORT=5000
DATABASE_URL=postgresql://user:password@localhost/notes_db
JWT_SECRET_KEY=your-very-long-random-secret-key-here-min-32-chars
DEBUG=False
```

---

## 🗄️ Database Models

### User Model
```python
User {
  id: String (UUID) [Primary Key]
  email: String (unique)
  password_hash: String
  created_at: DateTime
  
  Relationships:
  - notes: One-to-Many (Note)
  - shared_notes: One-to-Many (SharedNote)
}
```

### Note Model
```python
Note {
  id: String (UUID) [Primary Key]
  user_id: String (Foreign Key → User)
  title: String (max 255)
  content: String (max 10000)
  created_at: DateTime
  updated_at: DateTime
  
  Relationships:
  - author: Many-to-One (User)
  - shared_with: One-to-Many (SharedNote)
}
```

### SharedNote Model
```python
SharedNote {
  id: String (UUID) [Primary Key]
  note_id: String (Foreign Key → Note)
  shared_with_user_id: String (Foreign Key → User)
  shared_at: DateTime
  
  Unique Constraint: (note_id, shared_with_user_id)
  
  Relationships:
  - note: Many-to-One (Note)
  - shared_with_user: Many-to-One (User)
}
```

---

## ✅ Input Validation

### Email Validation
- RFC 5322 compliant regex pattern
- Must contain @ and valid domain
- Checked on registration and sharing

### Password Validation
- Minimum 6 characters
- Maximum 255 characters
- Case-sensitive

### Note Validation
- Title: Required, max 255 characters
- Content: Required, max 10000 characters
- Whitespace trimmed

### Search Query
- Minimum 2 characters
- Case-insensitive matching
- Searches title and content

---

## 🚨 Error Handling

### Common HTTP Status Codes

| Status | Meaning | Example |
|--------|---------|---------|
| **200** | OK | Note retrieved successfully |
| **201** | Created | Note or user created |
| **204** | No Content | Note deleted successfully |
| **400** | Bad Request | Invalid input data |
| **401** | Unauthorized | Missing or invalid token |
| **403** | Forbidden | Access denied (not owner) |
| **404** | Not Found | Resource doesn't exist |
| **409** | Conflict | Email already registered |
| **500** | Server Error | Unexpected error |

### Error Response Format
```json
{
  "message": "Error description"
}
```

### Example Error Responses
```json
// Missing token
{"message": "Authorization token is missing"}

// Invalid email
{"message": "Invalid email format"}

// Email already exists
{"message": "Email already registered"}

// Note not found
{"message": "Note not found"}

// Access denied
{"message": "Access denied"}
```

---

## 🔒 Security Best Practices

### ✅ Implemented
- JWT token-based authentication
- Password hashing with PBKDF2-SHA256
- SQL injection prevention via SQLAlchemy ORM
- CORS support for cross-origin requests
- Email format validation
- Access control checks
- Token expiration (30 days)

### 🛡️ Production Recommendations
- Use HTTPS only (redirect HTTP to HTTPS)
- Set strong `JWT_SECRET_KEY` (minimum 32 characters)
- Use PostgreSQL instead of SQLite
- Enable rate limiting on auth endpoints
- Implement CAPTCHA for registration
- Add request logging and monitoring
- Use environment variables for secrets
- Regular security audits
- Keep dependencies updated

---

## 📈 Performance Optimizations

- Database indexing on frequently queried fields
- Pagination for large note collections
- Connection pooling (configurable)
- Efficient query optimization
- Caching headers support
- Compression support (gzip)

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'flask'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue: `sqlite3.OperationalError: database is locked`
```bash
# Solution: Remove and recreate database
rm notes.db
python app.py
```

### Issue: `Address already in use` (Port 5000)
```bash
# Solution: Use different port
PORT=5001 python app.py
```

### Issue: `JWT token expired`
```bash
# Solution: Login again to get new token
```

### Issue: CORS errors in frontend
```bash
# Solution: Flask-CORS is already enabled
# Check that you're sending proper headers
```

---





## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---



## 👨‍💻 Author

**Your Name**
- Email: ayan988ahmad@gmail.com
- GitHub: [@marcusayan](https://github.com/Ayanstringer2002)

---

## 🙏 Acknowledgments

- Flask documentation
- SQLAlchemy ORM
- JWT authentication
- OpenAPI/Swagger specification

---

## 📞 Support

If you have questions or need help:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)
3. Open an issue on GitHub
4. Contact: your.email@example.com

---

## 🚀 Roadmap

- [ ] Rate limiting on API endpoints
- [ ] Note labels/categories
- [ ] Note attachments
- [ ] Rich text editor support
- [ ] Mobile app
- [ ] Websocket support for real-time updates
- [ ] Note version history
- [ ] Collaborative editing
- [ ] End-to-end encryption
- [ ] Analytics dashboard

---

**Last Updated:** May 2026

**Status:** ✅ Production Ready

---

## Quick Links

- 📚 [Complete Setup Guide](COMPLETE_GUIDE.md)
- 🐍 [Python Requirements](requirements.txt)
- 🐳 [Docker Configuration](Dockerfile)
- 📖 [OpenAPI Spec](GET /openapi.json)
- 💬 [API Feedback](#support)

---

**Made with ❤️ for developers**