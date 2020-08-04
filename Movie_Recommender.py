from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from flask_table import Table, Col

#building flask table for showing recommendation results
class Results(Table):
    id = Col('Id',show=False)
    title = Col('movie_title')

app = Flask(__name__)

#Welcome Page
@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method=="POST":
        return render_template('recommendation.html')
    return render_template('welcome.html')

#Results Page
@app.route("/recommendation", methods=["GET", "POST"])
def recommendation():
    if request.method == 'POST':
        
        #reading the original dataset
        df = pd.read_csv('movies.csv')

        #reading movie title given by user in the front-end
        Movie = request.form.get('fmovie')
       
        def recommend(m_or_i):
            m_or_i = m_or_i.lower()
            if m_or_i in df['Id'].unique():
                m = df.iloc[int(m_or_i)]['movie_title']
                m = m.lower()
            elif m_or_i in df['movie_title'].str.lower().unique():
                m = m_or_i
            else:
                print('Ce film n''est pas dans notre database. Veuillez choisir un autre film.')
                raise ValueError('The film is not in our database. Please choose another film.')

            i = df.loc[df['movie_title'].str.lower() == m].index[0]
            cluster = df.iloc[i]['cluster'] 
            dfresult = df[(df.cluster==cluster) & (df.movie_title.str.lower() != m)].sort_values('score', ascending=False).head(20)
            dfresult = dfresult.sample(5)
            dfresult = dfresult.reset_index()
            return (dfresult['movie_title'])

        #printing top-10 recommendations
        try:
            output = recommend(Movie)
            table = Results(output)
            table.border = True
            return render_template('recommendation.html', table=table)
        except ValueError as e:
            return render_template('welcome.html', error=e)

if __name__ == '__main__':
   app.run(debug = True)