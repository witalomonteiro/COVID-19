import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

CENTER_LAT, CENTER_LON = -14.272572694355336, -51.25567404158474

# =========================== Importação do Dataset ============================


# pt1_2020 = pd.read_csv(
#     "datasets/HIST_PAINEL_COVIDBR_2020_Parte1_29jul2022.csv", sep=";")
# pt2_2020 = pd.read_csv(
#     "datasets/HIST_PAINEL_COVIDBR_2020_Parte2_29jul2022.csv", sep=";")
# pt1_2021 = pd.read_csv(
#     "datasets/HIST_PAINEL_COVIDBR_2021_Parte1_29jul2022.csv", sep=";")
# pt2_2021 = pd.read_csv(
#     "datasets/HIST_PAINEL_COVIDBR_2021_Parte2_29jul2022.csv", sep=";")
# pt1_2022 = pd.read_csv(
#     "datasets/HIST_PAINEL_COVIDBR_2022_Parte1_29jul2022.csv", sep=";")
# pt2_2022 = pd.read_csv(
#     "datasets/HIST_PAINEL_COVIDBR_2022_Parte2_29jul2022.csv", sep=";")

# consolidated = pd.concat([
#     pt1_2020, pt1_2020, pt1_2021, pt2_2021, pt1_2022, pt2_2022,
# ], axis=0)

# df_estados = consolidated[(~consolidated["estado"].isna())
#                           & (consolidated["codmun"].isna())]
# df_brasil = consolidated.query('regiao == "Brasil"', engine='python')

# df_estados.to_csv("datasets/df_estados.csv", sep=";",
#                   encoding='utf-8-sig', index=False)
# df_brasil.to_csv("datasets/df_brasil.csv", sep=";",
#                  encoding='utf-8-sig', index=False)

df_estados = pd.read_csv("datasets/df_estados.csv", sep=";")
df_brasil = pd.read_csv("datasets/df_brasil.csv", sep=";")

brasil_geo = json.load(open("geojson/brazil_geo.json", "r", encoding="utf8"))

df_estados_ = df_estados[df_estados["data"] == "2020-05-13"]
df_data = df_estados[df_estados["estado"] == "RJ"]

selecao_colunas = {
    "casosAcumulado": "Casos Acumulados",
    "casosNovos": "Novos Casos",
    "obitosAcumulado": "Óbitos Acumulados",
    "obitosNovos": "Novos Óbitos"
}

# ============================ Intanciação do Dash =============================

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

map_fig = px.choropleth_mapbox(
    # df_estados_,
    # locations="estado",
    # color="casosNovos",
    # center={"lat": CENTER_LAT, "lon": CENTER_LON},
    # zoom=4,
    # geojson=brasil_geo,
    # color_continuous_scale="Redor",
    # opacity=0.55,
    # labels={'unemp':'unemployment rate'},
    # hover_data={"casosAcumulado": True, "casosNovos": True,
    #             "obitosNovos": True, "estado": True}
)

# map_fig.update_layout(
#     paper_bgcolor="#242424",
#     autosize=True,
#     margin=go.Margin(l=0, r=0, t=0, b=0),
#     showlegend=False,
#     mapbox_style="carto-darkmatter"
# )

int_fig = go.Figure(layout={"template": "plotly_dark"})
# int_fig.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
# int_fig.update_layout(
#     paper_bgcolor="#242424",
#     plot_bgcolor="#242424",
#     autosize=True,
#     margin=dict(l=10, r=10, t=10, b=10)
# )

# ============================ Construção do Layout ============================

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([
                # html.H4("Monteiro Academy", style={
                        # "font": "Montserrat"}, id="logo"),
                html.H3("Evolução COVID-19"),
                dbc.Button("BRASIL", id="local-btn",
                           color="primary", size="lg")
            ], style={}),
            html.P("Selecione a data na qual deseja obter informações:",
                   style={"margin-top": "40px"}),
            html.Div(id="teste-div", children=[
                dcc.DatePickerSingle(
                    id="date-picker",
                    min_date_allowed=df_brasil["data"].min(),
                    max_date_allowed=df_brasil["data"].max(),
                    initial_visible_month=df_brasil["data"].min(),
                    date=df_brasil["data"].max(),
                    display_format="D MMMM YYYY",
                    style={"border": "0px, solid black"}
                )
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Casos recuperados"),
                            html.H3(style={"color": "#ADFC92"},
                                    id="casos-recuperados-txt"),
                            html.Span("Em acompanhamento"),
                            html.H5(id="em-acompanhamento-txt"),
                        ])
                    ], color="light", outline=True, style={"margin-top": "10px", "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                                           "color": "#FFFFFF"})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Casos acumulados"),
                            html.H3(style={"color": "#389FD6"},
                                    id="casos-confirmados-txt"),
                            html.Span("Novos casos no dia"),
                            html.H5(id="novos-casos-txt"),
                        ])
                    ], color="light", outline=True, style={"margin-top": "10px", "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                                           "color": "#FFFFFF"})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Óbitos acumulados"),
                            html.H3(style={"color": "#DF2935"},
                                    id="obitos-confirmados-txt"),
                            html.Span("Novos óbitos no dia"),
                            html.H5(id="novos-obitos-txt"),
                        ])
                    ], color="light", outline=True, style={"margin-top": "10px", "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                                           "color": "#FFFFFF"})
                ], md=4),
            ]),

            html.Div([
                html.P("Selecione o tipo de dado que deseja visualizar:",
                       style={"margin-top": "25px"}),
                dcc.Dropdown(id="local-dropdown",
                             options=[{"label": x, "value": y}
                                      for y, x in selecao_colunas.items()],
                             value="casosNovos",
                             style={"margin-top": "10px"}
                             ),
                dcc.Graph(id="int_fig", figure=int_fig)
            ]),
        ], md=5, style={"padding": "25px", "background-color": "#242424"}),
        dbc.Col([
            dcc.Loading(id="carregamento", type="default", children=[
                dcc.Graph(id="map-fig", figure=map_fig,
                          style={"height": "100vh"})
            ])
        ], md=7, style={})
    ], class_name='g-0', justify='start')
