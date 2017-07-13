#!usr/bin/python

import pandas as pd

parkingData = pd.read_csv('./parking2007_2008.csv')

statsByLocation = parkingData.groupby('Location').describe().unstack()

ticketAmountByLocation = statsByLocation['Amount Due'].reset_index()

ticketAmountByLocation.to_csv('./parking_aggregate_2007_2008.csv')