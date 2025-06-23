# 🌟 Weather Applications Collection

A comprehensive set of 6 amazing weather-based applications using the Foreca API! Each application provides unique insights and recommendations based on weather data.

## 🚀 Quick Start

Add this to your Jupyter notebook after your existing weather setup:

```python
# Import the weather applications
from weather_apps import run_all_weather_apps, display_results, show_all_plots

# Set your location (use your existing location_id)
location_id = 100109223  # Your location ID from the notebook
city_name = "Madina"     # Your city name

# Run all 6 weather applications at once!
results = run_all_weather_apps(api, location_id, city_name)

# Display all results and plots
if results:
    display_results(results)
    show_all_plots(results)
else:
    print("❌ No results - check your location_id and API connection!")
```

## 🔮 Applications Overview

### 1. **What Should I Wear Today?** 👕
- **Purpose**: Suggests outfits based on weather conditions
- **Features**:
  - Temperature-based clothing recommendations
  - Rain/wind accessories suggestions
  - Interactive chart with outfit details
- **Output**: Interactive plot + detailed recommendations

### 2. **Weather-Based Event Planner** 📅
- **Purpose**: Find the best days for outdoor activities
- **Features**:
  - Scores each day (0-100) for outdoor activities
  - Considers temperature, precipitation, and wind
  - Suggests specific activities based on conditions
- **Output**: Activity scores chart + ranked recommendations

### 3. **Smart Notification Bot** 💡
- **Purpose**: Generate weather alerts and notifications
- **Features**:
  - Heatwave and freezing alerts
  - Heavy rain and wind warnings
  - Severity-based alert system
- **Output**: Alert visualization + detailed alert messages

### 4. **Travel Companion App** 🎒
- **Purpose**: Generate packing lists based on destination weather
- **Features**:
  - Weather-based clothing recommendations
  - Accessories for different conditions
  - Essential gear suggestions
- **Output**: Packing list summary + detailed categories

### 5. **Weather Trends Visualizer** 📈
- **Purpose**: Create comprehensive trend visualizations
- **Features**:
  - Temperature trends (high/low)
  - Precipitation patterns
  - Wind speed analysis
  - Statistical summaries
- **Output**: Multiple trend charts + detailed statistics

### 6. **Global Weather Heatmap** 🌎
- **Purpose**: Worldwide weather overview
- **Features**:
  - Interactive world map
  - Temperature visualization for major cities
  - Color-coded temperature scale
- **Output**: Interactive global heatmap

## 📊 Individual Application Usage

### Run Individual Applications

```python
from weather_apps import WeatherApps

# Initialize the apps
apps = WeatherApps(api)

# Get forecast data
daily_forecast = api.get_daily_forecast(location_id, periods=7)

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

## 🎯 Customization Options

### Change Location
```python
# Search for a new location
locations = api.search_location("London", country="GB")
new_location_id = locations[0]['id']

# Run apps for new location
results = run_all_weather_apps(api, new_location_id, "London")
```

### Customize Trip Duration
```python
# For a 14-day trip
packing_fig, packing_list = apps.travel_companion_app(daily_forecast, trip_duration_days=14)
```

### Modify Alert Thresholds
You can modify the alert thresholds in the `notification_bot_app` method:
- Temperature alerts: >35°C (heatwave), <0°C (freezing)
- Precipitation alerts: >20mm (heavy rain), >10mm (rain)
- Wind alerts: >30 m/s (high wind)

## 📈 Understanding the Outputs

### Activity Scores (Event Planner)
- **80-100**: Perfect for outdoor activities
- **60-79**: Good for light outdoor activities
- **40-59**: Indoor activities recommended
- **0-39**: Stay indoors

### Outfit Recommendations
- **Temperature-based**: Heavy coat (<10°C), Light jacket (10-20°C), T-shirt (20-25°C), Tank top (>25°C)
- **Accessories**: Added based on rain, wind, and extreme temperatures

### Packing List Categories
- **Clothing**: Weather-appropriate clothes
- **Accessories**: Umbrellas, sunglasses, etc.
- **Gear**: Essential travel items

## 🔧 Advanced Features

### Access Raw Data
```python
# Get the forecast data used by all applications
forecast_data = results['forecast_data']
print(forecast_data)

# Access individual application results
outfit_recommendations = results['outfit_recs']
event_scores = results['event_recs']
weather_alerts = results['alerts']
packing_list = results['packing_list']
trend_statistics = results['trend_stats']
```

### Custom Visualizations
```python
# Create custom plots using the data
import plotly.express as px

# Custom temperature plot
fig = px.line(forecast_data, x='date', y=['maxTemp', 'minTemp'])
fig.show()

# Custom precipitation plot
fig = px.bar(forecast_data, x='date', y='precipAccum')
fig.show()
```

## 🚀 Next Steps & Enhancements

### Potential Improvements
1. **Real-time Notifications**: Integrate with Telegram/Slack/Email
2. **Machine Learning**: Improve predictions with historical data
3. **Web Application**: Deploy as a Streamlit or Flask app
4. **Mobile App**: Create a mobile-friendly interface
5. **More Weather Parameters**: Add humidity, UV index, air quality
6. **Historical Analysis**: Compare with past weather patterns

### Integration Ideas
- **Calendar Integration**: Sync with Google Calendar for event planning
- **E-commerce**: Link outfit recommendations to clothing stores
- **Travel Booking**: Integrate with travel booking platforms
- **Social Features**: Share weather insights with friends

## 🎉 Congratulations!

You now have 6 powerful weather applications that can:
- Help you decide what to wear each day
- Plan the best days for outdoor activities
- Get notified of extreme weather conditions
- Pack efficiently for your travels
- Analyze weather trends and patterns
- Explore global weather conditions

Happy weather coding! 🌤️