# Soda
 #### Sonification of Data for Learning Analytics

Open source application to sonify learning analytics data based on users preference.
Designed to be used as a data exploration tool.

### Sonification
“A systematic and reproducible transformation technique that can be used with different input data to produce sound that reflects objective properties or relations in the data.”

We think that new radical ideas are needed for learning analytics and we want to drastically reverse the traditional approach that is actually based on data visualization. We want to explore the potential of data sonification for the analysis of complex datasets in the field of educational sciences. Thus, Soda aims at evaluating the feasibility and the potential value of sonification for learning analytics.

### Tutorial

The first step after starting Soda is to load your data. Soda will try to automatically detect which column is suitable to be treated as timestamp. If multiple columns are detected or if Soda doesn't recognize your time format, it will be necessary to select the appropriate column.

![Use case example](data/img/tutorial/2.PNG)

After validation, you can create your first track to sonify your data!
![Use case example](data/img/tutorial/3.PNG)

Once this is done, you can select your favorite variable in the drop down menu and press "randomize all" to assign a random note to each entry. Pressing play will then start your first music!
![Use case example](data/img/tutorial/4.PNG)

You can modify which note is associated to which instance of your variable, so that the end music makes more sense to your ear. Trying different pattern and combination of notes can yield really different results!

Grouping instances of variables under the same note will reduce the complexity of the music. You can also encode specific behavior to a natural progression of notes (A->B->C) 
![Use case example](data/img/tutorial/5.PNG)

Multiple tracks can be added, duplicated or deleted. Each track has its own instrument alongside its own volume, offset and encoding options.

Specific instances of a variable can be muted for each track using the green or red dot, or by pressing "check all" or "switch all" buttons.

This enables more complex encoding to emerge and can improve the quality of the music.
![Use case example](data/img/tutorial/6.PNG)

More general options can be found under File->Settings or by pressing the cog button on the top left.

The most important options are song length and beat/row per minutes, which will change the speed at which data is processed and played. Changing one of these options will update the other one.
![Use case example](data/img/tutorial/7.PNG)

Adding drum tracks with the same note for each instance of a variable can enrich the music.
![Use case example](data/img/tutorial/8.PNG)

Changing the value of a note is not the only encoding possible! Encodings of the duration (how long a note is played) or volume (how loud a note is played) can be fine tuned for each instance.
![Use case example](data/img/tutorial/9.PNG)

Multiple utilities can be found under File: you can save a project for later or export your end music to a .wav format.
Multiple data set can be loaded concurrently, but they should have the same headers and structure. You can switch between files by selecting the corresponding tab on the data visualization module.
![Use case example](data/img/tutorial/10.PNG)


### Install
Check release page for the latest version.
github.com/AndreCI/sodaMidi/releases

### About
André Cibils\
UNIGE - Technologies de Formation et d'Apprentissage\
Sous la supervision du Pr. Eric Sanchez