import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from django.shortcuts import render

def dashboard_view(request):
    # Load the dataset (update the path to your dataset file)
    data = pd.read_csv('./data/dataset_traffic_accident_prediction1.csv')
    data = data.dropna()  # Drop rows with missing data

    # Handle filters from the request
    filter_params = {}
    if 'weather' in request.GET and request.GET['weather']:
        filter_params['Weather'] = request.GET['weather']
    if 'road_type' in request.GET and request.GET['road_type']:
        filter_params['Road_Type'] = request.GET['road_type']
    if 'time_of_day' in request.GET and request.GET['time_of_day']:
        filter_params['Time_of_Day'] = request.GET['time_of_day']

    # Apply filters if any
    filtered_data = data
    for key, value in filter_params.items():
        filtered_data = filtered_data[filtered_data[key] == value]

    # Define the static folder path
    static_folder = os.path.join('static', 'charts')
    os.makedirs(static_folder, exist_ok=True)  # Ensure the folder exists

    # 1. Pie Chart: Distribution of Weather Conditions
    weather_counts = filtered_data['Weather'].value_counts()
    plt.figure(figsize=(8, 8))
    weather_counts.plot.pie(autopct='%1.1f%%', title="Weather Conditions Distribution")
    plt.ylabel('')  # Hide the y-axis label
    pie_chart_path = os.path.join(static_folder, 'weather_conditions_pie_chart.png')
    plt.savefig(pie_chart_path)
    plt.close()

    # 2. Bar Chart: Accidents by Road Type
    road_type_counts = filtered_data['Road_Type'].value_counts()
    plt.figure(figsize=(10, 6))
    road_type_counts.plot(kind='bar', color='skyblue', title="Accidents by Road Type")
    plt.xlabel('Road Type')
    plt.ylabel('Count of Accidents')
    bar_chart_path = os.path.join(static_folder, 'accidents_by_road_type_bar_chart.png')
    plt.savefig(bar_chart_path)
    plt.close()

    # 3. Histogram: Driver Age Distribution
    filtered_data['Driver_Age'] = pd.to_numeric(filtered_data['Driver_Age'], errors='coerce')
    filtered_data = filtered_data.dropna(subset=['Driver_Age'])
    plt.figure(figsize=(8, 6))
    filtered_data['Driver_Age'].plot(kind='hist', bins=15, color='orange', title="Driver Age Distribution")
    plt.xlabel('Driver Age')
    plt.ylabel('Frequency')
    histogram_path = os.path.join(static_folder, 'driver_age_histogram.png')
    plt.savefig(histogram_path)
    plt.close()

    # 4. Line Chart: Speed Limit Trends for Accidents
    filtered_data['Speed_Limit'] = pd.to_numeric(filtered_data['Speed_Limit'], errors='coerce')
    speed_accidents = filtered_data.groupby('Speed_Limit')['Accident'].count()
    plt.figure(figsize=(10, 6))
    speed_accidents.plot(kind='line', marker='o', color='green', title="Accidents vs. Speed Limit")
    plt.xlabel('Speed Limit')
    plt.ylabel('Number of Accidents')
    line_chart_path = os.path.join(static_folder, 'speed_limit_line_chart.png')
    plt.savefig(line_chart_path)
    plt.close()

    # 5. Count Plot: Accidents by Time of Day
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Time_of_Day', data=filtered_data, palette='viridis')
    plt.title("Accidents by Time of Day")
    plt.xlabel('Time of Day')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    count_plot_path = os.path.join(static_folder, 'accidents_by_time_count_plot.png')
    plt.savefig(count_plot_path)
    plt.close()

    # 6. Heatmap: Correlation Between Numerical Variables
    numeric_data = filtered_data.select_dtypes(include=['float64', 'int64'])
    plt.figure(figsize=(10, 8))
    sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Between Variables")
    heatmap_path = os.path.join(static_folder, 'correlation_heatmap.png')
    plt.savefig(heatmap_path)
    plt.close()

    # Prepare graph paths for rendering
    graph_paths = {
        'pie_chart': pie_chart_path,
        'bar_chart': bar_chart_path,
        'histogram': histogram_path,
        'line_chart': line_chart_path,
        'count_plot': count_plot_path,
        'heatmap': heatmap_path
    }

    # Render the template with the charts and filter values
    return render(request, 'dashboard.html', {
        'graphs': graph_paths,
        'filters': filter_params,
    })
