# task-manager-api

Multi-tenant task management API built with FastAPI, PostgreSQL, and Docker.

## Features (Planned)
- ✅ User CRUD operations (Create, Read, Delete)
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Docker containerized database
- 🔄 User authentication with JWT (next)
- 🔄 Task management
- 🔄 Organize tasks by projects


## Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **Deployment:** Docker + Docker Compose

## Getting Started


### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/jaspersanchez/task-manager-api.git
cd task-manager-api
```

2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup environment variables
```bash
# Create .env file
DATABASE_URL=postgresql://username:password@localhost:5432/taskmanager
SECRET_KEY=your-secret-key-here-generate-with-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Start PostgreSQL with Docker
```bash
docker-compose up -d
```

6. Create database tables
```bash
python -m app.core.init_db
```

7. Run the server
```bash
uvicorn app.main:app --reload
```

8. Visit http://127.0.0.1:8000/docs for API documentation

## Development Progress
- [x] Initial FastAPI setup
- [x] Basic endpoints
- [x] PostgreSQL database setup
- [x] User model and CRUD endpoints
- [x] Docker Compose for database
- [ ] User authentication (JWT)
- [ ] Task CRUD operations
- [ ] Full Docker deployment

## Author
Jasper A. Sanchez

## License
MIT
