from flask import Flask, render_template
import json

class Charts:
    def createDateChart(self):
        data = self

        # Convert the data to Highcharts format
        chart_data = {'x': [], 'y': []}
        for d in data:
            chart_data['x'].append(d['date'])
            chart_data['y'].append(d['publications'])

        # Convert the chart data to a JSON string
        chart_data_json = json.dumps(chart_data)

        # Render the template with the chart data
        return chart_data_json
    def createPubnameChart(self):
        data = self

        # Convert the data to Highcharts format
        chart_data = {'x': [], 'y': []}
        for d in data:
            chart_data['x'].append(d['Citation'])
            chart_data['y'].append(d['publications'])

        # Convert the chart data to a JSON string
        chart_data_json = json.dumps(chart_data)

        # Render the template with the chart data
        return chart_data_json

