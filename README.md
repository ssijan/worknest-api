# WorkNest API

A production-ready multi-tenant SaaS task management REST API built with Django REST Framework.

## Live Demo
- **API Base URL:** https://worknest-api-e7mg.onrender.com/api/health/
- **Swagger Docs:** https://worknest-api-e7mg.onrender.com/api/docs/
- **ReDoc:** https://worknest-api-e7mg.onrender.com/api/docs/redoc/
- **Admin:**
```
{
    "email": "test@worknest.com",
    "name": "Test User",
    "password": "test123"
}
```

## Tech Stack
- **Backend:** Django 6, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (SimpleJWT)
- **Documentation:** drf-spectacular (Swagger / ReDoc)
- **Filtering:** django-filter
- **Deployment:** Render

## Features
- JWT-based authentication (register, login, token refresh)
- Multi-tenant architecture — complete data isolation between companies
- Role-based access control (Admin / Member)
- Project management with status tracking
- Task management with assignment, priority, and due dates
- Activity/audit log system
- Filtering, search, ordering, and pagination on all list endpoints
- Auto-generated Swagger and ReDoc API documentation

## API Endpoints

### Auth
```
POST   /api/auth/register/          Register new user
POST   /api/auth/login/             Login and get JWT tokens
POST   /api/auth/token/refresh/     Refresh access token
GET    /api/auth/profile/           Get current user profile
```

### Companies
```
GET    /api/companies/              List my companies
POST   /api/companies/              Create a company
GET    /api/companies/{id}/         Company details
DELETE /api/companies/{id}/         Delete company (admin only)
GET    /api/companies/{id}/members/ List members
POST   /api/companies/{id}/members/ Add member (admin only)
```

### Projects
```
GET    /api/companies/{id}/projects/        List projects
POST   /api/companies/{id}/projects/        Create project
GET    /api/companies/{id}/projects/{id}/   Project details
PATCH  /api/companies/{id}/projects/{id}/   Update project
DELETE /api/companies/{id}/projects/{id}/   Delete project (admin only)
```

### Tasks
```
GET    /api/companies/{id}/projects/{id}/tasks/             List tasks
POST   /api/companies/{id}/projects/{id}/tasks/             Create task
GET    /api/companies/{id}/projects/{id}/tasks/{id}/        Task details
PATCH  /api/companies/{id}/projects/{id}/tasks/{id}/        Update task
DELETE /api/companies/{id}/projects/{id}/tasks/{id}/        Delete task (admin only)
PATCH  /api/companies/{id}/projects/{id}/tasks/{id}/status/ Change status
```

### Activity
```
GET    /api/companies/{id}/activity/                        Company activity feed
GET    /api/companies/{id}/projects/{id}/activity/          Project activity feed
```

## Filtering & Search

### Tasks
```
?status=todo|in_progress|done
?priority=low|medium|high
?search=keyword
?ordering=due_date|-due_date
?page=1&page_size=10
```

### Projects
```
?status=active|completed|archived
?search=keyword
?ordering=name|-created_at
```

## Local Setup

### Prerequisites
- Python 3.12+
- PostgreSQL

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/worknest-api.git
cd worknest-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python3 manage.py migrate

# Start server
python3 manage.py runserver
```

### Environment Variables
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=worknest_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

## Database Schema

| Table | Description |
|-------|-------------|
| accounts_user | Custom user model with email login |
| companies_company | Tenant/company model |
| companies_membership | User-company relationship with roles |
| projects_project | Projects belonging to companies |
| tasks_task | Tasks with assignment and status |
| core_activitylog | Audit log of all actions |

## Author
Md. Sakibur Rahman
