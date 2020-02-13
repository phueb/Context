from flask import Flask, make_response
from flask import request
from flask import jsonify
import pandas as pd
import random


app = Flask(__name__)


NUM_PARTS = 256
PART_SIZE = 100
NUM_WORDS = 50

words = ['w{}'.format(i) for i in range(NUM_WORDS)]
parts = [random.choices(random.choices(words, k=10), k=PART_SIZE)
         for _ in range(NUM_PARTS)]


@app.route('/', methods=['POST'])
def demo():
    """return html table showing linguistic contexts for word in HTTP POST request"""

    if request.form.get('text') is not None:
        word = request.form.get('text')
    else:
        word = 'BAD'

    # make html table containing linguistic contexts
    probe_context_df = pd.DataFrame(index=[probe_id] * len(probe_x_mat), data=probe_x_mat)
    table_df = probe_context_df.apply(
        lambda term_ids: [model.hub.train_terms.types[term_id] for term_id in term_ids])
    table_html = table_df.to_html(index=False, header=False).replace('border="1"', 'border="0"')

    # make json response + add headers
    response = make_response(jsonify({'result': table_html}))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    return response


if __name__ == "__main__":  # pycharm does not use this
    app.run(port=5000, debug=True, host='0.0.0.0')
