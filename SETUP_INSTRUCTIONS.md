# Quick Setup Instructions

## Prerequisites Check
- ✅ Python 3.10+ installed
- ✅ Node.js 16+ installed
- ✅ MySQL 8.0+ installed and running
- ✅ Git installed

## Step-by-Step Setup

### 1. Database Setup (5 minutes)

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE IF NOT EXISTS text_summarizer 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Exit MySQL
EXIT;

# Import schema
mysql -u root -p text_summarizer < database/schema.sql
```

### 2. Backend Setup (10 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install --force-reinstall scikit-learn
# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Update database URL in backend/app/config.py
# Change: DATABASE_URL = "mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/text_summarizer"

# Run backend
python run.py
```

Backend runs at: `http://localhost:8000`

### 3. Frontend Setup (5 minutes)

```bash
# Open NEW terminal
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start frontend
npm start
```

Frontend runs at: `http://localhost:3000`

## Test Login

- Email: `manojvatti2004@gmail.com`
- Password: `manoj123`

## Troubleshooting

### Database Connection Failed
```bash
# Check MySQL is running
# Windows: Check Services
# Linux: sudo systemctl status mysql

# Test connection
mysql -u root -p -e "SELECT 1"
```

### Backend Port Already in Use
```bash
# Find and kill process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill
```

### Frontend Port Already in Use
Change port in `frontend/package.json` or use:
```bash
PORT=3001 npm start
```

### Model Download Issues
- First run downloads T5 model (~500MB)
- Ensure stable internet connection
- Check disk space (need ~2GB free)

## Verification

1. ✅ Backend: Visit `http://localhost:8000/docs` - should show API docs
2. ✅ Frontend: Visit `http://localhost:3000` - should show login page
3. ✅ Database: Run `mysql -u root -p text_summarizer -e "SELECT COUNT(*) FROM users;"`

## Next Steps

1. Register a new account
2. Login with credentials
3. Paste some text in the chatbot
4. Get a summary
5. View explanation
6. Rate the summary

Enjoy your Automated Text Summarizer! 🎉
