# 🎓 Student Result Analyzer

A Python-based application that manages student records and generates performance reports. This project was developed as part of the **Python Development Track Internship** to strengthen fundamental programming and problem-solving skills.

---

## 📖 Project Overview

The **Student Result Analyzer** helps analyze student performance by calculating total marks, percentages, assigning grades, ranking students, and generating reports.

This project demonstrates the use of:

* Python Functions
* Lists and Dictionaries
* Loops and Conditional Statements
* Sorting Algorithms
* Data Processing

---

## ✨ Features

✅ Store student information

✅ Calculate total marks

✅ Calculate percentage

✅ Assign grades automatically

✅ Rank students based on marks

✅ Generate detailed reports

---

## 🛠️ Technologies Used

* **Python 3**
* Functions
* Lists
* Dictionaries
* Loops
* Conditional Statements
* Sorting (`sort()`)
* String Formatting (f-strings)

---

## 📂 Project Structure

```text
Student_Result_Analyzer/
│
├── main.py
└── README.md
```

---

## 🧠 Concepts Learned

This project helped in understanding:

* Variables and Data Types
* Functions and Code Reusability
* Lists and Dictionaries
* Iteration using Loops
* Conditional Logic
* Sorting Data
* Problem Solving and Debugging

---

## 🚀 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/Madhusmita412/python_development_track.git
```

### 2. Navigate to the Project Folder

```bash
cd python_development_track
```

### 3. Run the Program

```bash
python main.py
```

---

## 📌 Sample Student Data

```python
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
    }
]
```

---

## ⚙️ Project Workflow

### 1. Store Students

Student information is stored using a list of dictionaries.

### 2. Calculate Total Marks

The program sums the marks of all subjects.

### 3. Calculate Percentage

Percentage is calculated using:

```python
percentage = total / 3
```

### 4. Assign Grades

| Percentage | Grade |
| ---------: | :---: |
|        90+ |   A+  |
|      80–89 |   A   |
|      70–79 |   B   |
|      60–69 |   C   |
|   Below 60 |  Fail |

### 5. Rank Students

Students are ranked in descending order based on total marks.

### 6. Generate Reports

The system displays:

* Student Name
* Total Marks
* Percentage
* Grade

---

## 📊 Sample Output

```text
===== RANKINGS =====

1. Priya - Total: 277
2. Rahul - Total: 263
3. Aman - Total: 233


===== STUDENT REPORTS =====

----- REPORT -----
Name: Priya
Total: 277
Percentage: 92.33
Grade: A+

----- REPORT -----
Name: Rahul
Total: 263
Percentage: 87.67
Grade: A

----- REPORT -----
Name: Aman
Total: 233
Percentage: 77.67
Grade: B
```

---

## 🎯 Learning Outcomes

By completing this project, I gained experience in:

* Python Programming Fundamentals
* Data Structures
* Modular Programming
* Debugging and Error Handling
* Writing Clean and Maintainable Code
* Git and GitHub Version Control

---

## 🔮 Future Enhancements

* Add student records dynamically
* Search student by name
* Update marks
* Delete student records
* Export reports to CSV
* Save reports as text files
* Convert the project into an OOP-based application

---

## 👩‍💻 Author

**Madhusmita**

Python Development Track Intern

GitHub: https://github.com/Madhusmita412

---

⭐ If you like this project, consider giving it a star on GitHub!
