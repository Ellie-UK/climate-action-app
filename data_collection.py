from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service
import plotly.express as px
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls
import pandas as pd
import schedule
from models import Temp_Anomaly, C02_Concentration, Sea_Level_Rise
from models import db
from app import app
import csv
import time
import os
import datetime

def data_collections(URL, FilePath):

    # Set file path for downloads
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "C:\\Uni\\CSC2033\\Climate App\\Climate Datasets\\"}
    options.add_experimental_option("prefs", prefs)

    # Initialise Web Driver
    service = Service("C:/Users/ethan/OneDrive - Newcastle University/Desktop/chromedriver.exe")
    driver = webdriver.Chrome(service=service,options=options)

    # Open URL
    driver.get(URL)

    driver.maximize_window()
    time.sleep(3)

    # Agree to terms and conditions
    driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div/div/div[2]/button").click()

    # Create wait case to allow webpage to catchup
    wait = WebDriverWait(driver,20, 3, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException, TimeoutException])

    # Click on First Download Button
    driver.find_element(By.XPATH, "/html/body/main/div/div[3]/div/div[3]/div[2]/nav/ul/li[4]").click()

    # Click on Download Button
    wait.until(expected_conditions.element_to_be_clickable((By.XPATH,"/html/body/main/div/div[3]/div/div[4]/div/div[2]/div/button"))).click()

    # Allow time for download to complete before closing browser
    time.sleep(3)
    driver.close()

    # Rename File
    old_name = r"C:/Uni/CSC2033/Climate App/Climate Datasets/climate-change.csv"
    new_name = FilePath

    os.rename(old_name, new_name)

def Load_Data(file_name):
    # Read csv file and load data to array
    f = open(file_name, 'r')
    reader = csv.reader(f)
    next(reader)
    data = []
    for r in reader:
        data.append(r)
    f.close
    return data  # Return array of climate change data

def write_to_database(FilePath_List):
    with app.app_context():
        try:
            for p in range(0, len(FilePath_List)):
                file_name = FilePath_List[p]
                data = Load_Data(file_name)
                print("Data loaded")
                for i in data:
                    if p == 0:
                        record = Temp_Anomaly(**{
                            'Entity' : i[0],
                            'Code' : i[1],
                            'Day' : i[2],
                            'Temperature_Anomaly' : i[3]
                        })
                        db.session.add(record)  # Add all records
                    elif p == 1:
                        record = Sea_Level_Rise(**{
                            'entity': i[0],
                            'code': i[1],
                            'day': i[2],
                            'sea_level_rise_average': i[3],
                        })
                        db.session.add(record)  # Add all records
                    elif p == 2:
                        record = C02_Concentration(**{
                            'entity': i[0],
                            'code': i[1],
                            'day': i[2],
                            'average_co2_concentrations': i[3],
                            'trend_co2_concentrations': i[4]
                        })
                        db.session.add(record)  # Add all records

            db.session.commit()  # Commit records
            print("Success: Data written to database")
            return True
        except:
            db.session.rollback()  # Rollback changes on error
            print("Rollback: Failed to write to database")
            return False
        finally:
            db.session.close()

def delete_datasets(FilePath_List):
    find_dataset = []
    for d in range(0,len(FilePath_List)):
        # Check to see if file exists
        if os.path.exists(FilePath_List[d]):
            # delete file
            os.remove(FilePath_List[d])
            find_dataset.append(True)
        else:
            print("File does not exist")
            find_dataset.append(False)
    return find_dataset

#            db.sessions.query(Temp_Anomaly).delete()
 #           db.sessions.query(Sea_Level_Rise).delete()
 #           db.session.query(C02_Concentration).delete()
#Temp_Anomaly.query.delete()
#Sea_Level_Rise.query.delete()
#C02_Concentration.query.delete()
def clear_databases():

    # Clear all data from climate change tables
    try:
        with app.app_context():
            db.session.query(Temp_Anomaly).delete()
            db.session.query(Sea_Level_Rise).delete()
            db.session.query(C02_Concentration).delete()
            db.session.commit()
            print("Success: Database cleared")
            return True
    except:
        db.session.rollback()
        print("Failure: Could not clear database")
        return False

