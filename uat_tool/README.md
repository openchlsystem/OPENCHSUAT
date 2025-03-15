# UAT Tool API Documentation

[![API Status](https://img.shields.io/badge/status-active-brightgreen)](https://yourapi.statuspage.io)
[![OpenAPI Spec](https://img.shields.io/badge/OpenAPI-3.0-success)](http://localhost:8000/api/schema/)
[![Authentication](https://img.shields.io/badge/auth-JWT%20%2B%20OTP-orange)]()

A comprehensive User Acceptance Testing management system API with WhatsApp-based OTP authentication.

## 📚 Table of Contents
- [Interactive Documentation](#-interactive-documentation)
- [Authentication](#-authentication)
- [API Endpoints](#-api-endpoints)
- [Data Schemas](#-data-schemas)
- [Examples](#-examples)
- [Error Handling](#-error-handling)
- [Development Setup](#-development-setup)

## 🌐 Interactive Documentation
Explore our live API documentation using Swagger UI:  
`http://localhost:8000/api/docs/`

[![Swagger UI](https://i.imgur.com/4jJdQ9T.png)](http://localhost:8000/api/docs/)

**Features:**
- Live endpoint testing
- Model schemas visualization
- Direct API requests from browser
- Authentication configuration

Access raw OpenAPI schema:  
`http://localhost:8000/api/schema/`

## 🔒 Authentication
### JWT + OTP Flow
```mermaid
sequenceDiagram
    User->>API: POST /auth/request-otp (whatsapp_number)
    API->>User: OTP via WhatsApp
    User->>API: POST /auth/verify-otp (whatsapp_number, otp)
    API->>User: Access + Refresh Tokens