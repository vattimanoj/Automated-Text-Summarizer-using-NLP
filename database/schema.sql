-- Database: text_summarizer
-- Create database (run this manually first)
-- CREATE DATABASE IF NOT EXISTS text_summarizer CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE text_summarizer;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Documents Table
CREATE TABLE IF NOT EXISTS documents (
    doc_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    original_text LONGTEXT NOT NULL,
    domain VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Summaries Table
CREATE TABLE IF NOT EXISTS summaries (
    summary_id INT AUTO_INCREMENT PRIMARY KEY,
    doc_id INT NOT NULL,
    model_version VARCHAR(50) DEFAULT 't5-base-v1',
    summary_text TEXT NOT NULL,
    rouge_1_score FLOAT DEFAULT 0.0,
    rouge_2_score FLOAT DEFAULT 0.0,
    rouge_l_score FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doc_id) REFERENCES documents(doc_id) ON DELETE CASCADE,
    INDEX idx_doc_id (doc_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Feedback Table
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    summary_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    corrected_summary TEXT,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    used_for_training BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (summary_id) REFERENCES summaries(summary_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_summary_id (summary_id),
    INDEX idx_user_id (user_id),
    INDEX idx_rating (rating),
    INDEX idx_used_for_training (used_for_training)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Explanations Table
CREATE TABLE IF NOT EXISTS explanations (
    explanation_id INT AUTO_INCREMENT PRIMARY KEY,
    summary_id INT NOT NULL,
    sentence_importance TEXT,
    attention_weights TEXT,
    highlighted_words TEXT,
    FOREIGN KEY (summary_id) REFERENCES summaries(summary_id) ON DELETE CASCADE,
    UNIQUE KEY unique_summary (summary_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert demo admin user (password: manoj123)
-- Password hash for 'manoj123' using pbkdf2_sha256 (matches backend auth.py)
INSERT INTO users (name, email, password_hash, role) 
VALUES ('Admin User', 'manojvatti2004@gmail.com', '$pbkdf2-sha256$29000$LiLcnqbx/Ke38FVJKejf1w$ozDYcUEAeBQXAzuI1DKj1L2S8WoCuALNWW9ry0/lZuA', 'admin')
ON DUPLICATE KEY UPDATE name=name;
