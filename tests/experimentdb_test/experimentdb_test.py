from experimentdb.experimentdb import ExperimentDB
from experimentdb.measurement import Measurement
from sqlalchemy import create_engine, Column, Integer, String, update, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import os

def test_experimentdb(association_table: Table):
    experimentdb = ExperimentDB("2023.03.11_19.30.16", association_table)
    experimentdb.set_name("test name")
    experimentdb.set_experiment_date("2023.03.11_19.30.16")
    experimentdb.set_device("Sunbrick")
    experimentdb.set_notes("Initial test notes")
    experimentdb.add_notes("Additional test notes")
    experimentdb.set_console({"2023.03.11_19.30.16": "Initial test console"})
    experimentdb.add_console("2023.03.11_19.30.17", "Additional test console")

    m = Measurement("G:/My Drive/Data/Sunbrick/2023/01-January/test/Position_1/IV_2022_12_20_09_29_06.txt", "test 1")
    m.set_colour('white')
    n = Measurement("G:/My Drive/Data/Sunbrick/2023/01-January/test/Position_2/IV_2022_12_20_09_29_32.txt", "test 2")
    n.set_colour('white')
    experimentdb.set_all_measurements([m, n])

    o = Measurement("G:/My Drive/Data/Sunbrick/2023/01-January/test/Position_3/IV_2022_12_20_14_11_30.txt", "test 3")
    o.set_colour('white')
    experimentdb.add_measurement(o)

    print(experimentdb.get_name())
    print(experimentdb.get_creation_date())
    print(experimentdb.get_experiment_date())
    print(experimentdb.get_device())
    print(experimentdb.get_notes())
    print(experimentdb.get_console())

    print(experimentdb.get_measurements())


# Provided by SQLAlchemy
Base = declarative_base()

association_table = Table(
    "association_table",
    Base.metadata,
    Column("experiment_id", Integer, ForeignKey("experiment.id")),
    Column("measurement_id", Integer, ForeignKey("measurement.id"))
)
test_experimentdb(association_table)