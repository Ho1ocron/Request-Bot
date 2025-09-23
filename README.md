# 📩 Requset-bot

A **Requset-bot** built with [Aiogram](https://docs.aiogram.dev/) that forwards user messages to selected channels.  
Supports:
- ✅ Text messages  
- ✅ Photos  
- ✅ Media groups (albums)  

Uses [Tortoise ORM](https://tortoise.github.io/) with **PostgreSQL** for database management.

---

## 🚀 Features
- Forward messages (text, images, albums) to Telegram channels.  
- Users can choose which channel(s) to forward their messages to.  
- Persistent data storage using PostgreSQL + TortoiseORM.  
- Asynchronous and lightweight with **Aiogram**.  

---

## 🛠️ Tech Stack
- **Python 3.10+**  
- [Aiogram](https://github.com/aiogram/aiogram) – Telegram bot framework  
- [Tortoise ORM](https://tortoise.github.io/) – Async ORM  
- **PostgreSQL** – Database  

---

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
python -m venv venv
source venv/bin/activate   # On Linux / Mac
venv\Scripts\activate      # On Windows
```
---
### 2. Install libraries
```bash
pip install -r requirements.txt
```
### 3. Bot configurations
```bash
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgres://user:password@db:5432/db_name
```
---

## 📦 Database

### Run database migrations 
```bash
aerich init -t app.models.TORTOISE_ORM
aerich init-db
aerich migrate
aerich upgrade
```

## Start the bot
```bash
python ./src/bot.py
```
---

## Docker
### 1. Build and start services
```bash
docker-compose up --build -d
```

### 2. Run database migrations inside the contain
```bash
docker-compose exec bot aerich upgrade
```

### 3. Stop containers
```bash
docker-compose down
```

---
## 📂 Project Structure
```
├── app/
│   ├── bot.py          # Entry point for the bot
│   ├── handlers/       # Message handlers
│   ├── models.py       # Tortoise ORM models
│   ├── services/       # Business logic
│   └── utils/          # Helper functions
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```