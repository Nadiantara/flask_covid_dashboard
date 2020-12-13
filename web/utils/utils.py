import numpy as np
from datetime import datetime,timedelta, date
# check your pickle compability, perhaps its pickle not pickle5
import pandas as pd
import json


def load_chartjs_map_data(final_df, df_pop):
  # ref : https://www.highcharts.com/demo/maps/tooltip
  chartjs_ccode = pd.read_json(
      "https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json")
  chartjs_ccode
  chartjs_map = final_df[["code3", "Country/Region", "confirmed"]]
  chartjs_map.columns = ["code3", "name", "value"]
  chart_json = chartjs_map.to_dict('records')
  return chart_json




#loading data
def load_data():

    total_confirmed = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', encoding='utf-8', na_values=None)
    total_death = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv', encoding='utf-8', na_values=None)

    total_recovered = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv', encoding='utf-8', na_values=None)
    total_confirmed.replace(
        to_replace='US', value='United States', regex=True, inplace=True)
    total_recovered.replace(
        to_replace='US', value='United States', regex=True, inplace=True)
    total_death.replace(
        to_replace='US', value='United States', regex=True, inplace=True)
    # I need data that contain population for each country to calculate confirmed cases/population
    # I download it from : https://github.com/samayo/country-json/blob/master/src/country-by-population.json
    df_pop = pd.read_json(
        'https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json')
    #some country name has different  format, so I need to change it to match my first dataset
    df_pop.columns = ['Country/Region', 'population']
    df_pop = df_pop.replace(to_replace='Russian Federation', value='Russia')
    

    return total_confirmed, total_death, total_recovered, df_pop


def preprocessed_data(total_confirmed, total_death, total_recovered):
    #grouped total confirmed data
    grouped_total_confirmed = total_confirmed[["Country/Region", total_confirmed.columns[-1]]].groupby(
        "Country/Region").sum().sort_values(by=total_confirmed.columns[-1], ascending=False)
    grouped_total_confirmed.reset_index(inplace=True)
    grouped_total_confirmed.columns = ["Country/Region", 'confirmed']
    grouped_total_confirmed.replace(
        to_replace='US', value='United States', regex=True, inplace=True)

    #Chart.js can't plot dataframe object, so we need to change some to list
    barplot_confirmed_values = grouped_total_confirmed["confirmed"].values.tolist(
    )
    country_names = grouped_total_confirmed["Country/Region"].values.tolist()

    #global time series confirmed data frame
    global_confirmed_timeseries = pd.DataFrame(
        total_confirmed[total_confirmed.columns[4:]].sum())
    global_confirmed_timeseries.reset_index(inplace=True)
    global_confirmed_timeseries.columns = ['date', 'total confirmed']

    #global daily new cases = global daily confirmed at date (t) -  global daily confirmed at date (t-1)
    global_confirmed_timeseries["daily new cases"] = global_confirmed_timeseries['total confirmed'] - \
        global_confirmed_timeseries['total confirmed'].shift()
    global_confirmed_timeseries = global_confirmed_timeseries.fillna(0)

    #grouped total recovered data
    grouped_total_recovered = total_recovered[["Country/Region", total_recovered.columns[-1]]].groupby(
        "Country/Region").sum().sort_values(by=total_recovered.columns[-1], ascending=False)
    grouped_total_recovered.reset_index(inplace=True)
    grouped_total_recovered.columns = ["Country/Region", 'recovered']
    grouped_total_recovered.replace(
        to_replace='US', value='United States', regex=True, inplace=True)

    #Chart.js can't plot dataframe object, so we need to change some to list
    barplot_recovered_values = grouped_total_recovered["recovered"].values.tolist(
    )
    country_names = grouped_total_confirmed["Country/Region"].values.tolist()

    #global time series recovered data frame
    global_recovered_timeseries = pd.DataFrame(
        total_recovered[total_recovered.columns[4:]].sum())
    global_recovered_timeseries.reset_index(inplace=True)
    global_recovered_timeseries.columns = ['date', 'total recovered']

    #global daily recovered = global daily recovered at date (t) -  global daily recovered at date (t-1)
    global_recovered_timeseries["daily new recovered"] = global_recovered_timeseries['total recovered'] - \
        global_recovered_timeseries['total recovered'].shift()
    global_recovered_timeseries = global_recovered_timeseries.fillna(0)

    # grouping the data by each country to get total confirmed cases
    grouped_total_death = total_death[["Country/Region", total_death.columns[-1]]].groupby(
        "Country/Region").sum().sort_values(by=total_death.columns[-1], ascending=False)
    grouped_total_death.reset_index(inplace=True)
    grouped_total_death.columns = ["Country/Region", 'deaths']
    grouped_total_death.replace(
        to_replace='US', value='United States', regex=True, inplace=True)

    #Chart.js can't plot dataframe object, so we need to change some to list
    barplot_death_values = grouped_total_death["deaths"].values.tolist()
    global_death_timeseries = total_death[total_death.columns[4:]].sum()

    #global time series death data frame
    global_death_timeseries = pd.DataFrame(
        total_death[total_death.columns[4:]].sum())
    global_death_timeseries.reset_index(inplace=True)
    global_death_timeseries.columns = ['date', 'total deaths']

    #global daily deaths = global daily deaths at date (t) -  global daily deaths at date (t-1)
    global_death_timeseries["daily new deaths"] = global_death_timeseries['total deaths'] - \
        global_death_timeseries['total deaths'].shift()
    global_death_timeseries = global_death_timeseries.fillna(0)
    global_death_timeseries

    #merge all the data to get full time series dataframe
    timeseries_final = pd.merge(
        global_confirmed_timeseries, global_recovered_timeseries, how='inner', on='date')
    timeseries_final = pd.merge(
        timeseries_final, global_death_timeseries, how='inner', on='date')
    timeseries_final
    return grouped_total_confirmed, grouped_total_recovered, grouped_total_death, timeseries_final, country_names


