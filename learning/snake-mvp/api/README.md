# Backend API Stubs

## Overview

This directory is a placeholder for future backend API development. Currently, the Snake Learning MVP is a fully static web application that stores all data in the browser's localStorage. This README provides guidance on how to add server-side endpoints for persistence, authentication, and multi-user features.

## Current Architecture (Static MVP)

```
Browser (Client)
├── HTML/CSS/JavaScript
├── Brython (Python in browser)
└── localStorage
    ├── student_name
    ├── coins
    └── quiz_scores
```

**Limitations:**
- Data is stored only in the user's browser
- No data synchronization across devices
- No teacher dashboard with real student data
- No authentication or user management

## Proposed Backend Architecture

```
Client (Browser)                 Server                    Database
├── HTML/CSS/JS         <->      ├── API Gateway           ├── PostgreSQL
├── Brython                      ├── Auth Service          │   ├── users
└── REST/WebSocket calls         ├── Student Service       │   ├── quiz_scores
                                 ├── Quiz Service          │   ├── code_edits
                                 └── Analytics Service     │   └── sessions
```

## Recommended Technology Stack

### Backend Framework Options:
1. **Node.js + Express** (JavaScript/TypeScript)
   - Easy integration with existing frontend
   - Large ecosystem of packages
   - Good for real-time features with Socket.io

2. **Python + FastAPI** (Python)
   - Modern, fast async framework
   - Automatic API documentation
   - Natural fit with Brython/Python learning theme

3. **Python + Django** (Python)
   - Full-featured web framework
   - Built-in admin panel for teachers
   - Robust ORM for database management

### Database Options:
1. **PostgreSQL** - Reliable, feature-rich relational database
2. **MongoDB** - Flexible document store for varied data structures
3. **SQLite** - Simple option for small deployments

### Authentication:
- **JWT (JSON Web Tokens)** for stateless authentication
- **OAuth 2.0** for social login (Google, GitHub, etc.)
- **Session-based auth** for traditional approach

## API Endpoints to Implement

### Authentication Endpoints

```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
POST   /api/auth/refresh
GET    /api/auth/me
```

### Student Endpoints

```
GET    /api/students              # List all students (teacher only)
GET    /api/students/:id          # Get student profile
PUT    /api/students/:id          # Update student profile
GET    /api/students/:id/progress # Get student progress
```

### Quiz Endpoints

```
GET    /api/quizzes               # List available quizzes
GET    /api/quizzes/:id           # Get specific quiz
POST   /api/quiz-attempts         # Submit quiz attempt
GET    /api/quiz-attempts         # Get user's quiz history
GET    /api/quiz-attempts/:id     # Get specific attempt details
```

### Coins/Rewards Endpoints

```
GET    /api/coins                 # Get user's coin balance
POST   /api/coins/award           # Award coins (system/teacher)
GET    /api/coins/history         # Get coin transaction history
```

### Code Editor Endpoints

```
POST   /api/code/save             # Save code edits
GET    /api/code/history          # Get user's code history
POST   /api/code/share            # Share code with teacher/peers
GET    /api/code/shared/:id       # View shared code
```

### Teacher Dashboard Endpoints

```
GET    /api/teacher/students      # Get all students in class
GET    /api/teacher/analytics     # Get class analytics
GET    /api/teacher/leaderboard   # Get student leaderboard
POST   /api/teacher/assign-quiz   # Assign quiz to students
```

## Implementation Steps

### Phase 1: Basic Backend Setup
1. Choose your backend framework and set up the project
2. Configure database connection
3. Create database schema/models for:
   - Users (students, teachers)
   - Quiz questions and answers
   - Quiz attempts and scores
   - Coin transactions
   - Code edits

### Phase 2: Authentication
1. Implement user registration and login
2. Add JWT token generation and validation
3. Create middleware for protected routes
4. Add role-based access control (student vs teacher)