def update_datasets():

    URL_List = [
        "https://ourworldindata.org/explorers/climate-change?facet=none&country=~OWID_WRL&Metric=Temperature+anomaly&Long-run+series%3F=false",
        "https://ourworldindata.org/explorers/climate-change?facet=none&country=~OWID_WRL&Metric=Sea+level+rise&Long-run+series%3F=false",
        "https://ourworldindata.org/explorers/climate-change?facet=none&country=~OWID_WRL&Metric=CO%E2%82%82+concentrations&Long-run+series%3F=false"]

    FilePath_List = [r"C:/Uni/CSC2033/Climate App/Climate Datasets/temperature-change.csv",
                     r"C:/Uni/CSC2033/Climate App/Climate Datasets/sea-level-rise.csv",
                     r"C:/Uni/CSC2033/Climate App/Climate Datasets/co2-concentration.csv"]

    # Clear previous version of datasets
    delete_datasets(FilePath_List)

    for i in range(0, len(URL_List)):
        try:
            data_collections(URL_List[i], FilePath_List[i])
        except:
            print("Unable to update Datasets")
            break

    # Clear database before updating it
    proceed = clear_databases()
    if proceed:
        # Write new datasets to database
        proceed = write_to_database(FilePath_List)
        if proceed:
            graph_generator()
        else:
            print("Cannot proceed to generate graphs")
    else:
        print("Cannot proceed with write to database")


def get_datasets():
    with app.app_context():
        # Graph data for temperature_anomaly
        t_dates = [r for (r,) in Temp_Anomaly.query.with_entities(Temp_Anomaly.Day).filter(Temp_Anomaly.Entity == 'World').all()]
        temperature = [r for (r,) in Temp_Anomaly.query.with_entities(Temp_Anomaly.Temperature_Anomaly).filter(Temp_Anomaly.Entity == 'World').all()]

        # Graph data for sea_level_rise
        s_dates = [r for (r,) in Sea_Level_Rise.query.with_entities(Sea_Level_Rise.day).all()]
        sea_level = [r for (r,) in Sea_Level_Rise.query.with_entities(Sea_Level_Rise.sea_level_rise_average).all()]

        # Graph data for c02_concentration
        c_dates = [r for (r,) in C02_Concentration.query.with_entities(C02_Concentration.day).all()]
        c02_con = [r for (r,) in C02_Concentration.query.with_entities(C02_Concentration.average_co2_concentrations).all()]

        temp_anomaly_dataset = pd.DataFrame(dict(
            Date=t_dates,
            Temperature=temperature
        ))

        sea_level_rise_dataset = pd.DataFrame(dict(
            Date=s_dates,
            Sea_Level_Rise=sea_level
        ))

        c02_con_dataset = pd.DataFrame(dict(
            Date=c_dates,
            C02_Concentration=c02_con
        ))

        return [temp_anomaly_dataset, sea_level_rise_dataset, c02_con_dataset]


def graph_generator():

    # Setup credentials for chart_studio account
    username = 'Planet_Effect'
    api_key = 'ur5Sf90VaEkiqZMxw5WJ'
    chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

    combined_datasets = get_datasets()
    titles = ["Temperature Anomaly", "Sea Level Rise", "C02 Concentration"]
    y_axis = ["Temperature", "Sea_Level_Rise", "C02_Concentration"]
    filenames = ["temperature_anomaly", "sea_level_rise", "c02_concentration"]

    for i in range(0,len(combined_datasets)):
        # Generate Graph
        fig = px.line(combined_datasets[i], x="Date", y=y_axis[i], title=titles[i])
        # Push graph to chart_studio
        chart_url = py.plot(fig, filename=filenames[i], auto_open=True, show_link=False)
        # Get html code for chart
        chart_html = tls.get_embed(chart_url)
        print("Success: Graphs Generated")
        print(chart_html)

def schedule_monthly_updates():
    schedule.every().day.at('12:00').do(update_datasets)
    while True:
        if datetime.date.today().day != 1:
            return

        schedule.run_pending()
        time.sleep(1)
