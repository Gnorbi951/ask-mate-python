import csv


def get_data():
    """Get the data from the csv as an Ordered_Dict list"""
    csv_data = []
    with open('sample_data/questions.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = dict(row)
            csv_data.append(d)
    return csv_data[::-1]
