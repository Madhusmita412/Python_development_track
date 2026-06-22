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
root.geometry("1000x700")

folder_path = ""


def select_folder():
    global folder_path

    folder_path = filedialog.askdirectory()

    folder_label.config(text=folder_path)


def analyze_resumes():

    # Clear previous table data
    for item in tree.get_children():
        tree.delete(item)

    if folder_path == "":
        status_label.config(text="Please select a resume folder first")
        return

    resumes = get_resumes(folder_path)

    shortlisted_candidates = []

    for resume in resumes:

        name = extract_name(resume["content"])

        email = extract_email(resume["content"])

        skills = extract_skills(resume["content"])

        score = calculate_score(skills)

        if score >= 60:
            status = "Shortlisted"

            shortlisted_candidates.append({
                "Name": name,
                "Email": email,
                "Score": score
            })

        else:
            status = "Rejected"

        tree.insert(
            "",
            "end",
            values=(
                name,
                email,
                f"{score}%",
                status
            )
        )

    with open(
        "candidate_report.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            ["Name", "Email", "Score"]
        )

        for candidate in shortlisted_candidates:

            writer.writerow(
                [
                    candidate["Name"],
                    candidate["Email"],
                    candidate["Score"]
                ]
            )

    status_label.config(
        text="Analysis Completed Successfully"
    )




heading = tk.Label(
    root,
    text="Resume Sorting Automation System",
    font=("Arial", 24, "bold")
)

heading.pack(pady=20)



button_frame = tk.Frame(root)
button_frame.pack(pady=10)

select_btn = tk.Button(
    button_frame,
    text="Select Resume Folder",
    command=select_folder,
    width=20
)

select_btn.grid(row=0, column=0, padx=10)

analyze_btn = tk.Button(
    button_frame,
    text="Analyze Resumes",
    command=analyze_resumes,
    width=20
)

analyze_btn.grid(row=0, column=1, padx=10)


folder_label = tk.Label(
    root,
    text="No Folder Selected",
    font=("Arial", 10)
)

folder_label.pack(pady=5)



tree = ttk.Treeview(
    root,
    columns=("Name", "Email", "Score", "Status"),
    show="headings",
    height=15
)

tree.heading("Name", text="Candidate Name")
tree.heading("Email", text="Email Address")
tree.heading("Score", text="Match Score")
tree.heading("Status", text="Status")

tree.column("Name", width=220, anchor="center")
tree.column("Email", width=320, anchor="center")
tree.column("Score", width=120, anchor="center")
tree.column("Status", width=180, anchor="center")

tree.pack(
    padx=20,
    pady=20,
    fill="both",
    expand=True
)



status_label = tk.Label(
    root,
    text="Ready",
    bd=1,
    relief="sunken",
    anchor="w"
)

status_label.pack(
    side="bottom",
    fill="x"
)

root.mainloop()