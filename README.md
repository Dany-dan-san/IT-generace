# Synthetic IT Workforce Generator

**Python | Statistical Simulation | Synthetic Data Generation**

### Overview

A personal Python project designed to generate a synthetic workforce for a fictional IT company. It uses statistical distributions, probabilistic sampling, and rule-based assignments to simulate employee demographics, organizational structures, and professional competencies.

The project serves as the foundation for a future management simulation game inspired by *SimCompanies* and *Simuland*.

### Project Structure

**1. `00_pop_generation.py` — Population Generation**

Generates fictional employees with demographic characteristics, including names, nationalities, age, gender, height, weight, and geographic location.

Uses configurable probabilities and statistical distributions (Beta, Normal, and Lognormal).

**2. `01_corp_attributions.py` — Corporate Attributes**

Assigns employees to departments, seniority levels, and job positions using organizational quotas and weighted random sampling. Includes executive role allocation.

**3. `02_skill_generation.py` — Skill Generation (In Progress)**

Introduces managerial classifications and a competency framework covering six skill categories:

- Marketing
- Sales
- Accounting
- Administration
- Programming
- Executive Management

Skill allocation is designed to reflect departmental specialization, seniority, and managerial responsibilities.

### Technologies

- **Python:** Core programming language
- **Pandas & NumPy:** Data manipulation and numerical operations
- **SciPy:** Statistical distributions and random sampling
- **Names Dataset:** Nationality-specific name generation
- **JSON:** Employee data storage

### Getting Started

Install the required dependencies:

```bash
pip install pandas numpy scipy names-dataset
```

Configure the local JSON file paths, then execute the scripts sequentially:

```bash
python 00_pop_generation.py
python 01_corp_attributions.py
python 02_skill_generation.py
```

### Development Status

**Work in progress (2026).**

The population and organizational generation components are implemented. The skill-generation system and gameplay mechanics remain under development.

The long-term goal is to simulate employee performance, career progression, and organizational management within an interactive business environment.
