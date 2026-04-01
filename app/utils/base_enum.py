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

class Location(str, Enum):
    SHELF = "shelf"
    MEMBER="with member"
    NONE= "none"

class MemberStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"