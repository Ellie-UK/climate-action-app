# Planet Effect 🌎

<p align="center">
  <b>CSC2033 Team 11 Climate Action App</b>
</p>
<p align="center">
<img src="/static/Logo.png" height="150" alt="(Planet Effect Logo)" href="http://planeteffect.ellie.gg">
</p>

## What is this?
This is **Team 11**’s project called **Planet Effect**. 
This project is aimed toward the climate action UN development goal. 
The purpose of this website is to provide an introduction to climate action, 
and give users a few ways to learn about it. This includes articles with information 
ranging from a background in global warming - to charities we’ve picked out, 
with information on why we have. There are also more personal ways to learn including a 
forum and FAQ page. You may also sign up to the newsletter which is controlled by the site 
admins to give information as either a weekly newsletter or a monthly digest. 
Finally, there is also a weekly quiz which admins can create questions for, 
including a leaderboard to track your progress. We hope you can get involved with the 
website and take part in the activities and discussions on the site! To do this, 
you should register an account and then take a look around! 

## How do I access it?
### Online
The website can be accessed at [planeteffect.ellie.gg](http://planeteffect.ellie.gg).

### Locally
1. **Clone this repo**. You must first clone this repo. A guide on how to do so can [be found here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository). **Make sure to set the project as a Flask server**.

2. **Install requirements**. This can be done by installing the dependencies listed in `requirements.txt`.

3. **Set up Environment Variables**. You must set up your environment variables if you wish to run this project yourself. All environtment variables can be found in `config.py`.
Some parts of the web scraping requires access to local file
paths. We will not provide our environment variable values as this would lead to the compromise of our accounts.

4. **Set up data scraping**:

    **Firstly**, you will need to specify the default download
directory, this can be found on line 25 with variable name
"prefs", set the file path to that of Climate Datasets folder
found in the Climate App file.

    `Example` `"C:\\Uni\\CSC2033\\Climate App\\Climate Datasets\\"`
    <br>
    **Secondly**, the code will need access to a webdriver, specifically
Chrome Webdriver, this can be downloaded via this link, https://chromedriver.chromium.org/downloads,
ensure that the version of the webdriver matches that of your
Chrome web browser. Then on line 29 you will need to set the 
path of the executable file.

    `Example` `"C:/Users/ethan/OneDrive - Newcastle University/Desktop/chromedriver.exe"`

    **Thirdly**, you will need to set the file path of the csv files
that will be downloaded, use the same file path of that of 
the default download directory, at the end add the name climate-change.csv,
see example for clearer picture, place that on line 55.

    `Example` `r"C:/Uni/CSC2033/Climate App/Climate Datasets/climate-change.csv"`

    **Finally**, You will need to set the file path for the three datasets
that have been downloaded, in the array found on line 147 replace
paths with your own, ensure you include the name of the datasets
on the end of the path, see example.

    `Example 1` `r"C:/Uni/CSC2033/Climate App/Climate Datasets/temperature-change.csv"`
                     
    `Example 2` `r"C:/Uni/CSC2033/Climate App/Climate Datasets/sea-level-rise.csv"`
                     
    `Example 3` `r"C:/Uni/CSC2033/Climate App/Climate Datasets/co2-concentration.csv"`

    **Furthermore**, changes to file paths in data_collection_test.py will be necessary
in order for the tests to pass

## License
[The MIT License](https://opensource.org/licenses/mit-license.php)

Copyright 2022 Newcastle University & Team 11

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
