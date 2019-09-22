import csv
import time


def get_questions(id=None):
    """Get the data from the questions csv as an Ordered_Dict list"""
    csv_data = []
    with open('sample_data/questions.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = dict(row)

            if id is not None and id == d['id']:
                return d

            csv_data.append(d)

    return csv_data[::-1]


def get_answers(question_id=None):
    """Get the data from the answers csv as an Ordered_Dict list"""
    csv_data = []
    with open('sample_data/answer.csv') as f:
        reader = csv.DictReader(f)
        answers = []
        for row in reader:
            d = dict(row)
            if str(question_id) is not None and str(question_id) == d['question_id']:
                answers.append(d['message'])

            csv_data.append(d)

        if question_id is not None:
            return answers
    return csv_data


def get_time():
    return str(int(time.time()))


def get_question_max_id(filename):
    with open(filename) as f:
        read = csv.DictReader(f)
        max_id = '0'
        for row in read:
            if max_id < row['id']:
                max_id = row['id']
    return max_id


def pass_question_to_handler(site_input):
    id = str(int(get_question_max_id('sample_data/questions.csv')) + 1)
    submission_time = get_time()
    view_number = '0'
    vote_number = '0'
    title = site_input[0]
    message = site_input[1]
    image = 'No image'
    return_value = [id, submission_time,
                    view_number, vote_number,
                    title, message, image]
    write_to_questions_csv(return_value)


def write_to_questions_csv(new_data):
    fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    new_dict = {}
    counter = 0
    for _ in new_data:
        new_dict[fieldnames[counter]] = new_data[counter]
        counter += 1

    with open('sample_data/questions.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(new_dict)


def pass_answers_to_handler(site_input):
    id = str(int(get_question_max_id('sample_data/answer.csv')) + 1)
    question_id = site_input[0]
    submission_time = get_time()
    vote_number = '0'
    message = site_input[1]
    image = 'No image'
    return_value = [id, submission_time,
                    vote_number, question_id,
                    message, image]
    write_to_answers_csv(return_value)


def write_to_answers_csv(new_data):
    fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
    new_dict = {}
    counter = 0
    for _ in new_data:
        new_dict[fieldnames[counter]] = new_data[counter]
        counter += 1

    with open('sample_data/answer.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(new_dict)
