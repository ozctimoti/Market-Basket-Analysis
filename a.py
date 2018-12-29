import os
import csv
import numpy as np
import pandas as pd

os.chdir('./Data/')

a = pd.read_csv('Adsız.csv', sep=';')
a.to_csv('Sonunda.csv', sep=',')
