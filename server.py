from flask import Flask, request, render_template, url_for
import util
import data_manager
import connection

app = Flask(__name__)


@app.route('/')
def list_questions():
    data = data_manager.get_questions()
    return render_template('list.html', data=data)


@app.route('/question')
def display_question(data):
    pass


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )