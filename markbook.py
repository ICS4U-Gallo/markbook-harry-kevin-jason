"""
Markbook Application
Group members: 
"""
from typing import Dict


classrooms = []

def main():
    while True:
        print()
        print("Markbook")
        print("========")
        print("[1] Create classroom.")
        print("[2] List classrooms.")
        print("[0] Exit")

        choice = get_valid_int_input("Select a menu option: ")

        if choice == 1:
            menu_create_classroom()
        elif choice == 2:
            menu_list_classrooms()
        elif choice == 0:
            exit()
        else:
            print("Invalid menu option.")


def menu_create_classroom():
    print()
    print("Create Classroom")
    print("----------------")
    course_code = input("Course code: ")
    course_name = input("Course name: ")
    period = get_valid_int_input("Period: ")
    teacher = input("Teacher: ")
    new_classroom = create_classroom(course_code,
                                     course_name,
                                     period,
                                     teacher)
    classrooms.append(new_classroom)


def menu_list_classrooms():
    print()
    print("Classrooms")
    print("----------")
    print("{:>15}{:>15}{:>15}".format("Course", "Code", "Teacher"))
    for room in classrooms:
        print("{:>15}{:>15}{:>15}".format(room["course_name"],
                                          room["course_code"],
                                          room["teacher"]))


def get_valid_int_input(msg: str) -> int:
    while True:
        try:
            value = int(input(msg))
        except ValueError:
            print("Invalid. Please enter a number.")
        else:
            return value


def create_assignment(name: str, due: str, points: int) -> Dict:
    """Creates an assignment represented as a dictionary
    
    Args:
        name: the name of the assignment.
        due: the due date for the assignment.
        points: what the assignment is out of (denominator).
    Returns:
        Assignment as a dictionary.
    """
    return {"name": name, "due": due, "points": points}


def create_classroom(course_code: str, course_name: str, period: int, teacher: str) -> Dict:
    """Creates a classroom dictionary"""
    return {
        "course_code": course_code,
        "course_name": course_name,
        "period": period,
        "teacher": teacher,
        "student_list": [],
        "assignment_list": []
    }


def calculate_average_mark(student: Dict) -> float:
    """Calculates the average mark of a student"""
    total = 0
    for mark in student["marks"]:
        total += mark
    return total / len(student["marks"])


def add_student_to_classroom(student, classroom):
    """Adds student to a classroom

    Args:
        student: Student dict
        classroom: The classroom to add the student to
    """
    classroom["student_list"].append(student)


def remove_student_from_classroom(student: Dict, classroom: Dict):
    """Removes student from classroom

    Args:
        student: The student to be removed
        classroom: the class from which the student will be removed.
    """
    classroom["student_list"].remove(student)


def edit_student(student: Dict, **kwargs: Dict):
    """Edits the student's info with the provided key/value pairs

    Args:
        student: The student whose data needs to be udated.
        **kwargs: KeyWordARGumentS. The key/value pairs of the
            data that needs to be changed. Can come in the form
            of a dictionary.
    """
    for key, value in kwargs.items():
        student[key] = value


if __name__ == "__main__":
    main()