import pandas as pd
import numpy as np
import json
import datetime

FILE_USER_PATH = "C:\\Users\\demps\\Who_Am_I\\data\\users\\users.json"
FILE_CORP_CREDS_PATH = "C:\\Users\\demps\\Who_Am_I\\data\\users\\user_corporate_creds.json"
DEPTS = ["Accounting", "Administration","Marketing", "Development", "Sales"]

file_user_path = FILE_USER_PATH
file_corp_creds_path = FILE_CORP_CREDS_PATH


with open (file_user_path, "r") as file:

    data = json.load(file)
    df = pd.DataFrame(data)
    df_sorted = df.sort_values(by = "ID")
    dob = df_sorted["dob"]
    dobs = pd.to_datetime(dob, format = "%d-%m-%Y")
    today = datetime.datetime.now()
    age_days = (today - dobs).dt.days
    ages = age_days / 365.25

with open(file_corp_creds_path, "r") as file:
    data = json.load(file)
    df = pd.DataFrame(data)
    df_sorted = df.sort_values(by = "ID")
    df_sorted["age"] = ages

    print(df_sorted.head(5))
    print("ID TYPE")
    print(type(df_sorted["ID"]))
    bin_manag = [0] * len(df)
    df_sorted["manag"] = bin_manag


    list_output = []

    for i in DEPTS:

        subset = df_sorted[df_sorted["department"] == i]
        target_max = subset["age"].idxmax()
        idt = subset.loc[target_max, "ID"]

        target_idx = df_sorted.index[df_sorted["ID"] == idt]

        df_sorted.loc[target_idx,"manag"] = 1
        print(df_sorted.loc[target_idx])

    bin_upper_manag = [0] * len(df)
    df_sorted["upper_manag"] = bin_upper_manag

    bin_exec_manag = [0] * len(df)
    df_sorted["exec_manag"] = bin_exec_manag
    target_idx = df_sorted.index[df_sorted["seniority"] == "Executive"]
    df_sorted.loc[target_idx, "exec_manag"] = 1 

print(df_sorted.sort_values(by = "department"))

df_output = pd.DataFrame({
       "ID":df_sorted["ID"],
       "seniority":df_sorted["seniority"],
       "department":df_sorted["department"],
       "position":df_sorted["position"],
       "manag":df_sorted["manag"],
       "upper_manag":df_sorted["upper_manag"],
       "exec_manag":df_sorted["exec_manag"]
})

data = df_output.to_dict(orient="records")

with open(FILE_CORP_CREDS_PATH, "w") as json_file:
    json.dump(
        data,
        json_file,
        indent=7
    )




# ===============================================
# SKILLS SECTION
# ===============================================

DEPTS = ["Accounting", "Executive", "Administration","Marketing", "Development", "Sales"]

DEPT_SKILLS = [
    ["Administrative","Accounting"],
    ["Administrative", "Executive"],
    ["Administrative", "Executive"],
    ["Marketing", "Sales"],
    ["Administrative","Programming"],
    ["Marketing", "Sales"]
]

DEPT_SKILL_WEIGHTS = [

    [1,2],
    [1,2],
    [2,1],
    [2,1],
    [1,2],
    [1,2]

]

SKILLS = ["Marketing", "Sales", "Accounting", "Administrative", "Programming", "Executive"]

SENIORITIES_RANGES = [
    ["Entry",[0.56]],
    ["Junior", [1.45]],
    ["Medior",[1.55]],
    ["Senior",[61,80]],
    ["Executive",[81,100]]
]

MANAG_B00ST = 0.15

with open (FILE_CORP_CREDS_PATH, "r") as file:
    
    data = json.load(file)
    df = pd.DataFrame(data)

    for i, d in enumerate(DEPTS):

        df_idx = df.index[df["department"] == d]
        df_dpt = df.loc[df_idx]

        skill_set = DEPT_SKILLS[i]
        skill_wts = DEPT_SKILL_WEIGHTS[i]

        skill_1 = skill_set[0]
        skill_2 = skill_set[1]

        skill_1_wt = skill_wts[0]
        skill_2_wt = skill_wts[1]

        for j, s in enumerate(SENIORITIES_RANGES):

            senior_set = SENIORITIES_RANGES[j]
            senior_lvl = senior_set[0]
            senior_range = senior_set[1]

            range_low = senior_range[0]
            range_high = senior_range[1]

            senior_idx = df_dpt.index[df_dpt["seniority"] == senior_lvl]
            df_senior = df_dpt.loc[senior_idx]

            
