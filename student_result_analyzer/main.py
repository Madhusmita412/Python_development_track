students = [
    {
        "name": "Rahul",
        "math": 90,
        "science": 85,
        "english": 88
    },
    {
        "name": "Priya",
        "math": 95,
        "science": 92,
        "english": 90
    },
    {
        "name": "Aman",
        "math": 78,
        "science": 80,
        "english": 75
    }
]

print("\nStudents Data:")
print(students)


#Calculate total marks
def calculate_total(student):
    return (
        student["math"] +
        student["science"] +
        student["english"]
    )


#Calculate percentage
def calculate_percentage(student):
    total = calculate_total(student)
    return total / 3


#Assign grade
def assign_grade(student):
    percentage = calculate_percentage(student)

    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    else:
        return "Fail"


#Rank students
def rank_students(students):
    students.sort(
        key=calculate_total,
        reverse=True
    )

    print("\n===== RANKINGS =====")

    for rank, student in enumerate(students, start=1):
        print(
            f"{rank}. {student['name']} "
            f"- Total: {calculate_total(student)}"
        )


#Display rankings
rank_students(students)


#Generate reports
print("\n===== STUDENT REPORTS =====")

for student in students:

    total = calculate_total(student)

    percentage = calculate_percentage(student)

    grade = assign_grade(student)

    print("\n----- REPORT -----")
    print("Name:", student["name"])
    print("Total:", total)
    print("Percentage:", round(percentage, 2))
    print("Grade:", grade)



