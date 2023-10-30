from abc import abstractmethod

from sqlalchemy import Column, Float, Integer, ForeignKey, String, JSON, Identity
from sqlalchemy.ext.declarative import declarative_base

MSCHM_Base = declarative_base()

class MSCHMModel(MSCHM_Base):

    __abstract__ = True

    @property
    @abstractmethod
    def __tablename__(self) -> str:
        pass

    @classmethod
    def get_key(cls, key: str):
        return f'{cls.__tablename__}.{key}'

    @classmethod
    def get_key_id(cls):
        return cls.get_key("id")

    id = Column(Integer, Identity(start=1), primary_key=True)

class BasicWork(MSCHMModel):

    __tablename__ = "basic_works"

    name = Column(String, nullable=False)


class BasicResource(MSCHMModel):

    __tablename__ = "basic_resources"

    name = Column(String, nullable=False)


class Precalculation(MSCHMModel):

    __tablename__ = "precalculations"

    work_value = Column(Float, nullable=False)
    res_value = Column(Float, nullable=False)
    probability = Column(Integer, nullable=False)
    work_value_probability = Column(Float, nullable=False)

    # Foreign Keys
    id_basic_work = Column(Integer, ForeignKey(BasicWork.get_key_id()), nullable=False, index=True)
    id_basic_resource = Column(Integer, ForeignKey(BasicResource.get_key_id()), nullable=False, index=True)


class WorkModel(MSCHMModel):
    __tablename__ = "work_models"

    id_basic_work = Column(Integer, ForeignKey(BasicWork.get_key_id()))


class Unit(MSCHMModel):

    __tablename__ = "units"

    name = Column(String, nullable=False)


class Parameter(MSCHMModel):
    __tablename__ = "parameters"

    mean = Column(Float, default=0)
    regressor_obj = Column(JSON)
    regressor = Column(String)
    variance = Column(Float)
    serialization = Column(String)

    id_unit = Column(Integer, ForeignKey(Unit.get_key_id()))
    id_model = Column(Integer, ForeignKey(WorkModel.get_key_id()))


class Edge(MSCHMModel):
    __tablename__ = "edges"

    id_model = Column(Integer, ForeignKey(WorkModel.get_key_id()))
    id_start = Column(Integer, ForeignKey(Unit.get_key_id()))
    id_finish = Column(Integer, ForeignKey(Unit.get_key_id()))


class UnitType(MSCHMModel):
    __tablename__ = "types"

    value = Column(String)

    id_unit = Column(Integer, ForeignKey(Unit.get_key_id()))
    id_model = Column(Integer, ForeignKey(WorkModel.get_key_id()))


class Sign(MSCHMModel):
    __tablename__ = "signs"

    value = Column(String)

    id_unit = Column(Integer, ForeignKey(Unit.get_key_id()))
    id_model = Column(Integer, ForeignKey(WorkModel.get_key_id()))
