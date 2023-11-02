# MySQL Student Management System

## Group Members

- Joshua Randez Perez (MAT 918802)
- Simone Madaghiele (MAT 918569)
- Manuel Marceca (MAT 919784)

## Gitlab repository link

https://gitlab.com/MarcecaManu/2023_assignment1_student_records

## Description

This is a Python script for a simple student management system using MySQL. It provides basic functionalities to manage students and their grades in a MySQL database. You can use this script as a starting point for building more advanced student management systems or integrating it into your applications.

## Prerequisites

Before running this script, ensure that you have the following:

- Python installed on your system.
- MySQL server running, and you have the necessary credentials to connect to the database.


## Configuration

The script uses environment variables to configure the MySQL connection. Make sure to set the following environment variables in your system:

- `MYSQL_DATABASE`: The name of the MySQL database.
- `MYSQL_USER`: Your MySQL username.
- `MYSQL_PASSWORD`: Your MySQL password.
- `MYSQL_HOST`: The hostname or IP address of the MySQL server.

You can set these environment variables by exporting them in your shell or by modifying the script to include them directly.

## Usage

This script provides several functions for managing students and their grades. You can use these functions in your Python program as needed.

### 1. `establish_connection()`

This function establishes a connection to the MySQL database using the provided configuration.

### 2. `add_student(db_connection, student_name, student_email)`

Use this function to add a new student to the database. Provide the `db_connection`, `student_name`, and `student_email` as parameters.

### 3. `add_grade(db_connection, student_id, course_name, grade)`

This function adds a grade for a specific student. Provide the `db_connection`, `student_id`, `course_name`, and `grade` as parameters.

### 4. `view_grades(db_connection, student_id)`

View all the grades for a specific student by providing the `db_connection` and `student_id`.

### 5. `view_students(db_connection)`

Retrieve a list of all students in the database by providing the `db_connection`.

### 6. `update_grade(db_connection, grade_id, new_grade)`

Update a student's grade by providing the `db_connection`, `grade_id`, and the `new_grade`.

### 7. `delete_student(db_connection, student_id)`

Delete a student and their associated grades using this function. Provide the `db_connection` and `student_id`.

## Example

Here's an example of how to use these functions:

```python
import mysql.connector
import os

# Import MySQL configuration from environment variables
mysql_database = os.environ.get("MYSQL_DATABASE")
mysql_user = os.environ.get("MYSQL_USER")
mysql_password = os.environ.get("MYSQL_PASSWORD")
mysql_host = os.environ.get("MYSQL_HOST")

# Establish a database connection
db_connection = establish_connection()

# Add a new student
add_student(db_connection, "John Doe", "john@example.com")

# Add a grade for the student
add_grade(db_connection, 1, "Math", 90)

# View all grades for a student
grades = view_grades(db_connection, 1)
print(grades)

# View all students
students = view_students(db_connection)
print(students)

# Update a grade
update_grade(db_connection, 1, 95)

# Delete a student and their grades
delete_student(db_connection, 1)

# Close the database connection when done
db_connection.close()
```

## Continuous Integration/Continuous Deployment (CI/CD) Pipeline Configuration

This YAML file defines a Continuous Integration/Continuous Deployment (CI/CD) pipeline for a Python project. The pipeline automates various stages of software development, including building, testing, verifying, packaging, releasing, and generating documentation.

### Stages

The CI/CD pipeline consists of the following stages:

- **Build**:
    - *Build*: Install project dependencies specified in `requirements.txt`.
    - *Setup Database*: Prepare the MySQL database for integration tests. It sets up the database schema and provides access credentials.

- **Verify**:
    - *Prospector*: Use the Prospector tool to analyze the project's code quality and generate reports.
    - *Bandit*: Use the Bandit tool to perform static code analysis for security issues.

- **Test**:
    - *Integration Test*: Execute integration tests using a pre-configured MySQL database. It verifies that the project integrates with the database correctly.
    - *Unit Test*: Run unit tests on the project code to ensure individual components function as expected.

- **Package**:
    - *Setuptools*: Build Python setuptools and create distribution packages for the project.

- **Release**:
    - *Release*: Upload distribution packages to the Python Package Index (PyPI) for distribution.

- **Docs**: 
    - *Documentation*: Generate project documentation using MkDocs.

### Services

- **MySQL Database (5.7)**: The CI/CD pipeline uses a MySQL database service (version 5.7) for integration testing. It specifies configuration variables for the database, including the database name, root password, user, password, and host.

### Variables

- **Environment Variables**: Various environment variables are set to configure the MySQL database connection, access credentials and PYPI login information. These variables include `MYSQL_DATABASE`, `MYSQL_ROOT_PASSWORD`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `TWINE_USERNAME` and `TWINE_PASSWORD`.

### Script Execution

The YAML file specifies scripts to be executed at each stage of the pipeline. These scripts include installing dependencies, setting up the database, running tests, and generating documentation.

### Artifacts

- **Artifacts**: The pipeline generates and stores artifacts, such as the `db_vars.env` file and SQL dump files.

- **Distribution Packages**: The pipeline creates distribution packages (e.g., wheels and source distributions) and stores them in the `dist/` directory.

### Continuous Integration and Deployment

- The pipeline includes verification stages (`Prospector` and `Bandit`) that only run on specific branches (typically the main branch) to ensure code quality and security before deployment.

- The pipeline is configured to upload distribution packages to the Python Package Index (PyPI) upon successful build and verification.

- Documentation is generated using MkDocs to provide comprehensive project documentation.

