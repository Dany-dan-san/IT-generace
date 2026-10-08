from scipy.stats import beta
from names_dataset import NameDataset
import pandas as pd
import numpy as np
import random
import datetime
from datetime import date, timedelta
import json
import os

def gen_pop(n, 
            prob_male, 
            prob_female, 
            probs_age=None,
            countries=None, 
            countr_probs=None, 
            male_mu_height=None, 
            male_sigma_height=None, 
            female_mu_height=None, 
            female_sigma_height=None, 
            male_mu_weight=None, 
            male_signa_weight=None,
            female_mu_weight=None,
            female_sigma_weight=None):


    if countries is None:
        countries = ["CZ","SK","FR","DE"]
    if countr_probs is None:
        countr_probs = [0.7,0.1,0.15,0.05]
    if probs_age is None:
        probs_age = [0.10,0.15,0.40,0.30,0.05]
    if male_mu_height is None:
        male_mu_height = 178.58
    if male_sigma_height is None:
        male_sigma_height = 6.6
    if female_mu_height is None:
        female_mu_height = 165.99
    if female_sigma_height is None:
        female_sigma_height = 6.2
    if male_mu_weight is None:
        male_mu_weight = 84.5
    if male_signa_weight is None:
        male_signa_weight = 14.5
    if female_mu_weight is None:
        female_mu_weight = 69.8
    if female_sigma_weight is None:
        female_sigma_weight = 13.2

    # ============================================================
    # I. POPULATION AGE GENERATION
    # ============================================================
    
    quotas_discrete = [int(x * n) for x in probs_age[:-1]]
    quotas_discrete.append(n - sum(quotas_discrete))

    ages = []
    params = [[1.5,2],[2,2],[2,2],[3.1,2],[4.4,2]]
    ranges = [[18,21],[22,24],[24,39],[40,55],[56,64]]

    for i, subset in enumerate(params):

        a = subset[0]
        b = subset[1]

        num = quotas_discrete[i]
        age_range = ranges[i]
        lower = age_range[0]
        upper = age_range[1]
        age_list = beta.rvs(

            a,
            b,
            loc = lower,
            scale = upper - lower,
            size = num,
            random_state = 33
        )

        ages.append(age_list) 

    ages = np.concatenate(ages).astype(int)
        
    # ============================================================
    # II. POPULATION GENDER GENERATION
    # ============================================================

    outcome = [1,0]
    probs = [prob_male,prob_female]
    gen_gender = random.choices(outcome, weights = probs, k = n)

    # ============================================================
    # III. POPULATION NATIONALITIES AND FNAMES/LNAMES
    # ============================================================

    nationalities = countries
    probs = countr_probs
    gen_nations = random.choices(nationalities, weights = probs, k = n)

    nd = NameDataset()

    demo_bind = pd.DataFrame({
        "nationality":gen_nations,
        "gender":gen_gender,
        "age":ages
    })

    df_output = pd.DataFrame(columns=["nationality","gender","age","fname","lname"])

    for nat in nationalities:

        subset = demo_bind[demo_bind["nationality"] == nat]

        if nat == "SK" or nat == "CZ":

            names_list = nd.get_top_names(
                n=100,
                use_first_names=True,
                country_alpha2="CZ"
            )

            lnames_list = nd.get_top_names(
                n=100,
                use_first_names=False,
                country_alpha2="CZ"
            )

            f_lnames = [
                name for name in lnames_list["CZ"]
                if name.endswith("ová")
            ]

            m_lnames = [
                name for name in lnames_list["CZ"]
                if not name.endswith("ová")
            ]

            f_names = names_list["CZ"]["F"]
            m_names = names_list["CZ"]["M"]

            target_names = [
                random.choice(m_names) if x == 1 else random.choice(f_names)
                for x in subset["gender"]
            ]

            target_lnames = [
                random.choice(m_lnames) if x == 1 else random.choice(f_lnames)
                for x in subset["gender"]
            ]

        else:

            names_list = nd.get_top_names(
                n=100,
                use_first_names=True,
                country_alpha2=nat
            )

            lnames_list = nd.get_top_names(
                n=100,
                use_first_names=False,
                country_alpha2=nat
            )

            lnames = lnames_list[nat]

            f_names = names_list[nat]["F"]
            m_names = names_list[nat]["M"]

            target_names = [
                random.choice(m_names) if x == 1 else random.choice(f_names)
                for x in subset["gender"]
            ]

            target_lnames = [
                random.choice(lnames)
                for x in subset["gender"]
            ]

        # runs for ALL nationalities
        token = pd.DataFrame({
            "nationality": subset["nationality"],
            "gender": subset["gender"],
            "age": subset["age"],
            "fname": target_names,
            "lname": target_lnames
        })

        df_output = pd.concat(
            [df_output, token],
            ignore_index=True
        )
    # ============================================================
    # IV. POPULATION HEIGHTS
    # ============================================================

    heights = [random.normalvariate(mu = male_mu_height, sigma = male_sigma_height) if x == 1 else random.normalvariate(mu = female_mu_height, sigma = female_sigma_height) for x in df_output["gender"]]

    df_output["height"] = heights

    # ============================================================
    # V. POPULATION WEIGHTS
    # ============================================================

    m_mu = male_mu_weight
    m_sigma = male_signa_weight

    f_mu = female_mu_weight
    f_sigma = female_sigma_weight

    m_log_mu = np.log(m_mu**2 / np.sqrt((m_mu**2 + m_sigma**2)))
    m_log_sigma = np.sqrt(np.log((1 + (m_sigma**2 / m_mu**2))))

    f_log_mu = np.log(f_mu**2 / np.sqrt((f_mu**2 + f_sigma**2)))
    f_log_sigma = np.sqrt(np.log((1 + (f_sigma**2 / f_mu**2))))


    weights = [random.lognormvariate(mu = m_log_mu, sigma = m_log_sigma) if x == 1 else random.lognormvariate(mu = f_log_mu, sigma=f_log_sigma) for x in df_output["gender"]]

    df_output["weight"] = weights

    # ============================================================
    # VI. POPULATION DATE OF BIRTHS
    # ============================================================

    reference_date = date.today()

    df_output["dob"] = [
        (reference_date - timedelta(days=age * 365.2425)).strftime("%d-%m-%Y")
        for age in df_output["age"]
    ]

    # ========================================================================================================
    # VI. IDs
    # ========================================================================================================

    IDs = [
        ''.join(random.choices('0123456789', k=6))
        for _ in range(len(df_output))
    ]

    # ========================================================================================================
    # VII. LOCATION
    # ========================================================================================================   

    french_set = ["Paris", "Lyon", "Montpellier"]
    probs = [0.7,0.2,0.1]

    locations = [random.choices(population=french_set, k = 1, weights = probs) if x == "FR" else "Prague" for x in df_output["nationality"]]

    # ========================================================================================================
    # VIII. FINAL OUTPUT
    # ========================================================================================================

    df_final = pd.DataFrame({
        "ID":IDs,
        "nationality":df_output["nationality"],
        "gender":df_output["gender"],
        "fname":df_output["fname"],
        "lname":df_output["lname"],
        "height":df_output["height"],
        "weight":df_output["weight"],
        "location":locations,
        "dob":df_output["dob"],
        "time_stamp":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    file_path = "C:\\Users\\demps\\Who_Am_I\\data\\users\\users.json"
    data = df_final.to_dict(orient="records")

    if not os.path.exists(file_path):

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=9)

    else:
        with open(file_path, 'r+') as json_file:

            df = json.load(json_file)

            df.extend(data)

            json_file.seek(0)
            json.dump(df, json_file, indent=9)
            json_file.truncate()


gen_pop(n=50, prob_male=0.75,prob_female=0.25)