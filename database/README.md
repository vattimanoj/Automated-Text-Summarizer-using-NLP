# Database Setup Instructions

## Prerequisites
- MySQL Server installed and running
- MySQL root access

## Setup Steps

1. **Login to MySQL:**
```bash
mysql -u root -p
```

2. **Create Database:**
```sql
CREATE DATABASE IF NOT EXISTS text_summarizer CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. **Run Schema Script:**
```bash
mysql -u root -p text_summarizer < schema.sql
```

Or manually copy and paste the SQL from `schema.sql` into MySQL.

4. **Update Backend Config:**
Update `backend/app/config.py` or create `.env` file with your database credentials:
```
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/text_summarizer
```

## Test Admin User
- Email: admin@example.com
- Password: admin123

## Notes
- All tables use InnoDB engine for foreign key support
- Character set is utf8mb4 for full Unicode support
- Foreign keys use CASCADE delete for data consistency
