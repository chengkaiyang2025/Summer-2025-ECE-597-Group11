import logging

from flask import Flask, render_template, request

from models.check_result import HuggingFaceModelResult1, DumbCheckResult

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,  #  DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
from services.model_loader import d1, h1, p1


@app.route('/', methods=['GET', 'POST'])
def index():
    body = ""
    result = HuggingFaceModelResult1("",0)
    subject = ""
    if request.method == 'POST':
        subject = request.form.get('subject')
        body = request.form.get('body')
        model_type = request.form.get('model_type')
        print(model_type)
        #
        # result = h1.process(body,subject)
        if model_type == 'huggingface1':
            result = h1.process(body, subject)
        elif model_type == 'dumb':
            result = d1.process(body, subject)
        elif model_type == 'logistic-regression':
            result = p1.process(body, subject)
        print(result)

    return render_template('index.html', result=result,body=body,subject=subject)
    # else:
    #     return render_template("index.html")

if __name__ == '__main__':
    # Test mode
    app.run(host='0.0.0.0', port=5000,debug=False)
    # Debug mode
    # app.run(debug=True)
