from flask import Flask
import tasks

app = Flask(__name__)
app.register_blueprint(tasks.bp)
app.add_url_rule("/", endpoint="tasks", view_func=tasks.index)


if __name__ == '__main__':
    app.run()
