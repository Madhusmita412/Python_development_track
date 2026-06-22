import os
import re


def get_resumes(folder_path):

    resumes = []

    for file in os.listdir(folder_path):

        if file.endswith(".txt"):

            file_path = os.path.join(
                folder_path,
                file
            )

            with open(
                file_path,"r"
            )as resume:

                content = resume.read()

            resumes.append(
                {"file": file,  "content": content})

    return resumes


def extract_email(text):

    email_pattern = (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

    emails = re.findall(email_pattern,text)

    if emails:
        return emails[0]

    return "Email Not Found"


def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        if line.startswith("Name:"):

            return line.replace("Name:","").strip()

    return "Name Not Found"


def extract_skills(text):

    skills = []

    skill_list = [
        "Python",
        "Flask",
        "SQL",
        "Git",
        "HTML",
        "CSS",
        "JavaScript"
    ]

    for skill in skill_list:

        if skill.lower() in text.lower():

            skills.append(skill)

    return skills


def calculate_score(skills):

    required_skills = [
        "Python",
        "Flask",
        "SQL",
        "Git"
    ]

    matched_skills = 0

    for skill in required_skills:

        if skill in skills:

            matched_skills += 1

    score = (matched_skills /len(required_skills)) * 100

    return round(score, 2)