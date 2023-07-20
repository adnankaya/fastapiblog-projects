import pathlib
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from sqlalchemy.orm import Session
#  internals
import qs
import models
import schemas
from database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# app create
app = FastAPI()

BASE_DIR = pathlib.Path(__file__).parent
print(BASE_DIR)
templates = Jinja2Templates(directory=[
    BASE_DIR / "templates",
])
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/', response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    context = {
        "request": request,
        "title": "Home Page"
    }
    response = templates.TemplateResponse("index.html", context)
    return response


@app.get('/employees/create/', response_class=HTMLResponse)
async def create_employee_page(request: Request, db: Session = Depends(get_db)):
    departments = qs.get_departments(db)
    roles = qs.get_roles(db)
    context = {
        "request": request,
        "roles": roles,
        "departments": departments,
        "title": "Employee create Page"
    }
    response = templates.TemplateResponse("employee/create.html", context)
    return response


@app.post('/employees/', response_class=RedirectResponse)
async def create_employee(request: Request,
                          firstname: str = Form(...),
                          lastname: str = Form(...),
                          title: str = Form(...),
                          bio: str = Form(...),
                          age: int = Form(...),
                          department_id: int = Form(...),
                          role_id: int = Form(...),
                          db: Session = Depends(get_db)):
    qs.create_employee(db=db, payload=schemas.EmployeeCreate(firstname=firstname,
                                                             lastname=lastname,
                                                             title=title,
                                                             bio=bio,
                                                             age=age),
                       department_id=department_id, role_id=role_id)
    return RedirectResponse(url="/employees/", status_code=status.HTTP_303_SEE_OTHER)


@app.post('/employees/{employee_id}/update/', response_class=RedirectResponse)
async def update_employee(request: Request,
                          employee_id: int,
                          firstname: str = Form(...),
                          lastname: str = Form(...),
                          title: str = Form(...),
                          bio: str = Form(...),
                          age: int = Form(...),
                          department_id: int = Form(...),
                          role_id: int = Form(...),
                          db: Session = Depends(get_db)):
    qs.update_employee(db, employee_id, payload=schemas.EmployeeCreate(firstname=firstname,
                                                                       lastname=lastname,
                                                                       title=title,
                                                                       bio=bio,
                                                                       age=age),
                       department_id=department_id, role_id=role_id)
    return RedirectResponse(url="/employees/", status_code=status.HTTP_303_SEE_OTHER)


@app.get('/employees/', response_class=HTMLResponse)
async def employees(request: Request, db: Session = Depends(get_db)):
    employees = qs.get_employees(db)

    context = {
        "request": request,
        "employees": employees,
        "title": "Employee Page"
    }
    response = templates.TemplateResponse("employee/list.html", context)
    return response


@app.get('/employees/{employee_id}', response_class=HTMLResponse)
async def employee(request: Request, employee_id: int, db: Session = Depends(get_db)):
    employee = qs.get_employee(db, employee_id)
    departments = qs.get_departments(db)
    roles = qs.get_roles(db)
    context = {
        "request": request,
        "employee": employee,
        "roles": roles,
        "departments": departments,
        "title": "Employee Detail Page"
    }
    response = templates.TemplateResponse("employee/detail.html", context)
    return response


@app.post('/employees/{employee_id}/delete/', response_class=RedirectResponse)
async def delete_employee(request: Request, employee_id: int, db: Session = Depends(get_db)):
    qs.delete_employee(db, employee_id)
    return RedirectResponse(url="/employees/", status_code=status.HTTP_303_SEE_OTHER)


@app.post('/companies/', response_class=RedirectResponse)
async def create_company(request: Request, companyname: str = Form(...), db: Session = Depends(get_db)):
    qs.create_company(db=db, payload=schemas.RoleCreate(name=companyname))
    return RedirectResponse(url="/companies/", status_code=status.HTTP_303_SEE_OTHER)


@app.get('/companies/', response_class=HTMLResponse)
async def companies(request: Request, db: Session = Depends(get_db)):
    companies = qs.get_companies(db)
    context = {
        "request": request,
        "companies": companies,
        "title": "Company Page"
    }
    response = templates.TemplateResponse("company/list.html", context)
    return response


@app.get('/companies/{company_id}', response_class=HTMLResponse)
async def company(request: Request, company_id: int, db: Session = Depends(get_db)):
    company = qs.get_company(db, company_id)
    context = {
        "request": request,
        "company": company,
        "title": "Company Detail Page"
    }
    response = templates.TemplateResponse("company/detail.html", context)
    return response


