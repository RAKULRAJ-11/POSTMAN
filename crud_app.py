from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Student CRUD API", version="1.0")

# Enable CORS so your frontend website and Postman can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database (a Python list to hold student dictionaries)
fake_db = []

# Pydantic model for incoming student data
class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str
    marks: float

# Pydantic model for updating student data (all fields optional)
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    course: Optional[str] = None
    marks: Optional[float] = None

# 1. CREATE (POST)
@app.post("/students/", response_model=Student)
def create_student(student: Student):
    # Check if student ID already exists
    for s in fake_db:
        if s["id"] == student.id:
            raise HTTPException(status_code=400, detail="Student ID already exists")
    
    fake_db.append(student.dict())
    return student

# 2. READ ALL (GET)
@app.get("/students/", response_model=List[Student])
def get_students():
    return fake_db

# 2. READ ONE (GET by ID)
@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    for s in fake_db:
        if s["id"] == student_id:
            return s
    raise HTTPException(status_code=404, detail="Student not found")

# 3. UPDATE (PUT)
@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_data: StudentUpdate):
    for s in fake_db:
        if s["id"] == student_id:
            # Update fields only if provided
            if updated_data.name is not None:
                s["name"] = updated_data.name
            if updated_data.age is not None:
                s["age"] = updated_data.age
            if updated_data.course is not None:
                s["course"] = updated_data.course
            if updated_data.marks is not None:
                s["marks"] = updated_data.marks
            return s
            
    raise HTTPException(status_code=404, detail="Student not found")

# 4. DELETE (DELETE)
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index, s in enumerate(fake_db):
        if s["id"] == student_id:
            deleted_student = fake_db.pop(index)
            return {"message": f"Student '{deleted_student['name']}' deleted successfully"}
            
    raise HTTPException(status_code=404, detail="Student not found")