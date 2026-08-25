# 🏃‍♂️ Exercise Prescription Calculator

## The app:
https://zonytepu.streamlit.app

### Swift:
https://github.com/TommiBu/ZonyTepu -> exploratory try of transfer from streamlit to swift

A simple and interactive web application built with Python and Streamlit to calculate optimal heart rate zones for physical training. 

This tool uses the **Karvonen method (Heart Rate Reserve - HRR)** and **$VO_2max$** to prescribe safe and effective exercise intensity based on the user's age, gender, resting heart rate, and overall fitness level.

## Features
* **Max Heart Rate Calculation:** Uses gender-specific regression formulas or accepts actual data from a stress test.
* **$VO_2max$ Integration:** Automatically calculates the optimal training percentage based on the formula: `%HRR = 60 + (VO2max / 3.5)`.
* **Current vs. Optimal Load:** Compares the user's current training heart rate with their optimal target and provides instant feedback.
* **Safety Corrections:** Adjusts the final target heart rate zone based on the population category (Weakened/Obese, General, or Fit/Active).
* **Data Export:** Allows users to download the calculated FITT prescription as a `.txt` report or a `.csv` data table.

## Tech Stack
* **Python**
* **Streamlit** (for the web GUI)
* **Pandas** (for CSV data handling)
