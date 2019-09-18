from flask import Flask, request, render_template, redirect
import data_manager

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def list_questions():
    data = data_manager.get_questions()
    return render_template('list.html', data=data)


@app.route('/question/<question_id>')
def display_question(question_id: int):
    question_data = data_manager.get_questions(question_id)
    answer_data = data_manager.get_answers(question_id)
    if isinstance(answer_data, list):
        answer_data = {'message': 'No answer so far...'}
    return render_template('display_a_question.html',
                           question_data=question_data,
                           answer_data=answer_data
                           )


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        site_input = request.form['title']
        print(site_input)
        return redirect('/')
    else:
        return render_template('add_a_question.html')


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )