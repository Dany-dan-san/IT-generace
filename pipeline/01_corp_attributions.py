
# =======================================================================================================
# STEP 1: CORPORATE ATTRIBUTES AND JOB POSITION GENERATION
# =======================================================================================================

# This script assigns corporate attributes to the workers generated in Step 0.
# It simulates the organizational structure of an IT company by assigning
# seniority levels, departments, and job positions based on configurable
# quotas, age thresholds, and weighted random sampling.

# ===============================================================================
# A. KEY PARAMETERS
# ===============================================================================

# The main configurable parameters are:

# - REGISTER_PATH: Path to the JSON file containing workers generated in Step 0.
# - OUTPUT_PATH: Destination JSON file for the corporate attributes.

# - SENIORITIES: Five seniority levels (Entry, Junior, Medior, Senior, Executive),
#   assigned according to predefined age thresholds.

# - DEPARTMENTS: Six corporate departments (Marketing, Sales, Administration,
#   Accounting, Development, Executive).

# - PROBS: Target percentage breakdown of workers across departments
#   (e.g., [0.15, 0.20, 0.10, 0.05, 0.50]).

# - SENIOR_QUOTAS: Fixed number of administrative employees by seniority level.
# - LVL_PROBS: Target seniority distribution within the other departments
#   (e.g., [0.10, 0.15, 0.45, 0.30]).

# - ALL_JOBS: Available job positions for each department and seniority level,
#   together with their respective selection probabilities.

# - EXEC_POSITIONS: List of executive positions (CEO, COO, CFO, CTO, etc.),
#   assigned to executive workers in descending order of age.

# The assign_positions() function handles departmental allocations and job
# assignments using quotas and weighted random sampling.

# ===============================================================================
# B. KEY OUTPUT
# ===============================================================================

# The script reads the existing population data and produces a JSON file
# containing the following corporate attributes for each employee:

# - Unique employee ID (inherited from Step 0)
# - Seniority level (Entry, Junior, Medior, Senior, Executive)
# - Department
# - Job position

# The output is saved in "user_corporate_creds.json", which is used
# by the next script to generate managerial attributes and employee skills.

# NOTE: Developed without the use of AI. 

# ===========================================================
# C. FULL SCRIPT
# ===========================================================



import json
import pandas as pd
import numpy as np
import datetime
import random
import os

REGISTER_PATH = "C:\\Users\\demps\\Who_Am_I\\data\\users\\users.json"
OUTPUT_PATH = "C:\\Users\\demps\\Who_Am_I\\data\\users\\user_corporate_creds.json"

