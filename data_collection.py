from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service
import time
import os


def data_collection(URL, FilePath):

    # Set file path for downloads
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "C:\\Uni\\CSC2033\\Climate Datasets\\"}
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
    old_name = r"C:/Uni/CSC2033/Climate Datasets/climate-change.csv"
    new_name = FilePath

    os.rename(old_name, new_name)

def delete_datasets(FilePath_List):

    for d in range(0,len(FilePath_List)):
        # Check to see if file exists
        if os.path.exists(FilePath_List[d]):
            # delete file
            os.remove(FilePath_List[d])
        else:
            print("File does not exist")

def update_datasets():

    URL_List = [
        "https://ourworldindata.org/explorers/climate-change?facet=none&country=~OWID_WRL&Metric=Temperature+anomaly&Long-run+series%3F=false",
        "https://ourworldindata.org/explorers/climate-change?facet=none&country=~OWID_WRL&Metric=Sea+level+rise&Long-run+series%3F=false",
        "https://ourworldindata.org/explorers/climate-change?facet=none&country=~OWID_WRL&Metric=CO%E2%82%82+concentrations&Long-run+series%3F=false"]

    FilePath_List = [r"C:/Uni/CSC2033/Climate Datasets/temperature-change.csv",
                     r"C:/Uni/CSC2033/Climate Datasets/sea-level-rise.csv",
                     r"C:/Uni/CSC2033/Climate Datasets/co2-concentration.csv"]

    delete_datasets(FilePath_List)

    for i in range(0, len(URL_List)):
        try:
            data_collection(URL_List[i], FilePath_List[i])
        except:
            print("Unable to update Datasets")
            break