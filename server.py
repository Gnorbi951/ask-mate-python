from flask import Flask, request, render_template, redirect, session, url_for

import data_manager
import validation

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET', 'POST'])
def list_questions():
    if request.method == 'POST':
        data = data_manager.get_existing_users()
        for line in data:
            if request.form['username'] == line.get('user_name') \
                    and validation.verify_password(request.form['password'], line.get('password')):
                session['username'] = request.form['username']
                session['password'] = request.form['password']
        return redirect('/list')
    else:
        data = data_manager.get_least_questions()
        return render_template('index.html', data=data)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('list_questions'))


@app.route('/search')
def search():
    search_result = data_manager.search(*request.args.values())
    return render_template('search.html', search_result=search_result)


@app.route('/list')
def show_all_questions():
    question_list = data_manager.get_all_questions()
    return render_template('list.html', question_list=question_list)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def show_specific_question(question_id: int):
    question_data = data_manager.get_question_by_id(question_id)
    question_comment = data_manager.get_comments_for_question(question_id)
    question_answer = data_manager.get_answers_for_questions(question_id)
    return render_template('question_details.html', question_comment=question_comment,
                           question_answer=question_answer, question_data=question_data)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_to_question(question_id: int):
    question_data = data_manager.get_question_by_id(question_id)
    question_comment = data_manager.get_comments_for_question(question_id)
    user_name = data_manager.get_answers_for_questions(question_id)
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            user_id = data_manager.get_user_id_by_name(username)
            site_input = [question_id, request.form['comment'], 'question', user_id[0].get('id')]
            data_manager.add_comment(site_input)
        else:
            site_input = [question_id, request.form['comment'], 'question', None]
            data_manager.add_comment(site_input)
        return redirect(url_for('add_new_comment_to_question', question_id=question_id))
    return render_template('add_question_comment.html', question_data=question_data,
                           question_id=question_id, question_comment=question_comment,
                           user_name=user_name)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_to_answer(answer_id: int):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    question_id = question_id[0].get('id')
    user_name = data_manager.get_answers_for_questions(question_id)
    answer_data = data_manager.get_answer_by_id(answer_id)
    question_data = data_manager.get_question_by_id(question_id)
    answer_comment = data_manager.get_comments_for_answer(answer_id)
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            user_id = data_manager.get_user_id_by_name(username)
            site_input = [answer_id, request.form['comment'], 'answer', user_id[0].get('id')]
            data_manager.add_comment(site_input)
        else:
            site_input = [answer_id, request.form['comment'], 'answer', None]
            data_manager.add_comment(site_input)
        return redirect(url_for('add_new_comment_to_answer', answer_id=answer_id))

    return render_template('add_answer_comment.html', answer_data=answer_data,
                           answer_comment=answer_comment, question_id=question_id,
                           question_data=question_data, user_name=user_name)


@app.route('/question/<question_id>/add-answer', methods=['GET', 'POST'])
def add_answer(question_id: int):
    answer_data = data_manager.get_question_by_id(question_id)
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            user_id = data_manager.get_user_id_by_name(username)
            site_input = request.form['new-answer']
            data_manager.add_answer(site_input, user_id[0].get('id'), question_id)
        else:
            site_input = request.form['new-answer']
            data_manager.add_answer(site_input, None, question_id)
        return redirect(url_for('show_specific_question', question_id=question_id))

    return render_template('add_answer.html', question_id=question_id, answer_data=answer_data)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id: int):
    answer_data = data_manager.get_answer_by_id(answer_id)
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    question_id = question_id[0].get('id')
    if request.method == 'POST':
        site_input = [request.form['new-answer']]
        site_input.append(answer_id)
        data_manager.edit_answer(site_input)
        return redirect(url_for('show_specific_question', question_id=question_id))
    return render_template('edit_answer.html', answer_data=answer_data,
                           question_id=question_id)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_a_question.html')

    if 'username' in session:
        username = session['username']
        user_id = data_manager.get_user_id_by_name(username)
        site_input = [request.form['title'], request.form['message'], user_id[0].get('id')]
        data_manager.add_question(site_input)
    else:
        site_input = [request.form['title'], request.form['message'], None]
        data_manager.add_question(site_input)
    return redirect(url_for('show_all_questions'))


@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def edit_question(question_id: int):
    question_data = data_manager.get_question_by_id(question_id)

    if request.method == 'POST':
        user_input = [request.form['title'], request.form['message'], question_id]
        data_manager.edit_question(user_input)
        return redirect(url_for('show_specific_question', question_id=question_id))

    return render_template('edit_question.html', question_data=question_data)


@app.route('/user-registration', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        if validation.check_if_user_name_exists(user_name):
            message = 'Name already taken'
            return render_template('registration.html', message=message)
        else:
            password = request.form.get('pw')
            hashed_password = validation.hash_password(password)
            all_input = [user_name, hashed_password]
            data_manager.add_user(all_input)
            message = 'Registration successful'
            return render_template('registration.html', message=message)
    return render_template('registration.html')


@app.route('/users')
def list_users():
    users = data_manager.list_users()
    return render_template('list_users.html', users=users)


@app.route('/user/<user_id>')
def user_page(user_id: int):
    user_name = data_manager.get_user_name_by_id(user_id)
    question_data = data_manager.get_question_by_user_id(user_id)
    answer_data = data_manager.get_answer_by_user_id(user_id)
    comment_data = data_manager.get_comment_by_user_id(user_id)
    return render_template('user_page.html', user_name=user_name, question_data=question_data,
                           answer_data=answer_data, comment_data=comment_data)


@app.route('/question/<question_id>/vote_up')
def vote_up(question_id: int):
    data_manager.vote_up(question_id)
    return redirect('/list')


@app.route('/question/<question_id>/vote_down')
def vote_down(question_id: int):
    data_manager.vote_down(question_id)
    return redirect('/list')


@app.route('/question/<question_id>/delete')
def delete_question(question_id: int):
    data_manager.delete_question(question_id)
    return redirect('/list')


@app.route('/answer/<answer_id>/vote_up')
def vote_up_answer(answer_id: int):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    question_id = question_id[0].get('id')
    data_manager.vote_up_answer(answer_id)
    return redirect(url_for('show_specific_question', question_id=question_id))


@app.route('/answer/<answer_id>/vote_down')
def vote_down_answer(answer_id: int):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    question_id = question_id[0].get('id')
    data_manager.vote_down_answer(answer_id)
    return redirect(url_for('show_specific_question', question_id=question_id))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id: int):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    question_id = question_id[0].get('id')
    data_manager.delete_answer(answer_id)
    return redirect(url_for('show_specific_question', question_id=question_id))


@app.route('/comments/<comment_id>/delete-a')
def delete_answer_comment(comment_id: int):
    answer_id = data_manager.get_answer_id_by_comment_id(comment_id)
    answer_id = answer_id[0].get('answer_id')
    data_manager.delete_comment(comment_id)
    return redirect(url_for('add_new_comment_to_answer', answer_id=answer_id))


@app.route('/comments/<comment_id>/delete-q')
def delete_question_comment(comment_id: int):
    question_id = data_manager.get_question_id_by_comment_id(comment_id)
    question_id = question_id[0].get('question_id')
    data_manager.delete_comment(comment_id)
    return redirect(url_for('add_new_comment_to_question', question_id=question_id))


if __name__ == '__main__':
    app.run(
        debug=True,
        host='10.44.1.170',
        port=7654
    )
