# Backend API Stubs

This directory contains documentation for the backend API that should be implemented to replace localStorage and add security to the Snake MVP.

## Overview

The current MVP uses localStorage for data persistence, which is:
- **Insecure**: No validation or sanitization
- **Limited**: Data is local to one browser
- **Unscalable**: Can't support multiple users or classrooms
- **Unsafe**: Evaluates user code without sandboxing

A production backend should provide secure authentication, data persistence, and code execution sandboxing.

## Proposed API Endpoints

### Authentication

#### POST /api/auth/register
Register a new user (student or teacher).

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securePassword123",
  "role": "student"
}
```

**Response:**
```json
{
  "success": true,
  "userId": "user_123",
  "token": "jwt_token_here",
  "message": "User registered successfully"
}
```

#### POST /api/auth/login
Authenticate a user and receive a JWT token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "success": true,
  "token": "jwt_token_here",
  "user": {
    "id": "user_123",
    "name": "John Doe",
    "role": "student",
    "coins": 150
  }
}
```

#### POST /api/auth/logout
Invalidate the current session token.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### User Profile

#### GET /api/users/me
Get current user's profile and statistics.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": "user_123",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student",
    "coins": 150,
    "gamesPlayed": 25,
    "highScore": 340,
    "quizzesTaken": 5,
    "createdAt": "2025-01-15T10:30:00Z"
  }
}
```

#### PATCH /api/users/me
Update user profile.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "name": "Johnny Doe"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": "user_123",
    "name": "Johnny Doe",
    "email": "john@example.com"
  }
}
```

### Game Progress

#### POST /api/games/scores
Submit a game score.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "score": 340,
  "duration": 180,
  "level": 1
}
```

**Response:**
```json
{
  "success": true,
  "scoreId": "score_789",
  "highScore": 340,
  "coinsEarned": 34,
  "message": "New high score!"
}
```

#### GET /api/games/scores
Get user's game history.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Query Parameters:**
- `limit`: Number of scores to return (default: 10)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "success": true,
  "scores": [
    {
      "id": "score_789",
      "score": 340,
      "duration": 180,
      "level": 1,
      "playedAt": "2025-01-20T14:30:00Z"
    }
  ],
  "total": 25,
  "highScore": 340
}
```

#### GET /api/games/leaderboard
Get leaderboard for all users.

**Query Parameters:**
- `limit`: Number of entries (default: 10)
- `timeframe`: "daily", "weekly", "monthly", "alltime" (default: "alltime")

**Response:**
```json
{
  "success": true,
  "leaderboard": [
    {
      "rank": 1,
      "userId": "user_456",
      "name": "Jane Smith",
      "score": 580,
      "playedAt": "2025-01-20T10:00:00Z"
    }
  ],
  "timeframe": "alltime"
}
```

### Quiz System

#### GET /api/quizzes
Get available quizzes.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "quizzes": [
    {
      "id": "quiz_1",
      "title": "Python Basics",
      "description": "Test your Python fundamentals",
      "questionCount": 6,
      "coinsPerQuestion": 10,
      "difficulty": "beginner"
    }
  ]
}
```

#### GET /api/quizzes/:id
Get a specific quiz with questions.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "quiz": {
    "id": "quiz_1",
    "title": "Python Basics",
    "questions": [
      {
        "id": "q1",
        "question": "What data structure is best for the snake?",
        "options": ["String", "List", "Dictionary", "Variable"],
        "correctIndex": 1,
        "explanation": "Lists are ordered collections."
      }
    ]
  }
}
```

#### POST /api/quizzes/:id/submit
Submit quiz answers.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "answers": [1, 2, 1, 1, 1, 1]
}
```

**Response:**
```json
{
  "success": true,
  "score": 5,
  "totalQuestions": 6,
  "coinsEarned": 50,
  "results": [
    {
      "questionId": "q1",
      "correct": true,
      "explanation": "Lists are ordered collections."
    }
  ]
}
```

#### GET /api/quizzes/progress
Get user's quiz progress.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "progress": [
    {
      "quizId": "quiz_1",
      "title": "Python Basics",
      "attempts": 3,
      "bestScore": 5,
      "lastAttempt": "2025-01-20T14:30:00Z"
    }
  ]
}
```

### Code Editor & Execution

#### POST /api/code/save
Save user's code.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "language": "python",
  "code": "# Snake game code here...",
  "title": "My Snake Game",
  "description": "Modified snake with faster speed"
}
```

**Response:**
```json
{
  "success": true,
  "codeId": "code_999",
  "message": "Code saved successfully"
}
```

#### GET /api/code
Get user's saved code snippets.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "codes": [
    {
      "id": "code_999",
      "title": "My Snake Game",
      "language": "python",
      "code": "# Code here...",
      "createdAt": "2025-01-20T15:00:00Z",
      "updatedAt": "2025-01-20T15:30:00Z"
    }
  ]
}
```

