# User Metrics Ingestion Pipeline
## Overview
This project provides a solution for ingesting user metrics data into a PostgreSQL database. The pipeline consists of a Flask-based application for data ingestion and a PostgreSQL database to store the metrics. The solution is containerized using Docker and orchestrated with Docker Compose for ease of deployment.
## Table of Contents
1. Setup and Run Instructions
2. Database Schema Explanation
3. Stored Procedures
4. Maintenance and Extension Guidelines
5. Assumptions
6. Potential Limitations
7. Future Improvements
## Setup and Run Instructions
### Prerequisites
- Docker
- Docker Compose
### Steps to Set Up and Run
1. **Clone the Repository:**
`git clone repo-url`
`cd repo-directory`
2. **Environment Configuration:**
Ensure the .env file contains the correct database credentials and configurations.
3. **Build and Run the Containers:**
Use Docker Compose to build and start the application and database containers:
`docker-compose up --build`
This command will build the Docker images and start the containers. The application will be accessible at `http://localhost:5001`
4. **Verify Setup:**
You can verify the application is running by accessing the health check endpoint:
`curl http://localhost:5001/health`
You should get a response indicating the service is healthy.
5. **Stopping the Containers:**
`docker-compose down`

## Stored Procedures
1. Aggregate User Metrics (Aggregates total talked time and counts distinct sessions for individual users)
2. Get Session Details (Provides details about a specific session, including the user's name, email, session timings, and device information used during the session)
3. Generate Weekly Report (Generates a weekly report summarizing user activity across the system. It reports on session counts, total talked time, and the date of the last session for each user over the past week)
 
## Maintenance and Extension Guidelines
- Monitor application logs (ingestion.log) to detect and troubleshoot issues.
- Implement additional features such as user authentication.

## Assumptions
- Each user has a unique email address.
- Metrics are sent in a JSON format with all required fields present.

## Potential Limitations
- The current implementation uses threading, which may not be suitable for high concurrency scenarios.

## Future Improvements
- Implement user authentication and authorization for accessing the ingestion endpoints.

   
