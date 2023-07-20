from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Company(Base):
    __tablename__ = "t_company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    departments = relationship("Department", back_populates="company")


class Department(Base):
    __tablename__ = "t_department"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    company_id = Column(Integer, ForeignKey("t_company.id"))
    company = relationship("Company", back_populates="departments")
    employees = relationship("Employee", back_populates="department")


class Role(Base):
    __tablename__ = "t_role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Employee(Base):
    __tablename__ = "t_employee"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    title = Column(String, index=True)
    bio = Column(String)
    is_active = Column(Boolean, default=True)
    age = Column(Integer)
    department_id = Column(Integer, ForeignKey("t_department.id"))
    department = relationship("Department", back_populates="employees")
    role_id = Column(Integer, ForeignKey("t_role.id"))
    role = relationship("Role")
