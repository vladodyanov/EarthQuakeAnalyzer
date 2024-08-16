# EarthQuakeAnalyzer
Wellcome to my first Data Science project. A comprehensive Python-based tool for analyzing and visualizing seismic activity data. EQA provides in-depth insights into earthquake patterns, magnitudes, and geographical distributions. All seizmic data is provided by The U.S. Geological Survey ( https://www.usgs.gov/).

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Contact](#contact)


## General Information
EarthQuakeAnalyzer (EQA) is a powerful tool designed for evertbody who has interest in seismology and related fields. It allows users to fetch, process, analyze, and visualize earthquake data from the USGS API. The application provides a user-friendly interface for inputting parameters and displays comprehensive analysis results, including statistical data, visualizations, and seismic hazard assessments.


## Technologies Used
- Python - version 3.11
- NumPy
- Pandas
- CartoPy
- MathplotLib
- wxPython


## Features
- Fetch and process earthquake data from USGS API
- Interactive GUI for data input and result display
- Advanced seismic activity analysis, including:
  - Aftershock patterns
  - Activity change over time
  - Correlation between earthquake depth and magnitude
- Seismic hazard assessment with region-specific recommendations
- Analysis of seismic activity changes between two time periods
- Continent-based filtering of earthquake data
- Visualizations including:
  - Time series plots
  - Magnitude distributions
  - Interactive world maps

## Screenshots
<img align="center" width=480px  alt="home page view" src="https://github.com/vladodyanov/EarthQuakeAnalyzer/blob/main/screenshots/Screenshot%202024-08-15%20104948.jpg" />

<img align="center" width=480px  alt="home page view" src="https://github.com/vladodyanov/EarthQuakeAnalyzer/blob/main/screenshots/Screenshot%202024-08-15%20105047.jpg" />

<img align="center" width=480px  alt="home page view" src="https://github.com/vladodyanov/EarthQuakeAnalyzer/blob/main/screenshots/Screenshot%202024-08-15%20105135.jpg" />

<img align="center" width=480px  alt="home page view" src="https://github.com/vladodyanov/EarthQuakeAnalyzer/blob/main/screenshots/Screenshot%202024-08-15%20105216.jpg" />

<img align="center" width=480px  alt="home page view" src="https://github.com/vladodyanov/EarthQuakeAnalyzer/blob/main/screenshots/Screenshot%202024-08-15%20105435.jpg" />


## Setup
To run this project, install it locally using pip:
pip install -r requirements.txt
Note: wxPython might require additional setup steps depending on your operating system. Please refer to the wxPython documentation for specific instructions.

## Usage
1. Run the main.py file to start the application:
 - python main.py
2. Use the GUI to input the desired parameters:
3. Select Start and end dates for the analysis period
4. Minimum magnitude of earthquakes to consider
5. Select a continent (or all continents)
6. Click the "Analyze" button to process the data and view the results
7. Explore the generated visualizations and analysis reports

## Project Status
Project is: underdevelopment

## Room for Improvement
 - Areas for improvement:
   - Implement caching of earthquake data for faster repeated analyses
   - Add more interactive features to the world map visualization
   - Expand the range of statistical analyses offered

- Future features:
  - Export functionality for analysis results and visualizations
  - Comparison tool for analyzing seismic activity across different time periods or regions
  - Integration with additional data sources for more comprehensive analysis


## Contact
Created by Vladimir Dyanov - feel free to contact me!

