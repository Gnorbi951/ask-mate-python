from flask import Flask, request, render_template, url_for
import util
import data_manager
import connection

app = Flask(__name__)


@app.route('/')
def modify_me():
    return render_template('list.html')


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )