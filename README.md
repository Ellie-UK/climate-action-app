# Planet Effect

<p align="center">
  <b>CSC2033 Team 11 Climate Action App</b>
</p>
<p align="center">
<img src="/static/Logo.png" height="150" alt="(Planet Effect Logo)">
</p>

Setup for Climate Data web scraping found in data_collection,py

Some parts of the web scraping requires access to local file
paths.

Firstly you will need to specify the default download
directory, this can be found on line 25 with variable name
"prefs", set the file path to that of Climate Datasets folder
found in the Climate App file.

Example : "C:\\Uni\\CSC2033\\Climate App\\Climate Datasets\\"

Secondly the code will need access to a webdriver, specifically
Chrome Webdriver, this can be downloaded via this link, https://chromedriver.chromium.org/downloads ,
ensure that the version of the webdriver matches that of your
Chrome web browser. Then on line 29 you will need to set the 
path of the executable file.

Example : "C:/Users/ethan/OneDrive - Newcastle University/Desktop/chromedriver.exe"

Thirdly you will need to set the file path of the csv files
that will be downloaded, use the same file path of that of 
the default download directory, at the end add the name climate-change.csv,
see example for clearer picture, place that on line 55.

Example: r"C:/Uni/CSC2033/Climate App/Climate Datasets/climate-change.csv"

Finally You will need to set the file path for the three datasets
that have been downloaded, in the array found on line 147 replace
paths with your own, ensure you include the name of the datasets
on the end of the path, see example.

Example 1 : r"C:/Uni/CSC2033/Climate App/Climate Datasets/temperature-change.csv",
                     
Example 2 : r"C:/Uni/CSC2033/Climate App/Climate Datasets/sea-level-rise.csv",
                     
Example 3 : r"C:/Uni/CSC2033/Climate App/Climate Datasets/co2-concentration.csv"

Furthermore, changes to file paths in data_collection_test.py will be necessary
in order for the tests to pass