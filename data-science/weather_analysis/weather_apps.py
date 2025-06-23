"""
Weather Applications Collection
A comprehensive set of 6 weather-based applications using the Foreca API.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np


class WeatherApps:
    """Collection of weather-based applications using Foreca API data."""

    def __init__(self, api_client):
        """Initialize with a Foreca API client."""
        self.api = api_client

    def what_to_wear_app(self, forecast_data: pd.DataFrame) -> Tuple[go.Figure, pd.DataFrame]:
        """🔮 What Should I Wear Today? App - Suggests outfits based on weather."""
        recommendations = []

        for _, day in forecast_data.iterrows():
            temp = day['maxTemp']
            precip = day.get('precipAccum', 0)
            wind_speed = day.get('maxWindSpeed', 0)
            date = day['date'].strftime('%Y-%m-%d')

            # Base clothing recommendations
            if temp < 10:
                base_outfit = "Heavy coat, scarf, gloves, warm hat"
            elif temp < 20:
                base_outfit = "Light jacket or sweater"
            elif temp < 25:
                base_outfit = "T-shirt or light shirt"
            else:
                base_outfit = "Tank top or short sleeves"

            # Add accessories based on conditions
            accessories = []
            if precip > 5:
                accessories.append("🌂 Umbrella")
            if precip > 10:
                accessories.append("🥾 Waterproof shoes")
            if wind_speed > 20:
                accessories.append("🧥 Windbreaker")
            if temp > 30:
                accessories.append("🕶️ Sunglasses")
            if temp < 5:
                accessories.append("🧤 Winter gloves")

            # Combine recommendations
            full_outfit = f"{base_outfit}"
            if accessories:
                full_outfit += f" + {', '.join(accessories)}"

            recommendations.append({
                'date': date,
                'temperature': temp,
                'precipitation': precip,
                'outfit': full_outfit,
                'weather_summary': f"{temp}°C, {precip}mm rain"
            })

        rec_df = pd.DataFrame(recommendations)

        # Create interactive chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=rec_df['date'],
            y=rec_df['temperature'],
            mode='markers+text',
            text=rec_df['outfit'],
            textposition='top center',
            marker=dict(size=15, color='lightblue'),
            name='Temperature & Outfit'
        ))

        fig.update_layout(
            title='👕 What Should I Wear This Week?',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
            height=600,
            showlegend=False
        )

        return fig, rec_df

    def event_planner_app(self, forecast_data: pd.DataFrame) -> Tuple[go.Figure, pd.DataFrame]:
        """📍 Weather-Based Event Planner - Find best days for outdoor activities."""
        def calculate_day_score(day_data):
            """Calculate a score for outdoor activities (0-100)."""
            score = 50  # Base score

            # Temperature scoring (ideal: 15-25°C)
            temp = day_data['maxTemp']
            if 15 <= temp <= 25:
                score += 30
            elif 10 <= temp <= 30:
                score += 20
            elif 5 <= temp <= 35:
                score += 10

            # Precipitation penalty
            precip = day_data.get('precipAccum', 0)
            if precip == 0:
                score += 20
            elif precip < 5:
                score += 10
            elif precip > 10:
                score -= 20

            # Wind penalty
            wind = day_data.get('maxWindSpeed', 0)
            if wind < 15:
                score += 10
            elif wind > 25:
                score -= 15

            return max(0, min(100, score))

        recommendations = []

        for _, day in forecast_data.iterrows():
            score = calculate_day_score(day)
            date = day['date'].strftime('%Y-%m-%d')

            # Suggest activities based on score
            if score >= 80:
                activities = ["🏃‍♂️ Running", "🚴‍♂️ Cycling", "🏕️ Picnic", "🎾 Tennis"]
            elif score >= 60:
                activities = ["🚶‍♂️ Walking", "📸 Photography", "☕ Outdoor coffee"]
            elif score >= 40:
                activities = ["🏠 Indoor activities recommended"]
            else:
                activities = ["🏠 Stay indoors", "📚 Reading", "🎬 Movie day"]

            recommendations.append({
                'date': date,
                'score': score,
                'temperature': day['maxTemp'],
                'precipitation': day.get('precipAccum', 0),
                'activities': activities,
                'weather_summary': f"{day['maxTemp']}°C, {day.get('precipAccum', 0)}mm rain"
            })

        rec_df = pd.DataFrame(recommendations)

        # Create visualization
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=rec_df['date'],
            y=rec_df['score'],
            text=rec_df['score'].round(0),
            textposition='auto',
            marker_color='lightgreen',
            name='Activity Score'
        ))

        fig.update_layout(
            title='📅 Best Days for Outdoor Activities (Score: 0-100)',
            xaxis_title='Date',
            yaxis_title='Activity Score',
            height=500
        )

        return fig, rec_df

    def notification_bot_app(self, forecast_data: pd.DataFrame) -> Tuple[Optional[go.Figure], List[Dict]]:
        """💡 Smart Notification Bot - Generate weather alerts and notifications."""
        alerts = []

        for _, day in forecast_data.iterrows():
            date = day['date'].strftime('%Y-%m-%d')
            temp = day['maxTemp']
            precip = day.get('precipAccum', 0)
            wind = day.get('maxWindSpeed', 0)

            day_alerts = []

            # Temperature alerts
            if temp > 35:
                day_alerts.append("🔥 HEATWAVE ALERT: Stay hydrated, avoid outdoor activities")
            elif temp < 0:
                day_alerts.append("❄️ FREEZING ALERT: Bundle up, risk of frostbite")

            # Precipitation alerts
            if precip > 20:
                day_alerts.append("🌧️ HEAVY RAIN ALERT: Flooding possible, stay indoors")
            elif precip > 10:
                day_alerts.append("☔ RAIN ALERT: Bring umbrella, wet conditions")

            # Wind alerts
            if wind > 30:
                day_alerts.append("💨 HIGH WIND ALERT: Secure loose objects")

            if day_alerts:
                alerts.append({
                    'date': date,
                    'alerts': day_alerts,
                    'severity': len(day_alerts)
                })

        # Create alert visualization if there are alerts
        if alerts:
            alert_dates = [alert['date'] for alert in alerts]
            alert_severity = [alert['severity'] for alert in alerts]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=alert_dates,
                y=alert_severity,
                marker_color='red',
                name='Alert Severity'
            ))

            fig.update_layout(
                title='🚨 Weather Alerts This Week',
                xaxis_title='Date',
                yaxis_title='Number of Alerts',
                height=400
            )

            return fig, alerts
        else:
            return None, []

    def travel_companion_app(self, forecast_data: pd.DataFrame, trip_duration_days: int = 7) -> Tuple[go.Figure, Dict]:
        """🎒 Travel Companion App - Generate packing list based on destination weather."""
        packing_list = {
            'clothing': set(),
            'accessories': set(),
            'gear': set()
        }

        # Analyze weather patterns
        temps = forecast_data['maxTemp'].tolist()
        precip = forecast_data.get('precipAccum', [0] * len(forecast_data)).tolist()
        wind = forecast_data.get('maxWindSpeed', [0] * len(forecast_data)).tolist()

        min_temp = min(temps)
        max_temp = max(temps)
        total_precip = sum(precip)
        max_wind = max(wind)

        # Clothing recommendations
        if max_temp > 30:
            packing_list['clothing'].update(['T-shirts', 'Shorts', 'Light dresses', 'Swimwear'])
        elif max_temp > 20:
            packing_list['clothing'].update(['T-shirts', 'Light pants', 'Light sweater'])
        elif max_temp > 10:
            packing_list['clothing'].update(['Long-sleeve shirts', 'Jeans', 'Sweater', 'Light jacket'])
        else:
            packing_list['clothing'].update(['Heavy sweater', 'Warm pants', 'Winter coat', 'Thermal underwear'])

        if min_temp < 5:
            packing_list['clothing'].add('Winter hat')
            packing_list['clothing'].add('Gloves')
            packing_list['clothing'].add('Scarf')

        # Accessories
        if total_precip > 20:
            packing_list['accessories'].update(['Umbrella', 'Rain jacket', 'Waterproof shoes'])
        elif total_precip > 5:
            packing_list['accessories'].add('Light rain jacket')

        if max_temp > 25:
            packing_list['accessories'].update(['Sunglasses', 'Sunscreen', 'Hat'])

        if max_wind > 20:
            packing_list['accessories'].add('Windbreaker')

        # Gear
        packing_list['gear'].add('Phone charger')
        packing_list['gear'].add('Weather app')

        if trip_duration_days > 3:
            packing_list['gear'].add('Power bank')

        # Create visualization
        categories = list(packing_list.keys())
        item_counts = [len(items) for items in packing_list.values()]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=categories,
            y=item_counts,
            text=item_counts,
            textposition='auto',
            marker_color=['lightblue', 'lightgreen', 'lightcoral']
        ))

        fig.update_layout(
            title='🎒 Packing List Summary',
            xaxis_title='Category',
            yaxis_title='Number of Items',
            height=400
        )

        return fig, packing_list

    def trends_visualizer_app(self, forecast_data: pd.DataFrame) -> Tuple[List[go.Figure], Dict]:
        """📈 Weather Trends Visualizer - Create comprehensive trend visualizations."""
        figures = []

        # Temperature trend
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=forecast_data['date'],
            y=forecast_data['maxTemp'],
            mode='lines+markers',
            name='High Temp',
            line=dict(color='red', width=3)
        ))
        fig_temp.add_trace(go.Scatter(
            x=forecast_data['date'],
            y=forecast_data['minTemp'],
            mode='lines+markers',
            name='Low Temp',
            line=dict(color='blue', width=3),
            fill='tonexty'
        ))
        fig_temp.update_layout(
            title='🌡️ Temperature Trends',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
            height=400
        )
        figures.append(fig_temp)

        # Precipitation trend
        fig_precip = go.Figure()
        fig_precip.add_trace(go.Bar(
            x=forecast_data['date'],
            y=forecast_data.get('precipAccum', [0] * len(forecast_data)),
            name='Precipitation',
            marker_color='lightblue'
        ))
        fig_precip.update_layout(
            title='🌧️ Precipitation Trends',
            xaxis_title='Date',
            yaxis_title='Precipitation (mm)',
            height=400
        )
        figures.append(fig_precip)

        # Wind trend (if available)
        if 'maxWindSpeed' in forecast_data.columns:
            fig_wind = go.Figure()
            fig_wind.add_trace(go.Scatter(
                x=forecast_data['date'],
                y=forecast_data['maxWindSpeed'],
                mode='lines+markers',
                name='Wind Speed',
                line=dict(color='gray', width=2)
            ))
            fig_wind.update_layout(
                title='💨 Wind Speed Trends',
                xaxis_title='Date',
                yaxis_title='Wind Speed (m/s)',
                height=400
            )
            figures.append(fig_wind)

        # Calculate statistics
        stats = {
            'temperature': {
                'avg_high': forecast_data['maxTemp'].mean(),
                'avg_low': forecast_data['minTemp'].mean(),
                'temp_range': forecast_data['maxTemp'].max() - forecast_data['minTemp'].min(),
                'hottest_day': forecast_data.loc[forecast_data['maxTemp'].idxmax(), 'date'].strftime('%Y-%m-%d'),
                'coldest_day': forecast_data.loc[forecast_data['minTemp'].idxmin(), 'date'].strftime('%Y-%m-%d')
            }
        }

        if 'precipAccum' in forecast_data.columns:
            stats['precipitation'] = {
                'total_precip': forecast_data['precipAccum'].sum(),
                'rainy_days': (forecast_data['precipAccum'] > 0).sum(),
                'heaviest_rain': forecast_data['precipAccum'].max()
            }

        return figures, stats

    def global_heatmap_app(self) -> go.Figure:
        """🌎 Global Weather Heatmap - Create a simulated global weather visualization."""
        # Sample cities with their coordinates
        cities = [
            {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060, 'temp': 22},
            {'name': 'London', 'lat': 51.5074, 'lon': -0.1278, 'temp': 18},
            {'name': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503, 'temp': 25},
            {'name': 'Sydney', 'lat': -33.8688, 'lon': 151.2093, 'temp': 20},
            {'name': 'Dubai', 'lat': 25.2048, 'lon': 55.2708, 'temp': 35},
            {'name': 'Moscow', 'lat': 55.7558, 'lon': 37.6176, 'temp': 12},
            {'name': 'Rio de Janeiro', 'lat': -22.9068, 'lon': -43.1729, 'temp': 28},
            {'name': 'Cape Town', 'lat': -33.9249, 'lon': 18.4241, 'temp': 16}
        ]

        cities_df = pd.DataFrame(cities)

        fig = go.Figure()
        fig.add_trace(go.Scattergeo(
            lon=cities_df['lon'],
            lat=cities_df['lat'],
            text=cities_df['name'] + '<br>' + cities_df['temp'].astype(str) + '°C',
            mode='markers',
            marker=dict(
                size=15,
                color=cities_df['temp'],
                colorscale='RdYlBu_r',
                showscale=True,
                colorbar=dict(title="Temperature (°C)")
            ),
            name='Global Weather'
        ))

        fig.update_layout(
            title='🌎 Global Weather Heatmap',
            geo=dict(
                scope='world',
                projection_type='equirectangular',
                showland=True,
                landcolor='lightgray',
                showocean=True,
                oceancolor='lightblue'
            ),
            height=600
        )

        return fig


def run_all_weather_apps(api_client, location_id: int, city_name: str = "Your City"):
    """
    Run all 6 weather applications for a given location.

    Args:
        api_client: ForecaWeatherAPI instance
        location_id: Foreca location ID
        city_name: Name of the city for display

    Returns:
        Dictionary containing all application results
    """
    print(f"🌤️ Running all weather applications for {city_name}...")

    apps = WeatherApps(api_client)

    # Get forecast data
    daily_forecast = api_client.get_daily_forecast(location_id, periods=7)

    if daily_forecast.empty:
        print("❌ No forecast data available!")
        return {}

    results = {
        'forecast_data': daily_forecast,
        'city_name': city_name
    }

    # Run each application
    print("🔮 1. What Should I Wear Today? App")
    results['outfit_fig'], results['outfit_recs'] = apps.what_to_wear_app(daily_forecast)

    print("📍 2. Weather-Based Event Planner")
    results['event_fig'], results['event_recs'] = apps.event_planner_app(daily_forecast)

    print("💡 3. Smart Notification Bot")
    results['alert_fig'], results['alerts'] = apps.notification_bot_app(daily_forecast)

    print("🎒 4. Travel Companion App")
    results['packing_fig'], results['packing_list'] = apps.travel_companion_app(daily_forecast)

    print("📈 5. Weather Trends Visualizer")
    results['trend_figs'], results['trend_stats'] = apps.trends_visualizer_app(daily_forecast)

    print("🌎 6. Global Weather Heatmap")
    results['global_fig'] = apps.global_heatmap_app()

    print("✅ All applications completed successfully!")
    return results


def display_results(results: Dict):
    """Display all application results in a formatted way."""
    city_name = results.get('city_name', 'Unknown City')

    print(f"\n{'='*60}")
    print(f"🌟 WEATHER APPLICATIONS RESULTS FOR {city_name.upper()}")
    print(f"{'='*60}")

    # 1. Outfit Recommendations
    print("\n🔮 1. WHAT SHOULD I WEAR TODAY?")
    print("-" * 40)
    outfit_recs = results.get('outfit_recs', pd.DataFrame())
    if not outfit_recs.empty:
        for _, rec in outfit_recs.iterrows():
            print(f"📅 {rec['date']}: {rec['weather_summary']}")
            print(f"   👔 {rec['outfit']}")
            print()

    # 2. Event Planning
    print("📍 2. EVENT PLANNING RECOMMENDATIONS")
    print("-" * 40)
    event_recs = results.get('event_recs', pd.DataFrame())
    if not event_recs.empty:
        sorted_events = event_recs.sort_values('score', ascending=False)
        for i, (_, event) in enumerate(sorted_events.iterrows(), 1):
            print(f"{i}. 📅 {event['date']} (Score: {event['score']:.0f})")
            print(f"   🌤️ {event['weather_summary']}")
            print(f"   🎯 Activities: {', '.join(event['activities'])}")
            print()

    # 3. Weather Alerts
    print("💡 3. WEATHER ALERTS")
    print("-" * 40)
    alerts = results.get('alerts', [])
    if alerts:
        for alert in alerts:
            print(f"📅 {alert['date']}:")
            for alert_msg in alert['alerts']:
                print(f"   {alert_msg}")
            print()
    else:
        print("✅ No weather alerts for this week!")

    # 4. Packing List
    print("🎒 4. TRAVEL PACKING LIST")
    print("-" * 40)
    packing_list = results.get('packing_list', {})
    for category, items in packing_list.items():
        print(f"\n{category.upper()}:")
        for item in sorted(items):
            print(f"   ✅ {item}")

    # 5. Weather Trends
    print("\n📈 5. WEATHER TRENDS ANALYSIS")
    print("-" * 40)
    trend_stats = results.get('trend_stats', {})

    if 'temperature' in trend_stats:
        temp_stats = trend_stats['temperature']
        print(f"🌡️ Temperature Analysis:")
        print(f"   Average High: {temp_stats['avg_high']:.1f}°C")
        print(f"   Average Low: {temp_stats['avg_low']:.1f}°C")
        print(f"   Temperature Range: {temp_stats['temp_range']:.1f}°C")
        print(f"   Hottest Day: {temp_stats['hottest_day']}")
        print(f"   Coldest Day: {temp_stats['coldest_day']}")

    if 'precipitation' in trend_stats:
        precip_stats = trend_stats['precipitation']
        print(f"\n🌧️ Precipitation Analysis:")
        print(f"   Total Precipitation: {precip_stats['total_precip']:.1f}mm")
        print(f"   Rainy Days: {precip_stats['rainy_days']}")
        print(f"   Heaviest Rain: {precip_stats['heaviest_rain']:.1f}mm")

    print(f"\n{'='*60}")
    print("🎉 ALL APPLICATIONS COMPLETED SUCCESSFULLY!")
    print(f"{'='*60}")


def show_all_plots(results: Dict):
    """Display all interactive plots from the applications."""
    print("\n📊 DISPLAYING ALL VISUALIZATIONS:")
    print("=" * 50)

    # Outfit recommendations
    if 'outfit_fig' in results:
        print("🔮 Outfit Recommendations Chart:")
        results['outfit_fig'].show()

    # Event planning
    if 'event_fig' in results:
        print("📍 Event Planning Chart:")
        results['event_fig'].show()

    # Weather alerts
    if 'alert_fig' in results:
        print("💡 Weather Alerts Chart:")
        results['alert_fig'].show()

    # Packing list
    if 'packing_fig' in results:
        print("🎒 Packing List Chart:")
        results['packing_fig'].show()

    # Trend visualizations
    if 'trend_figs' in results:
        print("📈 Weather Trends Charts:")
        for i, fig in enumerate(results['trend_figs'], 1):
            print(f"   Chart {i}:")
            fig.show()

    # Global heatmap
    if 'global_fig' in results:
        print("🌎 Global Weather Heatmap:")
        results['global_fig'].show()