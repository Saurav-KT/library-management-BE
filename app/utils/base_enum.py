from enum import Enum

class MemberType(str, Enum):
    STUDENT = "Student"
    TEACHER = "Teacher"
    GENERAL = "General"

class Status(str, Enum):
    AVAILABLE = "available"
    ISSUED = "issued"
    LOST = "lost"
    DAMAGED= "damaged"