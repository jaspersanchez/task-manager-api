# task-manager-api

Multi-tenant task management API built with FastAPI, PostgreSQL, and Docker.

## Features (Planned)
- User authentication with JWT
- Create read, update, delete tasks
- Organize tasks by projects
- RESTful API design
- Docker deployment

## Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **Deployment:** Docker + Docker Compose

## Getting Started


### Prerequisites
- Python 3.9+
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

4. Run the server
```bash
uvicorn app.main:app --reload
```

5. Visit http://127.0.0.1:8000/docs for API documentation

## Development Progress
- [x] Initial FastAPI setup
- [x] Basic endpoints
- [ ] User authentication
- [ ] Database models
- [ ] Task CRUD operations
- [ ] Docker deployment

## Author
Jasper A. Sanchez

## License
MIT
