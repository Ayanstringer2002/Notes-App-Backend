"""
System routes: /about, /openapi.json
"""

from flask import Blueprint, jsonify
import json

system_bp = Blueprint('system', __name__)

@system_bp.route('/about', methods=['GET'])
def about():
    """
    Get information about the API and developer
    
    Endpoint: GET /about
    
    Response: Information about the service and features
    """
    return jsonify({
        "name": "Ayan",
        "email": "ayan.email@example.com",
        "my_features": {
            "Note Sharing": "Users can share notes with other registered users via email. This enables collaboration and knowledge sharing across teams.",
            "Full-Text Search": "Search notes by keyword in title and content. Supports complex queries and returns matching notes in real-time.",
            "Note Pagination": "GET /notes endpoint supports pagination with page and per_page parameters for efficient data retrieval.",
            "Unshare Notes": "Users can revoke access to previously shared notes via POST /notes/{id}/unshare endpoint.",
            "JWT Authentication": "Secure token-based authentication using JWT. Tokens expire after 30 days for enhanced security.",
            "Input Validation": "Comprehensive validation for all inputs including email format, password strength, and note content limits."
        }
    }), 200


@system_bp.route('/openapi.json', methods=['GET'])
def openapi_spec():
    """
    Get OpenAPI specification for the API
    
    Endpoint: GET /openapi.json
    
    Response: OpenAPI 3.0 specification
    """
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Multi-User Notes Service API",
            "description": "A REST API backend for managing users and their personal notes with sharing capabilities",
            "version": "1.0.0",
            "contact": {
                "name": "Your Name",
                "email": "your.email@example.com"
            }
        },
        "servers": [
            {
                "url": "https://your-notes-app.com",
                "description": "Production server"
            }
        ],
        "paths": {
            "/register": {
                "post": {
                    "summary": "Register a new user",
                    "tags": ["Authentication"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "email": {"type": "string", "format": "email"},
                                        "password": {"type": "string", "minLength": 6}
                                    },
                                    "required": ["email", "password"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "User registered successfully"},
                        "400": {"description": "Bad request"},
                        "409": {"description": "Email already registered"}
                    }
                }
            },
            "/login": {
                "post": {
                    "summary": "Authenticate user and get JWT token",
                    "tags": ["Authentication"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "email": {"type": "string", "format": "email"},
                                        "password": {"type": "string"}
                                    },
                                    "required": ["email", "password"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Login successful"},
                        "401": {"description": "Invalid credentials"}
                    }
                }
            },
            "/notes": {
                "get": {
                    "summary": "Get all notes for authenticated user",
                    "tags": ["Notes"],
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}},
                        {"name": "per_page", "in": "query", "schema": {"type": "integer", "default": 10}}
                    ],
                    "responses": {
                        "200": {"description": "List of notes"},
                        "401": {"description": "Unauthorized"}
                    }
                },
                "post": {
                    "summary": "Create a new note",
                    "tags": ["Notes"],
                    "security": [{"BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string", "maxLength": 255},
                                        "content": {"type": "string", "maxLength": 10000}
                                    },
                                    "required": ["title", "content"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Note created successfully"},
                        "400": {"description": "Bad request"},
                        "401": {"description": "Unauthorized"}
                    }
                }
            },
            "/notes/{id}": {
                "get": {
                    "summary": "Get a specific note by ID",
                    "tags": ["Notes"],
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "responses": {
                        "200": {"description": "Note details"},
                        "401": {"description": "Unauthorized"},
                        "403": {"description": "Access denied"},
                        "404": {"description": "Note not found"}
                    }
                },
                "put": {
                    "summary": "Update a note",
                    "tags": ["Notes"],
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string", "maxLength": 255},
                                        "content": {"type": "string", "maxLength": 10000}
                                    },
                                    "required": ["title", "content"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Note updated successfully"},
                        "400": {"description": "Bad request"},
                        "401": {"description": "Unauthorized"},
                        "403": {"description": "Access denied"},
                        "404": {"description": "Note not found"}
                    }
                },
                "delete": {
                    "summary": "Delete a note",
                    "tags": ["Notes"],
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "responses": {
                        "204": {"description": "Note deleted successfully"},
                        "401": {"description": "Unauthorized"},
                        "403": {"description": "Access denied"},
                        "404": {"description": "Note not found"}
                    }
                }
            },
            "/notes/{id}/share": {
                "post": {
                    "summary": "Share a note with another user",
                    "tags": ["Notes"],
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "share_with_email": {"type": "string", "format": "email"}
                                    },
                                    "required": ["share_with_email"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Note shared successfully"},
                        "400": {"description": "Bad request"},
                        "401": {"description": "Unauthorized"},
                        "403": {"description": "Access denied"},
                        "404": {"description": "Note or user not found"}
                    }
                }
            },
            "/search": {
                "get": {
                    "summary": "Search notes by keyword",
                    "tags": ["Notes"],
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {"name": "q", "in": "query", "required": True, "schema": {"type": "string", "minLength": 2}}
                    ],
                    "responses": {
                        "200": {"description": "Search results"},
                        "400": {"description": "Bad request"},
                        "401": {"description": "Unauthorized"}
                    }
                }
            },
            "/about": {
                "get": {
                    "summary": "Get API information",
                    "tags": ["System"],
                    "responses": {
                        "200": {"description": "API information"}
                    }
                }
            },
            "/openapi.json": {
                "get": {
                    "summary": "Get OpenAPI specification",
                    "tags": ["System"],
                    "responses": {
                        "200": {"description": "OpenAPI specification"}
                    }
                }
            }
        },
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        },
        "tags": [
            {"name": "Authentication", "description": "User registration and login"},
            {"name": "Notes", "description": "Note CRUD and sharing operations"},
            {"name": "System", "description": "System information endpoints"}
        ]
    }
    
    return jsonify(spec), 200