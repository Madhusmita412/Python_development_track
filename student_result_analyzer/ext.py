students = []

num_students = int(input("Enter number of students: "))

for i in range(num_students):

    print(f"\nEnter details for Student {i+1}")

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

print("\nStudents Data:")
print(students)