from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = [
    {
        "id": 1,
        "title": "Complete Docker assignment",
        "completed": False
    },
    {
        "id": 2,
        "title": "Test GitHub Actions",
        "completed": False
    }
]


@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()

    if title:
        new_id = max(
            [task["id"] for task in tasks],
            default=0
        ) + 1

        tasks.append({
            "id": new_id,
            "title": title,
            "completed": False
        })

    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break

    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    tasks[:] = [
        task for task in tasks
        if task["id"] != task_id
    ]

    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)