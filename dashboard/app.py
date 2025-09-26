from dash import Dash, dcc, html, Output, Input, callback_context
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from pipeline.db import run_query_file

# Initialize app with dark theme
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "NYC Taxi Analytics | DJM Tech"

# Custom color palette matching professional branding
COLORS = {
    'primary': '#1f77b4',      # Professional blue
    'secondary': '#ff7f0e',    # Orange accent
    'success': '#2ca02c',      # Green
    'warning': '#d62728',      # Red
    'info': '#9467bd',         # Purple
    'light': '#bcbd22',        # Yellow-green
    'dark': '#17becf',         # Cyan
    'background': '#1e1e1e',   # Dark background
    'surface': '#2d2d2d',      # Card background
    'text': '#ffffff',         # White text
    'text_secondary': '#b0b0b0' # Gray text
}

# Define tabs and their queries
TABS = {
    "📍 Top Pickups": "queries/pickups.sql",
    "💰 Tip Analysis": "queries/tips.sql", 
    "🔄 Popular Routes": "queries/pairs.sql",
    "✈️ Airport Traffic": "queries/airports.sql",
    "⏱️ Travel Duration": "queries/durations.sql"
}

def create_professional_chart(df, chart_type, title, x_col, y_col, color_col=None, x_label=None, y_label=None, hover_template=None):
    """Create professionally styled charts with consistent branding and clear labels"""
    
    # Base layout template
    layout_template = {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': COLORS['text'], 'family': 'Inter, sans-serif'},
        'title': {
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': COLORS['text']}
        },
        'xaxis': {
            'gridcolor': '#404040',
            'color': COLORS['text_secondary'],
            'title_font': {'color': COLORS['text'], 'size': 14},
            'tickfont': {'color': COLORS['text_secondary'], 'size': 12},
            'title': x_label or x_col.replace('_', ' ').title()
        },
        'yaxis': {
            'gridcolor': '#404040', 
            'color': COLORS['text_secondary'],
            'title_font': {'color': COLORS['text'], 'size': 14},
            'tickfont': {'color': COLORS['text_secondary'], 'size': 12},
            'title': y_label or y_col.replace('_', ' ').title()
        },
        'margin': {'l': 80, 'r': 60, 't': 80, 'b': 80},
        'hovermode': 'closest'
    }
    
    if chart_type == 'bar':
        fig = px.bar(
            df.head(15),  # Limit to top 15 for readability
            x=x_col, 
            y=y_col,
            color=y_col if not color_col else color_col,
            color_continuous_scale='viridis',
            template='plotly_dark',
            hover_data=df.columns.tolist()
        )
        # Format y-axis for better readability
        if 'pickups' in y_col or 'trips' in y_col or 'trip_count' in y_col:
            fig.update_layout(yaxis_tickformat=',')
        elif 'tip' in y_col:
            fig.update_layout(yaxis_tickformat='$.2f')
            
    elif chart_type == 'scatter':
        fig = px.scatter(
            df.head(20),  # Limit for performance
            x=x_col,
            y=y_col,
            size='trip_count' if 'trip_count' in df.columns else None,
            color=color_col if color_col else COLORS['primary'],
            template='plotly_dark',
            hover_data=df.columns.tolist(),
            size_max=30
        )
        # Format axes for duration scatter plot
        if 'duration' in y_col:
            fig.update_layout(
                yaxis_tickformat='.1f',
                yaxis_title=f"{y_label or y_col.replace('_', ' ').title()} (minutes)"
            )
        if 'trip_count' in df.columns:
            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                              f"{y_label or y_col.replace('_', ' ').title()}: %{{y:.1f}} min<br>" +
                              "Trip Count: %{marker.size}<br>" +
                              "<extra></extra>"
            )
    else:
        fig = px.line(df, x=x_col, y=y_col, template='plotly_dark')
    
    fig.update_layout(**layout_template)
    
    # Add custom hover templates for better data clarity
    if hover_template:
        fig.update_traces(hovertemplate=hover_template)
    
    return fig

