# ✨ Kalyani Portfolio — Setup & Deployment Guide

## 📁 Project Structure
```
kalyani-portfolio/
├── frontend/
│   ├── index.html          ← Main portfolio page
│   ├── css/style.css       ← All styles
│   └── js/main.js          ← All frontend JS
├── backend/
│   ├── main.py             ← FastAPI app entry point
│   ├── database.py         ← MongoDB connection
│   ├── requirements.txt
│   ├── .env.example        ← Copy → .env and fill in
│   ├── models/             ← Beanie document models
│   │   ├── blog.py
│   │   ├── project.py
│   │   ├── contact.py
│   │   ├── analytics.py
│   │   └── photo.py
│   ├── routers/            ← API route handlers
│   │   ├── auth.py
│   │   ├── blogs.py
│   │   ├── projects.py
│   │   ├── contact.py
│   │   ├── analytics.py
│   │   ├── github.py
│   │   ├── spotify.py
│   │   └── photos.py
│   ├── schemas/
│   │   └── schemas.py      ← Pydantic request/response models
│   └── utils/
│       └── auth.py         ← JWT utilities
├── admin/
│   ├── index.html          ← Admin dashboard
│   └── admin.js            ← Dashboard JavaScript
└── SCHEMA.md               ← MongoDB schema docs
```

---

## 🚀 Local Development Setup

### Step 1: Clone & Setup Backend

```bash
cd kalyani-portfolio/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and fill environment variables
cp .env.example .env
# Edit .env with your values (MongoDB URI, secrets, etc.)
```

### Step 2: Generate Admin Password Hash

```python
# Run in Python:
from passlib.context import CryptContext
ctx = CryptContext(schemes=["bcrypt"])
print(ctx.hash("your_chosen_password"))
# Copy the output into ADMIN_PASSWORD_HASH in .env
```

### Step 3: Run the Backend

```bash
# From backend/ directory:
uvicorn main:app --reload --port 8000

# API docs available at:
# http://localhost:8000/docs
```

### Step 4: Run the Frontend

```bash
# Option 1: VS Code Live Server (recommended)
# Install "Live Server" extension → right-click index.html → Open with Live Server

# Option 2: Python simple server
cd frontend/
python -m http.server 5500

# Option 3: npx serve
npx serve frontend/
```

### Step 5: Admin Dashboard

```bash
# Simply open admin/index.html in your browser, or serve it:
npx serve admin/
# Navigate to http://localhost:3000
```

---

## 🌐 API Reference

### Auth
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/login` | No | Admin login → JWT token |

**Request:**
```json
POST /auth/login
{ "username": "kalyani", "password": "your_password" }

Response:
{ "access_token": "eyJ...", "token_type": "bearer", "expires_in": 86400 }
```

### Blogs
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/blogs/` | No | List published blogs |
| GET | `/blogs/{slug}` | No | Get single blog (increments views) |
| GET | `/blogs/featured` | No | Get featured blogs |
| POST | `/blogs/` | Admin | Create blog |
| PUT | `/blogs/{id}` | Admin | Update blog |
| DELETE | `/blogs/{id}` | Admin | Delete blog |

**Example GET /blogs/?limit=3:**
```json
{
  "blogs": [
    {
      "id": "6758abc123...",
      "title": "Why Attention is All You Need",
      "slug": "why-attention-is-all-you-need",
      "excerpt": "Breaking down transformers...",
      "tag": "ML",
      "read_time": "8 min read",
      "published": true,
      "views": 142,
      "created_at": "2024-11-15T10:30:00Z"
    }
  ],
  "total": 12,
  "skip": 0,
  "limit": 3
}
```

### Projects
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/projects/` | No | List all projects |
| GET | `/projects/{slug}` | No | Get single project |
| POST | `/projects/` | Admin | Create project |
| PUT | `/projects/{id}` | Admin | Update project |
| DELETE | `/projects/{id}` | Admin | Delete project |

### Contact
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/contact/` | No | Submit contact form |
| GET | `/contact/` | Admin | Get all messages |
| PATCH | `/contact/{id}/read` | Admin | Mark as read |

**Example POST /contact/:**
```json
// Request:
{
  "name": "Priya Sharma",
  "email": "priya@example.com",
  "subject": "collaboration",
  "message": "Hi! I loved your work..."
}

// Response:
{ "success": true, "message": "Message received! I'll get back to you soon 💌" }
```

### Analytics
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/analytics/visit` | No | Track page visit |
| GET | `/analytics/summary` | Admin | Get analytics summary |

### GitHub
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/github/stats` | No | Cached GitHub stats |

### Spotify
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/spotify/now-playing` | No | Current/recent track |

### Photos
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/photos/` | No | Get all photos |
| POST | `/photos/` | Admin | Add photo |
| DELETE | `/photos/{id}` | Admin | Delete photo |

---

## ☁️ Deployment

### MongoDB Atlas (Database)

1. Sign up at [cloud.mongodb.com](https://cloud.mongodb.com)
2. Create a free M0 cluster
3. Create database user → copy credentials
4. Whitelist IP: `0.0.0.0/0` (or your server's IP)
5. Get connection string → paste into `MONGODB_URI`

### Backend → Render (Free)

1. Push your `backend/` folder to a GitHub repo
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repo
4. Settings:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. Add all environment variables from `.env`
6. Deploy!

> 💡 Free Render tier spins down after 15 min of inactivity. Consider UptimeRobot for keep-alive pings.

### Frontend → Vercel (Free)

1. Push `frontend/` to GitHub
2. Go to [vercel.com](https://vercel.com) → New Project
3. Import repo → set root to `frontend/`
4. No build command needed (static HTML)
5. Deploy!
6. **Important:** Update `API_BASE` in `frontend/js/main.js` to your Render URL

### Admin → Vercel or Netlify

1. Push `admin/` as a separate repo or subfolder
2. Deploy the same way as frontend
3. **Important:** Update `const API` in `admin/admin.js` to your Render URL

---

## 🎵 Spotify Setup

1. Go to [developer.spotify.com](https://developer.spotify.com/dashboard)
2. Create an App → get Client ID & Secret
3. Add redirect URI: `http://localhost:8888/callback`
4. Get your refresh token using [this guide](https://developer.spotify.com/documentation/web-api/tutorials/refreshing-tokens) or use [spotify-refresh-token](https://github.com/alecchen/spotify-refresh-token)
5. Scopes needed: `user-read-currently-playing user-read-recently-played`
6. Add `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REFRESH_TOKEN` to `.env`

---

## 🐣 Easter Egg

- Click the `✦` in the footer
- OR type the Konami code: `↑ ↑ ↓ ↓ ← → ← → B A`

---

## 🎨 Customisation Checklist

- [ ] Replace `kalyani` with your GitHub username in `js/main.js` and `.env`
- [ ] Update social links in `index.html`
- [ ] Add your real photo (replace `.photo-placeholder` with `<img>`)
- [ ] Upload your resume to `backend/static/Kalyani_Resume.pdf`
- [ ] Update projects with your real work
- [ ] Configure Spotify for live music display
- [ ] Add your real email in `.env` (NOTIFY_EMAIL)
- [ ] Change admin password and generate a strong JWT secret

---

## 🛡️ Security Notes

- Never commit `.env` (it's in `.gitignore`)
- Change `ADMIN_PASSWORD_HASH` before going live
- Generate a strong `JWT_SECRET_KEY` (32+ random chars)
- Set `ALLOWED_ORIGINS` to only your domain in production
- Consider rate-limiting the `/contact` endpoint for spam prevention

---

*Built with ✨ FastAPI + MongoDB + Vanilla JS*
