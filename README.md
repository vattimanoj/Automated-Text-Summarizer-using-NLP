# Automated Text Summarizer using NLP

**Final Year B.Tech Project (2026 Batch)**

An AI-powered abstractive text summarization system with continuous learning, explainable AI, and chatbot-style interface.

## 📋 Project Overview

This project implements an advanced **Automated Text Summarizer** using Natural Language Processing (NLP) and Deep Learning techniques. The system uses Transformer-based architectures (T5/BART) for abstractive summarization, includes explainable AI features, and continuously learns from user feedback.

### Key Features

✅ **Abstractive Summarization** - Uses T5/BART transformer models  
✅ **Explainable AI** - Attention visualization and sentence importance scores  
✅ **Continuous Learning** - Auto-training from user feedback (LoRA fine-tuning)  
✅ **Chatbot Interface** - ChatGPT-style conversational UI  
✅ **User Authentication** - JWT-based login/registration  
✅ **Feedback System** - Rating and correction mechanisms  
✅ **ROUGE Evaluation** - Automatic quality metrics  

## 🏗️ System Architecture

```
User (Web / Chatbot UI)
        |
        v
Authentication Service (JWT)
        |
        v
API Gateway (FastAPI)
        |
        v
Text Processing Engine
        |
        v
Abstractive Summarization (T5/BART)
        |
        v
Explainable AI Layer
        |
        v
Feedback & Auto-Training Engine
        |
        v
MySQL Database
```

## 🛠️ Technology Stack

### Backend
- **Python 3.10+**
- **FastAPI** - REST API framework
- **PyTorch** - Deep learning framework
- **HuggingFace Transformers** - Pre-trained models (T5/BART)
- **SQLAlchemy** - ORM
- **PyMySQL** - MySQL connector
- **JWT** - Authentication
- **bcrypt** - Password hashing

### Frontend
- **React.js 18**
- **React Router** - Navigation
- **Axios** - HTTP client
- **CSS3** - Styling

### Database
- **MySQL 8.0+**

### ML Models
- **T5-base** or **BART-large-cnn** for summarization

## 📦 Installation & Setup

### Prerequisites

1. **Python 3.10+**
2. **Node.js 16+** and **npm**
3. **MySQL 8.0+**
4. **Git**

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd "Automated Text Summarizer using NLP"
```

### Step 2: Database Setup

1. **Start MySQL Server**

2. **Create Database:**
```bash
mysql -u root -p
```

```sql
CREATE DATABASE IF NOT EXISTS text_summarizer 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

3. **Run Schema Script:**
```bash
mysql -u root -p text_summarizer < database/schema.sql
```

### Step 3: Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data:**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

5. **Configure environment:**
   - Copy `.env.example` to `.env` (if needed)
   - Update `DATABASE_URL` in `backend/app/config.py`:
   ```python
   DATABASE_URL = "mysql+pymysql://root:yourpassword@localhost:3306/text_summarizer"
   ```

6. **Run backend server:**
```bash
python run.py
```

# Train model manually
python train_model.py

# Force retrain even if model exists

python train_model.py --force


Backend will run at: `http://localhost:8000`

API docs available at: `http://localhost:8000/docs`

### Step 4: Frontend Setup

1. **Open new terminal and navigate to frontend:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start development server:**
```bash
npm start
```

Frontend will run at: `http://localhost:3000`

## 🚀 Usage

### 1. Registration
- Navigate to `http://localhost:3000`
- Click "Sign up" to create an account
- Enter name, email, and password

### 2. Login
- Use your credentials to log in
- You'll be redirected to the dashboard

### 3. Summarize Text
- Paste or type text in the chatbot interface
- Click the send button or press Enter
- Wait for AI to generate summary

### 4. View Explanation
- After getting a summary, click "Explain Summary"
- View sentence importance scores and attention weights

### 5. Provide Feedback
- Rate the summary (1-5 stars)
- Optionally provide corrected summary
- High ratings (≥4) trigger auto-training

### 6. View Statistics
- Check your usage statistics in the sidebar
- See documents, summaries, and feedback count

## 📁 Project Structure

