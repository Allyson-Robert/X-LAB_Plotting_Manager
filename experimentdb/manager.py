"""
    Responsible for managing the experiment database.
    This loads, saves and updates the database as required by the GUI/user.
"""
from experimentdb import ExperimentDB
from sqlalchemy import create_engine, Column, Integer, String, update, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


