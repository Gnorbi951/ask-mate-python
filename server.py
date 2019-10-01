from flask import Flask, request, render_template, redirect
import data_manager

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def list_questions():
    data = data_manager.get_least_questions()

    return render_template('index.html', data=data)


@app.route('/list')
def show_all_questions():
    question_list = data_manager.get_all_questions()
    return render_template('list.html', question_list=question_list)


@app.route('/question/<question_id>')
def show_specific_question(question_id: int):
    question_comment = data_manager.get_comments_for_question(question_id)
    return render_template('question_details.html', question_comment=question_comment)

"""
@app.route('/question/<question_id>')
def display_question(question_id: int):
    question_data = data_manager.get_questions(question_id)
    answer_data = data_manager.get_answers(question_id)
    '''if isinstance(answer_data, list):
        answer_data = {'message': 'No answer so far...'}'''
    if isinstance(question_data, list):
        return redirect('/error')
    return render_template('display_a_question.html',
                           question_data=question_data,
                           answer_data=answer_data)


@app.route('/question/<answer_id>/new-answer', methods=['GET', 'POST'])
def answer_question(answer_id: int):
    if request.method == 'POST':
        data_manager.pass_answers_to_handler([answer_id, request.form['new-answer']])
        return redirect('/') #It should redirect to display question and not homepage.
    return render_template('add_answer.html')


@app.route('/error')
def handle_exceptions():
    return render_template('exception_handing.html')


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_a_question.html')

    site_input = [request.form['title'], request.form['message']]
    data_manager.pass_question_to_handler(site_input)
    return redirect('/')
"""

if __name__ == '__main__':
    app.run(
        debug=True
    )
