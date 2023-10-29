from PIL import Image
import pickle
import os
from pathlib import Path
import wget
import requests
from folktables import ACSDataSource, ACSIncome
import folktables
import numpy as np
import kaggle
from zipfile import ZipFile
import pandas as pd

os.makedirs("data_format", exist_ok=True)

def load_utk():
    def flatten(x):
        img = np.mean(x,axis=2)
        out = np.zeros(200*200).astype(float)
        for i in range(199):
            out[i*200:(i+1)*200] = img[i,:]
        return out

    path = Path("data_raw", "UTK")
    os.makedirs(path, exist_ok=True)
    #Toggle this switch to download or use predownload utk 
    if True:
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files("jangedoo/utkface-new", path)
        with ZipFile(Path(path, "utkface-new.zip")) as z:
            z.extractall(path=path)

    imgpath = Path(path,"utkface_aligned_cropped","crop_part1")

    files = os.listdir(imgpath)
    #Parse file name to obtain labels and attributes 
    x = []
    xflat = []
    zrace = []
    zsex = []
    y = []
    for file in files:
        a = file.find("_")
        age = int(int(file[:a])>50)
        b = 1+a+file[a+1:].find("_")
        sex = int(file[a+1:b])
        c = 1+b+file[b+1:].find("_")
        try:
            race = int(file[b+1:c])
        except:
            race = 3
        if race==0 or race==1:
            x += [np.asarray(Image.open(Path(imgpath,file)))]
            xflat += [flatten(Image.open(Path(imgpath,file)))]
            y += [age]
            zrace += [race]
            zsex += [sex]

    x = np.array(x)
    xflat = np.array(xflat)
    y = np.array(y)
    zrace = np.array(zrace)
    zsex = np.array(zsex)

    d = {}
    n = np.shape(x)[0]
    idx = np.linspace(0,n-1,n).astype(int)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    d["x"] = x[idx]
    d["zrace"] = zrace[idx]
    d["zsex"] = zsex[idx]
    d["y"] = y[idx]
    with open(Path("data_format","UTK.pickle"), "wb") as f:
        pickle.dump(d, f)

    d["x"]=xflat[idx]
    with open(Path("data_format","UTKflat.pickle"), "wb") as f:
        pickle.dump(d, f)


#Can't find reliable source with uncensored sensitive attributes.
"""
def load_credit():
    kaggle.api.authenticate()
    path = Path("data_raw", "CREDIT")
    kaggle.api.dataset_download_files("hassanamin/uci-credit-card", path)
    with ZipFile(Path(path,"uci-credit-card.zip")) as zObject:
        zObject.extractall(path=path)
    df = pd.read_csv(Path(path,"UCI_Credit_Card.csv"), sep=',')
    print(df.columns)
    quit()
    df = df.rename(columns={'PAY_0': 'PAY_1'})
    df['LIMIT_BAL'] = df['default.payment.next.month'] + np.random.normal(scale=0.5, size=df.shape[0])
    df.loc[df['SEX'] == 2, 'LIMIT_BAL'] = np.random.normal(scale=0.5, size=df[df['SEX'] == 2].shape[0])
    y = df['default.payment.next.month']
    df['AGE'] = (df['AGE'] < 40).astype(int)
    sex = df.SEX.values - 1
    race = df.AGE.values
    Z = pd.DataFrame({'race': race,'sex': sex})
    X = df.drop(["SEX","ID","default.payment.next.month"], 1)
    d = {}
    d["x"] = X.to_numpy()
    d["y"] = y.to_numpy()
    d["zrace"] = Z["race"].to_numpy()
    d["zsex"] = Z["sex"].to_numpy()
    with open("data_format/CREDIT.pickle", "wb") as f:
        pickle.dump(d, f)
"""
      
