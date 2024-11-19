from sqlite3 import IntegrityError
import pytest

from sqlalchemy import insert, select, text
from models import User

# test db connection
def test_db_connection(db_session):
    # Use db_session to interact with the database
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1

# test to insert a user
# you can count this as one of your 5 test cases :)
def test_insert_user(db_session, sample_signup_input):
    insert_stmt = insert(User).values(sample_signup_input)

    # execute insert query
    db_session.execute(insert_stmt)
    # commit the changes to the db
    db_session.commit()

    # not part of the app.py code, just being used to get the inserted data
    selected_user = db_session.query(User).filter_by(FirstName="Calista").first()

    assert selected_user is not None
    assert selected_user.LastName == "Phippen"

# Test for logging in the user (valid login)
def test_login_success(db_session, sample_signup_input, successful_login_input):
    # Insert user with plain-text password
    insert_stmt = insert(User).values(sample_signup_input)
    db_session.execute(insert_stmt)
    db_session.commit()

    # Simulate the login with correct email and password (plain-text comparison)
    user = db_session.query(User).filter_by(Email=successful_login_input['Email']).first()
    
    assert user is not None  # Check if user exists
    assert user.Password == successful_login_input['Password']  # Compare the plain-text password

# Test for logging in with invalid credentials (wrong password)
@pytest.mark.xfail
def test_login_invalid(db_session, sample_signup_input, fail_login_input):
    # Insert user with plain-text password
    insert_stmt = insert(User).values(sample_signup_input)
    db_session.execute(insert_stmt)
    db_session.commit()

    # Try to log in with incorrect password
    user = db_session.query(User).filter_by(Email=fail_login_input['Email']).first()

    assert user is not None  # User should exist
    assert user.Password == fail_login_input['Password']  # Password should not match

# Test missing Email for signing up:
@pytest.mark.xfail
def test_insert_user_missing_Email(db_session, missing_signup_input):
    try:
        insert_stmt = insert(User).values(missing_signup_input)
        # execute insert query
        db_session.execute(insert_stmt)
        # commit the changes to the db
        db_session.commit()
        assert False, "Expected a critical database error due to missing required field 'Email', but it didn't happen."
    except IntegrityError as e:
        print(f"Expected critical error occurred: {e}")
        assert True

# Test wrong type  phone number for signing up:
@pytest.mark.xfail
def test_wrong_type_phone_number_user(db_session, wrong_type_signup_input):
    try:
        insert_stmt = insert(User).values(wrong_type_signup_input)

        # execute insert query
        db_session.execute(insert_stmt)
        # commit the changes to the db
        db_session.commit()
        assert False, "Expected a critical database error due to wrong type required field 'PhoneNumber', but it didn't happen."
    except IntegrityError as e:
        print(f"Expected critical error occurred: {e}")
        assert True
