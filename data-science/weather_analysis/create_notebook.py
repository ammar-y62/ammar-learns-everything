import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Weather Analysis Playground\n\n",
    "Welcome! This notebook is your interactive playground for fetching real-time weather data from the Foreca API and creating visualizations.\n\n",
    "**How to use:** Run each cell one by one by pressing `Shift + Enter`."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 1: Load Libraries and API Keys\n\n",
    "First, we import the necessary libraries and securely load your API credentials from the `.env` file."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "from dotenv import load_dotenv\n",
    "import pandas as pd\n",
    "import plotly.express as px\n",
    "from api_integrations.foreca_weather_api import ForecaWeatherAPI\n\n",
    "# Load the .env file from the current directory\n",
    "load_dotenv()\n\n",
    "api_username = os.getenv(\"FORECA_API_USERNAME\")\n",
    "api_password = os.getenv(\"FORECA_API_PASSWORD\")\n\n",
    "print(\"✅ Setup complete.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 2: Connect to the Foreca API\n\n",
    "Now, let's create our API client. It will handle authentication for us automatically."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if not api_username or not api_password:\n",
    "    print(\"❌ Error: API credentials not found in .env file!\")\n",
    "else:\n",
    "    api = ForecaWeatherAPI(username=api_username, password=api_password)\n",
    "    print(\"🌤️ Successfully connected to Foreca API.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 3: Find a Location ID\n\n",
    "To get a forecast, we first need the unique ID for a city. Let's search for **Mecca**."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "locations_df = pd.DataFrame(api.search_location(\"Mecca\", country=\"SA\"))\n",
    "locations_df"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The ID for Mecca is `102024449`. Let's save it."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "location_id = 102024449"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 4: Get the Weather Forecast\n\n",
    "Now we can use the ID to fetch the 7-day daily forecast."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "daily_forecast = api.get_daily_forecast(location_id, periods=7)\n",
    "daily_forecast"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 5: Create Interactive Graphs\n\n",
    "This is the fun part! Let's visualize the data with Plotly."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Graph 1: Daily High and Low Temperatures"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "fig_temp = px.line(\n",
    "    daily_forecast, \n",
    "    x='date', \n",
    "    y=['maxTemp', 'minTemp'], \n",
    "    title='7-Day Temperature Forecast',\n",
    "    labels={'date': 'Date', 'value': 'Temperature (°C)', 'variable': 'Forecast'},\n",
    "    markers=True\n",
    ")\n",
    "fig_temp.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Graph 2: Daily Precipitation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "fig_precip = px.bar(\n",
    "    daily_forecast,\n",
    "    x='date',\n",
    "    y='precipAccum',\n",
    "    title='7-Day Precipitation Forecast',\n",
    "    labels={'date': 'Date', 'precipAccum': 'Precipitation (mm)'}\n",
    ")\n",
    "fig_precip.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Your Turn to Experiment!\n\n",
    "This notebook is your playground. Try these ideas:\n\n",
    "- **Change the city**: In Step 3, change `\"Mecca\"` to your hometown or any other city.\n",
    "- **Fetch hourly data**: Use `api.get_hourly_forecast(location_id)` to get more detailed data.\n",
    "- **Create new plots**: Can you visualize `maxWindSpeed`?"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

# The name of the notebook file to be created
file_name = "Weather_Analysis_Playground.ipynb"

# Write the dictionary to a JSON file, with proper formatting
with open(file_name, 'w') as f:
    json.dump(notebook_content, f, indent=1)

print(f"✅ Successfully created notebook file: {file_name}")
