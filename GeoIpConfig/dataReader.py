import csv
import json
from GeoIpConfig import BASE_DIR



def read_csv_ip_file(name):
    """This function take a csvfile name and return content of it"""
    filePath = BASE_DIR.joinpath("GeoIpConfig") / name
    with open(file=filePath, encoding="UTF-8", mode="r") as fp:
        reader = csv.reader(fp)
        reader.__next__()
        data = []
        for row in reader:
            data.append(row)
        return data


def read_country_info():
    filePath = BASE_DIR.joinpath("GeoIpConfig/data.json")
    with open(file=filePath, encoding="UTF-8", mode="r") as fp:
        dt = json.load(fp)
        for row in dt:
            yield row
