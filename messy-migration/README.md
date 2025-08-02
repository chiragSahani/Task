# Code Refactoring Challenge

## Overview
You've inherited a legacy user management API that works but has significant issues. Your task is to refactor and improve this codebase while maintaining its functionality.

## Getting Started

### Prerequisites
- Python 3.8+ installed
- 3 hours of uninterrupted time

### Setup (Should take < 5 minutes)
```bash
# Clone/download this repository
# Navigate to the assignment directory
cd messy-migration

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py

# Start the application
python app.py

# The API will be available at http://localhost:5000
```

### Testing the Application
The application provides these endpoints:
- `GET /` - Health check
- `GET /users` - Get all users
- `GET /user/<id>` - Get specific user
- `POST /users` - Create new user
- `PUT /user/<id>` - Update user
- `DELETE /user/<id>` - Delete user
- `GET /search?name=<name>` - Search users by name
- `POST /login` - User login

## Your Task

### Time Limit: 3 Hours

Refactor this codebase to improve its quality, security, and maintainability. The application currently works but has numerous issues that need addressing.

### What We're Looking For

1. **Code Organization (25%)**
   - Proper separation of concerns
   - Clear project structure
   - Meaningful function/variable names

2. **Security Improvements (25%)**
   - Identify and fix security vulnerabilities
   - Implement proper data validation
   - Secure sensitive information

3. **Best Practices (25%)**
   - Error handling
   - Proper HTTP status codes
   - Code reusability

4. **Documentation (25%)**
   - Clear explanation of changes made
   - Justification for architectural decisions
   - Any trade-offs you made

### What to Focus On
- Identify the most critical issues first
- Make the code production-ready
- Ensure the API remains functional
- Write at least a few tests for critical functionality

### What NOT to Do
- Don't add new features or endpoints
- Don't spend time on UI/frontend
- Don't over-engineer the solution
- Don't aim for 100% test coverage
- Don't create extensive documentation beyond explaining your changes

## Submission

### Deliverables
1. Your refactored code
2. A `CHANGES.md` file documenting:
   - Major issues you identified
   - Changes you made and why
   - Any assumptions or trade-offs
   - What you would do with more time

### How to Submit
1. Create a new git repository with your solution
2. Include all necessary files to run the application
3. Ensure `python app.py` still works after setup
4. Share the repository link on https://forms.gle/gpaV5LW5boDFk7uT6

## Evaluation Criteria

We will evaluate your submission based on:
- Identification of critical issues
- Quality of solutions implemented
- Code readability and organization
- Pragmatic decision-making
- Clear communication of changes

## AI Usage Policy

You are permitted to use AI assistants (ChatGPT, GitHub Copilot, etc.) as you would any other tool. If you use AI significantly, please note in your CHANGES.md:
- Which tools you used
- What you used them for
- Any AI-generated code you modified or rejected

## Questions?

If you have questions about the requirements, please email [anand@retainsure.com] within the first 30 minutes of starting.

---

Remember: We're not looking for perfection. We want to see how you approach real-world code problems, prioritize improvements, and communicate your decisions.