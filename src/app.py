from flask import Flask, make_response
from flask import request
from flask import jsonify
import pandas as pd
from pathlib import Path
from functools import reduce
from operator import iconcat


app = Flask(__name__)

CONTEXT_SIZE = 3
CORPUS_NAME = 'childes-20191112'
NUM_DOCS = 10_000

# load tokens
p = Path(__file__).parent.parent / 'corpora' / f'{CORPUS_NAME}.txt'
if not p.exists():  # on pythonanywhere.com
    p = Path(__file__).parent / 'corpora' / f'{CORPUS_NAME}.txt'
text_in_file = p.read_text()
docs = text_in_file.split('\n')[:NUM_DOCS]
tokenized_docs = [d.split() for d in docs]
tokens = reduce(iconcat, tokenized_docs, [])  # flatten list of lists


@app.route('/', methods=['POST'])
def demo():
    """return html table showing linguistic contexts for word in HTTP POST request"""

    if request.form.get('text') is not None:
        word = request.form.get('text')
    else:
        word = 'orange'

    # make html table containing linguistic contexts
    col2data = {d: [] for d in range(-CONTEXT_SIZE, CONTEXT_SIZE + 1, 1)}
    for loc, w in enumerate(tokens):
        if w == word:
            for d in range(-CONTEXT_SIZE, CONTEXT_SIZE + 1, 1):
                col2data[d].append(tokens[loc+d])

    df = pd.DataFrame(data=col2data)
    table_html = df.to_html(index=False, header=False).replace('border="1"', 'border="0"')

    # make json response + add headers
    response = make_response(jsonify({'result': table_html}))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    return response


if __name__ == "__main__":
    app.run()