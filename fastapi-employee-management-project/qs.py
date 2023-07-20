from sqlalchemy.orm import Session

import models
import schemas

# Company


def create_company(db: Session, payload: schemas.CompanyCreate):
    new_company = models.Company(**payload.model_dump())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()


def delete_company(db: Session, company_id: int):
    company = db.query(models.Company).where(
        models.Company.id == company_id).first()
    db.delete(company)
    db.commit()


def update_company(db: Session, company_id: int, payload: schemas.CompanyBase):
    company = db.query(models.Company).where(
        models.Company.id == company_id).first()
    company.name = payload.name
    db.commit()
    db.refresh(company)
    return company

#  Department


def create_department(db: Session, payload: schemas.DepartmentCreate, company_id: int):
    new_department = models.Department(**payload.model_dump(),
                                       company_id=company_id)
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


def get_department(db: Session, department_id: int):
    return db.query(models.Department).filter(models.Department.id == department_id).first()


def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Department).offset(skip).limit(limit).all()


def delete_department(db: Session, department_id: int):
    department = db.query(models.Department).where(
        models.Department.id == department_id).first()
    db.delete(department)
    db.commit()


def update_department(db: Session, department_id: int, payload: schemas.DepartmentBase):
    department = db.query(models.Department).where(
        models.Department.id == department_id).first()
    department.name = payload.name
    db.commit()
    db.refresh(department)
    return department

# Role


def create_role(db: Session, payload: schemas.RoleCreate):
    new_role = models.Role(**payload.model_dump())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()


def delete_role(db: Session, role_id: int):
    role = db.query(models.Role).where(models.Role.id == role_id).first()
    db.delete(role)
    db.commit()


def update_role(db: Session, role_id: int, payload: schemas.RoleBase):
    role = db.query(models.Role).where(models.Role.id == role_id).first()
    role.name = payload.name
    db.commit()
    db.refresh(role)
    return role

# Employee


def delete_employee(db: Session, employee_id: int):
    employee = db.query(models.Employee).where(
        models.Employee.id == employee_id).first()
    db.delete(employee)
    db.commit()


def update_employee(db: Session, employee_id: int, payload: schemas.EmployeeBase, department_id, role_id):
    employee = db.query(models.Employee).where(
        models.Employee.id == employee_id).first()
    employee.firstname = payload.firstname
    employee.lastname = payload.lastname
    employee.title = payload.title
    employee.bio = payload.bio
    employee.age = payload.age
    employee.department_id = department_id
    employee.role_id = role_id
    db.commit()
    db.refresh(employee)
    return employee


def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()


def create_employee(db: Session, payload: schemas.EmployeeCreate, department_id: int, role_id: int):
    new_employee = models.Employee(
        **payload.model_dump(),
        department_id=department_id,
        role_id=role_id,
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee
