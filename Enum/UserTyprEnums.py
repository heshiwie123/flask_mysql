from enum import Enum

class UsreType(Enum):
    Student = 0
    Instructor = 1
    Admin = 2


print(UsreType.Instructor.value)