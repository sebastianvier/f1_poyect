import sys, math
import urllib.request as urlr
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse


def circuit_row_generator(url_array):
    """ This will get the driver info needed as an array"""
    ## The yielding is done authomatically because there is
    ## only one scrap to do in each url. ::

    for url in url_array: 
        
        url = url[1] # In the url_array there are 2 elements
        path = urlparse(url).path
        
        ## Create the soup based on the url
        url = urlr.urlopen(url)
        soup = BeautifulSoup(url, 'html.parser')   
            
        ## Get the info
        table = soup.find('table')

        name = " ".join(path.split('/')[-1].split('-'))
        name = name.title()
        country = table.find_all('tr')[0].find_all('td')[1].text.strip()
        coordinates = table.find_all('tr')[1].find_all('td')[1].text.strip()
            
        ## Return array with the info
        yield [name, country, coordinates]

def driver_row_generator(url_array):
    def get_driver_info(url):
        """ This will get the driver info needed as an array"""

        ## Create the sup based on the url
        url = urlr.urlopen(url)
        soup = BeautifulSoup(url, 'html.parser' )   
        
        
        ## Get the info
        first_name  = soup.find('h1').text.split(' ')[0]
        last_name   = soup.find('h1').text.split(' ')[1]
        print(f'{first_name} {last_name}')
        nationality = soup.find('table').find_all('span')[1].text
        birth_date  = soup.find('table').find_all('span')[2].text.strip()
        birth_date  = datetime.strptime(birth_date,'%d %B %Y')
        gender      = soup.find('meta',property="profile:gender")['content']
        
        ## Return array with the info
        return [first_name, last_name, nationality, birth_date, gender]
    
    for url in url_array: # Because this will used for every url in the url_array.
        yield np.array(get_driver_info(url))
        print(f'{url_array.index(url) + 1}/{len(url_array)}') 
        # This final code will print the progress of the action.

def get_links_from_table(url, table_number, cell_position, verification_list, year_flag=False,s_name=True):
    """Given a url, a table_number and a cell where the links are, this generator gets every name and the link into an array. """
    
    ## Create Soup
    soup = BeautifulSoup(urlr.urlopen(url), 'lxml')
    rows = soup.find_all('table')[table_number].find_all('tr')[1:]

    ## Make a generator that performs in every row.
    for row in rows:
        year = row.find_all('td')[1].text[:4]
        cell = row.find_all('td')[cell_position] # Get the cell that will lead to the driver.



        ## Get all the names and urls
        name = cell.text
        ## Just an extra step in order to add the years to the Grand Prixes
        if year_flag:
            name = name + ' ' + year



        url = cell.find('a')['href']

        if url not in verification_list: # Exclude duplicates (This can be done in other places.)
            yield [name, url]
            verification_list.append(url)
            if s_name:
                print(name)
        # else:
        #     print("already there") ## This 2 lines are for testing

def get_results(url, result_type='race', table_number=2):
    """Given a url with the results select race or grid and specify which table are the results on"""
    ## Functions

    def get_soup(url):
        url = urlr.urlopen(url)
        soup = BeautifulSoup(url, 'html.parser')
        return soup

    def create_race_result_array(soup, generator):
        table = soup.find_all('table')[2] # This is the number of the table
        
        results_array = np.array([i for i in generator])
        return results_array    
    
    def create_result_array(): ## The variables are globlal
        if result_type == 'grid':
            results_array = np.array([i for i in grid_row_generator()])
            return results_array
        elif result_type == 'race':
            results_array = np.array([i for i in race_row_generator()])
            return results_array


    ## Generators
 
    def grid_row_generator():

        for row in table.find_all('tr')[1:]:
            # The first one is the columns titles, the code above is
            # getting the full table. 
    
            table_data = row.find_all('td')
            position = table_data[0].text.strip() # Position
            time = table_data[4].text.strip() # Time (sometimes it is missing)            
            name = table_data[2].text.strip() # Driver Name
            constructor = table_data[3].text.strip() # Constructor
            
            
            yield [position, time, name, constructor, race_name]       

    def race_row_generator():    
        
        for row in table.find_all('tr')[1:]:

            ## Get all the row_data
            table_data = row.find_all('td')

            ## Get all the information to yield
            position = table_data[0].text.strip() # Position
            time = table_data[5].text.strip() # Time
            laps = table_data[4].text.strip() # Laps
            points = table_data[6].text.strip() # Points
            name = table_data[2].text.strip() # Driver Name
            constructor = table_data[3].text.strip() # Constructor

            ## Yield
            yield [position, time, laps, points, name, constructor, race_name]
            

    ## Functionality


    ## 1. Get the soup
    soup = get_soup(url)

    ## 2. Get the table and the race_name
    race_name = ' '.join(soup.find_all('h1')[0].text.split(' ')[2:-1])
    table = soup.find_all('table')[table_number]

    ## 3. Return the array
    result_array = create_result_array()
    result = result_array
    return result
            
def season_link_gen(rows):
    """ This function will reseive a row and """
    for row in rows:
        yield ['Season ' + row.find('a').text ,
               row.find('a')['href']] 
        # The text is just the year of the season. So this will add 'season as well.'
        # There is only one link so this is what we need.              

