from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import pickle
import sqlite3
import os
import numpy as np


app = Flask(__name__)

######## Preparing the Classifier
cur_dir = os.path.dirname(__file__)
pkl_dir = os.path.join(cur_dir, 'pkl_objects')

try:
    d = open(os.path.join(pkl_dir, 'label_encoder.p'), 'rb')
    le = pickle.load(d)
finally:
    d.close()

try:
    d = open(os.path.join(pkl_dir, 'countv.p'), 'rb')
    vect = pickle.load(d)
finally:
    d.close()

try:
    d = open(os.path.join(pkl_dir, 'clf_countv.p'), 'rb')
    clf = pickle.load(d)
finally:
    d.close()



def classify(document):

    x_vect = vect.transform([document])
    proba = np.max(clf.predict_proba(x_vect))
    pred = clf.predict(x_vect)[0]
    label = le.inverse_transform(pred)
    return label, proba


######## Flask
class ReviewForm(Form):
    moviereview = TextAreaField('',
                                [validators.DataRequired(),
                                validators.length(min=15)])

@app.route('/')
def index():
    form = ReviewForm(request.form)
    return render_template('reviewform.html', form=form)

@app.route('/results', methods=['POST'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = request.form['moviereview']
        y, proba = classify(review)
        return render_template('results.html',
                                content=review,
                                prediction=y,
                                probability=round(proba*100, 2))
    return render_template('reviewform.html', form=form)

@app.route('/thanks', methods=['POST'])
def feedback():
    feedback = request.form['feedback_button']
    review = request.form['review']
    prediction = request.form['prediction']

    inv_label = {'negative': 0, 'positive': 1}
    y = inv_label[prediction]

    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
