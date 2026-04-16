# WorkNest API — Endpoints Reference

## Base URL
`http://127.0.0.1:8000/api/`

## Authentication
All endpoints except register, login, and health check require:
`Authorization: Bearer <access_token>`

---

## Auth
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /auth/register/ | Register new user | No |
| POST | /auth/login/ | Login and get tokens | No |
| POST | /auth/token/refresh/ | Refresh access token | No |
| GET | /auth/profile/ | Get current user profile | Yes |

## Companies
| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| GET | /companies/ | List my companies | Member |
| POST | /companies/ | Create a company | Any |
| GET | /companies/{id}/ | Company details | Member |
| DELETE | /companies/{id}/ | Delete company | Admin |
| GET | /companies/{id}/members/ | List members | Member |
| POST | /companies/{id}/members/ | Add member | Admin |

## Projects
| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| GET | /companies/{id}/projects/ | List projects | Member |
| POST | /companies/{id}/projects/ | Create project | Member |
| GET | /companies/{id}/projects/{id}/ | Project details | Member |
| PATCH | /companies/{id}/projects/{id}/ | Update project | Member |
| DELETE | /companies/{id}/projects/{id}/ | Delete project | Admin |

## Tasks
| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| GET | /companies/{id}/projects/{id}/tasks/ | List tasks | Member |
| POST | /companies/{id}/projects/{id}/tasks/ | Create task | Member |
| GET | /companies/{id}/projects/{id}/tasks/{id}/ | Task details | Member |
| PATCH | /companies/{id}/projects/{id}/tasks/{id}/ | Update task | Member |
| DELETE | /companies/{id}/projects/{id}/tasks/{id}/ | Delete task | Admin |
| PATCH | /companies/{id}/projects/{id}/tasks/{id}/status/ | Change status | Member |

## Activity
| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| GET | /companies/{id}/activity/ | Company activity feed | Member |
| GET | /companies/{id}/projects/{id}/activity/ | Project activity feed | Member |

## Filtering & Search
### Tasks
- `?status=todo` or `in_progress` or `done`
- `?priority=low` or `medium` or `high`
- `?search=keyword`
- `?ordering=due_date` or `-due_date`
- `?page=1&page_size=10`

### Projects
- `?status=active` or `completed` or `archived`
- `?search=keyword`
- `?ordering=name` or `-created_at`
