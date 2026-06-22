from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import csv

from resume_processor import (
    get_resumes,
    extract_name,
    extract_email,
    extract_skills,
    calculate_score
)

root = tk.Tk()

root.title("Resume Sorting Automation System")

root.geometry("900x600")

folder_path = ""


def select_folder():

    global folder_path

    folder_path = filedialog.askdirectory()

    folder_label.config(
        text=folder_path
    )


def analyze_resumes():

    if folder_path == "":

        print("Please select a folder first")

        return

    resumes = get_resumes(folder_path)

    shortlisted_candidates = []

    print("\n===== RESUME ANALYSIS =====")

    for resume in resumes:

        name = extract_name(
            resume["content"]
        )

        email = extract_email(
            resume["content"]
        )

        skills = extract_skills(
            resume["content"]
        )

        score = calculate_score(
            skills
        )

        if score >= 60:

            status = "Shortlisted"

            shortlisted_candidates.append(
                {
                    "Name": name,
                    "Email": email,
                    "Score": score
                }
            )

        else:

            status = "Rejected"

        print("\n====================")

        print(
            "File:",
            resume["file"]
        )

        print(
            "Name:",
            name
        )

        print(
            "Email:",
            email
        )

        print(
            "Skills:",
            skills
        )

        print(
            "Score:",
            score,
            "%"
        )

        print(
            "Status:",
            status
        )

    with open(
        "candidate_report.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Name",
                "Email",
                "Score"
            ]
        )

        for candidate in shortlisted_candidates:

            writer.writerow(
                [
                    candidate["Name"],
                    candidate["Email"],
                    candidate["Score"]
                ]
            )

    print(
        "\nReport Generated Successfully"
    )


heading = tk.Label(
    root,
    text="Resume Sorting Automation System",
    font=("Arial", 20, "bold")
)

heading.pack(pady=20)

select_btn = tk.Button(
    root,
    text="Select Resume Folder",
    command=select_folder
)

select_btn.pack(pady=10)

folder_label = tk.Label(
    root,
    text="No Folder Selected"
)

folder_label.pack()

analyze_btn = tk.Button(
    root,
    text="Analyze Resumes",
    command=analyze_resumes
)

analyze_btn.pack(pady=10)

root.mainloop()

tree = ttk.Treeview(
    root,
    columns=("Name", "Email", "Score", "Status"),
    show="headings"
)

tree.heading("Name", text="Name")
tree.heading("Email", text="Email")
tree.heading("Score", text="Score")
tree.heading("Status", text="Status")

tree.pack(fill="both", expand=True, padx=20, pady=20)