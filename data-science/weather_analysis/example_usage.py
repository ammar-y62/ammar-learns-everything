"""
Example Usage of Weather Applications
This script shows how to use the weather applications in your Jupyter notebook.
"""

# Example usage for your Jupyter notebook:

"""
# Step 1: Import the weather applications
from weather_apps import run_all_weather_apps, display_results, show_all_plots

# Step 2: Run all applications for your location
# Replace with your actual location_id and city name
location_id = 100109223  # Your location ID from the notebook
city_name = "Madina"     # Your city name

# Run all 6 weather applications
results = run_all_weather_apps(api, location_id, city_name)

# Step 3: Display the results
display_results(results)

# Step 4: Show all interactive plots
show_all_plots(results)

# Step 5: Access individual results
if results:
    print(f"📊 Weather forecast for {results['city_name']}:")
    print(results['forecast_data'])

    print(f"\n👕 Outfit recommendations:")
    print(results['outfit_recs'])

    print(f"\n📅 Event planning scores:")
    print(results['event_recs'])

    print(f"\n🎒 Packing list:")
    for category, items in results['packing_list'].items():
        print(f"{category}: {', '.join(sorted(items))}")
"""

# Individual application examples:

"""
# 🔮 1. What Should I Wear Today? App
from weather_apps import WeatherApps

apps = WeatherApps(api)
daily_forecast = api.get_daily_forecast(location_id, periods=7)
outfit_fig, outfit_recs = apps.what_to_wear_app(daily_forecast)

print("👕 Outfit Recommendations:")
print(outfit_recs)
outfit_fig.show()

# 📍 2. Weather-Based Event Planner
event_fig, event_recs = apps.event_planner_app(daily_forecast)

print("📅 Event Planning Recommendations:")
print(event_recs.sort_values('score', ascending=False))
event_fig.show()

# 💡 3. Smart Notification Bot
alert_fig, alerts = apps.notification_bot_app(daily_forecast)

if alerts:
    print("🚨 Weather Alerts:")
    for alert in alerts:
        print(f"📅 {alert['date']}: {alert['alerts']}")
    alert_fig.show()
else:
    print("✅ No weather alerts!")

# 🎒 4. Travel Companion App
packing_fig, packing_list = apps.travel_companion_app(daily_forecast)

print("🎒 Packing List:")
for category, items in packing_list.items():
    print(f"{category.upper()}: {', '.join(sorted(items))}")
packing_fig.show()

# 📈 5. Weather Trends Visualizer
trend_figs, trend_stats = apps.trends_visualizer_app(daily_forecast)

print("📈 Weather Trends Analysis:")
print(f"Temperature stats: {trend_stats['temperature']}")
if 'precipitation' in trend_stats:
    print(f"Precipitation stats: {trend_stats['precipitation']}")

for fig in trend_figs:
    fig.show()

# 🌎 6. Global Weather Heatmap
global_fig = apps.global_heatmap_app()
global_fig.show()
"""

# Quick start function:
def quick_start_example():
    """
    Quick start example - copy this into your notebook!
    """
    print("""
# 🌟 QUICK START - Copy this into your notebook!

# Import the weather applications
from weather_apps import run_all_weather_apps, display_results, show_all_plots

# Set your location (replace with your actual values)
location_id = 100109223  # Your location ID
city_name = "Madina"     # Your city name

# Run all 6 weather applications at once!
results = run_all_weather_apps(api, location_id, city_name)

# Display all results and plots
if results:
    display_results(results)
    show_all_plots(results)
else:
    print("❌ No results - check your location_id and API connection!")

# That's it! You now have 6 amazing weather applications running! 🎉
    """)

if __name__ == "__main__":
    quick_start_example()