# from flask import Flask, make_response
# from flask import jsonify
# import base64

# app = Flask(__name__)


# @app.route('/', methods=['POST', 'GET'])
# def demo():
#     """
#     return an image.
#     """

#     print('loading image!')
#     print()

#     with open("/home/phueb001/mysite/under-construction.png", "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())

#     response = make_response(jsonify({'result': encoded_string}))
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

#     return response


# if __name__ == "__main__":
#     app.run()


from flask import Flask, make_response
from flask import request
from flask import jsonify
import pandas as pd
import random


app = Flask(__name__)

CONTEXT_SIZE = 2

CORPUS_SIZE = 10_000
VOCAB_SIZE = 32

words = ['w{}'.format(i) for i in range(VOCAB_SIZE)]
tokens = [random.choice(random.choices(words, k=10)) for _ in range(CORPUS_SIZE)]


@app.route('/', methods=['POST'])
def demo():
    """return html table showing linguistic contexts for word in HTTP POST request"""

    if request.form.get('text') is not None:
        word = request.form.get('text')
    else:
        word = 'BAD'

    # make html table containing linguistic contexts
    col2data = {d: [] for d in range(-CONTEXT_SIZE, CONTEXT_SIZE, 1)}
    print(tokens[:10])
    for loc, w in enumerate(tokens):
        if w == word:
            for d in range(-CONTEXT_SIZE, CONTEXT_SIZE, 1):
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
