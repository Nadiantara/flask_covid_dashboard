import csv
import datetime
import emoji
import gensim
import json
import math
import matplotlib.pyplot as plt
import matplotlib.dates
import nltk
import numpy as np
import operator
import os  # accessing directory structure
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.offline as offline
import plotly.express as px
import pyLDAvis
import pyLDAvis.gensim
import requests
import re
import regex
import seaborn as sns
import semver
import spacy
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import summary_table
import statsmodels.api as sm
import string
import time
import wordcloud
from bs4 import BeautifulSoup
from datetime import datetime
from distutils.version import LooseVersion
from distutils.version import StrictVersion
from gensim import corpora
from matplotlib.dates import date2num
from mpl_toolkits.mplot3d import Axes3D
from nltk.corpus import stopwords
from plotly.subplots import make_subplots
from plotly import tools
from textblob import TextBlob
from tqdm import tqdm
from wordcloud import WordCloud


def plot_totalreview_google_date(dataframe):
  df = dataframe
  df.index = df['at']
  df = pd.DataFrame(df['content'].resample('MS').count()).join(
      pd.DataFrame(df['score'].resample('MS').mean()))
  fig = go.Figure()
  fig = make_subplots(specs=[[{"secondary_y": True}]])

  fig.add_trace(
      go.Bar(
          x=df.index,
          y=df.content,
          name="Total Review",
          marker_color='#14c2a5',
          opacity=1
      ),
      secondary_y=False
  )

  fig.add_trace(
      go.Scatter(
          x=df.index,
          y=df.score,
          mode="lines",
          name="Average Rating",
          marker_color='#3d4a57',
          opacity=0.4
      ),
      secondary_y=True
  )

  # Add figure title
  fig.update_layout(legend=dict(
      orientation="h",
      yanchor="bottom",
      y=1.02,
      xanchor="right",
      x=0.93),
      title={
      'text': '<span style="font-size: 25px;">Google User Total Review and Average Rating</span>',
      'y': 0.97,
      'x': 0.45,
      'xanchor': 'center',
      'yanchor': 'top'},
      paper_bgcolor="#ffffff",
      plot_bgcolor="#ffffff",
      width=1500, height=700
  )

  # Add image
  fig.add_layout_image(
      dict(
          source="https://res-2.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco/k5gw7klohl445zwak3mc",
          xref="paper", yref="paper",
          x=0.92, y=1.04,
          sizex=0.1, sizey=0.1,
          xanchor="right", yanchor="bottom"
      )
  )

  # Set x-axis title
  fig.update_xaxes(title_text="Time")

  # Set y-axes titles
  fig.update_yaxes(title_text="Number of Reviews",
                   secondary_y=False, showgrid=False)
  fig.update_yaxes(title_text="Rating", range=[
                   0, 5], secondary_y=True, showgrid=False)
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


def plot_totalreview_google_version(dataframe):
  df_google = dataframe

  #df_google['reviewCreatedVersion'] = df_google['reviewCreatedVersion'].apply(LooseVersion)
  #df_google.sort_values(by='reviewCreatedVersion',inplace=True)
  #df_google.reset_index(drop=True, inplace=True)

  #split review
  neg_google = df_google[df_google['score'] <= 3].groupby(['reviewCreatedVersion']).count(
  ).reset_index().drop(['score', 'at'], axis=1).rename(columns={"content": "negative_review"})
  pos_google = df_google[df_google['score'] > 3].groupby(['reviewCreatedVersion']).count(
  ).reset_index().drop(['score', 'at'], axis=1).rename(columns={"content": "positive_review"})

  #merge it
  df = pd.merge(neg_google, pos_google, on=[
                'reviewCreatedVersion'], how='outer')
  df.fillna({'positive_review': 0, 'negative_review': 0}, inplace=True)
  list_version = df['reviewCreatedVersion'].tolist()
  list_version.sort(key=LooseVersion)
  dict_version = []
  for i in range(len(list_version)):
    dict_version.append(i)
  sorted_version = pd.DataFrame()
  sorted_version['dict'] = dict_version
  sorted_version['reviewCreatedVersion'] = list_version
  df = pd.merge(df, sorted_version, on=['reviewCreatedVersion'], how='right')
  df.sort_values(by=['dict'], inplace=True, ignore_index=True)

  # plot
  plot = go.Figure(data=[go.Bar(
      name='Positive Review',
      x=df['reviewCreatedVersion'],
      y=df['positive_review'],
      marker_color='rgb(52,186,83)'
  ),
      go.Bar(
      name='Negative Review',
      x=df['reviewCreatedVersion'],
      y=df['negative_review'],
      marker_color='rgb(234,67,53)'
  )
  ])
  plot.update_layout(barmode='stack')
  plot.update_layout(legend=dict(
      orientation="h",
      yanchor="bottom",
      y=1.02,
      xanchor="right",
      x=0.93),
      title={
      'text': '<span style="font-size: 25px;">Google User Review across Versions</span>',
      'y': 0.97,
      'x': 0.45,
      'xanchor': 'center',
      'yanchor': 'top'},
      paper_bgcolor="#ffffff",
      plot_bgcolor="#ffffff",
      width=1500, height=700
  )
  # Add image
  plot.add_layout_image(
      dict(
          source="https://res-2.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco/k5gw7klohl445zwak3mc",
          xref="paper", yref="paper",
          x=0.92, y=1.04,
          sizex=0.1, sizey=0.1,
          xanchor="right", yanchor="bottom"
      )
  )
  # Set x-axis title
  plot.update_xaxes(title_text="Version")
  # Set y-axes titles
  plot.update_yaxes(title_text="Number of Reviews", showgrid=False)
  graphJSON = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


