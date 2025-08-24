import ipywidgets as widgets
from ipywidgets import interact, interact_manual
import cufflinks as cf
from IPython.display import display
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

path = r"C:\Users\rikaa\bwSyncShare\Uni\WorldVeg\Data"

df1 = pd.read_excel(path+"\All_Data_LMM.xlsx",
                   parse_dates=True, na_values={"NAN"})

df1['ID']=df1['Tillage'].astype(str)+"_"+df1['Fertilizer'].astype(str)+"_"+df1['Cover'].astype(str)

var_names = df1.columns[6:52].tolist()
group_vars = ["ID", "Tillage", "Fertilizer", "Cover", "No_Pract"]



# Beispiel-Daten
df = df1.copy()
var_names = df.columns[6:52].tolist()
group_vars = ["ID", "Tillage", "Fertilizer", "Cover", "No_Pract"]
replicates = sorted(df["Replicate"].unique())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])  # Try FLATLY, LUX, or CYBORG
server = app.server
#app.layout = dbc.Container([
#    html.H2("Interactive Plots", className="text-center my-4"),
#    dbc.Row([
#        dbc.Col([
#            html.Label("Dependent Variable"),
#            dcc.Dropdown(var_names, var_names[0], id="y-dropdown"),
#            html.Label("Group 1"),
#            dcc.Dropdown(group_vars, group_vars[0], id="group1-dropdown"),
#            html.Label("Group 2"),
#            dcc.Dropdown(["None"] + group_vars, "None", id="group2-dropdown"),
#            html.Label("Replicate"),
#            dcc.Dropdown(["All"] + replicates, "All", id="rep-dropdown")
#        ], width=3),
#        dbc.Col([
#            dcc.Graph(id="boxplot", style={"height": "700px"})
#        ], width=9)
#    ])
#], fluid=True)

app.layout = dbc.Container([
    html.H2("Interactive Plots", className="text-center my-4"),

    # Horizontal row of dropdowns
    dbc.Row([
        dbc.Col([
            html.Label("Dependent Variable"),
            dcc.Dropdown(var_names, var_names[0], id="y-dropdown")
        ], width=3),
        dbc.Col([
            html.Label("Group 1"),
            dcc.Dropdown(group_vars, group_vars[0], id="group1-dropdown")
        ], width=2),
        dbc.Col([
            html.Label("Group 2"),
            dcc.Dropdown(["None"] + group_vars, "None", id="group2-dropdown")
        ], width=2),
        dbc.Col([
            html.Label("Replicate"),
            dcc.Dropdown(["All"] + replicates, "All", id="rep-dropdown")
        ], width=2)
    ], className="mb-4"),

    # Full-width plot
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="boxplot", style={"height": "800px"})
        ], width=12)
    ])
], fluid=True)

@app.callback(
    Output("boxplot", "figure"),
    Input("y-dropdown", "value"),
    Input("group1-dropdown", "value"),
    Input("group2-dropdown", "value"),
    Input("rep-dropdown", "value")
)
def update_plot(y_var, group1, group2, rep):
    dff = df.copy()
    if rep != "All":
        dff = dff[dff["Replicate"] == rep]

    if group2 != "None":
        dff["Interaction"] = dff[group1].astype(str) + " | " + dff[group2].astype(str)
        x_col = "Interaction"
    else:
        x_col = group1

    fig = px.box(dff,
                x=x_col,
                y=y_var,
                color=group1 if group2 == "None" else "Interaction",
                points="all",
                title=f"{y_var} | {group1} + {group2} | Rep: {rep}")
    fig.update_layout(
        template="simple_white",
        boxmode="group",
        title_font=dict(size=30, family="Arial"),
        xaxis_title=x_col,
        yaxis_title=y_var,
        margin=dict(t=60, b=120, l=40, r=20),
        showlegend=True
        )
    fig.update_traces(marker=dict(size=6, opacity=0.6, line=dict(width=1, color='DarkSlateGrey')), jitter=0.3,boxmean="sd", width=0.5)

    return fig


if __name__ == "__main__":

    app.run(debug=True)
