# task-manager-api

Multi-tenant task management API built with FastAPI, PostgreSQL, and Docker.

## Features (Planned)
- ✅ User authentication with JWT
- ✅ Password hashing with bcrypt
- ✅ Task CRUD operations (Create, Read, Update, Delete)
- ✅ Task filtering by status and priority
- ✅ Task statistics and completion tracking
- ✅ User-task relationships with data isolation
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Docker containerized database
- ✅ Auto-generated API documentation
- 🔄 Project organization (next)
- 🔄 Full Docker deployment


## Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL 15
- **Authentication:** JWT (JSON Web Tokens)
- **Security:** bcrypt password hashing
- **ORM:** SQLAlchemy
- **Deployment:** Docker + Docker Compose

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/auth/logout` - Logout

### Users
- `POST /api/v1/users/` - Register new user
- `GET /api/v1/users/me` - Get current user (protected)
- `GET /api/v1/users/` - List users (protected)
- `GET /api/v1/users/{user_id}` - Get specific user (protected)
- `DELETE /api/v1/users/{user_id}` - Delete user (protected)

### Tasks
- `POST /api/v1/tasks/` - Create new task (protected)
- `GET /api/v1/tasks/` - List your tasks with filters (protected)
- `GET /api/v1/tasks/{task_id}` - Get specific task (protected)
- `PUT /api/v1/tasks/{task_id}` - Update task (protected)
- `DELETE /api/v1/tasks/{task_id}` - Delete task (protected)
- `GET /api/v1/tasks/stats/summary` - Get task statistics (protected)

#### Task Filters
- `status`: Filter by todo, in_progress, or done
- `priority`: Filter by low, medium, or high
- `skip` & `limit`: Pagination

## Database Schema

### Users Table
- `id` - Primary key
- `email` - Unique, indexed
- `username` - Unique, indexed
- `hashed_password` - bcrypt hashed
- `is_active` - Boolean
- `is_superuser` - Boolean
- `created_at`, `updated_at` - Timestamps

### Tasks Table
- `id` - Primary key
- `title` - Required, indexed
- `description` - Optional
- `status` - Enum (todo, in_progress, done)
- `priority` - Enum (low, medium, high)
- `is_completed` - Boolean
- `owner_id` - Foreign key to users
- `created_at`, `updated_at`, `completed_at` - Timestamps

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

## Key Features

### Data Isolation
Each user can only access their own tasks. Multi-tenant architecture ensures privacy and security.

### Task Status Tracking
- **TODO**: Task is planned
- **IN_PROGRESS**: Task is being worked on
- **DONE**: Task is completed

### Priority Levels
- **LOW**: Nice to have
- **MEDIUM**: Should do soon
- **HIGH**: Urgent, do first

### Automatic Timestamps
- `created_at`: When task was created
- `updated_at`: When task was last modified
- `completed_at`: When task was marked complete

## Development Progress
- [x] Initial FastAPI setup
- [x] PostgreSQL database setup
- [x] User model and CRUD endpoints
- [x] Docker Compose for database
- [x] JWT Authentication
- [x] Password hashing (bcrypt)
- [x] Protected routes
- [x] Task model with relationships
- [x] Task CRUD operations
- [x] Task filtering and statistics
- [x] Data isolation (multi-tenancy)
- [ ] Project organization
- [ ] Full Docker deployment

## Author
Jasper A. Sanchez

## License
MIT
