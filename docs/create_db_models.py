# using resolved_model gpt-4o-2024-08-06# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import date   
from datetime import datetime


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py

from sqlalchemy.dialects.sqlite import *


class User(Base):
    """description: Represents a user who can have multiple accesses, groups, and profiles."""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    is_special_user = Column(Boolean, default=False)
    group_id = Column(Integer, ForeignKey('group.id'), nullable=True)
    profile_id = Column(Integer, ForeignKey('profile.id'), nullable=True)
    access_count = Column(Integer, default=0)
    invitation_count = Column(Integer, default=0)


class Group(Base):
    """description: Represents a group of users tied to specific permissions."""
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    user_count = Column(Integer, default=0)


class Profile(Base):
    """description: Represents different profiles defining user permissions."""
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    user_count = Column(Integer, default=0)


class Access(Base):
    """description: Represents permanent access assigned to special users or owners."""
    __tablename__ = 'access'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    door_id = Column(Integer, ForeignKey('door.id'), nullable=False)
    is_permanent = Column(Boolean, default=False)


class Invitation(Base):
    """description: Represents temporary invitations including schedule-based invitations."""
    __tablename__ = 'invitation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    door_id = Column(Integer, ForeignKey('door.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_recurring = Column(Boolean, default=False)


class Door(Base):
    """description: Represents a physical door in a building or house."""
    __tablename__ = 'door'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100), nullable=False)


# end of model classes


try:
    
    
    
    
    # ALS/GenAI: Create an SQLite database
    
    engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    
    Base.metadata.create_all(engine)
    
    
    
    Session = sessionmaker(bind=engine)
    
    session = Session()
    
    
    
    # ALS/GenAI: Prepare for sample data
    
    
    
    session.commit()
    user1 = User(id=1, name="Alice", is_special_user=True, group_id=1, profile_id=1, access_count=0, invitation_count=0)
    user2 = User(id=2, name="Bob", is_special_user=False, group_id=2, profile_id=2, access_count=0, invitation_count=0)
    user3 = User(id=3, name="Charlie", is_special_user=True, group_id=1, profile_id=1, access_count=0, invitation_count=0)
    user4 = User(id=4, name="David", is_special_user=False, group_id=2, profile_id=2, access_count=0, invitation_count=0)
    group1 = Group(id=1, name="Admin", user_count=2)
    group2 = Group(id=2, name="Users", user_count=2)
    profile1 = Profile(id=1, name="FullAccess", user_count=2)
    profile2 = Profile(id=2, name="LimitedAccess", user_count=2)
    access1 = Access(id=1, user_id=1, door_id=1, is_permanent=True)
    access2 = Access(id=2, user_id=3, door_id=2, is_permanent=False)
    access3 = Access(id=3, user_id=2, door_id=1, is_permanent=True)
    access4 = Access(id=4, user_id=4, door_id=2, is_permanent=False)
    invitation1 = Invitation(id=1, user_id=2, door_id=1, start_date=date(2023, 1, 1), end_date=date(2023, 1, 10), is_recurring=False)
    invitation2 = Invitation(id=2, user_id=3, door_id=2, start_date=date(2023, 2, 1), end_date=date(2023, 2, 28), is_recurring=True)
    invitation3 = Invitation(id=3, user_id=4, door_id=1, start_date=date(2023, 3, 15), end_date=date(2023, 3, 25), is_recurring=False)
    invitation4 = Invitation(id=4, user_id=1, door_id=2, start_date=date(2023, 4, 1), end_date=date(2023, 4, 15), is_recurring=True)
    door1 = Door(id=1, description="Main Entrance")
    door2 = Door(id=2, description="Back Door")
    
    
    
    session.add_all([user1, user2, user3, user4, group1, group2, profile1, profile2, access1, access2, access3, access4, invitation1, invitation2, invitation3, invitation4, door1, door2])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
