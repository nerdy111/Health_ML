COVID Outbreak Alert System

A Python project to monitor COVID-19 cases and detect outbreaks based on week-over-week or month-over-month growth rates.

Features

⦁	Tracks COVID-19 cases over time.
⦁	Calculates weekly or monthly growth rates.
⦁	Detects sudden spikes and triggers alerts if growth exceeds a threshold.
⦁	Visualizes data with line plots and highlights outbreak points.

Installation
1. Clone the repository:
git clone https://github.com/nerdy111/Health_ML.git
cd Health_ML
Create a virtual environment:
python -m venv venv
Activate the virtual environment:

Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt
Dependencies: pandas, numpy, matplotlib

Usage
Place your dataset CSV (rv-dashboard.csv) in the project folder.

Run the script:
python outbreak_alert.py

Outputs include:
Line plot of COVID cases over time.
Scatter points highlighting outbreak alerts.

Example Output
Line Plot: Total COVID cases per week or month.
Red points: Weeks/months where growth rate exceeded the threshold.

