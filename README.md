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
git clone https://github.com/Ho1ocron/Request-Bot.git
cd Request-Bot
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

## 🗃️ Database

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

## 🗄️ Database structure

### 👤 User table
| id | user_id | username   | name            |
|:--:|:-------:|:----------:|:---------------:|
| 1  | U1001   | johndoe    | John Doe        |
| 2  | U1002   | janesmith  | Jane Smith      |
| 3  | U1003   | alexj      | Alex Johnson    |
| 4  | U1004   | mariab     | Maria Brown     |
| 5  | U1005   | chrisp     | Chris Parker    |
| 6  | U1006   | lindaw     | Linda White     |
| 7  | U1007   | robertk    | Robert King     |
| 8  | U1008   | sarahl     | Sarah Lewis     |
| 9  | U1009   | danielt    | Daniel Taylor   |
| 10 | U1010   | emilyr     | Emily Robinson  |

### 👥 Group table
| id | group_id | group_name      |
|:--:|:--------:|:---------------:|
| 1  | G2001    | Admins          |
| 2  | G2002    | Editors         |
| 3  | G2003    | Viewers         |
| 4  | G2004    | Contributors    |
| 5  | G2005    | Moderators      |
| 6  | G2006    | Guests          |
| 7  | G2007    | Developers      |
| 8  | G2008    | Designers       |
| 9  | G2009    | Testers         |
| 10 | G2010    | Managers        |

### 🔄 User to Group table
| id | user_id | group_id |
|:--:|:-------:|:--------:|
| 1  | U1001   | G2001    |
| 2  | U1001   | G2002    |
| 3  | U1002   | G2003    |
| 4  | U1002   | G2004    |
| 5  | U1003   | G2005    |
| 6  | U1004   | G2006    |
| 7  | U1005   | G2007    |
| 8  | U1006   | G2008    |
| 9  | U1007   | G2009    |
| 10 | U1008   | G2010    |
---

## 📂 Project Structure
```
├── src/                   # Main source code
│   ├── bot.py             # Entry point for the bot
│   ├── config.py
│   ├── settings.py
│   ├── states.py
│   ├── test.py
│   ├── utils.py
│   ├── handlers/          # Message handlers
│   └── database/          # Database models & migrations
├── .env                   # Environment variables
├── .env.example           # Environment variables example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```