# GTFS Tools for Faster Public Transit Simulation

This package consists of python codes for processing standard static GTFS datasets for aiding faster simulation of public transit systems. The package consists of the following two notebook files.

- ```gtfs_generator.ipynb```: This notebook contains codes to generate GTFS datasets for cities and subregions from a region-level GTFS dataset. For example, GTFS datasets for Amsterdam, The Hauge or Amsterdam can be created from the Netherlands GTFS dataset.

- ```transit_schedule_table.ipynb```: This notebook contains codes to generate time schedule tables of typical weekdays and weekends from static GTFS datasets. The time schedule tables provides a simpler approximation of trips on various routes using start times, stop sequences, and inter-station times.

- ```transit_trip_analysis.ipynb```: This notebook contains codes to analyze the daily trips and routes count over the timeframe for which the GTFS dataset is applicable. This can be useful in identifying daily and weekly patterns in the dataset and help in making informed decisions regarding the selection of dates for generating the transit schedule tables.


*Please refer to the codes for more detailed documentation.*