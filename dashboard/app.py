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

def create_professional_chart(df, chart_type, title, x_col, y_col, color_col=None):
    """Create professionally styled charts with consistent branding"""
    
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
            'title_font': {'color': COLORS['text']}
        },
        'yaxis': {
            'gridcolor': '#404040', 
            'color': COLORS['text_secondary'],
            'title_font': {'color': COLORS['text']}
        },
        'margin': {'l': 60, 'r': 60, 't': 80, 'b': 60}
    }
    
    if chart_type == 'bar':
        fig = px.bar(
            df.head(15),  # Limit to top 15 for readability
            x=x_col, 
            y=y_col,
            color=y_col if not color_col else color_col,
            color_continuous_scale='viridis',
            template='plotly_dark'
        )
    elif chart_type == 'scatter':
        fig = px.scatter(
            df.head(20),  # Limit for performance
            x=x_col,
            y=y_col,
            size=y_col if 'trip_count' in df.columns else None,
            color=color_col if color_col else COLORS['primary'],
            template='plotly_dark',
            hover_data=df.columns.tolist()
        )
    else:
        fig = px.line(df, x=x_col, y=y_col, template='plotly_dark')
    
    fig.update_layout(**layout_template)
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
                'pickup_zone', 'pickups'
            )
        elif "tips" in query_path:
            return create_professional_chart(
                df, 'bar', 'Average Tip Amount by Pickup Zone',
                'pickup_zone', 'avg_tip'
            )
        elif "pairs" in query_path:
            return create_professional_chart(
                df, 'bar', 'Most Popular Pickup-Dropoff Routes',
                'pickup_zone', 'trip_count', 'dropoff_zone'
            )
        elif "airports" in query_path:
            return create_professional_chart(
                df, 'bar', 'Airport Traffic Volume',
                'airport_zone', 'trips'
            )
        elif "durations" in query_path:
            return create_professional_chart(
                df, 'scatter', 'Average Travel Duration by Route',
                'pickup_zone', 'avg_duration', 'dropoff_zone'
            )
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
                color: white;
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

