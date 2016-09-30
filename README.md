# MusicMood

### A machine learning approach to classify music by mood based on song lyrics.

This project is about building a music recommendation system for users who want to listen to *happy* songs. Such a system can not only be used to brighten up one's mood on a rainy weekend; especially in hospitals, other medical clinics, or public locations such as restaurants, the MusicMood classifier could be used to spread positive mood among people.

<br>

### Links

- [The web application](http://sebastianraschka.com/Webapps/musicmood.html)
- [The data collection IPython notebook](http://nbviewer.ipython.org/github/rasbt/musicmood/blob/master/code/collect_data/data_collection.ipynb)
- [The initial model training IPython notebook](http://nbviewer.ipython.org/github/rasbt/musicmood/blob/master/code/classify_lyrics/nb_init_model.ipynb)
- [The updated model training with white lists IPython notebook](http://nbviewer.ipython.org/github/rasbt/musicmood/blob/master/code/classify_lyrics/nb_whitelist_model.ipynb)
- [Experiments with Random Forests IPython notebook](http://nbviewer.ipython.org/github/rasbt/musicmood/blob/master/code/classify_lyrics/random_forests.ipynb)
- [An article about my experiences with this project](http://sebastianraschka.com/Articles/2014_musicmood.html)
- [A keynote presentation about this project](http://www.slideshare.net/SebastianRaschka/musicmood-20140912)

<br>
<br>

### Sections
<hr>

- [Dataset Summary](#dataset-summary)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Results](#results)

<hr>

<br>
<br>

![](./images/flowchart.png)


<br>
<br>



## Dataset Summary
[back to top](#sections)

- A 10,000-song subset was downloaded from the [Million Song Dataset](http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset).
- Lyrics were automatically downloaded from [LyricWikia](http://lyrics.wikia.com/Lyrics_Wiki) and all songs for which lyrics have not been available were removed from the dataset.
 - An English language filter was applied to detect and remove all non-English songs.
 -  The remaining songs were randomly subsampled into a 1000-song training dataset and 200-song validation dataset.



<br>
<br>

## Exploratory Data Analysis

[back to top](#sections)

![](./images/exploratory_1.png)

<br>
<br>

![](./images/wordclouds.png)


<br>
<br>


## Results
[back to top](#sections)


![](./images/roc_best.png)

![](./images/performance_table.png)
