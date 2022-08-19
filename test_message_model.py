"""Message model tests."""
# remake
# FLASK_ENV=production python3.7 -m unittest test_message_model.py

import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes


os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app,CURR_USER_KEY

db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        
        user_1 = User.signup("test1", "email1@email.com", "password", None)
        user_1_id = 1435
        user_1.id = user_1_id

        db.session.commit()
        u1 = User.query.get(user_1_id)
        self.u1 = u1
        self.user_1_id = user_1_id
 
  
   
        self.client = app.test_client()
     

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        """Does this model work?"""
        m1 = Message(text="t_message",user_id=self.user_1_id)
        
        db.session.add(m1)
        db.session.commit()

        self.assertEqual(len(self.u1.messages), 1)
        self.assertEqual(self.u1.messages[0].text,"t_message")

    def test_message_likes(self):
        m1 = Message(
            text="a warble",
            user_id=self.user_1_id
        )

        m2 = Message(
            text="a very interesting warble",
            user_id=self.user_1_id
        )

        u = User.signup("yetanothertest", "t@email.com", "password", None)
        uid = 888
        u.id = uid
        db.session.add_all([m1, m2, u])
        db.session.commit()

        u.likes.append(m1)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, m1.id)