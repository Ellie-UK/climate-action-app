import unittest
import warnings

from data_collection import delete_datasets, clear_databases, Load_Data, write_to_database
from models import Temp_Anomaly, C02_Concentration, Sea_Level_Rise
from app import app
import time
import csv
import random

class TestDeleteDatasets(unittest.TestCase):
    def test_data_datasets_delete(self):
        '''
        Test to see if it can find and delete the datasets
        :return: [False, True, False]
        '''

        FilePath_List = [r"C:/Uni/CSC2033/Climate App/testing/Climate Datasets Test/notfound1.csv",
                         r"C:/Uni/CSC2033/Climate App/testing/Climate Datasets Test/sea-level-rise.csv",
                         r"C:/Uni/CSC2033/Climate App/testing/Climate Datasets Test/notfound2.csv"]

        file = open('C:/Uni/CSC2033/Climate App/testing/Climate Datasets Test/sea-level-rise.csv','w')
        filewriter = csv.writer(file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['test', 'test'])
        file.close()

        self.assertEqual(delete_datasets(FilePath_List), [False, True, False])
        time.sleep(2)



class TestWriteToDatabase(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed")
    def test_clear_databases(self):
        self.assertTrue(clear_databases())

    def test_write_data(self):
        '''
        Test to see if data from local files can be written to database
        :return: True
        '''
        self.maxDiff = None
        with app.app_context():
            FilePath_List = [r"C:/Uni/CSC2033/Climate App/Climate Datasets/temperature-change.csv",
                         r"C:/Uni/CSC2033/Climate App/Climate Datasets/sea-level-rise.csv",
                         r"C:/Uni/CSC2033/Climate App/Climate Datasets/co2-concentration.csv"]

            self.assertTrue(write_to_database(FilePath_List))
        time.sleep(2)


class TestReadDatabase(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed")
    def test_read_data(self):
        '''
        Test to see if random row from local data and database data match up.
        Includes read from database.
        :return: True
        '''
        with app.app_context():
            self.maxDiff = None
            FilePath_List = [r"C:/Uni/CSC2033/Climate App/Climate Datasets/temperature-change.csv",
                             r"C:/Uni/CSC2033/Climate App/Climate Datasets/sea-level-rise.csv",
                             r"C:/Uni/CSC2033/Climate App/Climate Datasets/co2-concentration.csv"]

            local_data = []

            CSVData = Load_Data(FilePath_List[0])
            for d in CSVData:
                record = [d[0], d[1], d[2], d[3]]
                local_data.append(record)

            database_data = Temp_Anomaly.query.all()
            plain_data = []
            for l in database_data:
                single_data = [getattr(l,'Entity'), getattr(l,'Code'), getattr(l,'Day'), str(getattr(l,'Temperature_Anomaly'))]
                plain_data.append(single_data)

            random_row = random.randint(0, len(local_data))
            print(local_data[random_row])
            print(plain_data[random_row])
            self.assertListEqual(local_data[random_row], plain_data[random_row])
            print("Success")
            time.sleep(2)


if __name__ == '__main__':
    unittest.main()
