from flask import Flask, request, render_template, url_for, redirect
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
    question_data = data_manager.get_questions(question_id)
    answer_data = data_manager.get_answers(question_id)
    if isinstance(answer_data, list):
        answer_data = {'message': 'No answer so far...'}
    if isinstance(question_data, list):
        return redirect('/error')
    return render_template('display_a_question.html',
                           question_data=question_data,
                           answer_data=answer_data
                           )

@app.route('/error')
def handle_exceptions():
    return render_template('exception_handing.html')


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )