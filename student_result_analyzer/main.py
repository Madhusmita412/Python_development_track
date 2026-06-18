students = []

# Take input from user
num_students = int(input("Enter number of students: "))

for i in range(num_students):

    print(f"\nEnter details for Student {i + 1}")

    name = input("Enter Name: ")
    math = int(input("Enter Math Marks: "))
    science = int(input("Enter Science Marks: "))
    english = int(input("Enter English Marks: "))

    student = {
        "name": name,
        "math": math,
        "science": science,
        "english": english
    }

    students.append(student)


print("\n===== STUDENTS DATA =====")
print(students)

# Calculate Total Marks
def calculate_total(student):
    return (
        student["math"] +
        student["science"] +
        student["english"]
    )

# Calculate Percentage
def calculate_percentage(student):
    total = calculate_total(student)
    subjects = 3
    return total / subjects

# Assign Grade
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


# Rank Students
def rank_students(students):
    students.sort(
    key=calculate_total,
    reverse=True
    )

print("\n===== STUDENT RANKINGS =====")

for rank, student in enumerate(students, start=1):

    print(
        f"{rank}. {student['name']} "
        f"- Total Marks: {calculate_total(student)}"
    )


# Display Rankings
rank_students(students)


# Generate Reports
print("\n===== STUDENT REPORTS =====")

for student in students:
    total = calculate_total(student)
    percentage = calculate_percentage(student)
    grade = assign_grade(student)

    print("\n-------------------------")
    print(f"Name       : {student['name']}")
    print(f"Total Marks: {total}")
    print(f"Percentage : {round(percentage, 2)}%")
    print(f"Grade      : {grade}")
    print("-------------------------")

