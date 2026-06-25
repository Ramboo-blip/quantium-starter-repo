import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load and prepare data
df = pd.read_csv('output.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')
df['sales'] = df['sales'].str.replace('$', '').astype(float)

# Build the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'backgroundColor': '#0D1B2A',
        'minHeight': '100vh',
        'padding': '40px 60px',
        'fontFamily': '"Segoe UI", Helvetica, Arial, sans-serif'
    },
    children=[

        # Top bar accent
        html.Div(style={
            'height': '5px',
            'backgroundColor': '#1E90FF',
            'borderRadius': '3px',
            'marginBottom': '30px'
        }),

        # Header
        html.H1(
            'Pink Morsel Sales Dashboard',
            style={
                'textAlign': 'center',
                'color': '#FFFFFF',
                'fontSize': '2.2rem',
                'fontWeight': '700',
                'letterSpacing': '1.5px',
                'marginBottom': '6px',
                'textTransform': 'uppercase'
            }
        ),

        html.P(
            'Soul Foods Pvt Ltd | Regional Sales Analysis | Price Increase: January 15, 2021',
            style={
                'textAlign': 'center',
                'color': '#7F8C9A',
                'fontSize': '0.9rem',
                'marginBottom': '35px',
                'letterSpacing': '0.5px'
            }
        ),

        # Divider
        html.Hr(style={'borderColor': '#1E3A5F', 'marginBottom': '30px'}),

        # Region Filter Section
        html.Div(
            style={
                'backgroundColor': '#132338',
                'borderRadius': '10px',
                'padding': '20px 30px',
                'marginBottom': '30px',
                'border': '1px solid #1E3A5F'
            },
            children=[
                html.Label(
                    'FILTER BY REGION',
                    style={
                        'color': '#1E90FF',
                        'fontWeight': '700',
                        'fontSize': '0.8rem',
                        'letterSpacing': '2px',
                        'display': 'block',
                        'marginBottom': '15px'
                    }
                ),
                dcc.RadioItems(
                    id='region-filter',
                    options=[
                        {'label': 'All Regions', 'value': 'all'},
                        {'label': 'North',       'value': 'north'},
                        {'label': 'South',       'value': 'south'},
                        {'label': 'East',        'value': 'east'},
                        {'label': 'West',        'value': 'west'},
                    ],
                    value='all',
                    inline=True,
                    inputStyle={
                        'marginRight': '6px',
                        'accentColor': '#1E90FF',
                        'width': '16px',
                        'height': '16px'
                    },
                    labelStyle={
                        'marginRight': '25px',
                        'fontSize': '0.95rem',
                        'color': '#D0D8E4',
                        'fontWeight': '600',
                        'cursor': 'pointer',
                        'letterSpacing': '0.3px'
                    }
                )
            ]
        ),

        # Chart Container
        html.Div(
            style={
                'backgroundColor': '#132338',
                'borderRadius': '10px',
                'padding': '25px',
                'border': '1px solid #1E3A5F',
                'boxShadow': '0 4px 24px rgba(0, 0, 0, 0.4)'
            },
            children=[
                dcc.Graph(id='sales-chart')
            ]
        ),

        # Footer
        html.P(
            'Soul Foods Pvt Ltd — Confidential & Internal Use Only',
            style={
                'textAlign': 'center',
                'color': '#3A4A5A',
                'fontSize': '0.75rem',
                'marginTop': '30px',
                'letterSpacing': '0.5px'
            }
        )
    ]
)


@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(region):
    if region == 'all':
        filtered = df.groupby('date')['sales'].sum().reset_index()
    else:
        filtered = df[df['region'] == region].groupby('date')['sales'].sum().reset_index()

    fig = px.line(
        filtered,
        x='date',
        y='sales',
        labels={'date': 'Date', 'sales': 'Total Sales ($)'},
        color_discrete_sequence=['#1E90FF']
    )

    fig.add_vline(
        x='2021-01-15',
        line_dash='dash',
        line_color='#FF4C4C',
        annotation_text='Price Increase — Jan 15, 2021',
        annotation_position='top left',
        annotation_font_color='#FF4C4C',
        annotation_font_size=12
    )

    fig.update_layout(
        plot_bgcolor='#132338',
        paper_bgcolor='#132338',
        font_color='#D0D8E4',
        font_family='"Segoe UI", Helvetica, Arial, sans-serif',
        xaxis=dict(
            showgrid=False,
            title='Date',
            title_font=dict(size=12, color='#7F8C9A'),
            tickfont=dict(color='#7F8C9A')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#1E3A5F',
            title='Total Sales ($)',
            title_font=dict(size=12, color='#7F8C9A'),
            tickfont=dict(color='#7F8C9A')
        ),
        hovermode='x unified',
        margin=dict(l=40, r=40, t=20, b=40)
    )

    fig.update_traces(line_width=2.5)

    return fig


if __name__ == '__main__':
    app.run(debug=True)