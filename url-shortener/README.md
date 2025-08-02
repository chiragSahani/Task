# URL Shortener Service

## Overview
Build a simple URL shortening service similar to bit.ly or tinyurl. This assignment tests your ability to design and implement a small but complete feature from scratch.

## Getting Started

### Prerequisites
- Python 3.8+ installed
- 3 hours of uninterrupted time

### Setup (Should take < 5 minutes)
```bash
# Clone/download this repository
# Navigate to the assignment directory
cd url-shortener

# Install dependencies
pip install -r requirements.txt

# Start the application
python -m flask --app app.main run

# The API will be available at http://localhost:5000
# Run tests with: pytest
```

### What's Provided
- Basic Flask application structure
- Health check endpoints
- One example test
- Empty files for your implementation

## Your Task

### Time Limit: 3 Hours

Build a URL shortener service with the following features:

### Core Requirements

1. **Shorten URL Endpoint**
   - `POST /api/shorten`
   - Accept a long URL in the request body
   - Return a short code (e.g., "abc123")
   - Store the mapping for later retrieval

2. **Redirect Endpoint**
   - `GET /<short_code>`
   - Redirect to the original URL
   - Return 404 if short code doesn't exist
   - Track each redirect (increment click count)

3. **Analytics Endpoint**
   - `GET /api/stats/<short_code>`
   - Return click count for the short code
   - Return creation timestamp
   - Return the original URL

### Technical Requirements

- URLs must be validated before shortening
- Short codes should be 6 characters (alphanumeric)
- Handle concurrent requests properly
- Include basic error handling
- Write at least 5 tests covering core functionality

### Example API Usage

```bash
# Shorten a URL
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'

# Response: {"short_code": "abc123", "short_url": "http://localhost:5000/abc123"}

# Use the short URL (this redirects)
curl -L http://localhost:5000/abc123

# Get analytics
curl http://localhost:5000/api/stats/abc123

# Response: {"url": "https://www.example.com/very/long/url", "clicks": 5, "created_at": "2024-01-01T10:00:00"}
```

## Implementation Guidelines

### What We're Looking For

1. **Code Quality (30%)**
   - Clean, readable code
   - Proper error handling
   - Good API design

2. **Functionality (30%)**
   - All requirements work correctly
   - Handles edge cases appropriately
   - Concurrent request handling

3. **Testing (20%)**
   - Tests for main functionality
   - Tests for error cases
   - Clear test descriptions

4. **Architecture (20%)**
   - Logical code organization
   - Separation of concerns
   - Scalable design decisions

### What to Focus On
- Get core functionality working first
- Use appropriate data structures
- Handle common error cases
- Keep it simple but complete

### What NOT to Do
- Don't implement user authentication
- Don't add a web UI
- Don't implement custom short codes
- Don't add rate limiting
- Don't use external databases (in-memory is fine)

## Evaluation Criteria

Your submission will be evaluated on:
- Core functionality completeness
- Code quality and organization
- Error handling and edge cases
- Test coverage of critical paths
- Clear and pragmatic design decisions

## AI Usage Policy

You are permitted to use AI assistants (ChatGPT, GitHub Copilot, etc.) as you would any other tool. If you use AI significantly, please note in a `NOTES.md` file:
- Which tools you used
- What you used them for
- Any AI-generated code you modified or rejected

## Tips

- Start with the URL shortening logic
- Use Python's built-in data structures
- Don't overthink the short code generation
- Focus on functionality over optimization
- Remember to handle thread safety

## Submission

### Deliverables
1. Your complete implementation
2. All tests passing
3. Brief notes about your approach (optional)

### How to Submit
1. Ensure all tests pass: `pytest`
2. Create a zip of your solution
3. Include any notes about your implementation choices
4. Share the repository link on https://forms.gle/gpaV5LW5boDFk7uT6

## Questions?

If you have questions about the requirements, please email [anand@retainsure.com] within the first 30 minutes of starting.

---

Good luck! We're excited to see your solution.