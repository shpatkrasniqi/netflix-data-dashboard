from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import pathlib

app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.title = "Netflix Data Dashboard"

def card_builder(header, myId,kids):
    card_content = [
        dbc.CardHeader(header),
        dbc.CardBody(html.H5(id=myId, className="card-text", children=kids)),
    ]
    return card_content

BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

#Read Data
df = pd.read_csv(DATA_PATH.joinpath('netflixdataset.csv'))

#Get number of mobies and series
movies = df.type.value_counts()[0]
series = df.type.value_counts()[1]

#Created a dataframe containing only movies
movies_df = df.loc[df.type == 'Movie']

#Formatted the 'duration' column and sorted the movies from shortest to longest on a new dataframe
movies_dff = movies_df.copy()
movies_dff= movies_dff[movies_dff['duration'].notna()]
movies_dff['duration'] = movies_dff['duration'].str.rstrip(' min').astype('int64')
movies_dff =  movies_dff.sort_values('duration').reset_index()

#Find the average lenght of the movies listed
avg_movie_len = str(round(movies_dff['duration'].mean(), 1)) + ' minutes'

#Sorted and listed all the directors and the nuber of movies they produced
directors_data = movies_df.director.str.split(", ").explode().value_counts()
dir_fig = px.line(directors_data, labels={'index':'Director', 'value':'Number of Movies'}, title='Directors with the most movies produced')

#Sorted and listed all the countries and the nuber of movies they produced
country_data = movies_df.country.str.split(", ").explode().value_counts()
country_fig = px.line(country_data, labels={'index':'Country', 'value':'Number of Movies'}, title='Countries with the most movies produced')

#Sorted and listed all the genres and the nuber of movies in those genres
genre_data = movies_df.listed_in.str.split(", ").explode().value_counts()
genre_fig = px.line(genre_data, labels={'index':'Genre', 'value':'Number of Movies'}, title='Most popular movie genres')

#Ploted the graph/chart containing the lengths of movies
length_fig = px.line(movies_dff, x='title', y='duration', labels={'title':'Title', 'duration':'Duration (in minutes)'}, title='Movie Lengths (shortest to longest)')

#Application layout 
app.layout = html.Div([
    #This Div contains all the text fields
    html.Div([
        dbc.Container([
            dbc.Row(html.H3('Netflix Data Dashboard')),

            html.Br(),

            dbc.Row(dbc.Col( dbc.Card(card_builder('Number of Movies', 'num-mov-out', movies), color='secondary', outline=True))),

            html.Br(),

            dbc.Row(dbc.Col(dbc.Card(card_builder('Number of Series', 'num-ser-out', series), color='secondary', outline=True))),
                
            html.Br(),

            dbc.Row(dbc.Col(dbc.Card(card_builder('Avg. Movie Length', 'avg-mov-out', avg_movie_len), color='secondary', outline=True))),

            ]),
        ], style={'padding':10, 'flex':2}),
    #This Div contains all the graphs/charts
    html.Div([
        dbc.Row(dcc.Graph(id='director-graph', figure=dir_fig)),
        dbc.Row(dcc.Graph(id='country-graph', figure=country_fig)),
        dbc.Row(dcc.Graph(id='genre-graph', figure=genre_fig)),
        dbc.Row(dcc.Graph(id='length-graph', figure=length_fig))

    ], style={'padding':10, 'flex':8})
], style={'display':'flex', 'flex-direction':'row'})


if __name__ == '__main__':
    app.run_server(debug=True)