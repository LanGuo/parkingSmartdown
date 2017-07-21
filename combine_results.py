import pandas as pd

geocoded = pd.read_csv('./top_address_geocoded_2007_2008.csv')
statsByMonth = pd.read_csv('./ticket_counts_n_total_fine_by_month_2007_2008.csv')

combined = geocoded.merge(statsByMonth, how='inner', on='address')

combined.to_csv('./top_addresses_parking_latlong_n_monthly_stats')
