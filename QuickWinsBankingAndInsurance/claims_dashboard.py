import dash
from dash import dcc, html # Dash Core Components & HTML Components
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# --- 1. Load Data ---
# (Repeat loading inside the script for self-containment)
file_path = 'datasets/claims_dashboard_data.csv'
claims_df = pd.read_csv(file_path)

# --- 2. Initialize the Dash App ---
app = dash.Dash(__name__)
app.title = "Claims Analysis Dashboard" # Browser tab title

# --- 3. Define the App Layout ---
app.layout = html.Div(children=[
    # Page Title
    html.H1(children='Insurance Claims Analysis'),

    # Subtitle/Description
    html.Div(children='''
        Analyze total claim amounts by policy type and region.
    '''),

    # Region Filter Dropdown
    html.Label('Select Region:'),
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': 'All Regions', 'value': 'All'}] + # Add 'All' option
                [{'label': region, 'value': region} for region in claims_df['region'].unique()],
        value='All', # Default value
        clearable=False, # Prevent the user from clearing the selection
        style={'width': '50%'} # Adjust dropdown width
    ),

    # Bar Chart (placeholder, will be updated by callback)
    dcc.Graph(
        id='claims-by-policy-type-graph'
    )
])

# --- 4. Define Callbacks for Interactivity ---
# This function links the dropdown (Input) to the graph (Output)
@app.callback(
    Output('claims-by-policy-type-graph', 'figure'), # The graph's figure property
    Input('region-dropdown', 'value')               # The dropdown's selected value
)
def update_graph(selected_region):
    # Filter data based on dropdown selection
    if selected_region == 'All':
        filtered_df = claims_df # Use all data if 'All' is selected
    else:
        filtered_df = claims_df[claims_df['region'] == selected_region]

    # Group by policy type and sum claim amounts
    grouped_data = filtered_df.groupby('policy_type')['claim_amount'].sum().reset_index()

    # Create the bar chart using Plotly Express
    fig = px.bar(grouped_data,
                 x='policy_type',
                 y='claim_amount',
                 title=f'Total Claim Amount by Policy Type ({selected_region})',
                 labels={'policy_type': 'Policy Type', 'claim_amount': 'Total Claim Amount ($)'},
                 template='plotly_white' # Use a clean template
                )

    # Update layout for better readability
    fig.update_layout(
        title_x=0.5, # Center title
        xaxis_title="Policy Type",
        yaxis_title="Total Claim Amount ($)"
    )

    return fig # Return the updated figure to the graph component

# --- 5. Run the App Server ---
if __name__ == '__main__':
    app.run(debug=True) # debug=True allows auto-reloading on code changes