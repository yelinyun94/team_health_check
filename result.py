import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the data from the Excel file
data = pd.read_excel("health_check.xlsx")

# Define the colors for categories
category_colors = {
    'Green': 'rgb(0, 255, 0)',
    'Red': 'rgb(255, 0, 0)',
    'Yellow': 'rgb(255, 255, 0)'
}

# Create the Dash app
app = dash.Dash(__name__)

# Define the specific team names you want to display
team_names = [
    'Telephony', 'Conferencing', 'Remote Access', 'Internet Access', 'LAN',
    'WAN/CNC', 'Cloud Network', 'DC Network', 'AGN Shared', 'Firewall', 'Automation'
]

# Define the app layout
app.layout = html.Div([
    html.H1("Team Health Check Results"),
    dcc.Dropdown(
        id='team-name-dropdown',
        options=[{'label': team, 'value': team} for team in team_names],
        value=team_names[0]
    ),
    dcc.Graph(id='health-check-heatmap'),
])

# Define the callback function to update the heatmap
@app.callback(
    Output('health-check-heatmap', 'figure'),
    Input('team-name-dropdown', 'value')
)
def update_heatmap(selected_team):
    # Filter the data based on the selected team name
    filtered_data = data[['Category / Team', selected_team]]

    # Create the heatmap figure with colored shapes
    fig = go.Figure(data=go.Heatmap(
        x=[selected_team],
        y=filtered_data['Category / Team'],
        z=filtered_data[selected_team].map(category_colors).tolist(),
        colorscale=[[0.0, 'rgb(255, 255, 255)']] + [[i / len(category_colors), category_colors[c]] for c in category_colors],
        colorbar=dict(
            tickvals=[0.167, 0.5, 0.833],
            ticktext=['Red', 'Yellow', 'Green']
        )
    ))

    fig.update_xaxes(title_text="Teams")
    fig.update_yaxes(title_text="Categories / Teams")
    fig.update_layout(title=f"Team Health Check Results for {selected_team}",
                      xaxis_showgrid=False,
                      yaxis_showgrid=False)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
