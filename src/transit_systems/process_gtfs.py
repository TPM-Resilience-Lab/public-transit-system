#------------------------------------------------------------------------------#
#                         GENERATE CITY-LEVEL GTFS                             #
# -----------------------------------------------------------------------------#
from pathlib import Path
import zipfile
import requests
import pandas as pd

import osmnx as ox
ox.config(use_cache=True, log_console=True)

class regional_gtfs:
    """
    A class to represent a city-level static GTFS dataset
    
    Attributes:
        region (str): Name of the region or country(for example, Netherlands)
        url (str)   : The link of the GTFS file
        date (str)  : Date of release of GTFS in DDMMYYYY format
    
    Methods:

    """

    def __init__(self, region, date, url):
        """
        Constructs all the necessaty attributes for the city-leel gtfs class

        Args:
            region (str): Name of the region or country(for example, Netherlands)
            city (str)  : name of the city or subregion for which the GTFS dataset is to be generated
            url (str)   : The link of the GTFS file
            date (str)  : Date of release of GTFS in DDMMYYYY format

        """

        self.region = region
        self.publish_date = date
        self.gtfs_url = url
        self.reg_zip_dir = 'data/raw/gtfs_zip/{0}/{1}'.format(region, date)
        self.reg_unzip_dir = 'data/raw/gtfs_unzip/{0}/{1}'.format(region, date)

    def download_reg_gtfs(self):
        """
        Downloads regional static GTFS dataset from given url

        Args:
            None

        Returns:
            None
        """

        #create the directory inside /data/raw/gtfs_zip folder using region and city name if not already avaialble
        Path(self.reg_zip_dir).mkdir(parents=True, exist_ok=True)
        
        # download the file fr
        r = requests.get(self.gtfs_url, stream=True)
        with open('{}/{}_{}.zip'.format(self.reg_zip_dir, self.region, self.publish_date), 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)


    def extract_reg_gtfs_files(self, zipped_gtfs):
        """
        Extract the content files from the zipped regional static GTFS dataset

        Args:
            zipped_gtfs (str)   : Path to the zipped GTFS file (include <filename>.zip)

        Returns:
            None
        """

        Path(self.reg_unzip_dir).mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zipped_gtfs, 'r') as file:
            file.extractall(self.reg_unzip_dir)
            print("Successfully extracted and saved GTFS dataset of {} region/country published on {} to {}".format(self.region, self.publish_date, self.reg_unzip_dir))


    def read_gtfs_content(self, gtfs_content):
        """
        Reads and returns the static GTFS text file from the extracted dataset as a pandas dataframe

        Args:
            gtfs_content (str) : Any of the content listed here (agency, calendar_dates, feed_info, routes, shapes, stop_times, stops, transfers, trips)

        Returns:
            A pandas dataframe containing the requested data
        """

        content_path = Path('{}/{}.txt'.format(self.reg_unzip_dir, gtfs_content))
        if content_path.is_file():
            content = pd.read_csv(content_path, low_memory=False)
            return content
        else:
            print("The requested GTFS content is not available. Please check the original dataset.")


    def get_reg_unique_values(self, gtfs_feature):
        """
        Returns the list of unique values of the requested GTFS feature 

        Args:
            gtfs_feature (str)  : Any of the following feature (route_id, trip_id, agency_id, route_type, stop_id, service_id)

        Returns:
            returns a list of unique values of the GTFS feature requested.
        """

        if gtfs_feature == 'route_id' or gtfs_feature == 'trip_id' or gtfs_feature == 'service_id':
            gtfs_content = self.read_gtfs_content('trips')
            unique_list = gtfs_content[gtfs_feature].unique().tolist()
            return unique_list
        elif gtfs_feature == 'route_type' or gtfs_feature == 'agnecy_id':
            gtfs_content = self.read_gtfs_content('routes')
            unique_list = gtfs_content[gtfs_feature].unique().tolist()
            return unique_list
        elif gtfs_feature == 'stop_id':
            gtfs_content = self.read_gtfs_content('stops')
            unique_list = gtfs_content[gtfs_feature].unique().tolist()
            return unique_list

    
    def generate_city_level_gtfs(self, city):
        """
        Generates a new static GTFS dataset for a city

        Args:
            city (str)  : The name of the city of interest. The city must be a subset of the GTFS region. Use the name attribute from the respective OSM page.\
                          For example, for creating a dataset of Hague, use "Den Haag" from https://www.openstreetmap.org/relation/192737). The city GTFS must be 
                          a subset of the regional GTFS.
        
        Returns:
            None
        """

        self.city_name = city
        self.city_unzip_dir = 'data/processed/city_gtfs/{0}/{1}/{2}'.format(self.region, city, self.publish_date)
        Path(self.reg_zip_dir).mkdir(parents=True, exist_ok=True)

        # define the place query.
        query = {'city': city}

        # get the boundaries of the place
        gdf = ox.geocode_to_gdf(query)
        #gdf.plot()


region = 'Netherlands'
date = '08032021'
url = 'http://gtfs.ovapi.nl/nl/gtfs-nl.zip'

Netherlands = regional_gtfs(region, date, url)
# Hague.download_reg_gtfs(region, url, date)

# zipped_gtfs = '{}/{}_{}.zip'.format(Hague.reg_zip_dir, Hague.region, Hague.publish_date)

# Hague.extract_reg_gtfs_files(zipped_gtfs)

#stop_times = Hague.read_gtfs_content('stop_times')

# reg_route_list = Hague.get_reg_unique_values('route_type')
# print(reg_route_list[0:5])

city = 'Den Haag'
Netherlands.generate_city_level_gtfs(city)
#city (str)  : Name of city for which the dataset is to be developed. Use the name attribute from the OSM page (Example, for Hague, use https://www.openstreetmap.org/relation/192737)
