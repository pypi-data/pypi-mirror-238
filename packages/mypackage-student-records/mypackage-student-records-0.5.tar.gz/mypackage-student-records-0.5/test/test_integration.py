from src.mypackage.student_records import add_student, add_grade, view_grades, delete_student, view_students, establish_connection

def test_establish_connection():
    """
    Test establishing a database connection.

    This test ensures that the database connection is successfully established.
    """
    connection = establish_connection()
    assert connection is not None
    connection.close()

def test_add_student_and_grades():
    """
    Test adding a student and their grades to the database.

    This test adds a student and a grade, then checks if the added grade is in the result.
    """
    connection = establish_connection()
    assert connection is not None

    # Test viewing grades for a specific student
    add_student(connection, "Alice Johnson", "alice@example.com")
    add_grade(connection, 1, "History", "B")

    result = view_grades(connection, 1)

    assert (1, 1, 'History', 'B') in result  # Check if the added grade is in the result

def test_delete_student_and_grades():
    """
    Test deleting a student and their associated grades from the database.

    This test adds a student, a grade, and then deletes the student and their grades, checking for success.
    """
    connection = establish_connection()
    assert connection is not None

    # Test deleting a student and their associated grades
    add_student(connection, "Bob Wilsonn", "bobb@example.com")
    add_grade(connection, 2, "Math", "C")

    result = delete_student(connection, 6)
    assert result is True

def test_add_student_and_view_students():
    """
    Test adding students and viewing the list of all students in the database.

    This test adds new students and then checks if they appear in the list of all students.
    """
    connection = establish_connection()
    assert connection is not None

    # Test adding a new student
    add_student(connection, "John Poe", "johnn@example.com")
    add_student(connection, "Alice Johnsonn", "alicee@example.com")
    add_student(connection, "Bob Wilson", "bob@example.com")
    result = view_students(connection)

    assert (3, 'John Poe', 'johnn@example.com') in result
    assert (4, 'Alice Johnsonn', 'alicee@example.com') in result
    assert (5, 'Bob Wilson', 'bob@example.com') in result