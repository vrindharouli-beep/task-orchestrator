<div align="center">

# 🗂️ Task Orchestrator

**A full-stack, Dockerized task management and monitoring system**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-REST_API-000000?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-Web_Server-009639?logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

</div>

---

## 📖 About

**Task Orchestrator** is a full-stack web application for managing tasks and monitoring system health from one dashboard. A Flask REST API talks to a PostgreSQL database, an Nginx-served frontend gives you the UI, and the whole stack starts with a single `docker compose up` command.

It was built as a hands-on project to practice full-stack development, containerization, and multi-container deployment.

## 📑 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#️-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#️-getting-started)
- [API Reference](#-api-reference)
- [Docker Commands](#-docker-commands)
- [Troubleshooting](#-troubleshooting)
- [Screenshots](#-screenshots)
- [Learning Outcomes](#-learning-outcomes)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

## 🚀 Features

**Task management**
- Add, delete, and manage tasks
- Set priorities: `HIGH`, `MED`, `LOW`
- Mark tasks as completed or pending
- Filter by **All**, **Pending**, or **Completed**
- Load sample tasks with one click

**Monitoring**
- Live database connection status
- Backend uptime display
- Database latency display

**Deployment**
- One-command setup with Docker Compose
- Persistent PostgreSQL storage that survives container restarts

## 🏗️ Architecture

```text
┌──────────────┐      ┌───────────────────┐      ┌──────────────────┐
│   Browser    │ ───▶ │  Frontend (Nginx) │ ───▶ │  Backend (Flask) │
│              │      │   HTML/CSS/JS     │      │    REST API      │
└──────────────┘      │   port 8080       │      │    port 5000     │
                      └───────────────────┘      └────────┬─────────┘
                                                          │
                                                          ▼
                                                 ┌──────────────────┐
                                                 │   PostgreSQL     │
                                                 │ (persistent vol) │
                                                 └──────────────────┘
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | REST API development |
| PostgreSQL | Database management |
| HTML, CSS, JavaScript | Frontend development |
| Nginx | Frontend web server |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |
| Git & GitHub | Version control |

## 📁 Project Structure

```text
task-orchestrator/
│
├── backend/
│   ├── app.py              # Flask application and API routes
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
│
├── frontend/
│   ├── index.html          # Dashboard UI
│   └── Dockerfile
│
├── database/
│   └── init.sql            # Database schema / initialization
│
├── screenshots/            # Project screenshots
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)
- A code editor such as Visual Studio Code (optional)

### 1. Clone the repository

```bash
git clone https://github.com/vrindharouli-beep/task-orchestrator.git
cd task-orchestrator
```

### 2. Configure environment variables

Copy the example file and set your database password:

```bash
# macOS / Linux
cp .env.example .env

# Windows (PowerShell)
copy .env.example .env
```

Then edit `.env`:

```env
DB_PASS=your_database_password
```

> ⚠️ Never commit your real `.env` file. It is already excluded through `.gitignore`.

### 3. Build and run

```bash
docker compose up --build -d
```

### 4. Open the application

| Service | URL |
|---|---|
| Frontend dashboard | http://localhost:8080 |
| Health check | http://localhost:5000/api/health |
| Tasks API | http://localhost:5000/api/tasks |

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Check application and database health |
| `GET` | `/api/tasks` | Retrieve all tasks |
| `POST` | `/api/tasks` | Create a new task |
| `PUT` | `/api/tasks/{id}` | Toggle task completion |
| `DELETE` | `/api/tasks/{id}` | Delete a task |
| `POST` | `/api/tasks/seed` | Load sample tasks |

**Quick test with curl:**

```bash
curl http://localhost:5000/api/health
curl http://localhost:5000/api/tasks
```

## 🐳 Docker Commands

| Purpose | Command |
|---|---|
| Check running containers | `docker compose ps` |
| View logs | `docker compose logs` |
| Follow logs live | `docker compose logs -f` |
| Stop containers | `docker compose down` |
| Stop and delete database data | `docker compose down -v` |
| Monitor resource usage | `docker stats` |

> ⚠️ `docker compose down -v` removes the database volume, so all saved tasks will be lost.

## 🩺 Troubleshooting

| Problem | Fix |
|---|---|
| Port 8080 or 5000 already in use | Stop the other app using that port, or change the port mapping in `docker-compose.yml` |
| Backend cannot connect to database | Make sure `DB_PASS` in `.env` is set, then rebuild with `docker compose up --build -d` |
| Changed the password but nothing works | Remove the old volume with `docker compose down -v` and start again |
| `docker` command not found | Install and start Docker Desktop |

## 📊 Screenshots

| Dashboard | Add Task |
|---|---|
| ![Dashboard](screenshots/01-dashboard.png) | ![Add Task](screenshots/02-add-task.png) |

| Task Filters | Task Actions |
|---|---|
| ![Filters](screenshots/03-task-filters.png) | ![Actions](screenshots/04-task-actions.png) |

**Running containers**

![Docker containers](screenshots/05-docker-containers.png)

## 🎯 Learning Outcomes

- Full-stack application development
- Building REST APIs with Flask
- Integrating PostgreSQL with a backend service
- Writing Dockerfiles and building images
- Multi-container deployment with Docker Compose
- Container networking and persistent storage
- Application health monitoring

## 🔮 Future Improvements

- User authentication and per-user task lists
- Due dates, reminders, and task categories
- Search and sorting
- Automated tests and a CI/CD pipeline with GitHub Actions
- Deployment to a cloud platform

## 👨‍💻 Author

**Vrind**

Final-year B.Tech – Computer Science and Engineering, DIT University

GitHub: [github.com/vrindharouli-beep](https://github.com/vrindharouli-beep)

---

<div align="center">

*Built as a hands-on project to explore full-stack development and Docker-based deployment.*

⭐ If you found this project useful, consider giving it a star!

</div>
