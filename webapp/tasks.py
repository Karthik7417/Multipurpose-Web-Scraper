from flask import Blueprint, redirect, render_template, request, url_for
from io import StringIO
import json
import pandas as pd
import data as data
bp = Blueprint("tasks", __name__, url_prefix="/web-scraper/tasks")


@bp.route("/")
def index():
    tasks = data.get_all_tasks()
    return render_template("tasks/index.html", tasks=tasks)


@bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        file = request.files["urls_file"]
        file_content = StringIO(file.read().decode("utf-8"))
        df = pd.read_csv(file_content, dtype="category", encoding="utf-8")
        urls_flat = json.loads(df.to_json(orient="records"))
        urls_formatted = []
        for url_row in urls_flat:
            url_new = dict()
            for key in ["website_name", "website_url", "keywords"]:
                url_new[key] = url_row.pop(key, None)
            url_new["input_tags"] = url_row
            url_new["status"] = "new"
            if url_new["website_name"] and (url_new["website_url"] or url_new["keywords"]):
                urls_formatted.append(url_new)
        task = request.form.to_dict()
        task_id = data.create_task(task)
        data.insert_task_websites(task_id, urls_formatted)
        return redirect(url_for("tasks.details", id=task_id))
    return render_template("tasks/create.html")


@bp.route("/<string:id>", methods=["GET"])
def details(id):
    task = data.get_task(id)
    return render_template("tasks/details.html", task=task)


@bp.route("/<string:id>/delete", methods=["GET", "POST"])
def delete(id):
    if request.method == "POST":
        data.delete_task(id)
        return redirect(url_for("tasks.index"))
    task = data.get_task(id)
    return render_template("tasks/delete.html", task=task)


@bp.route("/<string:id>/edit", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        task = request.form.to_dict()
        task_id = data.update_task(task)
        return redirect(url_for("tasks.details", id=task_id))
    task = data.get_task(id)
    return render_template("tasks/edit.html", task=task)


@bp.route("/<string:id>/input", methods=["GET"])
def input(id):
    websites = data.get_input_websites(id)
    return render_template("tasks/input.html", task_id=id, websites=websites)


@bp.route("/<string:id>/validated", methods=["GET"])
def validated(id):
    websites = data.get_validated_websites(id)
    return render_template("tasks/validated.html", task_id=id, websites=websites)


@bp.route("/<string:id>/crawled", methods=["GET"])
def crawled(id):
    websites = data.get_crawled_pages(id)
    return render_template("tasks/crawled.html", task_id=id, websites=websites)


@bp.route("/<string:id>/parsed", methods=["GET"])
def parsed(id):
    websites = data.get_parsed_entities(id)
    return render_template("tasks/parsed.html", task_id=id, websites=websites)


@bp.route("/<string:id>/validate", methods=["GET", "POST"])
def validate(id):
    if request.method == "POST":
        data.validate_websites(id)
        return redirect(url_for("tasks.details", id=id))
    task = data.get_task(id)
    return render_template("tasks/validate.html", task=task)


@bp.route("/<string:id>/crawl", methods=["GET", "POST"])
def crawl(id):
    if request.method == "POST":
        data.crawl_websites(id)
        return redirect(url_for("tasks.details", id=id))
    task = data.get_task(id)
    return render_template("tasks/crawl.html", task=task)


@bp.route("/<string:id>/parse", methods=["GET", "POST"])
def parse(id):
    if request.method == "POST":
        data.parse_pages(id)
        return redirect(url_for("tasks.details", id=id))
    task = data.get_task(id)
    return render_template("tasks/parse.html", task=task)
