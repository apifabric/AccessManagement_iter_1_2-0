# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 10, 2024 21:49:48
# Database: sqlite:////tmp/tmp.LwD85bPrSa/AccessManagement_iter_1_2/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Door(SAFRSBaseX, Base):
    """
    description: Represents a physical door in a building or house.
    """
    __tablename__ = 'door'
    _s_collection_name = 'Door'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    description = Column(String(100), nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    AccessList : Mapped[List["Access"]] = relationship(back_populates="door")
    InvitationList : Mapped[List["Invitation"]] = relationship(back_populates="door")



class Group(SAFRSBaseX, Base):
    """
    description: Represents a group of users tied to specific permissions.
    """
    __tablename__ = 'group'
    _s_collection_name = 'Group'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_count = Column(Integer)

    # parent relationships (access parent)

    # child relationships (access children)
    UserList : Mapped[List["User"]] = relationship(back_populates="group")



class Profile(SAFRSBaseX, Base):
    """
    description: Represents different profiles defining user permissions.
    """
    __tablename__ = 'profile'
    _s_collection_name = 'Profile'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_count = Column(Integer)

    # parent relationships (access parent)

    # child relationships (access children)
    UserList : Mapped[List["User"]] = relationship(back_populates="profile")



class User(SAFRSBaseX, Base):
    """
    description: Represents a user who can have multiple accesses, groups, and profiles.
    """
    __tablename__ = 'user'
    _s_collection_name = 'User'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    is_special_user = Column(Boolean)
    group_id = Column(ForeignKey('group.id'))
    profile_id = Column(ForeignKey('profile.id'))
    access_count = Column(Integer)
    invitation_count = Column(Integer)

    # parent relationships (access parent)
    group : Mapped["Group"] = relationship(back_populates=("UserList"))
    profile : Mapped["Profile"] = relationship(back_populates=("UserList"))

    # child relationships (access children)
    AccessList : Mapped[List["Access"]] = relationship(back_populates="user")
    InvitationList : Mapped[List["Invitation"]] = relationship(back_populates="user")



class Access(SAFRSBaseX, Base):
    """
    description: Represents permanent access assigned to special users or owners.
    """
    __tablename__ = 'access'
    _s_collection_name = 'Access'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    door_id = Column(ForeignKey('door.id'), nullable=False)
    is_permanent = Column(Boolean)

    # parent relationships (access parent)
    door : Mapped["Door"] = relationship(back_populates=("AccessList"))
    user : Mapped["User"] = relationship(back_populates=("AccessList"))

    # child relationships (access children)



class Invitation(SAFRSBaseX, Base):
    """
    description: Represents temporary invitations including schedule-based invitations.
    """
    __tablename__ = 'invitation'
    _s_collection_name = 'Invitation'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    door_id = Column(ForeignKey('door.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_recurring = Column(Boolean)

    # parent relationships (access parent)
    door : Mapped["Door"] = relationship(back_populates=("InvitationList"))
    user : Mapped["User"] = relationship(back_populates=("InvitationList"))

    # child relationships (access children)
