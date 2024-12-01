from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_student,
    retrieve_students,
    retrieve_student,
    update_student,
    delete_student
)

from app.server.models.student import (
    StudentSchema,
    ResponseModel,
    ErrorResponseModel,
    UpdateStudentModel
)

router = APIRouter()

@router.get("/", response_description="Students retrieved")
def get_students():
    students = retrieve_students()
    if students:
        return ResponseModel(students, "Students data retrieved successfully")
    return ResponseModel(students, "Empty list returned")

@router.post("/", response_description="Student data added into the database")
def create_student(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = add_student(student)
    return ResponseModel(new_student, "Student added successfully.")

@router.get("/{fullname}", response_description="Student data retrieved")
def get_student_data(fullname):
    student = retrieve_student(fullname)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")

@router.put("/{fullname}")
def update_student_data(fullname: str, req: UpdateStudentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = update_student(fullname, req)
    if updated_student:
        return ResponseModel(
            "Student with fullname: {} name update is successful".format(fullname),
            "Student name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )

@router.delete("/{fullname}", response_description="Student data deleted from the database")
def delete_student_data(fullname: str):
    deleted_student = delete_student(fullname)
    if deleted_student:
        return ResponseModel(
            "Student with fullname: {} removed".format(fullname), "Student deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Student with fullname {0} doesn't exist".format(id)
    )