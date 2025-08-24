import ipywidgets as widgets
from ipywidgets import interact, interact_manual
import cufflinks as cf
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])  # Try FLATLY, LUX, or CYBORG
server = app.server
server.config["BINARY_PLOTLY_JSON"] = False
#excel_url = "https://raw.githubusercontent.com/SoilScience-Data/data_dropdown/240e1867bd9565874cf94586852d73ffb99470cd/All_Data_LMM.xlsx"
df1 = pd.read_csv("data/All_Data_LMM.csv", na_values=["NAN"])
print("CSV row count:", len(df1))
print(df1)

#test = px.box(df1, x="Tillage", y="Protein_kg_ha", points="all")
#test.write_image("debug.png")    # locally this writes a file you can inspect
#print("Test figure for Protein_kg_ha on Tillage saved—check debug.png")


df1['ID']=df1['Tillage'].astype(str)+"_"+df1['Fertilizer'].astype(str)+"_"+df1['Cover'].astype(str)

#var_names = df1.columns[6:52].tolist()
#group_vars = ["ID", "Tillage", "Fertilizer", "Cover", "No_Pract"]

# Beispiel-Daten
df = df1.copy()
var_names = df.columns[6:52].tolist()
group_vars = ["ID", "Tillage", "Fertilizer", "Cover", "No_Pract"]
replicates = sorted(df["Replicate"].unique())


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
    
    print("🔥 DYNAMIC CALLBACK FIRED:", y_var, group1, group2, rep)
    dff = df1.copy()
    
    fig = px.box(
        df1,
        x="Tillage",
        y=y_var,            # ← dynamic here
        points="all",
        title=f"Testing y_var: {y_var}"
    )
    print(">>> y_var float values:", fig.data[0].y)
    return fig


if __name__ == "__main__":

    app.run(debug=True)





