```
Automated Text Summarizer using NLP/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # DB connection
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── auth.py              # JWT authentication
│   │   ├── routers/
│   │   │   ├── auth.py          # Login/Register
│   │   │   ├── summarization.py # Summarize endpoints
│   │   │   ├── feedback.py      # Feedback endpoints
│   │   │   └── user.py          # User stats
│   │   └── ml_model/
│   │       ├── summarizer.py    # T5/BART model
│   │       ├── evaluation.py    # ROUGE scores
│   │       └── auto_training.py # Auto-learning
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chatbot.js       # Main chatbot UI
│   │   │   ├── Message.js       # Message component
│   │   │   ├── InputArea.js     # Text input
│   │   │   ├── ExplanationPanel.js
│   │   │   └── UserStats.js
│   │   ├── pages/
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   └── Dashboard.js
│   │   ├── context/
│   │   │   └── AuthContext.js   # Auth state management
│   │   └── App.js
│   └── package.json
├── database/
│   └── schema.sql               # Database schema
└── README.md
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Summarization
- `POST /api/summarize/text` - Summarize text directly
- `POST /api/summarize/document/{id}` - Summarize saved document
- `GET /api/summarize/documents` - Get user documents
- `GET /api/summarize/document/{id}/explanation` - Get explanation

### Feedback
- `POST /api/feedback/` - Submit feedback
- `GET /api/feedback/summary/{id}` - Get feedback for summary
- `GET /api/feedback/user` - Get user feedback

### User
- `GET /api/user/stats` - Get user statistics

## 🧪 Evaluation Metrics

The system uses **ROUGE scores** (ROUGE-1, ROUGE-2, ROUGE-L) to evaluate summary quality.

## 🔄 Auto-Training Pipeline

1. User provides feedback (rating ≥ 4)
2. System collects high-quality feedback
3. Creates mini training dataset
4. Performs incremental fine-tuning using LoRA
5. Saves new model version
6. Model automatically improves over time

## 🎓 Viva Explanation Points

1. **Problem Statement:**
   - Manual summarization is time-consuming and biased
   - Need for automated, accurate summarization

2. **Solution:**
   - Abstractive summarization using Transformer models
   - Continuous learning from user feedback
   - Explainable AI for transparency

3. **Key Innovations:**
   - Auto-training system (LoRA fine-tuning)
   - Explainable AI layer (attention + importance scores)
   - Chatbot-style conversational interface

4. **Technical Highlights:**
   - T5/BART transformer models
   - FastAPI backend architecture
   - React frontend with JWT authentication
   - MySQL database with proper schema

5. **Results:**
   - High ROUGE scores
   - User satisfaction tracking
   - Continuous model improvement

## 🐛 Troubleshooting

### Backend Issues

**Database Connection Error:**
- Check MySQL is running
- Verify DATABASE_URL in config.py
- Ensure database exists

**Model Loading Error:**
- First run will download model (may take time)
- Check internet connection
- Ensure sufficient disk space (~2GB for T5-base)

**Port Already in Use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill
```

### Frontend Issues

**npm install errors:**
- Clear cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`
- Reinstall: `npm install`

**CORS Errors:**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`

## 📚 Datasets Used

- **CNN/DailyMail** - Base training dataset
- **XSum** - Short summaries
- **WikiHow** - Instruction summarization
- **User Data** - Auto-learning dataset

## 🔐 Default Test Account

- **Email:** manojvatti2004@gmail.com
- **Password:** manoj123

## 📝 Notes

- First model download may take 5-10 minutes
- GPU recommended but not required (CPU works)
- Auto-training requires sufficient feedback (≥8 examples by default)
- All passwords are hashed using bcrypt

## 🎯 Future Enhancements

- Multi-language support
- Real-time collaboration
- Export summaries as PDF
- Advanced visualization for explanations
- Support for longer documents (chunking)

## 📄 License

This project is developed for educational purposes as a Final Year B.Tech project.
Contact: manojvatti2004@gmail.com

## 👥 Contributors

Developed as part of Final Year B.Tech Project (CSE-C, Batch 7, 2026)
Email: manojvatti2004@gmail.com

---

**For any issues or questions, please check the documentation or contact the development team at manojvatti2004@gmail.com.**


Email	manojvatti2004@gmail.com
Password	manoj123
