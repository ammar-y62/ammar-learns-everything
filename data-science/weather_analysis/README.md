# Weather Analysis Playground

This project fetches real-time weather data from the [Foreca Weather API](https://developer.foreca.com/) and provides an interactive environment to explore and visualize it. The main workspace for this project is the `Weather_Analysis_Playground.ipynb` Jupyter Notebook.

## ✨ Features

- **Simple & Interactive**: A single Jupyter Notebook to guide you through the process.
- **Secure Credentials**: Uses a `.env` file to keep your API keys safe and out of the code.
- **Live Data**: Pulls daily and hourly forecast data directly from the Foreca API.
- **Interactive Graphs**: Generates plots with Plotly for easy data exploration.
- **🌟 6 Weather Applications**: Complete suite of practical weather-based applications:
  - **🔮 What Should I Wear Today?** - Outfit recommendations based on weather
  - **📍 Weather-Based Event Planner** - Find best days for outdoor activities
  - **💡 Smart Notification Bot** - Weather alerts and notifications
  - **🎒 Travel Companion App** - Packing lists for destinations
  - **📈 Weather Trends Visualizer** - Comprehensive trend analysis
  - **🌎 Global Weather Heatmap** - Worldwide weather overview

## 📁 Project Structure

```
weather_analysis/
├── api_integrations/
│   └── foreca_weather_api.py   # The reusable API wrapper
├── Weather_Analysis_Playground.ipynb # Your main workspace!
├── weather_apps.py             # 6 weather applications
├── example_usage.py            # Usage examples and tutorials
├── WEATHER_APPS_README.md      # Detailed apps documentation
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

---

## 🌟 Weather Applications

After completing the basic weather analysis, you can run the 6 weather applications! Add this to your notebook:

### Quick Start - All Applications

```python
# Import the weather applications
from weather_apps import run_all_weather_apps, display_results, show_all_plots

# Use your existing location_id and city name
location_id = 100292968  # Your location ID from the notebook
city_name = "Abu Dhabi"  # Your city name

# Run all 6 weather applications at once!
results = run_all_weather_apps(api, location_id, city_name)

# Display all results and plots
if results:
    display_results(results)
    show_all_plots(results)
else:
    print("❌ No results - check your location_id and API connection!")
```

### Individual Applications

```python
from weather_apps import WeatherApps

# Initialize the apps
apps = WeatherApps(api)

# Get your forecast data (you already have this)
# daily_forecast = api.get_daily_forecast(location_id, periods=7)

# 🔮 1. What Should I Wear Today?
outfit_fig, outfit_recs = apps.what_to_wear_app(daily_forecast)
print("👕 Outfit Recommendations:")
print(outfit_recs)
outfit_fig.show()

# 📍 2. Event Planner
event_fig, event_recs = apps.event_planner_app(daily_forecast)
print("📅 Event Planning Scores:")
print(event_recs.sort_values('score', ascending=False))
event_fig.show()

# 💡 3. Notification Bot
alert_fig, alerts = apps.notification_bot_app(daily_forecast)
if alerts:
    print("🚨 Weather Alerts:")
    for alert in alerts:
        print(f"📅 {alert['date']}: {alert['alerts']}")
    alert_fig.show()
else:
    print("✅ No weather alerts!")

# 🎒 4. Travel Companion
packing_fig, packing_list = apps.travel_companion_app(daily_forecast)
print("🎒 Packing List:")
for category, items in packing_list.items():
    print(f"{category.upper()}: {', '.join(sorted(items))}")
packing_fig.show()

# 📈 5. Trends Visualizer
trend_figs, trend_stats = apps.trends_visualizer_app(daily_forecast)
print("📈 Weather Trends Analysis:")
print(f"Temperature stats: {trend_stats['temperature']}")
for fig in trend_figs:
    fig.show()

# 🌎 6. Global Heatmap
global_fig = apps.global_heatmap_app()
global_fig.show()
```

### What Each Application Does

1. **🔮 What Should I Wear Today?**
   - Suggests outfits based on temperature, rain, and wind
   - Provides accessories recommendations (umbrella, sunglasses, etc.)
   - Interactive chart showing daily outfit suggestions

2. **📍 Weather-Based Event Planner**
   - Scores each day (0-100) for outdoor activities
   - Considers temperature, precipitation, and wind conditions
   - Suggests specific activities (running, picnics, indoor activities)

3. **💡 Smart Notification Bot**
   - Generates alerts for extreme weather conditions
   - Heatwave, freezing, heavy rain, and wind warnings
   - Severity-based alert system

4. **🎒 Travel Companion App**
   - Creates packing lists based on destination weather
   - Categorizes items (clothing, accessories, gear)
   - Considers trip duration and weather patterns

5. **📈 Weather Trends Visualizer**
   - Creates comprehensive trend visualizations
   - Temperature, precipitation, and wind analysis
   - Statistical summaries and comparisons

6. **🌎 Global Weather Heatmap**
   - Interactive world map with weather data
   - Temperature visualization for major cities
   - Color-coded temperature scale

### Customization Options

- **Change Location**: Use `api.search_location("City Name", country="XX")` to find new locations
- **Trip Duration**: Modify packing list for different trip lengths
- **Alert Thresholds**: Customize weather alert sensitivity
- **Activity Preferences**: Adjust scoring for different outdoor activities

For detailed documentation, see `WEATHER_APPS_README.md`.

---

## 🎯 Next Steps

- **Experiment**: Try different cities and weather conditions
- **Extend**: Add more weather parameters (humidity, UV index)
- **Integrate**: Connect to notification services (Telegram, Slack, Email)
- **Deploy**: Turn into web applications using Streamlit or Flask
- **Enhance**: Add machine learning for better predictions

Happy weather coding! 🌤️