#### POST /api/code/execute
Execute code in a sandboxed environment.

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "language": "python",
  "code": "print('Hello World')",
  "input": ""
}
```

**Response:**
```json
{
  "success": true,
  "output": "Hello World\n",
  "executionTime": 45,
  "error": null
}
```

### Teacher Dashboard

#### GET /api/teacher/students
Get list of students (teacher/admin only).

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Query Parameters:**
- `classId`: Filter by class (optional)
- `limit`: Number of students (default: 50)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "success": true,
  "students": [
    {
      "id": "user_123",
      "name": "John Doe",
      "email": "john@example.com",
      "coins": 150,
      "gamesPlayed": 25,
      "quizzesTaken": 5,
      "lastActive": "2025-01-20T14:30:00Z"
    }
  ],
  "total": 30
}
```

#### GET /api/teacher/analytics
Get classroom analytics (teacher/admin only).

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "analytics": {
    "totalStudents": 30,
    "activeToday": 15,
    "averageScore": 250,
    "totalQuizzesTaken": 150,
    "averageCoins": 200,
    "topPerformers": [
      {
        "id": "user_456",
        "name": "Jane Smith",
        "score": 580
      }
    ]
  }
}
```

#### POST /api/teacher/quizzes
Create a custom quiz (teacher/admin only).

**Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "title": "Advanced Python",
  "description": "Test advanced concepts",
  "difficulty": "advanced",
  "coinsPerQuestion": 15,
  "questions": [
    {
      "question": "What is a closure?",
      "options": ["A function", "A nested function", "A variable", "A loop"],
      "correctIndex": 1,
      "explanation": "A closure is a nested function that captures variables."
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "quizId": "quiz_999",
  "message": "Quiz created successfully"
}
```

## Implementation Notes

### Security Considerations

1. **Authentication**: Use JWT tokens with proper expiration
2. **Authorization**: Implement role-based access control (RBAC)
3. **Input Validation**: Validate all user inputs server-side
4. **Rate Limiting**: Prevent abuse of API endpoints
5. **Code Execution**: Use Docker containers or sandboxed environments
6. **HTTPS**: All endpoints must use HTTPS in production
7. **CORS**: Configure proper CORS policies
8. **SQL Injection**: Use parameterized queries
9. **XSS Prevention**: Sanitize all user-generated content

### Technology Recommendations

**Backend Framework Options:**
- Node.js + Express + MongoDB
- Python + Flask/FastAPI + PostgreSQL
- Ruby on Rails + PostgreSQL
- Go + Gin + PostgreSQL

**Code Execution Sandboxing:**
- Docker containers with resource limits
- AWS Lambda or Google Cloud Functions
- Judge0 API (third-party code execution service)
- Custom sandbox with Web Workers (client-side)

**Database Schema Example:**
```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL,
  coins INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Scores table
CREATE TABLE scores (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  score INTEGER NOT NULL,
  duration INTEGER NOT NULL,
  level INTEGER NOT NULL,
  played_at TIMESTAMP DEFAULT NOW()
);

-- Quiz attempts table
CREATE TABLE quiz_attempts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  quiz_id UUID NOT NULL,
  score INTEGER NOT NULL,
  total_questions INTEGER NOT NULL,
  coins_earned INTEGER NOT NULL,
  attempted_at TIMESTAMP DEFAULT NOW()
);

-- Code snippets table
CREATE TABLE code_snippets (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  language VARCHAR(50) NOT NULL,
  code TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

## Next Steps

1. Choose a backend technology stack
2. Set up development environment
3. Implement authentication endpoints first
4. Add database schema and migrations
5. Implement core API endpoints
6. Add code execution sandboxing
7. Create admin/teacher dashboard
8. Write API tests
9. Deploy to production environment
10. Update frontend to use real API instead of localStorage

## Testing the API

Use tools like:
- **Postman**: For manual API testing
- **Jest/Mocha**: For automated tests
- **Swagger/OpenAPI**: For API documentation
- **Artillery**: For load testing

Example test case:
```javascript
describe('POST /api/auth/login', () => {
  it('should authenticate valid credentials', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'test@example.com',
        password: 'password123'
      });
    
    expect(response.status).toBe(200);
    expect(response.body.success).toBe(true);
    expect(response.body.token).toBeDefined();
  });
});
```

## Resources

- [JWT Best Practices](https://jwt.io/introduction)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [REST API Design Guide](https://restfulapi.net/)
- [Code Sandboxing Techniques](https://blog.codecentric.de/en/2019/02/sandboxing-javascript/)
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