@app.post('/companies/{company_id}/update/', response_class=RedirectResponse)
async def update_company(request: Request, company_id: int, companyname: str = Form(...), db: Session = Depends(get_db)):
    company = qs.update_company(
        db, company_id, payload=schemas.RoleCreate(name=companyname))
    return RedirectResponse(url=f"/companies/{company_id}", status_code=status.HTTP_303_SEE_OTHER)


@app.post('/companies/{company_id}/delete/', response_class=RedirectResponse)
async def delete_company(request: Request, company_id: int, db: Session = Depends(get_db)):
    qs.delete_company(db, company_id)
    return RedirectResponse(url="/companies/", status_code=status.HTTP_303_SEE_OTHER)


@app.get('/departments/', response_class=HTMLResponse)
async def departments(request: Request, db: Session = Depends(get_db)):
    departments = qs.get_departments(db)
    companies = qs.get_companies(db)
    context = {
        "request": request,
        "departments": departments,
        "companies": companies,
        "title": "Department Page"
    }
    response = templates.TemplateResponse("department/list.html", context)
    return response


@app.post('/departments/', response_class=RedirectResponse)
async def create_department(request: Request,
                            departmentname: str = Form(...),
                            company_id: str = Form(...),
                            db: Session = Depends(get_db)):
    qs.create_department(db=db,
                         payload=schemas.DepartmentCreate(name=departmentname),
                         company_id=company_id)
    return RedirectResponse(url="/departments/", status_code=status.HTTP_303_SEE_OTHER)


@app.get('/departments/{department_id}', response_class=HTMLResponse)
async def department(request: Request, department_id: int, db: Session = Depends(get_db)):
    department = qs.get_department(db, department_id)
    context = {
        "request": request,
        "department": department,
        "title": "Department Detail Page"
    }
    response = templates.TemplateResponse("department/detail.html", context)
    return response


@app.post('/departments/{department_id}/update/', response_class=RedirectResponse)
async def update_department(request: Request, department_id: int, departmentname: str = Form(...), db: Session = Depends(get_db)):
    department = qs.update_department(
        db, department_id, payload=schemas.RoleCreate(name=departmentname))
    return RedirectResponse(url=f"/departments/{department_id}", status_code=status.HTTP_303_SEE_OTHER)


@app.post('/departments/{department_id}/delete/', response_class=RedirectResponse)
async def delete_department(request: Request, department_id: int, db: Session = Depends(get_db)):
    qs.delete_department(db, department_id)
    return RedirectResponse(url="/departments/", status_code=status.HTTP_303_SEE_OTHER)


@app.get('/roles/', response_class=HTMLResponse)
async def roles(request: Request, db: Session = Depends(get_db)):
    roles = qs.get_roles(db)
    context = {
        "request": request,
        "roles": roles,
        "title": "Role Page"
    }
    response = templates.TemplateResponse("role/list.html", context)
    return response


@app.get('/roles/{role_id}', response_class=HTMLResponse)
async def role(request: Request, role_id: int, db: Session = Depends(get_db)):
    role = qs.get_role(db, role_id)
    context = {
        "request": request,
        "role": role,
        "title": "Role Detail Page"
    }
    response = templates.TemplateResponse("role/detail.html", context)
    return response


@app.post('/roles/{role_id}/update/', response_class=RedirectResponse)
async def update_role(request: Request, role_id: int, rolename: str = Form(...), db: Session = Depends(get_db)):
    role = qs.update_role(
        db, role_id, payload=schemas.RoleCreate(name=rolename))
    return RedirectResponse(url=f"/roles/{role_id}", status_code=status.HTTP_303_SEE_OTHER)


@app.post('/roles/{role_id}/delete/', response_class=RedirectResponse)
async def delete_role(request: Request, role_id: int, db: Session = Depends(get_db)):
    qs.delete_role(db, role_id)
    return RedirectResponse(url="/roles/", status_code=status.HTTP_303_SEE_OTHER)


@app.post('/roles/', response_class=RedirectResponse)
async def create_role(request: Request, rolename: str = Form(...), db: Session = Depends(get_db)):
    qs.create_role(db=db, payload=schemas.RoleCreate(name=rolename))
    return RedirectResponse(url="/roles/", status_code=status.HTTP_303_SEE_OTHER)
