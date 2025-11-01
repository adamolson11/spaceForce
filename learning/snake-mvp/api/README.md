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