, fluid=True)

# ============================== Interatividade ================================


@app.callback(
    [
        Output("casos-recuperados-txt", "children"),
        Output("em-acompanhamento-txt", "children"),
        Output("casos-confirmados-txt", "children"),
        Output("novos-casos-txt", "children"),
        Output("obitos-confirmados-txt", "children"),
        Output("novos-obitos-txt", "children"),
    ],
    [Input("date-picker", "date"), Input("local-btn", "children")]
)
def display_status(date, location):
    if location == "BRASIL":
        df_data_on_date = df_brasil[df_brasil["data"] == date]
    else:
        df_data_on_date = df_estados[(df_estados["estado"] == location) & (
            df_estados["data"] == date)]

    recuperados_novos = "-" if df_data_on_date["Recuperadosnovos"].isna(
    ).values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(",", ".")
    acompanhamentos_novos = "-" if df_data_on_date["emAcompanhamentoNovos"].isna(
    ).values[0] else f'{int(df_data_on_date["emAcompanhamentoNovos"].values[0]):,}'.replace(",", ".")
    casos_acumulados = "-" if df_data_on_date["casosAcumulado"].isna(
    ).values[0] else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".")
    casos_novos = "-" if df_data_on_date["casosNovos"].isna(
    ).values[0] else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(",", ".")
    obitos_acumulados = "-" if df_data_on_date["obitosAcumulado"].isna(
    ).values[0] else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(",", ".")
    obitos_novos = "-" if df_data_on_date["obitosNovos"].isna(
    ).values[0] else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(",", ".")

    return (
        recuperados_novos,
        acompanhamentos_novos,
        casos_acumulados,
        casos_novos,
        obitos_acumulados,
        obitos_novos
    )


@app.callback(
    Output("int_fig", "figure"),
    [
        Input("local-dropdown", "value"),
        Input("local-btn", "children"),
    ]
)
def plot_linegraph(plot_type, location):
    if location == "BRASIL":
        df_data_on_location = df_brasil.copy()
    else:
        df_data_on_location = df_estados[df_estados["estado"] == location]
    bar_plots = ["casosNovos", "obitosNovos"]

    int_fig = go.Figure(layout={"template": "plotly_dark"})
    if plot_type in bar_plots:
        int_fig.add_trace(
            go.Bar(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    else:
        int_fig.add_trace(go.Scatter(
            x=df_data_on_location["data"], y=df_data_on_location[plot_type]))

    int_fig.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, t=10, b=10)
    )

    return int_fig


@app.callback(
    Output("map-fig", "figure"),
    [
        Input("date-picker", "date")
    ]
)
def update_map(date):
    df_data_on_estados = df_estados[df_estados["data"] == date]

    map_fig = px.choropleth_mapbox(
        df_data_on_estados,
        locations="estado",
        color="casosAcumulado",
        center={"lat": CENTER_LAT, "lon": CENTER_LON},
        zoom=4,
        geojson=brasil_geo,
        color_continuous_scale="Viridis",
        # range_color=(0, 12),
        opacity=0.5,
        labels={'casosAcumulado': 'Casos Acumulados'},
        hover_data={"casosAcumulado": True, "casosNovos": True,
                    "obitosNovos": True, "estado": True}
    )
    map_fig.update_layout(
        paper_bgcolor="#242424",
        font_color="#FFF",
        autosize=True,
        # margin=go.Margin(l=0, r=0, t=0, b=0),
        # margin=dict(l=10, r=10, t=10, b=10),
        margin_l=0, margin_r=0, margin_t=0, margin_b=0,
        showlegend=False,
        mapbox_style="carto-darkmatter"
    )
    return map_fig


@app.callback(
    Output("local-btn", "children"),
    [
        Input("map-fig", "clickData"),
        Input("local-btn", "n_clicks")
    ]
)
def update_local(click_data, n_clicks):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "local-btn.n_clicks":
        state = click_data["points"][0]["location"]
        return "{}".format(state)
    else:
        return "BRASIL"


# =============================== Executar App =================================
if __name__ == "__main__":
    app.run_server(debug=True)
