import os
import numpy as np 

import concurrent.futures
import pandas as pd
import csv

from utils import *


def pipeline (title, dict, num_pages = 5, num_workers = 8):

    continents_dict = dict

    title = title


    num_workers = num_workers
    num_pages = num_pages
    for continent in continents_dict:
        print("Currently in ", continent)
        start = 0
        path = f'urls/hotel_pages/{title}/{continent}/'

        if os.path.exists(path):
            pass
        else:
            os.makedirs(path)

        while (start < len(continents_dict[continent])):
            stop = start+num_workers
            subset_countries = continents_dict[continent][start:stop]
            start = stop

            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                results = list(executor.map(get_hotel_page_urls_from_main_page, subset_countries, [path]*num_workers,[num_pages]*num_workers))

        print()

    print('Extracted Page URLS!')

    path = f'urls/hotel_pages/{title}/'
    num_workers = 10
    error_csvs=[]

    for i in os.scandir(path):
        continent_path = i.path
        print("Currently in", i.name)

        try:
            
            path = f'urls/imgs/{title}/{i.name}/'

            if os.path.exists(path):
                pass
            else:
                os.makedirs(path)
            
            counter = 0
            total_files = len(os.listdir(continent_path))
            file_counter = 0

            for j in os.scandir(continent_path):

                print(f"Current City {j.name}")
                print(f"Files remaining {total_files-file_counter}")
                print()
                file_counter +=1
                hotel_pages = pd.read_csv(j.path).values.tolist()
            
                start = 0

                while (start < len(hotel_pages)):
                    stop = start+num_workers
                    subset_pages = hotel_pages[start:stop]
                    start = stop


                    try:
                        #print("Current subset of pages", subset_pages)
                        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
                            results = list(executor.map(get_img_urls_from_hotel_page, subset_pages))
                            
                            
                            flat_list = [[item] for sublist in results for item in sublist]

                            if len(flat_list) > 0:
                                continent_name = path.split('/')[-2]
                                file_path = path+continent_name+'.csv'


                                # Open the CSV file in append mode
                                with open(file_path, mode='a', newline='') as csv_file:

                                    # Create a writer object
                                    writer = csv.writer(csv_file)

                                    # Write a new row to the CSV file
                                    writer.writerows(flat_list)
                    except Exception as e:
                        print("ERROR inside of subset_page", subset_pages)
                        print("exception ", e)
                    #print("I have exited the j", subset_pages)
                print('I have exited i')
            print("I have come out")

            print()

        except Exception as e:
            print("ERROR ERROR")

            print("exception occured", e)
            error_csvs.append(continent_path)


    path = f'urls/imgs/{title}/'
    num_workers = 100
    workers = list(np.arange(1,num_workers+1))

    for folder in os.scandir(path):
        print(folder.path)
        if [] == os.listdir(folder.path):
            print(f"Failed to get URLs for {folder.path}")
            print("Try to extract urls again")

        else: 
            sub_folder = os.scandir(folder.path)
            sub_folder_name = folder.name
            for file in sub_folder:
                print('Here')
                print(file)
                print('########33')
                url_list = pd.read_csv(file).values.tolist()

            

            download_path = f'downloads/tripadvisor/{title}/{sub_folder_name}/'


            if os.path.exists(download_path):
                pass
            else:
                os.makedirs(download_path)
            
            start = 0
            download_counter = 0
            while (start < len(url_list)):
                stop = start+num_workers
                subset_urls = url_list[start:stop]
                start = stop

                with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
                    results = list(executor.map(downloader, subset_urls, [download_path]*num_workers, [download_counter]*num_workers, workers))

                download_counter+=1