import csv

with open('Giants.csv', mode ='r') as file:    
       csvFile = csv.DictReader(file)
       for lines in csvFile:
            print(lines)

