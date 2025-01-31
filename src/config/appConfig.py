# import json module
import json
from src.typeDefs.generator import IGenerator
from enum import Enum
import pandas as pd

# initialize the app config global variable
appConf = {}
solarGens: list[IGenerator] = []


def loadAppConfig(fName="secret/config.json"):
    global solarGens
    solarGens = parseGensFromCsv(pd.read_csv("secret/solar_gens_info.csv"))
    # load config json into the global variable
    with open(fName) as f:
        global appConf
        appConf = json.load(f)
        return appConf

def getAppConfig():
    # get the cached application config object
    global appConf
    return appConf

def getSolarGens():
    # get the cached solar generators
    global solarGens
    return solarGens

def parseGensFromCsv(gensDf: pd.DataFrame) -> list[IGenerator]:
    gens: list[IGenerator] = [{
        "name": g["name"],
        "actId": g["act_id"],
        "genType": g["gen_type"]
    } for g in gensDf.to_dict('records')]
    return gens
