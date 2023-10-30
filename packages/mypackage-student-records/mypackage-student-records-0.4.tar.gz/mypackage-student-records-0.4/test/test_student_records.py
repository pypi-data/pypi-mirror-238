from src.mypackage.student_records import add_student, add_grade, view_grades, view_students, update_grade, \
    delete_student, establish_connection


def test_establish_connection():
    """
    Test establishing a database connection.

    This test ensures that the database connection is successfully established.
    """
    connection = establish_connection()
    assert connection is not None
    connection.close()


def test_add_student():
    """
    Test adding a student to the database.

    This test adds a student and checks if the addition is successful.
    """
    connection = establish_connection()
    assert connection is not None

    student_name = "John Doe"
    student_email = "john.doe@example.com"

    result = add_student(connection, student_name, student_email)
    assert result is True

    connection.close()


def test_add_grade():
    """
    Test adding a grade for a student.

    This test adds a grade for a student and checks if the addition is successful.
    """
    connection = establish_connection()
    assert connection is not None

    # Add a grade for the test student
    student_id = 1  # Assuming this is the ID of the newly added student
    course_name = "Math"
    grade = 90
    result = add_grade(connection, student_id, course_name, grade)
    assert result is True

    connection.close()


def test_view_grades():
    """
    Test viewing grades for a specific student.

    This test retrieves the grades for a specific student and checks if the result is a list.
    """
    connection = establish_connection()
    student_id = 1  # Replace with a valid student_id

    # Act
    grades = view_grades(connection, student_id)

    assert isinstance(grades, list)


def test_view_student():
    """
    Test viewing the list of all students in the database.

    This test retrieves the list of all students and checks if the result is a list.
    """
    connection = establish_connection()
    assert connection is not None

    students = view_students(connection)

    assert isinstance(students, list)


def test_update_grade():
    """
    Test updating a student's grade.

    This test updates a student's grade and checks if the update is successful.
    """
    connection = establish_connection()
    assert connection is not None

    # Test updating a student's grade
    result = update_grade(connection, 1, "B")
    assert result is True


def test_delete_student():
    """
    Test deleting a student and their associated data from the database.

    This test deletes a student and their associated data and checks if the deletion is successful.
    """
    connection = establish_connection()
    assert connection is not None

    result = delete_student(connection, 1)
    assert result is True