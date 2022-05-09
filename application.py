import re
import os

import pandas as pd

import joblib
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.corpus import stopwords
from transformers import BertTokenizer

from flask import Flask, request, render_template

from celery import Celery
from celery.result import AsyncResult


SIZE = 100
STOP_WORDS = stopwords.words('english')
model = joblib.load('model_rfc_lsml2.joblib')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

app = Flask(__name__)

redis_host = os.environ.get('REDIS_HOST', 'localhost')
celery_app = Celery('application', backend=f'redis://{redis_host}', broker=f'redis://{redis_host}')


def get_test_text_preparation(text, size=SIZE):
    clean_text = ' '.join(nltk.word_tokenize(re.sub(r'[^a-zA-Z]', ' ', str(text)).lower()))
    tokens = tokenizer.convert_tokens_to_ids(
            ['[CLS]'] + tokenizer.tokenize(clean_text)[:(size - 2)] + ['[SEP]']
            )
    if len(tokens) < size:
        tokens.extend([0 for _ in range(size - len(tokens))])
    return pd.DataFrame([tokens]).fillna(0)


@celery_app.task
def get_comment_class(comment):
    vector = get_test_text_preparation(comment)
    prediction = model.predict(vector)[0]
    print(prediction)
    result = 'toxic' if prediction else 'not toxic'
    return result


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def submit():
    # time.sleep(3)
    comment = request.form['text']
    task = get_comment_class.delay(comment)
    task_id = task.id
    response = {'task_id': task_id}
    return response


@app.route('/task/<task_id>', methods=['GET'])
def task(task_id):
    task = AsyncResult(task_id, app=celery_app)
    response = {
        'ready': task.ready(),
        'result': str(task.result) if task.ready() else None
    }
    return response


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
