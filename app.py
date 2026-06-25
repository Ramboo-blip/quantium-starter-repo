import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load the processed data
df = pd.read_csv('output.csv')

# Convert date column to datetime and sort
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Group by date and sum sales (remove $ and convert to float first)
df['sales'] = df['sales'].str.replace('$', '').astype(float)
daily_sales = df.groupby('date')['sales'].sum().reset_index()

# Create the line chart
fig = px.line(
    daily_sales,
    x='date',
    y='sales',
    title='Pink Morsel Sales Over Time',
    labels={'date': 'Date', 'sales': 'Total Sales ($)'}
)

# Add vertical line for price increase on 15 Jan 2021
fig.add_vline(
    x='2021-01-15',
    line_dash='dash',
    line_color='red',
    annotation_text='Price Increase',
    annotation_position='top left'
)

# Build the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
        'Pink Morsel Sales Visualiser',
        style={'textAlign': 'center', 'fontFamily': 'Arial'}
    ),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)