def load_law():
    url = "https://raw.githubusercontent.com/tailequy/fairness_dataset/main/Law_school/law_dataset.arff"
    rep = requests.get(url)
    path = Path("data_raw", "LAW")
    os.makedirs(path, exist_ok=True)
    with open(Path(path,"law.arff"), 'wb') as f:
        f.write(rep.content)

    #Parsing arff format 
    #scipy.io.arff.loadarff give an error, so custom parser
    with open(Path(path,"law.arff"), 'r') as f:
        lines = f.readlines()
    header = []
    data = []
    lines = lines[1:] #first line is useless
    for line in lines:
        if line[0] == "@" and line != "@data\n":#If line is attribute def
            a = line.find(" ")
            b = line[a+1:].find(" ")
            header += [line[a+1:a+b+1]]

        else:
            data += [list(np.fromstring(line[:-1],sep=","))]

    df = pd.DataFrame(data,columns=header)
    d = {}
    x = df.drop(["pass_bar", "male", "racetxt"],axis=1).to_numpy()
    n = np.shape(x)[0]
    idx = np.linspace(0,n-1,n).astype(int)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    d["y"] = df["pass_bar"].to_numpy()[idx]
    d["zsex"] = df["male"].to_numpy()[idx]
    d["zrace"] = df["racetxt"].to_numpy()[idx]
    d["x"] = df.drop(["pass_bar", "male", "racetxt"],axis=1).to_numpy()[idx]

    with open("data_format/LAW.pickle", "wb") as f:
        pickle.dump(d, f)



def load_compas():
    kaggle.api.authenticate()
    path = Path("data_raw", "COMPAS")
    os.makedirs(path, exist_ok=True)
    kaggle.api.dataset_download_files("danofer/compass", path)
    with ZipFile(Path(path,"compass.zip")) as zObject:
        zObject.extractall(path=path)
    df = pd.read_csv(Path(path,"propublicaCompassRecividism_data_fairml.csv","propublica_data_for_fairml.csv"))
    d = {}
    x = df.drop(["Female","African_American","Asian", "Hispanic", "Native_American", "Other"], axis=1).to_numpy()
    n = np.shape(x)[0]
    idx = np.linspace(0,n-1,n).astype(int)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    d["y"] = df["Two_yr_Recidivism"].to_numpy()[idx]
    d["zsex"] = df["Female"].to_numpy()[idx]
    d["zrace"] = df["African_American"].to_numpy()[idx]
    d["x"] = df.drop(["Female","African_American","Asian", "Hispanic", "Native_American", "Other"], axis=1).to_numpy()[idx]
    with open("data_format/COMPAS.pickle", "wb") as f:
        pickle.dump(d, f)

