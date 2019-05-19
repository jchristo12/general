import pandas as pd
from bs4 import BeautifulSoup
import requests
from python_pkg import python_udf as udf

# =============================================================================
# Helper functions
# =============================================================================
def place_query(vintage, variable, dataset, api_key, labels=False):
    """
    Run a query from the ACS API\n
    Pulls the specified variable for all CDPs (census designated places); also returns the state ID\n
    Vintage = year of the data\n
    """
    assert isinstance(labels, bool)

    #API key
    key_url = '&key=' + api_key
    #basic url components
    base_acs = 'https://api.census.gov/data'
    dataset = 'acs/' + dataset

    #Return the place and state names or not
    if labels == False:
        #Estimated population for all CDPs in dataset
        query = 'get=' + variable + '&for=place:*&in=state:*'
    else:
        query = 'get=' + variable + ',NAME' + '&for=place:*&in=state:*'

    #build the full API call
    full_url = base_acs + '/' + vintage + '/' + dataset + '/?' + query + key_url
    #pull the data and put into dataframe
    data = requests.get(full_url).json()
    #end the function and return the  data
    return data


def query_to_df(data):
    """
    Convert the data from the API query to a pandas dataframe\n
    Changes the column data types to the appropriate types
    """
    df = pd.DataFrame(data[1:], columns=data[0])
    #Store the variable as a string
    var = df.columns[0]
    #Store the columns as the correct data type
    df = df.astype({'place': 'category',
                    'state': 'category',
                    var: 'float'})
    return df


def variables_scrape(vintage, dataset):
    """
    Scrape the page to capture varible names and labels\n
    Filters data to only capture variables that are data values (i.e. does not include MOE or annotations)
    """
    #Build the URL
    base_acs = 'https://api.census.gov/data'
    dataset= 'acs/' + dataset
    full_url = base_acs + '/' + vintage + '/' + dataset + '/' + 'variables.html'
    #scrape the page
    page = requests.get(full_url).content
    soup = BeautifulSoup(page, 'html.parser')
    rows = soup.find('tbody').find_all('tr')
    #initialize lists for the variable information
    names = []
    labels = []
    est = []
    #find all variable names and labels
    for r in rows:
        info = r.find_all('td')
        name = info[0].text
        label = info[1].text
        #append the data to the appropriate lists
        names.append(name)
        labels.append(label)
    #Find if variable ends in "E"
    for i in labels:
        result = i.startswith('Estimate')
        est.append(result)
    #convert into a dataframe
    df = pd.DataFrame({'name': names, 'label': labels, 'estimate': est})
    #filter dataframe to only include those that end in "E"
    df = df[df['estimate'] == True]
    return df


#combines the API call and the pandas df conversion and returns the data series
def api_data_to_series(vintage, variable, dataset, api_key, labels=False):
    json = place_query(vintage=vintage, variable=variable, dataset=dataset, api_key=api_key, labels=labels)
    df = query_to_df(json)
    series = df[variable]
    return series
