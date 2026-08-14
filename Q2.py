

grades = {
    "math": {
        "anna": 1.7,
        "ben": 2.3,
        "clara": 1.0
    },

    "physics": {
        "ben": 3.0,
        "clara": 1.3,
        "david": 2.0
    },

    "art": {
        "anna": 1.0,
        "david": 1.7
    }
}


def make_student_data():
    students = {}

    for subject in grades:
        for name in grades[subject]:

            if name not in students:
                students[name] = {}

            students[name][subject] = grades[subject][name]

    return students


def subjects_of(student):
    students = make_student_data()

    if student not in students:
        return set()

    return set(students[student].keys())


def student_average(student):
    students = make_student_data()

    if student not in students:
        return 0.0

    marks = list(students[student].values())

    return round(sum(marks) / len(marks), 2)


def takes_all():
    students = make_student_data()
    result = set()

    for name in students:

        if len(students[name]) == len(grades):
            result.add(name)

    return result


def honor_roll(limit=1.5):
    students = make_student_data()
    result = []

    for name in students:

        if student_average(name) <= limit:
            result.append(name)

    return sorted(result)


if __name__ == "__main__":
    print("Q2: GRADEBOOK")

    students = make_student_data()

    print("Student data:", students)

    for name in ["anna", "ben", "clara", "david"]:
        print(name, "subjects:", subjects_of(name))
        print(name, "average:", student_average(name))

    print("Students taking all subjects:", takes_all())

    print("Unknown student:", student_average("zoe"))

    print("Honor roll:", honor_roll())