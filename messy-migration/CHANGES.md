# CHANGES.md

This document outlines the major changes made to the legacy user management API. The goal of the refactoring was to improve code quality, security, and maintainability while preserving the existing functionality.

## 1. Major Issues Identified

The original codebase had several critical issues that made it unsuitable for production:

*   **No Separation of Concerns**: All the application logic, including routes, database interactions, and business logic, was contained in a single `app.py` file. This made the code difficult to read, maintain, and test.
*   **Critical Security Vulnerabilities**:
    *   **Plain Text Passwords**: Passwords were stored and managed in plain text, which is a major security risk.
    *   **SQL Injection**: The search endpoint was vulnerable to SQL injection attacks due to the use of f-strings to construct the query.
    *   **Lack of Input Validation**: There was no validation for email formats, password strength, or other user inputs.
*   **Poor Development Practices**:
    *   **Inefficient Database Management**: A new database connection was opened and closed for every request, which is inefficient.
    *   **Generic Error Handling**: The application used a generic `except Exception` block, which returned a `500 Internal Server Error` for all types of errors, hiding the root cause of issues.
    *   **Hardcoded Configuration**: The application had hardcoded configuration values, such as the debug mode setting.
*   **Unreliable Tests**: The tests were not independent, relied on a persistent database state, and did not cover failure scenarios.

## 2. Changes Made and Justification

To address these issues, the following changes were implemented:

### a. Code Organization

The project was restructured to follow best practices for a Flask application:

*   **Created a `src` directory**: The application's source code was moved to a `src` directory to separate it from other project files.
*   **Modularized the Code**: The application was split into several modules:
    *   `src/main.py`: The application's entry point.
    *   `src/routes.py`: Contains all the API endpoints.
    *   `src/database.py`: Manages the database connection.
    *   `src/config.py`: Manages the application's configuration.
    *   `src/errors.py`: Handles custom error pages.
*   **Used an Application Factory**: An application factory (`create_app`) was introduced in `src/__init__.py` to make the application more modular and easier to test.

**Justification**: This new structure promotes a clear separation of concerns, making the code more organized, reusable, and easier to maintain.

### b. Security Improvements

The following security enhancements were made:

*   **Password Hashing**: Passwords are now hashed using `bcrypt` before being stored in the database. The `login` endpoint was updated to compare the provided password with the stored hash.
*   **Prevented SQL Injection**: The SQL injection vulnerability in the `search_users` endpoint was fixed by using parameterized queries.
*   **Input Validation**: Basic email validation was added to the `create_user` and `update_user` endpoints.

**Justification**: These changes address the most critical security vulnerabilities, making the application more secure and resilient to common attacks.

### c. Best Practices

The following best practices were implemented:

*   **Improved Database Management**: The database connection is now managed using Flask's application context (`g`), which ensures that the connection is created once per request and closed automatically.
*   **Enhanced Error Handling**: A centralized error handling mechanism was implemented to provide more specific error messages and appropriate HTTP status codes. Generic `try-except` blocks were replaced with more specific error handling.
*   **Configuration Management**: Application settings are now managed in a `config.py` file, allowing for different configurations for development, testing, and production.

**Justification**: These improvements make the code more robust, efficient, and easier to debug.

### d. Enhanced Test Suite

The test suite was significantly improved:

*   **Test Isolation**: The tests were refactored to be independent of each other.
*   **In-Memory Database**: The tests now use a temporary, in-memory SQLite database, which ensures that each test runs in a clean environment.
*   **Failure Case Coverage**: New tests were added to cover failure scenarios, such as creating a user with a duplicate email or logging in with an incorrect password.

**Justification**: A reliable test suite is essential for ensuring the quality and stability of the application. These changes make the tests more robust and trustworthy.

## 3. Assumptions and Trade-offs

*   **Simplicity over Complexity**: The refactoring focused on addressing the most critical issues without over-engineering the solution. For example, I did not introduce an ORM like SQLAlchemy to keep the changes focused and the scope manageable.
*   **Authentication and Authorization**: While password security was improved, the application still lacks a comprehensive authentication and authorization system (e.g., JWT tokens). This was considered out of scope for this refactoring task.
*   **Basic Input Validation**: The input validation is still basic. In a real-world application, a more comprehensive validation library like `Pydantic` or `Marshmallow` would be used.

## 4. What I'd Do With More Time

Given more time, I would:

*   **Implement a Token-Based Authentication System**: Use JWT to secure the endpoints and manage user sessions.
*   **Add More Comprehensive Input Validation**: Integrate a library like `Pydantic` to validate all incoming data.
*   **Introduce an ORM**: Use SQLAlchemy to abstract the database interactions and make the code more maintainable.
*   **Containerize the Application**: Use Docker to create a reproducible environment for the application.
*   **Add Logging and Monitoring**: Integrate a logging library to capture important events and monitor the application's health.
*   **Set up a CI/CD Pipeline**: Automate the testing and deployment process.
