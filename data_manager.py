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


def get_answers(id=None):
    """Get the data from the answers csv as an Ordered_Dict list"""
    csv_data = []
    with open('sample_data/answer.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = dict(row)
            if id is not None and id == d['id']:
                return d

            csv_data.append(d)

    return csv_data


def get_time():
    return str(int(time.time()))


def get_question_max_id():
    with open('sample_data/questions.csv') as f:
        read = csv.DictReader(f)
        max_id = '0'
        for row in read:
            if max_id < row['id']:
                max_id = row['id']
    return max_id


def write_to_question_csv(site_input):
    id = str(int(get_question_max_id()) + 1)
    submission_time = get_time()
    view_number = '0'
    vote_number = '0'
    title = site_input[0]
    message = site_input[1]
    image = 'No image'
    return_value = [id, submission_time,
                    view_number, vote_number,
                    title, message, image]
    return return_value