def load_meps():
    kaggle.api.authenticate()
    path = Path("data_raw", "MEPS")
    os.makedirs(path, exist_ok=True)
    kaggle.api.dataset_download_files("nanrahman/mepsdata", path)
    with ZipFile(Path(path,"mepsdata.zip")) as zObject:
        zObject.extractall(path=path)
    df = pd.read_csv(Path(path,"h181.csv"), sep=',')
    def race(row):
        if ((row['HISPANX'] == 2) and (row['RACEV2X'] == 1)):  #non-Hispanic Whites are marked as WHITE; all others as NON-WHITE
            return 1
        return 0
    def gender(row):
        if (row['SEX'] == 1):
            return 0
        elif (row['SEX'] == 2):
            return 1
    df['RACEV2X'] = df.apply(lambda row: race(row), axis=1)
    df['SEX'] = df.apply(lambda row: gender(row), axis=1)
    df = df.rename(columns = {'RACEV2X' : 'race'})
    df = df.rename(columns = {'SEX' : 'sex'})
    df = df[df['PANEL'] == 19]
    # RENAME COLUMNS
    df = df.rename(columns = {'FTSTU53X' : 'FTSTU', 'ACTDTY53' : 'ACTDTY', 'HONRDC53' : 'HONRDC', 'RTHLTH53' : 'RTHLTH','MNHLTH53' : 'MNHLTH', 'CHBRON53' : 'CHBRON', 'JTPAIN53' : 'JTPAIN', 'PREGNT53' : 'PREGNT','WLKLIM53' : 'WLKLIM', 'ACTLIM53' : 'ACTLIM', 'SOCLIM53' : 'SOCLIM', 'COGLIM53' : 'COGLIM','EMPST53' : 'EMPST', 'REGION53' : 'REGION', 'MARRY53X' : 'MARRY', 'AGE53X' : 'AGE','POVCAT15' : 'POVCAT', 'INSCOV15' : 'INSCOV'})
    df = df[df['REGION'] >= 0] # remove values -1
    df = df[df['AGE'] >= 0] # remove values -1
    df = df[df['MARRY'] >= 0] # remove values -1, -7, -8, -9
    df = df[df['ASTHDX'] >= 0] # remove values -1, -7, -8, -9
    df = df[(df[['FTSTU','ACTDTY','HONRDC','RTHLTH','MNHLTH','HIBPDX','CHDDX','ANGIDX','EDUCYR','HIDEG','MIDX','OHRTDX','STRKDX','EMPHDX','CHBRON','CHOLDX','CANCERDX','DIABDX','JTPAIN','ARTHDX','ARTHTYPE','ASTHDX','ADHDADDX','PREGNT','WLKLIM','ACTLIM','SOCLIM','COGLIM','DFHEAR42','DFSEE42','ADSMOK42','PHQ242','EMPST','POVCAT','INSCOV']] >= -1).all(1)]  #for all other categorical features, remove values < -1
    def utilization(row):
        return int(row['OBTOTV15'] + row['OPTOTV15'] + row['ERTOT15'] + row['IPNGTD15'] + row['HHTOTD15'])
    df['TOTEXP15'] = df.apply(lambda row: utilization(row), axis=1)
    lessE = df['TOTEXP15'] < 10.0
    df.loc[lessE,'TOTEXP15'] = 0.0
    moreE = df['TOTEXP15'] >= 10.0
    df.loc[moreE,'TOTEXP15'] = 1.0
    df = df.rename(columns = {'TOTEXP15' : 'UTILIZATION'})
    df=df[['REGION','AGE','sex','race','MARRY','FTSTU','ACTDTY','HONRDC','RTHLTH','MNHLTH','HIBPDX','CHDDX','ANGIDX','MIDX','OHRTDX','STRKDX','EMPHDX','CHBRON','CHOLDX','CANCERDX','DIABDX','JTPAIN','ARTHDX','ARTHTYPE','ASTHDX','ADHDADDX','PREGNT','WLKLIM','ACTLIM','SOCLIM','COGLIM','DFHEAR42','DFSEE42','ADSMOK42','PCS42','MCS42','K6SUM42','PHQ242','EMPST','POVCAT','INSCOV','UTILIZATION','PERWT15F']]
    d = {}
    x = df.drop(['UTILIZATION','sex','race'],axis=1)
    n = np.shape(x)[0]
    idx = np.linspace(0,n-1,n).astype(int)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    d["y"]=df['UTILIZATION'].to_numpy().astype(int)[idx]
    d["zrace"]=df['race'].to_numpy()[idx]
    d["zsex"]=df['sex'].to_numpy()[idx]
    d["x"]=df.drop(['UTILIZATION','sex','race'],axis=1).to_numpy()[idx]
    with open("data_format/MEPS.pickle", "wb") as f:
        pickle.dump(d, f)

def load_census():
    data_source = ACSDataSource(survey_year='2018', horizon='1-Year', survey='person')
    ca_data = data_source.get_data(states=["CA"],download=True)

    data = {}
    ACSIncome = folktables.BasicProblem(
        features=[
            'AGEP',
            'COW',
            'SCHL',
            'MAR',
            'OCCP',
            'POBP',
            'RELP',
            'WKHP',
            #'SEX',
            #'RAC1P',
        ],
        target='PINCP',
        target_transform=lambda x: x > 50000,    
        group=['SEX','RAC1P'],
        preprocess=folktables.adult_filter,
        postprocess=lambda x: np.nan_to_num(x, -1),
    )
    ca_features, ca_labels, ca_attrib = ACSIncome.df_to_pandas(ca_data)
    x = ca_features.to_numpy()
    n = np.shape(x)[0]
    idx = np.linspace(0,n-1,n).astype(int)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    data["x"] = ca_features.to_numpy()[idx]
    data["y"] = (ca_labels.to_numpy()[idx]).astype(int)
    data["y"] = data["y"].reshape(len(data["y"]))
    data["zsex"] = ca_attrib['SEX'].to_numpy()[idx] - 1
    data["zrace"] = ca_attrib['RAC1P'].to_numpy()[idx]-1

    #https://api.census.gov/data/2019/acs/acs1/pums/variables/RAC1P.json
    #Remove races that are not black or white 
    mask = (data["zrace"]==0)|(data["zrace"]==1)
    data["x"] = data["x"][mask]
    data["y"] = data["y"][mask]
    data["zsex"] = data["zsex"][mask]
    data["zrace"] = data["zrace"][mask]

    with open("data_format/CENSUS.pickle", "wb") as f:
        pickle.dump(data, f)

