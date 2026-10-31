
from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "skills.json"


def load_skills():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_skills(skills):
    with open(DATA_FILE, "w") as file:
        json.dump(skills, file, indent=4)


@app.route("/")
def home():
    skills = load_skills()

    total_skills = len(skills)
    completed_skills = sum(
        1 for skill in skills if skill["progress"] == 100
    )

    if total_skills > 0:
        average_progress = round(
            sum(skill["progress"] for skill in skills) / total_skills
        )
    else:
        average_progress = 0

    return render_template(
        "index.html",
        skills=skills,
        total_skills=total_skills,
        completed_skills=completed_skills,
        average_progress=average_progress
    )


@app.route("/add", methods=["GET", "POST"])
def add_skill():
    if request.method == "POST":
        skills = load_skills()

        skill = {
            "id": max(
                (item["id"] for item in skills),
                default=0
            ) + 1,
            "name": request.form["name"].strip(),
            "category": request.form["category"],
            "progress": int(request.form["progress"]),
            "description": request.form["description"].strip()
        }

        skills.append(skill)
        save_skills(skills)

        return redirect(url_for("home"))

    return render_template("add_skill.html")


@app.route("/edit/<int:skill_id>", methods=["GET", "POST"])
def edit_skill(skill_id):
    skills = load_skills()

    skill = next(
        (item for item in skills if item["id"] == skill_id),
        None
    )

    if skill is None:
        return "Skill not found", 404

    if request.method == "POST":
        skill["name"] = request.form["name"].strip()
        skill["category"] = request.form["category"]
        skill["progress"] = int(request.form["progress"])
        skill["description"] = request.form.get(
            "description", ""
        ).strip()

        save_skills(skills)
        return redirect(url_for("home"))

    return render_template("edit_skill.html", skill=skill)


@app.route("/delete/<int:skill_id>", methods=["POST"])
def delete_skill(skill_id):
    skills = load_skills()

    updated_skills = [
        skill for skill in skills
        if skill["id"] != skill_id
    ]

    save_skills(updated_skills)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
