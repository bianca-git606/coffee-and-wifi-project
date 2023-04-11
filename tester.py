import csv

with open('cafe-data.csv', 'a') as file:
    w = csv.writer(file)
    w.writerow(f'\n{list}')