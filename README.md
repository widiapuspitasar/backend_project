

<h1 align="center">REVOU PROJECT</h1>
<h2 align="center">CAREERSEARCH</h2>

<p align="center">
<img src="\assets\image\CareerSearch_logo.png" width="200" height="150" />
 
<h4 align="center"> GROUP C</h4>

# CAREERSEARCH

CareerSearch is a modern job search platform designed to simplify the job search process and empower users with valuable resources and insights for career development. The platform aims to connect job seekers with relevant job opportunities while providing transparency in application tracking and personalized recommendations.

## Backend README CareerSearch Project 

This repository contains the backend code for a web application built using Flask and SQLAlchemy. It provides an API for managing job applications.

### Technologies Used
- Flask: A lightweight Python web framework.
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library.
- Docker: Containerization platform used to package the application.
- Railway: Deployment platform used to host the application.

### Setup
1. Clone the repository:

```bash
git clone <https://github.com/widiapuspitasar/backend_project.git>
cd backend_project
```

2. Install Depedencies
```bash
pip install -r requirements.txt
```

### Running the Application
To run the application in development mode:
```bash
flask --app index run --debug
```

The application will be accessible at http://localhost:5000.


### Docker
To run the application using Docker:
```bash
docker build -t backend_project .
docker run -p 5000:5000 backend_project
```

### Class Diagram
![Class Diagram](/assets/image/db-schema.png)

### Rest API Architecture System
![Class Diagram](/assets/image/Rest_API_schema.png)

## Building a REST API with Flask, MySQL, Docker, and React

This guide outlines the steps to create a REST API using Flask, MySQL database, Docker, and integrate it with a React frontend.

## Step 1: Prepare MySQL Database
- Ensure you have MySQL server installed.
- Create the necessary database and tables to store data. You can use SQL commands or database management tools like phpMyAdmin.

## Step 2: Create REST API with Flask
- Install Flask and Flask-SQLAlchemy extension to connect Flask with MySQL.
- Develop API endpoints to perform CRUD operations (Create, Read, Update, Delete) on data in the MySQL database.
- Configure MySQL database connection settings in the Flask application.

## Step 3: Dockerize Flask App
- Create a Dockerfile to configure the Docker container for your Flask application.
- Specify dependencies and necessary environment configurations in the Dockerfile.
- Create a docker-compose.yml file if needed to set up services to be used alongside the Flask application, such as MySQL service.

## Step 4: Display API through React
- Develop a React application using Create React App or other React application builders.
- Utilize fetch or axios to make HTTP requests to the API created with Flask.
- Set state and display the data received from the Flask API in React components.

## Example Implementation
- You can create Python models for your MySQL tables using Flask-SQLAlchemy.
- Develop API endpoints using Flask with Flask decorators like @app.route('/').
- Dockerize the Flask application with a Dockerfile that configures the environment and dependencies of the application.
- Create a React application containing components to display data from the Flask API.

## Notes
- Make sure to configure CORS (Cross-Origin Resource Sharing) to allow the React application to communicate with the Flask API running on a different domain.
- Don't forget to connect the Flask application to the MySQL database using the correct configuration, including host, username, password, and database name.


## Prerequisites

Before running the application, make sure you have the following installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- MySQL: [Install MySQL](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)


### API Documentation
Documentation for the API endpoints can be found at https://documenter.getpostman.com/view/32968385/2sA3JM6Lg7

### Deployment
The application can be deployed using Railway:

Set up a Railway project and link it to your repository.
Configure the Railway deployment settings, including environment variables.
Deploy the application to the Railway platform.

### Contact
You can contact our team via email:

- **Widia Puspitasari** (Team Lead | Backend Engineer)  
  Email: [puspitasariwidia@gmail.com](mailto:puspitasariwidia@gmail.com)

- **Kevin Jeonghun** (Frontend Engineer)  
  Email: [kevinjeonghun@gmail.com](mailto:kevinjeonghun@gmail.com)

- **Muhammad Umar** (Frontend Engineer)  
  Email: [umartsqb@gmail.com](mailto:umartsqb@gmail.com)

- **Muhammad Aldiansyah** (Documentation)  
  Email: [aldiansyahwork@gmail.com](mailto:aldiansyahwork@gmail.com)