### Phase 3: Student Features
1. Migrate quiz functionality to use backend API
2. Store quiz scores in database
3. Implement coin system on backend
4. Add code editor save/load functionality

### Phase 4: Teacher Features
1. Create teacher dashboard API endpoints
2. Implement class/student management
3. Add analytics and reporting
4. Enable quiz assignment and management

### Phase 5: Advanced Features
1. Add real-time updates with WebSockets
2. Implement code sharing and collaboration
3. Add automated code testing/validation
4. Create leaderboards and achievements
5. Add data export for teachers

## Example: FastAPI Implementation

Create a file `api/main.py`:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
import jwt
from datetime import datetime, timedelta

app = FastAPI(title="Snake Learning API")

# Models
class User(BaseModel):
    id: int
    username: str
    email: str
    role: str  # "student" or "teacher"

class QuizAttempt(BaseModel):
    quiz_id: int
    student_id: int
    score: int
    total: int
    timestamp: datetime
    coins_earned: int

class CoinBalance(BaseModel):
    student_id: int
    balance: int
    
# Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Implement JWT validation
    pass

# Endpoints
@app.post("/api/auth/register")
async def register(username: str, email: str, password: str):
    # Implement user registration
    pass

@app.post("/api/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Implement login
    pass

@app.get("/api/students/{student_id}/progress")
async def get_student_progress(student_id: int, current_user: User = Depends(get_current_user)):
    # Return student progress data
    pass

@app.post("/api/quiz-attempts")
async def submit_quiz(attempt: QuizAttempt, current_user: User = Depends(get_current_user)):
    # Save quiz attempt and award coins
    pass

@app.get("/api/teacher/analytics")
async def get_class_analytics(current_user: User = Depends(get_current_user)):
    # Return class-wide analytics (teacher only)
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teacher access required")
    pass
```

## Database Schema Example

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Quiz Attempts Table
```sql
CREATE TABLE quiz_attempts (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES users(id),
    quiz_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    coins_earned INTEGER NOT NULL,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Coin Transactions Table
```sql
CREATE TABLE coin_transactions (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES users(id),
    amount INTEGER NOT NULL,
    reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Code Edits Table
```sql
CREATE TABLE code_edits (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES users(id),
    code_content TEXT NOT NULL,
    description VARCHAR(255),
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Security Considerations

1. **Password Security**
   - Use bcrypt or argon2 for password hashing
   - Enforce strong password policies
   - Implement rate limiting on login attempts

2. **API Security**
   - Use HTTPS in production
   - Implement CORS properly
   - Validate all user inputs
   - Use parameterized queries to prevent SQL injection
   - Implement rate limiting on API endpoints

3. **Data Privacy**
   - Comply with COPPA for children's data (if applicable)
   - Allow students to delete their data
   - Ensure teachers can only access their own students' data
   - Log access to sensitive data

4. **Token Management**
   - Use short-lived access tokens (15-30 minutes)
   - Implement refresh token rotation
   - Store tokens securely on client
   - Implement token revocation

## Deployment Options

1. **Cloud Platforms**
   - Heroku (easy deployment, free tier available)
   - AWS (scalable, many services)
   - Google Cloud Platform
   - Microsoft Azure

2. **Container Deployment**
   - Docker + Docker Compose for local development
   - Kubernetes for production scale
   - Cloud Run (serverless containers)

3. **Serverless**
   - AWS Lambda + API Gateway
   - Google Cloud Functions
   - Vercel/Netlify Functions

## Next Steps

1. Choose your backend technology stack
2. Set up development environment
3. Create database schema
4. Implement authentication first
5. Migrate one feature at a time (start with quiz)
6. Test thoroughly before production deployment
7. Add monitoring and logging
8. Document your API (use Swagger/OpenAPI)

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Express.js Guide](https://expressjs.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT.io](https://jwt.io/) - JWT debugging and resources
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/)
- [REST API Design Best Practices](https://restfulapi.net/)

## Questions?

For questions or contributions to the backend implementation, please open an issue in the repository.
