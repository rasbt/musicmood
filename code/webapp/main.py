from flask import Flask, render_template, request, url_for
from wtforms import Form, TextField, validators, StringField, SubmitField
from flask.ext.wtf import Form, RecaptchaField
from wtforms.validators import Required
import sys
import os
import pickle
import sqlite3
#import dill



reload(sys)
sys.setdefaultencoding("utf-8")

my_dir = os.path.dirname(__file__)

DATABASE1 = os.path.join(my_dir, 'all_data.sqlite')
DATABASE2 = os.path.join(my_dir, 'artist_title_650.sqlite')

app = Flask(__name__)
app.config.from_object(__name__)


class SearchForm(Form):
    artistname = TextField('Artist name: ', [validators.DataRequired()])
    songtitle = TextField('Song title: ', [validators.DataRequired()])


### Load Pickle objects

try:
    d = open(os.path.join(my_dir, 'label_encoder.p'), 'rb')
    le = pickle.load(d)
finally:
    d.close()

try:
    d = open(os.path.join(my_dir, 'countv.p'), 'rb')
    vect  = pickle.load(d)
finally:
    d.close()

try:
    d = open(os.path.join(my_dir, 'clf_countv.p'), 'rb')
    clf = pickle.load(d)
finally:
    d.close()


#####################
# Lyrics Downloader
#####################


import urllib
import lxml.html
import unicodedata

import urllib, re
import bs4



def songlyrics(artist, title):
    artist = urllib.quote(artist.lower().replace(' ','-'))
    title = urllib.quote(title.lower().replace(' ','-'))

    try:
        lyrics = urllib.urlopen('http://www.songlyrics.com/%s/%s-lyrics/' % (artist,title))
    except:
        return None
    text = lyrics.read()
    soup = bs4.BeautifulSoup(text)
    lyrics = soup.findAll(attrs= {'id' : 'songLyricsDiv'})
    if not lyrics:
        return None
    else:
        if str(lyrics[0]).startswith("<p class='songLyricsV14 iComment-text' id='songLyricsDiv'></p>"):

            return None
        try:
            return re.sub('<[^<]+?>', '', ''.join(str(lyrics[0])))
        except:
            return None

def lyricsmode(artist, title):
    artist = urllib.quote(artist.lower().replace(' ','_'))
    title = urllib.quote(title.lower().replace(' ','_'))

    try:
        url = 'http://www.lyricsmode.com/lyrics/%s/%s/%s.html' % (artist[0],artist, title)
        lyrics = urllib.urlopen(url)
    except:
        return 'Sorry, can not download lyrics right now.'
    text = lyrics.read()
    soup = bs4.BeautifulSoup(text)
    #lyricsmode places the lyrics in a span with an id of "lyrics"
    lyrics = soup.findAll(attrs= {'id' : 'lyrics_text'})
    if not lyrics:
        return 'Lyrics not found.'
    try:
        return re.sub('<[^<]+?>', '', ''.join(str(lyrics[0])))
    except:
        return 'Lyrics not found.'

def get_lyrics(artist, title):
    lyr = songlyrics(artist, title)
    if not lyr:
        lyr = lyricsmode(artist, title)
    return lyr



#####################
# Flask apps
#####################



@app.route('/')
def index():
    form = SearchForm(request.form, csrf_enabled=False)
    return render_template('searchform.html', form=form)