def merge_data(grouped_total_confirmed, grouped_total_recovered, grouped_total_death, df_pop):
  # I also need country code for geographical analysis, Altair need numerical code and Plotly need alfabetical code
    #country code and id for later geographical analysis
    url = "https://gist.githubusercontent.com/komasaru/9303029/raw/9ea6e5900715afec6ce4ff79a0c4102b09180ddd/iso_3166_1.csv"
    country_code = pd.read_csv(url)
    country_code = country_code[[
        "English short name", "Alpha-3 code", "Numeric"]]
    country_code.columns = ["Country/Region", "code3", "id"]

    #Change the data for later merging
    #If not match the value will be deleted, so we need to make sure each country name from each table has same value
    country_code = country_code.replace(
        to_replace='Russian Federation (the)', value='Russia')
    country_code = country_code.replace(
        to_replace='United Kingdom (the)', value='United Kingdom')
    country_code = country_code.replace(
        to_replace='United States (the)', value='United States')
    country_code = country_code.replace(to_replace='Viet Nam', value='Vietnam')

    # merge them all
    final_df = pd.merge(grouped_total_confirmed,
                        grouped_total_recovered, how='inner', on='Country/Region')
    final_df = pd.merge(final_df, grouped_total_death,
                        how='inner', on='Country/Region')
    final_df = pd.merge(final_df, df_pop, how='inner', on='Country/Region')
    final_df = pd.merge(country_code, final_df,
                        how='inner', on='Country/Region')
    final_df = final_df.sort_values(by="confirmed", ascending=False)
    final_df.reset_index(inplace=True, drop=True)

    # calculate cases/million and total death rate
    final_df['cases/million'] = ((final_df['confirmed'] /
                                  final_df['population'])*1000000).round(2)
    final_df['death rate(%)'] = (
        (final_df['deaths']/final_df['confirmed'])*100).round(2)

    return final_df

# function to filter timeseries analysis by country
# I use "case" variable just for column name: e.g, case = confirmed, case = deaths


def get_by_country(df, country, case):
    mask = (df['Country/Region'] == country)
    df = df.loc[mask]
    df_country = df.groupby("Country/Region").sum()
    df_country = pd.DataFrame(df[df.columns[4:]].sum())
    df_country.reset_index(inplace=True)
    df_country.columns = ['date', f"value_{case}"]
    df_country[f"daily_new_{case}"] = df_country[f"value_{case}"] - \
        df_country[f"value_{case}"].shift()
    df_country = df_country.fillna(0)
    return df_country


#use function above to get merged dataframe
def get_by_country_merged(total_confirmed, total_death, total_recovered, country):
    #apply to each timeseries
    country_confirmed_tseries = get_by_country(
        total_confirmed, country, "confirmed")
    country_death_tseries = get_by_country(total_death, country, "death")
    country_recovered_tseries = get_by_country(
        total_recovered, country, "recovered")

    #merge them all
    country_timeseries_final = pd.merge(
        country_confirmed_tseries, country_death_tseries, how='inner', on='date')
    country_timeseries_final = pd.merge(
        country_timeseries_final, country_recovered_tseries, how='inner', on='date')
    country_timeseries_final.reset_index(inplace=True)
    return country_timeseries_final


def get_per_country_data(total_confirmed, total_death, total_recovered, country_name):
    #total confirmed per country
    total_confirmed_per_country = total_confirmed.groupby(
        "Country/Region").sum()
    total_confirmed_per_country.reset_index(inplace=True)
    mask = (total_confirmed_per_country['Country/Region'] == country_name)
    total_confirmed_per_country = total_confirmed_per_country.loc[mask]
    total_confirmed_per_country = total_confirmed_per_country[
        total_confirmed_per_country.columns[-1]].sum()

    #total deaths per country
    total_death_per_country = total_death.groupby("Country/Region").sum()
    total_death_per_country.reset_index(inplace=True)
    mask = (total_death_per_country['Country/Region'] == country_name)
    total_death_per_country = total_death_per_country.loc[mask]
    total_death_per_country = total_death_per_country[total_death_per_country.columns[-1]].sum(
    )

    #total recovered per country
    total_recovered_per_country = total_recovered.groupby(
        "Country/Region").sum()
    total_recovered_per_country.reset_index(inplace=True)
    mask = (total_recovered_per_country['Country/Region'] == country_name)
    total_recovered_per_country = total_recovered_per_country.loc[mask]
    total_recovered_per_country = total_recovered_per_country[
        total_recovered_per_country.columns[-1]].sum()
    return total_confirmed_per_country, total_death_per_country, total_recovered_per_country
