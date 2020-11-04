from altair import Chart, X, Y, Axis, Data, DataFormat
import pandas as pd
import numpy as np
from flask import render_template, url_for, flash, redirect, request, make_response, jsonify, abort
import pickle
from web import app
from web.utils import utils
from scipy.stats import zscore
import scipy.stats as stats
import csv
import requests


final_df = utils.load_confirmed()

@app.route("/")
@app.route("/index")
def index():
    countries = final_df['Country/Region'].values.tolist()
    total_values = final_df['values'].values.tolist()
    cases_per_million = final_df['cases/million'].values.round(2).tolist()
    context = {'countries': countries, 'total_values': total_values,
               'cases_per_million': cases_per_million}
    return render_template('chartjs.html', context=context)
