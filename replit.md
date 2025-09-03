# VaultLogic - AI Document Intelligence Platform

## Overview

VaultLogic is an enterprise-grade AI document intelligence platform that provides secure, on-premise document analysis and Q&A capabilities. The application is built as a Flask-based web application that serves as a marketing website and product demo for an AI-powered document processing system. The platform emphasizes security, compliance, and offline processing, targeting enterprise customers who need to analyze sensitive documents without sending data to external services.

The application features a comprehensive marketing website with pages for features, pricing, security information, and an interactive demo that simulates document intelligence capabilities. It includes a contact form for demo requests and a chat interface that demonstrates how users would interact with the AI system using predefined compliance handbook content.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework Architecture
The application uses Flask as the primary web framework with a modular structure. The main application is initialized in `app.py` with CSRF protection via Flask-WTF and proxy support for deployment behind load balancers. Routes are separated into a dedicated `routes.py` module for maintainability.

### Data Model Design
The system uses a dataclass-based approach for data modeling without a traditional database. Three main models are defined: `ComplianceSection` for handbook content structure, `ChatMessage` for chat interactions, and `DemoRequest` for contact form data. This approach suggests the application is primarily content-driven rather than data-intensive.

### Content Management System
Compliance handbook content is managed through a hybrid approach using both structured Python data (`compliance_data.py`) and a text file (`compliance_handbook.txt`). The content covers various compliance frameworks including SOC 2, GDPR, HIPAA, and ISO 27001. This suggests the platform targets highly regulated industries.

### Frontend Architecture
The frontend uses a traditional server-side rendered approach with Jinja2 templates extending a base layout. Bootstrap 5 provides the UI framework with custom CSS for branding. JavaScript functionality is modular, with separate files for general functionality (`main.js`) and chat-specific features (`chat.js`).

### Form Handling and Validation
Forms are implemented using Flask-WTF with server-side validation. Two primary forms exist: a demo request form for lead generation and a chat form for the interactive demo. CSRF protection is enabled across all forms.

### Security Implementation
The application implements several security measures including CSRF protection, secure session management, and proxy-aware configuration. The emphasis on on-premise deployment and offline processing indicates a security-first architectural approach.

## External Dependencies

### Frontend Libraries
- **Bootstrap 5.3.0**: UI framework and responsive design components
- **Font Awesome 6.4.0**: Icon library for consistent iconography
- **jQuery**: JavaScript library for DOM manipulation and AJAX interactions

### Python Web Framework
- **Flask**: Core web framework for routing, templating, and request handling
- **Flask-WTF**: Form handling, validation, and CSRF protection
- **Werkzeug**: WSGI utilities including ProxyFix middleware

### Development and Deployment
- **Python logging module**: Application logging and debugging
- **Jinja2**: Template engine (included with Flask)

### Static Asset Management
All CSS and JavaScript assets are served locally with CDN fallbacks for third-party libraries, maintaining the security-focused approach of keeping resources within the application boundary.

The architecture suggests this is a demonstration/marketing application for a larger AI document processing platform, with the actual AI processing capabilities referenced but not implemented in this codebase.