def load_figure(tab_name):
    try:
        query_path = TABS[tab_name]
        df = run_query_file(query_path)
        
        if df is None or df.empty:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color=COLORS['text_secondary'])
            )

        if "pickups" in query_path:
            return create_professional_chart(
                df, 'bar', 'Top Pickup Zones by Volume', 
                'pickup_zone', 'pickups',
                x_label='Pickup Zone',
                y_label='Number of Pickups',
                hover_template="<b>%{x}</b><br>Pickups: %{y:,}<br><extra></extra>"
            )
        elif "tips" in query_path:
            return create_professional_chart(
                df, 'bar', 'Average Tip Amount by Pickup Zone',
                'pickup_zone', 'avg_tip',
                x_label='Pickup Zone',
                y_label='Average Tip Amount ($)',
                hover_template="<b>%{x}</b><br>Avg Tip: $%{y:.2f}<br>Trips: %{customdata[2]:,}<br><extra></extra>"
            )
        elif "pairs" in query_path:
            fig = create_professional_chart(
                df, 'bar', 'Most Popular Pickup-Dropoff Routes',
                'pickup_zone', 'trip_count', 'dropoff_zone',
                x_label='Pickup Zone',
                y_label='Number of Trips'
            )
            # Fix hover template to show actual dropoff zone names
            # When using color='dropoff_zone', the dropoff zone is in customdata[0]
            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Dropoff: %{customdata[0]}<br>Trips: %{y:,}<br><extra></extra>"
            )
            return fig
        elif "airports" in query_path:
            return create_professional_chart(
                df, 'bar', 'Airport Traffic Volume',
                'airport_zone', 'trips',
                x_label='Airport Zone',
                y_label='Number of Trips',
                hover_template="<b>%{x}</b><br>Trips: %{y:,}<br><extra></extra>"
            )
        elif "durations" in query_path:
            fig = create_professional_chart(
                df, 'scatter', 'Average Travel Duration by Route',
                'pickup_zone', 'avg_duration', 'dropoff_zone',
                x_label='Pickup Zone',
                y_label='Average Duration (Minutes)'
            )
            # Add custom hover template for duration chart
            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Dropoff: %{customdata[1]}<br>Avg Duration: %{y:.1f} min<br>Trip Count: %{marker.size}<br><extra></extra>"
            )
            return fig
        else:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color=COLORS['text_secondary'])
            )
    except Exception as e:
        print(f"Error loading figure for {tab_name}: {e}")
        return go.Figure().add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['warning'])
        )

# Professional header component
header = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("NYC Taxi Analytics", className="mb-0"),
                html.P("Real-time insights powered by DuckDB", className="mb-0 text-muted")
            ], width=8),
            dbc.Col([
                html.A(
                    dbc.Button("Visit DJM Tech", color="primary", outline=True, size="sm"),
                    href="https://www.djm-tech.dev",
                    target="_blank"
                )
            ], width=4, className="text-end")
        ], className="w-100")
    ], fluid=True),
    color="dark",
    dark=True,
    className="mb-4"
)

# Professional footer
footer = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Hr(className="my-4"),
            html.P([
                "Built with ",
                html.Span("❤️", style={'color': COLORS['warning']}),
                " using DuckDB, Plotly Dash, and Python | ",
                html.A("DJM Tech", href="https://www.djm-tech.dev", target="_blank", 
                      style={'color': COLORS['primary']})
            ], className="text-center text-muted mb-0")
        ])
    ])
], fluid=True)

# Main app layout with professional styling
app.layout = dbc.Container([
    header,
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Analytics Dashboard", className="card-title mb-3"),
                    html.P("Explore NYC taxi data insights across different dimensions", 
                          className="card-text text-muted mb-4"),
                    
                    dcc.Tabs(
                        id="tabs",
                        value=list(TABS.keys())[0],
                        children=[
                            dcc.Tab(
                                label=label, 
                                value=label,
                                className="custom-tab",
                                selected_className="custom-tab-selected"
                            ) for label in TABS.keys()
                        ],
                        className="mb-4"
                    ),
                    
                    dcc.Loading(
                        dcc.Graph(
                            id="tab-content",
                            style={'height': '600px'},
                            config={'displayModeBar': True, 'displaylogo': False}
                        ),
                        type="circle",
                        color=COLORS['primary']
                    )
                ])
            ], className="shadow-lg")
        ], width=12)
    ]),
    
    footer
    
], fluid=True, className="py-4")

# Custom CSS for enhanced styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background-color: #1e1e1e;
            }
            .custom-tab {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                color: #b0b0b0;
                margin-right: 5px;
                border-radius: 8px 8px 0 0;
                padding: 12px 20px;
                font-weight: 500;
            }
            .custom-tab-selected {
                background-color: #1f77b4;
                color: white;
                border-color: #1f77b4;
            }
            .custom-tab:hover {
                background-color: #404040;
                color: black;
            }
            .card {
                background-color: #2d2d2d;
                border: 1px solid #404040;
            }
            .card-title {
                color: #ffffff;
                font-weight: 600;
            }
            .navbar-brand {
                font-weight: 700;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Callback to switch graphs
@app.callback(
    Output("tab-content", "figure"),
    Input("tabs", "value")
)
def update_tab(tab_name):
    return load_figure(tab_name)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)

