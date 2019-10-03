from flask import Flask, request, render_template, redirect
import data_manager

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def list_questions():
    data = data_manager.get_least_questions()
    return render_template('index.html', data=data)


@app.route('/search')
def search():
    search_result = data_manager.search(*request.args.values())
    return render_template('search.html', search_result=search_result)


@app.route('/list')
def show_all_questions():
    question_list = data_manager.get_all_questions()
    return render_template('list.html', question_list=question_list)


@app.route('/question/<question_id>')
def show_specific_question(question_id: int):
    question_data = data_manager.get_question_by_id(question_id)
    question_comment = data_manager.get_comments_for_question(question_id)
    question_answer = data_manager.get_answers_for_questions(question_id)
    #answer_comment = data_manager.get_comments_for_answer(question_id)
    print(question_answer)
    return render_template('question_details.html', question_comment=question_comment,
                           question_answer=question_answer, question_data=question_data)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_to_question(question_id: int):
    question_data = data_manager.get_question_by_id(question_id)
    status = ''
    if request.method == 'POST':
        comment = request.form['comment']
        data_to_manager = [question_id, comment, 'question']
        data_manager.add_comment(data_to_manager)
        status = 'Comment added successfully'
    return render_template('add_comment.html', question_data=question_data, status=status,
                           question_id=question_id)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_to_answer(answer_id: int):
    answer_data = data_manager.get_answer_by_id(answer_id)
    #question_id = data_manager.get_question_id_by_answer_id(answer_id)
    status = ''
    if request.method == 'POST':
        comment = request.form['comment']
        data_to_manager = [answer_id, comment, 'answer']
        data_manager.add_comment(data_to_manager)
        status = 'Comment added successfully'
    return render_template('add_comment.html', answer_data=answer_data, status=status)
'''                         question_id=question_id[0]'''


@app.route('/question/<question_id>/add-answer', methods=['GET', 'POST'])
def add_answer(question_id: int):
    if request.method == 'POST':
        site_input = request.form['new-answer']
        data_manager.add_answer(site_input, question_id)
    return render_template('add_answer.html',question_id=question_id)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id: int):
    answer_data=data_manager.get_answer_by_id(answer_id)
    if request.method == 'POST':
        site_input = [request.form['new-answer']]
        site_input.append(answer_id)
        data_manager.edit_answer(site_input)
        return redirect('/list')
    return render_template('edit_answer.html',answer_data=answer_data)


@app.route('/add-question', methods=['GET','POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_a_question.html')

    site_input = [request.form['title'], request.form['message']]
    data_manager.add_question(site_input)
    return redirect('/')





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



"""

if __name__ == '__main__':
    app.run(
        debug=True
    )
