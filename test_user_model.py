"""User model tests."""

# run these tests like:

# FLASK_ENV=production python3.7 -m unittest test_user_model.py

import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        user_1 = User.signup("test1", "email1@email.com", "password", None)
        user_1_id = 1435
        user_1.id = user_1_id

        user_2 = User.signup("test2", "email2@email.com", "password", None)
        user_2_id = 3423
        user_2.id= user_2_id

        db.session.commit()

        u1 = User.query.get(user_1_id)
        u2 = User.query.get(user_2_id)

        self.u1 = u1
        self.user_1_id = user_1_id

        self.u2 = u2
        self.user_2_id = user_2_id

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
    
    def test_repr_method(self):
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        

        self.assertEqual(u.__repr__(), "<User #None: testuser, test@test.com>")

    def test_user_follows(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertEqual(len(self.u2.following), 0)
        self.assertEqual(len(self.u2.followers),1)

        self.assertTrue(self.u2.is_followed_by(self.u1))

    def test_is_followed_by(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertFalse(self.u1.is_followed_by(self.u2))
        self.assertTrue(self.u2.is_followed_by(self.u1))

    def test_is_following(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_following(self.u1))


   # Signup Tests


    def test_valid_signup(self):
        user_test = User.signup("Markymark","marky@gmail.com", "HASHED_P", None)
        user_test_id = 102020
        user_test.id = user_test_id
        db.session.commit()

        u_test = User.query.get(user_test_id)
        self.assertEqual(u_test.username,"Markymark")
        self.assertEqual(u_test.email,"marky@gmail.com")
        self.assertEqual(u_test.password,"HASHED_P")
    
    def test_invalid_username_signup(self):
        user_test = User.signup(None,"marky@gmail.com", "HASHED_P", None)
        user_test_id = 102020
        user_test.id = user_test_id
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
        
        
