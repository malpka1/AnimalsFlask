# Flask Animals App

## Overview
This Flask application allows users to add animals to a database using both synchronous and asynchronous methods. The asynchronous operations are managed with Celery and Redis.

## Features
- **Synchronous Animal Creation:** Add animals to the database instantly through a simple web form.
- **Asynchronous Animal Creation:** Submit animals to be added in the background using Celery and Redis, allowing for better performance and scalability.
- **User-friendly Interface:** Simple and clean interface for adding and viewing animals.

## Technologies Used
- **Flask:** A lightweight WSGI web application framework.
- **SQLAlchemy:** SQL toolkit and Object-Relational Mapping (ORM) library for the database.
- **Celery:** Asynchronous task queue/job queue based on distributed message passing.
- **Redis:** In-memory data structure store, used as a message broker for Celery.
