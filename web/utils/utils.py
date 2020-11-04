import numpy as np
from datetime import datetime,timedelta, date
# check your pickle compability, perhaps its pickle not pickle5
import pickle5 as pickle
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import zscore
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,plot_confusion_matrix,classification_report



def load_confirmed():
  confirmedGlobal = pd.read_csv(
      'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', encoding='utf-8', na_values=None)
  barPlotData = confirmedGlobal[["Country/Region", confirmedGlobal.columns[-1]]].groupby(
      "Country/Region").sum().sort_values(by=confirmedGlobal.columns[-1], ascending=False)
  barPlotData.reset_index(inplace=True)
  barPlotData.columns = ["Country/Region", 'values']
  barPlotData = barPlotData.sort_values(by='values', ascending=False)
  barPlotData.replace(to_replace='US', value='United States',
                      regex=True, inplace=True)
  barPlotVals = barPlotData["values"].values.tolist()
  countryNames = barPlotData["Country/Region"].values.tolist()
  df_pop = pd.read_json('web/dataset/population.json')
  df_pop.columns = ['Country/Region', 'population']
  final_df = pd.merge(barPlotData, df_pop, how='inner', on='Country/Region')
  final_df['cases/million'] = (final_df['values']/final_df['population'])*1000000
  final_df.dropna(subset=['cases/million'], inplace=True)
  return final_df

def load_recovered():
  confirmedGlobal = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv', encoding='utf-8', na_values=None)
  barPlotData = confirmedGlobal[["Country/Region", confirmedGlobal.columns[-1]]].groupby(
    "Country/Region").sum().sort_values(by=confirmedGlobal.columns[-1], ascending=False)
  barPlotData.reset_index(inplace=True)
  barPlotData.columns = ["Country/Region", 'values']
  barPlotData = barPlotData.sort_values(by='values', ascending=False)
  barPlotData.replace(to_replace='US', value='United States',
                    regex=True, inplace=True)
  barPlotVals = barPlotData["values"].values.tolist()
  countryNames = barPlotData["Country/Region"].values.tolist()
  df_pop = pd.read_json('web/dataset/population.json')
  df_pop.columns = ['Country/Region', 'population']
  final_df = pd.merge(barPlotData, df_pop, how='inner', on='Country/Region')
  final_df['cases/million'] = (final_df['values']/final_df['population'])*1000000
  final_df.dropna(subset=['cases/million'], inplace=True)
  return final_df
  

def load_deaths():
  confirmedGlobal = pd.read_csv(
      'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv', encoding='utf-8', na_values=None)
  barPlotData = confirmedGlobal[["Country/Region", confirmedGlobal.columns[-1]]].groupby(
      "Country/Region").sum().sort_values(by=confirmedGlobal.columns[-1], ascending=False)
  barPlotData.reset_index(inplace=True)
  barPlotData.columns = ["Country/Region", 'values']
  barPlotData = barPlotData.sort_values(by='values', ascending=False)
  barPlotData.replace(to_replace='US', value='United States',
                      regex=True, inplace=True)
  barPlotVals = barPlotData["values"].values.tolist()
  countryNames = barPlotData["Country/Region"].values.tolist()
  df_pop = pd.read_json('web/dataset/population.json')
  df_pop.columns = ['Country/Region', 'population']
  final_df = pd.merge(barPlotData, df_pop, how='inner', on='Country/Region')
  final_df['cases/million'] = (final_df['values'] /
                               final_df['population'])*1000000
  final_df.dropna(subset=['cases/million'], inplace=True)
  return final_df




