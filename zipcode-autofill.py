import os
import requests
import json
import csv
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
apikey = os.environ.get("API_KEY")
    

def get_zipcode(csv_file_path):  
    with open(csv_file_path,'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            street = row['\ufeffStreet']
            street_new = street.replace(' ','%20')
            city = row['District']
            city_new = city.replace(' ','%20')
            state = row['State']
            url = f'https://api.zip-codes.com/ZipCodesAPI.svc/1.0/ZipCodeOfAddress?address={street_new}&address1=&city={city_new}&state={state}&zipcode=&key={apikey}'
            #print(url)
            response = requests.get(url)
            parsed_response = json.loads(response.text)
            for key in parsed_response.keys():
                if key == 'Result':
                    zipcode = parsed_response['Result']['Address']['Zip5']
                elif key == 'Error':
                    zipcode = 'Wrong'
                else:
                    zipcode = 'Other problems'  
                print(street,zipcode)
            with open('All.csv','a+') as csv_file2:
                writer = csv.DictWriter(csv_file2,fieldnames=['Street','Zipcode'])
                writer.writerow({'Street':street,'Zipcode':zipcode})