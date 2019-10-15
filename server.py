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
    #question_id = data_manager.get_question_id_by_answer_id(answer_id)
    answer_data = data_manager.get_answer_by_id(answer_id)
    answer_comment = data_manager.get_comments_for_answer(answer_id)
    status = ''
    if request.method == 'POST':
        comment = request.form['comment']
        data_to_manager = [answer_id, comment, 'answer']
        data_manager.add_comment(data_to_manager)
        status = 'Comment added successfully'
    return render_template('add_comment.html', answer_data=answer_data, status=status,
                           answer_comment=answer_comment)


@app.route('/question/<question_id>/add-answer', methods=['GET', 'POST'])
def add_answer(question_id: int):
    status = ''
    answer_data=data_manager.get_question_by_id(question_id)
    if request.method == 'POST':
        site_input = request.form['new-answer']
        data_manager.add_answer(site_input, question_id)
        status = 'Answer added successfully'
    return render_template('add_answer.html',question_id=question_id, answer_data=answer_data,
                           status=status)


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


@app.route('/users')
def list_users():
    users = data_manager.list_users()
    return render_template('list_users.html', users=users)


@app.route('/user/<user_id>')
def user_page(user_id: int):
    users = data_manager
    return users


if __name__ == '__main__':
    app.run(
        debug=True
    )
