from flask import Flask, request, render_template, url_for
import util
import data_manager
import connection

app = Flask(__name__)


@app.route('/')
def list_questions():
    data = data_manager.get_questions()
    return render_template('list.html', data=data)


@app.route('/question/<question_id>')
def display_question(question_id: int):
    question_data = data_manager.get_questions()
    answer_data = data_manager.get_answers()
    return render_template('display_a_question.html',
                           question_data=question_data,
                           answer_data=answer_data)


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )