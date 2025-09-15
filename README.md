Student: Gino Cleofa<br>
Periode A (2025/26)

This is the repository for the Master of Applied Data Science course "Data Analysis & Visualisation" at Hogeschool Utrecht.
The repo is forked from https://github.com/raoulg/MADS-DAV.

# Table of Contents
- [Background](#background)
- [Assignments](#assignments)
- [Project structure](#project-structure)
- [Script usage](#script-usage)


# Background
For this course, I am analyzing a WhatsApp group export from my apartment building.<br>
The project focuses on three main categories of discussion:
- Facilities
- Hygiene
- Security

Each category is linked to a specific keyword, which serves as a parameter for the analysis script.<br>
For example, in the Facilities category the keyword can be “lift.”

# Assignments
Weekly assignments are added to a dedicated feature branch in GitHub.

References:
- Week 2 - feature/dav_les2
- Week 3 - feature/dav_les3
- Week 4 - feature/dav_les4
- Week 5 - feature/dav_les5
- Week 6 - feature/dav_les6

# Project structure
Below tree depicts relevant project files related to the assignments.<br>
The main. script is `apartment_community.py`<br>
Generated images are saved in the `img` folder.<br>
Logs are saved in the `src` sub folder

```
.
├── README.md
├── checklist.md
├── config.example.toml
├── config.toml
├── dashboards
├── data
├── dev
├── dist
├── img
│   ├── lift_histogram_by_hour.png
│   ├── lift_scatter_length_vs_hour.png
│   ├── lift_trend.png
├── notebooks
│   ├── 01-cleaning.ipynb
│   ├── 02-Gino-comparing_categories.ipynb
...
├── presentations
├── pyproject.toml
├── references
├── src
│   └── wa_analyzer
│       ├── __init__.py
...
│       ├── apartment_community.py
...
│       ├── logs
│       │   └── logfile.log
...

```

# Script usage
1. Make sure you have `uv` installed. You can check this by typing `which uv` in the terminal. If that doesnt return a location but `uv not found` you need to install it.<br>
On Unix systems, you can use `curl -LsSf https://astral.sh/uv/install.sh | sh`, for Windows read the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/)


2. activate venv<br>
From the root directory of the project activate and verify the `venv`:<br>

```
(base) jdoe-MacBook-Pro:MADS-DAV jdoe$ source .venv/bin/activate
(wa-analyzer) (base) jdoe-MacBook-Pro:MADS-DAV jdoe$
```
3. Run script<br>
After this, you can run the scripts with the following `command` and `keyword`, eg:

```bash
apartment_community --keyword lift
```

4. Logs<br>
Inside the `log` folder you will find a logfile, which has some additional information that might be useful for debugging.<br>
For logfile folder location see section 'Project structure'. <br>
The logging is also printed on the terminal output.

5. Images<br>
Inside the `img` folder you will find the saved images after each run prefixed by the keyword.<br>
For image folder location see section 'Project structure'. <br>
The images depicts following analyses themes
- Trend line for total messages over the years, dutch title:<br> `'keyword' gesprekken door de jaren heen`.
- Histogram of message on hours per day, dutch title:<br> `Flatgebouw App-groep gonst: 'keyword' nieuws rond de klok`.
- Scatter plot to correlate message length vs timestamp, dutch title:<br> `De 'keyword' zorgt voor golf aan berichten, en stapelt zich op!`






