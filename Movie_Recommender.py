from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_table import Table, Col

#building flask table for showing recommendation results
class Results(Table):
    id = Col('Id',show=False)
    title = Col('movie')

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
        cv = CountVectorizer()
        
        count_matrix = cv.fit_transform(df['combination'])
        cosine_sim = cosine_similarity(count_matrix)

        #reading movie title given by user in the front-end
        Movie = request.form.get('fmovie')
       
        #Generating recommendations based on top score movies
        def recommendations(X, n_recommendations):
            movies['score'] = get_score(categories, preferences)
            return movies.sort_values(by=['score'], ascending=False)['title'][:n_recommendations]

        
        def recommend(m_or_i):
            dfresult = pd.DataFrame(columns=['Id','title'])
            if m_or_i in df['Id'].unique():
                m = df.iloc[int(m_or_i)]['movie_title']
            elif m_or_i in df['movie_title'].unique():
                m = m_or_i
            else:
                print('Ce film n''est pas dans notre database. Veuillez choisir un autre film.')
                raise ValueError('The film is not in our database. Please choose another film.')

            i = df.loc[df['movie_title'] == m].index[0]
            dfcluster = df.loc[df['cluster'] == df['cluster'][i]]
            dfcluster = dfcluster.reset_index()
            i = dfcluster.loc[dfcluster['movie_title'] == m].index[0]
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(dfcluster['combination'])
            cosine_sim = cosine_similarity(count_matrix)

            lst = list(enumerate(cosine_sim[i]))
            lst = sorted(lst,key = lambda x:x[1],reverse=True)
            lst = lst[1:6]
            l = []
            for i in range(len(lst)):
                a = lst[i][0]
                l.append(dfcluster['movie_title'][a])
                dfresult = dfresult.append({'title': l[i],'Id': i}, ignore_index=True)
            return (dfresult['title'])

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