from pipeline import *



if __name__ == '__main__':



    super_download_folder_title = 'tripadvisor_downloads'

    ## The dictionary here was designed to structure downloads in folders based on different criterias
    ## The key in dictionary can be the city, a hotel chain, a country, a continent, etc. 
    ## 
    search_dict = {
    'asia':['india'],
    'europe':['England'],
    'Continent':['Europe']
    }

    
    ## Multiprocessing is used only in one key value pair
    pipeline(super_download_folder_title, search_dict, num_pages = 1, num_workers = 8)
    