@app.route('/results', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.form, csrf_enabled=False)


    if (request.form['search_btn'] in ('Random song', 'Random happy song', 'Random sad song')) or\
                (request.method == 'POST' and form.validate()):


        # Return random artist and title or happy or sad
        if request.form['search_btn'] in ('Random song', 'Random happy song', 'Random sad song'):


            if request.form['search_btn'] == 'Random happy song':
                conn = sqlite3.connect(app.config['DATABASE1'])
                cursor = conn.cursor()
                sql = "SELECT artist,title FROM moodtable WHERE majoritymood='happy' ORDER BY RANDOM() LIMIT 1;"

            elif request.form['search_btn'] == 'Random sad song':
                conn = sqlite3.connect(app.config['DATABASE1'])
                cursor = conn.cursor()
                sql = "SELECT artist,title FROM moodtable WHERE majoritymood='sad' ORDER BY RANDOM() LIMIT 1;"

            else:
                conn = sqlite3.connect(app.config['DATABASE2'])
                cursor = conn.cursor()
                sql = "SELECT artist,title FROM artist_title ORDER BY RANDOM() LIMIT 1;"

            cursor.execute(sql)
            result = cursor.fetchone()
            artistname = result[0].decode('utf-8')
            songtitle = result[1].decode('utf-8')
            conn.close()

        # Get artist and title from form
        else:
            artistname=request.form['artistname']
            songtitle=request.form['songtitle']


        lyr = get_lyrics(artistname,songtitle)

        if len(lyr) < 5 or lyr == 'Lyrics not found.':
            lyr = 'Sorry, lyrics could not be found.'
            return render_template('nolyrics.html',
                                    artistname=artistname,
                                    songtitle=songtitle,
                                    lyrics=lyr,
                                   )
        else:
            x_vect = vect.transform([lyr])
            pred = clf.predict(x_vect)[0]
            label = le.inverse_transform(pred)
            if label == 'happy':
                font_color = 'green'
            else:
                font_color = 'red'


            #proba = clf.predict_proba(x_vect).ravel()[pred]
            #proba = round(proba * 100, 2)
            #proba = '  (probability %.2f%%)' % (proba)
            button_happy = 'happy'
            button_sad = 'sad'
            btn_type = 'submit'


            # save artistname and song title temporarily to update the database if
            # feedback is provided
            try:
                d = open(os.path.join(my_dir, 'temp.p'), 'wb')
                pickle.dump([unicode(artistname.lower()),unicode(songtitle.lower()),unicode(lyr)], d)
            finally:
                d.close()

            # print number of mood labels
            try:
                d = open(os.path.join(my_dir, 'num_moodlab.p'), 'rb')
                num_moodlab = pickle.load(d)
            finally:
                d.close()
            num_moodlab += 1
            try:
                d = open(os.path.join(my_dir, 'num_moodlab.p'), 'wb')
                pickle.dump(num_moodlab, d)
            finally:
                d.close()

            # printnumber of samples
            conn = sqlite3.connect(app.config['DATABASE1'])
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM moodtable"
            cursor.execute(sql)
            result = cursor.fetchone()
            conn.close()


        return render_template('foundlyrics.html',
                                artistname=artistname,
                                songtitle=songtitle,
                                lyrics=lyr, pred=label,
                                #proba=proba,
                                button_happy=button_happy,
                                button_sad=button_sad,
                                num_moodlab=num_moodlab,
                                num_lyrics=result[0],
                                font_color=font_color
                               )

    return render_template('searchform.html', form=form)


@app.route('/feedback', methods=['POST'])
def feedback():
    # get response and update sqlite table

    if request.form['feedback_button'] == 'happy':
        userlabel = u',happy'
    else:
        userlabel = u',sad'

    artistname, songtitle, lyr = pickle.load(open(os.path.join(my_dir, 'temp.p'), 'rb'))

    conn = sqlite3.connect(app.config['DATABASE1'])
    cursor = conn.cursor()

    sql = "SELECT mood FROM moodtable WHERE artist=? AND title=?"
    cursor.execute(sql, [(artistname), (songtitle)])
    cur =  cursor.fetchone()

    if cur:
        cur = cur[0]
        cur += userlabel

        sql = "UPDATE moodtable SET mood=? WHERE artist=? AND title=?"
        cursor.execute(sql, [(cur), (artistname), (songtitle)])

    else:
        sql = "INSERT INTO moodtable VALUES (?,?,?,?,?)"
        cursor.execute(sql, [(artistname), (songtitle), (lyr), (userlabel.strip(',')), (None)])

    conn.commit()
    conn.close()


    # print number of mood labels
    num_moodlab = pickle.load(open(os.path.join(my_dir, 'num_moodlab.p'), 'rb'))
    num_moodlab += 1
    pickle.dump(num_moodlab, open(os.path.join(my_dir, 'num_moodlab.p'), 'wb'))

    # printnumber of samples
    conn = sqlite3.connect(app.config['DATABASE1'])
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM moodtable"
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()


    return render_template('thanks.html',
                            num_moodlab=num_moodlab,
                            num_lyrics=result[0]
                            )



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

if __name__ == '__main__':
    app.run(debug=True)