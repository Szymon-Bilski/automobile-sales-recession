#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv')

app = dash.Dash(__name__)

dropdown_options = [
    {'label': '...........', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': '.........'}
]
year_list = [i for i in range(1980, 2024, 1)]

app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style = {'textAlign':'center', 'color':'#503D36', 'font-size':24}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options= [
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                           ],
            placeholder='Select a report type',
            value = 'Recession Period Statistics'
        )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='Select-year',
            placeholder = 'Select-year',
        )),
    html.Div([
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flexDirection': 'column'}),])
])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')])


def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        

    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        yearly_rec = (
            recession_data.groupby('Year')['Automobile_Sales']
            .mean()
            .reset_index()
        )
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales During Recession Years'
            )
        )

        average_sales = (
            data.groupby(['Vehicle_Type', 'Recession'])['Automobile_Sales']
            .mean()
            .reset_index()
        )

        average_sales['Period'] = average_sales['Recession'].map({
            0: 'Outside recessions',
            1: 'During recessions'
        })

        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                color='Period',
                barmode='group',
                category_orders={'Period': ['Outside recessions', 'During recessions']},
                labels={
                    'Vehicle_Type': 'Vehicle type',
                    'Automobile_Sales': 'Average sales per record'
                },
                title='Average Sales by Vehicle Type and Period'
            )
        )

        exp_rec = (
            recession_data.groupby('Vehicle_Type')['Advertising_Expenditure']
            .sum()
            .reset_index()
        )
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Advertising Expenditure Share by Vehicle Type'
            )
        )

        unemp_data = (
            recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales']
            .mean()
            .reset_index()
        )
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                barmode='group',
                labels={
                    'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales',
                    'Vehicle_Type': 'Vehicle Type'
                },
                title='Average Sales by Unemployment Rate and Vehicle Type'
            )
        )

        return [
            html.Div(
                className='chart-item',
                children=[html.Div(R_chart1), html.Div(R_chart2)],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[html.Div(R_chart3), html.Div(R_chart4)],
                style={'display': 'flex'}
            )
        ]

                            
    elif selected_statistics == 'Yearly Statistics' and input_year in year_list:
        yearly_data = data[data['Year'] == input_year]

        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales by Year'
            )
        )

        month_order = [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ]
        mas = (
            yearly_data.groupby('Month')['Automobile_Sales']
            .sum()
            .reindex(month_order)
            .reset_index()
        )
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales'
            )
        )

        avr_vdata = (
            yearly_data.groupby('Vehicle_Type')['Automobile_Sales']
            .mean()
            .reset_index()
        )
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title=f'Average Vehicles Sold by Vehicle Type in {input_year}'
            )
        )

        exp_data = (
            yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure']
            .sum()
            .reset_index()
        )
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                names='Vehicle_Type',
                values='Advertising_Expenditure',
                title=f'Advertising Expenditure by Vehicle Type in {input_year}'
            )
        )

        return [
            html.Div(
                className='chart-item',
                children=[html.Div(Y_chart1), html.Div(Y_chart2)],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[html.Div(Y_chart3), html.Div(Y_chart4)],
                style={'display': 'flex'}
            )
        ]

    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)

