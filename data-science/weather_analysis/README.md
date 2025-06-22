# Weather Analysis Playground

This project fetches real-time weather data from the [Foreca Weather API](https://developer.foreca.com/) and provides an interactive environment to explore and visualize it. The main workspace for this project is the `Weather_Analysis_Playground.ipynb` Jupyter Notebook.

## ✨ Features

- **Simple & Interactive**: A single Jupyter Notebook to guide you through the process.
- **Secure Credentials**: Uses a `.env` file to keep your API keys safe and out of the code.
- **Live Data**: Pulls daily and hourly forecast data directly from the Foreca API.
- **Interactive Graphs**: Generates plots with Plotly for easy data exploration.

## 📁 Project Structure

```
weather_analysis/
├── api_integrations/
│   └── foreca_weather_api.py   # The reusable API wrapper
├── Weather_Analysis_Playground.ipynb # Your main workspace!
├── .env                        # Your secret API keys (create this yourself)
├── requirements.txt            # Dependencies
└── README.md                   # This guide
```

---

## 🚀 How to Use This Project

### Step 1: Add Your API Credentials

Create a file named `.env` in this directory (`data-science/weather_analysis/`). Add your Foreca API keys to it like this:

```ini
# Foreca Weather API Credentials
FORECA_API_USERNAME="your_username_here"
FORECA_API_PASSWORD="your_password_here"
```
*(This file is ignored by Git, so your keys will remain private.)*

### Step 2: Install Dependencies

Open a terminal in this directory and run:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Jupyter Notebook

Start Jupyter from your terminal:

```bash
jupyter notebook
```

This will open a tab in your browser. Click on `Weather_Analysis_Playground.ipynb` to open it.

Inside the notebook, run each cell one by one by pressing `Shift + Enter`. This is where you can fetch data, create graphs, and play around with the code.