with open(REGISTER_PATH, "r") as register:
    file_data = json.load(register)

    df = pd.DataFrame(file_data)

    # =================================================================
    # SENIORITY GENERATION
    # =================================================================

    dobs = df["dob"]
    dobs = pd.to_datetime(dobs, format = "%d-%m-%Y")
    today = datetime.datetime.now()
    age_days = (today - dobs).dt.days
    ages = age_days / 365.25

    seniorities = ["Entry", "Junior", "Medior", "Senior", "Executive"]

    levels = [

        seniorities[0] if x < 21 # Entry
        else seniorities[1] if x >= 21 and x <= 24 # Junior
        else seniorities[2] if x > 24 and x <= 39 # Medior
        else seniorities[3] if x > 39 and x < 55 # Senior
        else seniorities[4]
        for x in ages
    ] 

    df_trans = pd.DataFrame({

        "ID":df["ID"],
        "age":ages,
        "seniority":levels,
        "department":None,
        "position":None
    })

    counts = df_trans['seniority'].value_counts()
    print(counts)

    # =================================================================
    # DEPARTMENT GENERATION
    # =================================================================

    departments = [
        "Marketing",
        "Sales",
        "Administration",
        "Accounting",
        "Development",
        "Executive"
    ]

    n_execs = len(df_trans[df_trans["seniority"] == "Executive"])
    n = len(df_trans)

    probs = [0.15, 0.20, 0.10, 0.05, 0.50,0]
    quotas = [int(x * n) for x in probs[:-1]]
    quotas.append(n - sum(quotas))
    quotas[5] = n_execs

    print(quotas)

    # ===========================
    # A. ADMINISTRATION
    # ===========================

    ids = df_trans["ID"]
    sen_lvls = df_trans["seniority"]

    senior_quotas = [
        ["Entry",1],
        ["Junior",1],
        ["Medior",2],
        ["Senior",1],
        ["Executive",0]
    ]

    for q in senior_quotas:

        lvl = q[0]
        qta = q[1]

        subset = df_trans.index[df_trans['seniority'] == lvl]
        subset = subset.to_list()
        hiree_idx = random.sample(population = subset, k = qta)

        index = pd.Index(hiree_idx)

        df_trans.loc[index,"department"] = "Administration"
        print(df_trans.loc[index])

    positions = [
        ["Entry", "Office Assistant"],
        ["Junior", "HR Specialist"],
        ["Medior", "Office Coordinator"],
        ["Medior", "Executive Assistant"],
        ["Senior", "Operations & HR Director"]
    ]

    for lvl, pos in positions:

        subset = df_trans.index[
            (df_trans["department"] == "Administration") &
            (df_trans["seniority"] == lvl) &
            (df_trans["position"].isna())
        ].to_list()

        hiree_idx = random.sample(
            population=subset,
            k=1
        )

        df_trans.loc[hiree_idx, "position"] = pos

    print(df_trans[df_trans['department'] == "Administration"])


    # ===========================
    # B. ALL OTHER DEPARTMENTS, EXCL. EXECUTIVE
    # =========================== 

    # REQUIRED ITEMS
    TARGET_DF = df_trans
    ALL_DPTS = [departments[0],departments[1],departments[3],departments[4]]
    ALL_QUOTAS = [quotas[0],quotas[1],quotas[3],quotas[4]]
    LVL_PROBS = [0.1, 0.15, 0.45, 0.3]

    ALL_JOBS = [

        # ==========================================================
        # MARKETING
        # ==========================================================
        [
            ["Entry", [
                "Content Specialist",
                "Campaign Specialist"
            ],[0.45,0.55]],

            ["Junior", [
                "Content Specialist",
                "Campaign Specialist",
                "SEO Specialist"
            ],[0.35,0.40,0.25]],

            ["Medior", [
                "Content Specialist",
                "Campaign Specialist",
                "SEO Specialist",
                "Market Research Analyst"
            ],[0.3,0.35,0.2,0.15]],

            ["Senior", [
                "Content Specialist",
                "Campaign Specialist",
                "SEO Specialist",
                "Market Research Analyst"
            ],[0.15,0.35,0.2,0.3]]
        ],

        # ==========================================================
        # SALES
        # ==========================================================
        [
            ["Entry", [
                "Sales Representative",
                "Business Development Representative"
            ], [0.70, 0.30]],

            ["Junior", [
                "Sales Representative",
                "Business Development Representative",
                "Account Specialist"
            ], [0.50, 0.30, 0.20]],

            ["Medior", [
                "Sales Representative",
                "Business Development Representative",
                "Account Specialist",
                "Sales Operations Specialist"
            ], [0.40, 0.20, 0.30, 0.10]],

            ["Senior", [
                "Sales Representative",
                "Account Specialist",
                "Sales Operations Specialist"
            ], [0.30, 0.45, 0.25]]
        ],

        [
            # ==========================================================
            # ACCOUNTING
            # ==========================================================

            ["Entry", [
                "Accountant",
                "Payroll Specialist"
            ], [0.70, 0.30]],

            ["Junior", [
                "Accountant",
                "Payroll Specialist",
                "Cost Analyst"
            ], [0.55, 0.25, 0.20]],

            ["Medior", [
                "Accountant",
                "Payroll Specialist",
                "Cost Analyst",
                "Financial Analyst"
            ], [0.40, 0.20, 0.20, 0.20]],

            ["Senior", [
                "Accountant",
                "Cost Analyst",
                "Financial Analyst"
            ], [0.25, 0.30, 0.45]]

        ],

        # ==========================================================
        # PROGRAMMING
        # ==========================================================
        [
            ["Entry", [
                "Software Developer",
                "QA Test Engineer"
            ],[0.7,0.3]],

            ["Junior", [
                "Software Developer",
                "QA Test Engineer",
                "Database Engineer"
            ],[0.65,0.25,0.10]],

            ["Medior", [
                "Software Developer",
                "QA Test Engineer",
                "DevOps Engineer",
                "Database Engineer"
            ],[0.55,0.2,0.15,0.1]],

            ["Senior", [
                "Software Developer",
                "QA Test Engineer",
                "DevOps Engineer",
                "Database Engineer"
            ],[0.5,0.15,0.2,0.15]]
        ]
    ]


    def assign_positions(df, dpts, qtas, lvl_probs, jobs):

        seniority_levels = [
            "Entry",
            "Junior",
            "Medior",
            "Senior"
        ]

        for i, dpt in enumerate(dpts):

            # ==========================================================
            # 1. DEPARTMENT QUOTA
            # ==========================================================

            dpt_qta = qtas[i]

            lvl_quotas = [
                int(prob * dpt_qta)
                for prob in lvl_probs
            ]

            remainder = dpt_qta - sum(lvl_quotas)

            largest_idx = lvl_probs.index(max(lvl_probs))
            lvl_quotas[largest_idx] += remainder

            senior_quotas = list(
                zip(seniority_levels, lvl_quotas)
            )

            # ==========================================================
            # 2. ASSIGN BY DESIRED SENIORITY
            # ==========================================================

            for lvl, lvl_qta in senior_quotas:

                subset = df.index[
                    (df["seniority"] == lvl) &
                    (df["department"].isna())
                ].to_list()

                sample_size = min(
                    lvl_qta,
                    len(subset)
                )

                hiree_idx = random.sample(
                    population=subset,
                    k=sample_size
                )

                df.loc[
                    hiree_idx,
                    "department"
                ] = dpt

            # ==========================================================
            # 3. FILL ANY REMAINING DEPARTMENT SLOTS
            # ==========================================================

            current_qta = (
                df["department"] == dpt
            ).sum()

            missing_qta = dpt_qta - current_qta

            if missing_qta > 0:

                remaining_workers = df.index[
                    (df["department"].isna()) &
                    (df["seniority"] != "Executive")
                ].to_list()

                sample_size = min(
                    missing_qta,
                    len(remaining_workers)
                )

                additional_hires = random.sample(
                    population=remaining_workers,
                    k=sample_size
                )

                df.loc[
                    additional_hires,
                    "department"
                ] = dpt

            # ==========================================================
            # 4. ASSIGN POSITIONS
            # ==========================================================

            job_set = jobs[i]

            for job_data in job_set:

                lvl = job_data[0]
                positions = job_data[1]
                weights = job_data[2]

                subset = df.index[
                    (df["department"] == dpt) &
                    (df["seniority"] == lvl) &
                    (df["position"].isna())
                ]

                df.loc[
                    subset,
                    "position"
                ] = random.choices(
                    population=positions,
                    weights=weights,
                    k=len(subset)
                )

        return df

    df_upgrade = assign_positions(df = df_trans, dpts = ALL_DPTS, qtas = ALL_QUOTAS, lvl_probs = LVL_PROBS, jobs = ALL_JOBS)
    print(df_upgrade)

    # ===========================
    # C. EXECUTIVE DEPARTMENT
    # =========================== 

    df_exec_idx = df_upgrade.index[
        df_upgrade["seniority"] == "Executive"
    ]

    df_upgrade.loc[df_exec_idx, "department"] = "Executive"

    df_subset = df_upgrade.loc[df_exec_idx]

    ordered = df_subset.sort_values(
        by="age",
        ascending=False
    )

    exec_positions = [
        "Chief Executive Officer",
        "Chief Operating Officer",
        "Chief Financial Officer",
        "Chief Technology Officer",
        "Chief Commercial Officer",
        "Chief People Officer"
    ]

    for i in range(min(len(ordered), len(exec_positions))):

        worker_idx = ordered.index[i]
        position = exec_positions[i]

        df_upgrade.loc[worker_idx, "position"] = position

    # ========================================================
    # FILE OUTPUT
    # ========================================================

    df_output = pd.DataFrame({
        "ID": df_upgrade["ID"],
        "seniority": df_upgrade["seniority"],
        "department": df_upgrade["department"],
        "position": df_upgrade["position"]
    })

    data = df_output.to_dict(orient="records")

    with open(OUTPUT_PATH, "w") as json_file:
        json.dump(
            data,
            json_file,
            indent=4
        )

