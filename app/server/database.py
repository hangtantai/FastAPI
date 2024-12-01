from pymongo import MongoClient

# Setting config
MONGO_USERNAME = "root"
MONGO_PASSWORD = "123"
MONGO_HOST = "localhost"
MONGO_PORT = 27019
MONGO_DB = "student"

client = MongoClient(f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}")
db = client[MONGO_DB]
collection_name = "student_collection"
collection = db[collection_name]

# Helper
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": str(student["fullname"]),
        "email": str(student["email"]),
        "course_of_study": str(student["course_of_study"]),
        "year": int(student["year"]),
        "GPA": float(student["gpa"]),
    }

# Retrieve all students present in the database
def retrieve_students():
    students = []
    for student in collection.find():
        students.append(student_helper(student))
    return students

# Add a new  student 
def add_student(student_data: dict) -> dict:
    student = collection.insert_one(student_data)
    new_student = collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)

# retrieve student with fullname
def retrieve_student(fullname: str) -> dict:
    student = collection.find_one({"fullname": fullname})
    if student:
        return student_helper(student)

# update information of student
def update_student(fullname: str, data: dict) -> dict:
    if len(data) < 1:
        return False
    student = collection.find_one({"fullname": fullname})

    if student:
        update_student = collection.update_one(
            {"fullname": fullname}, {"$set": data}
        )
        if update_student:
            return True
        return False

# Delete a student from the database
def delete_student(fullname: str):
    student = collection.find_one({"fullname": fullname})
    if student:
        collection.delete_one({"fullname": fullname})
        return True