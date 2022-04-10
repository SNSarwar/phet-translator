# app.py
import base64
import datetime
import io
import re
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, dash_table
from dash import html
import dash_bootstrap_components as dbc
import urllib.parse
import pandas as pd
from g_trans import google_translator
import dash_loading_spinners as dls
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE, external_stylesheets])

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div(
                        [
                            html.H2(
                                "PHET Simulator Translation Tool",
                                style={"text-align": "center", "margin-bottom": "0px"},
                            ),
                            html.H4(
                                "Agami Education Foundation", style={"text-align": "center", "margin-top": "0px"}
                            ),
                            html.H6(
                                "by Shomeek Sarwar", style={"text-align": "center", "margin-top": "0px"}
                            ),
                        ]
                    )
                ])
            ], color="light"),
        ], width=12),
    ], className='mb-2'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            html.H6(''),
            html.H6('Please upload HTML file'),
            'Drag and Drop or ',
            html.A('click inside the box to select files')
        ]),
        style={
            'width': '99%',
            'height': '120px',
            'lineHeight': '50px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '5px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    # html.Div(dcc.Loading(children="output-data-upload", color="#119DFF", type="dot", fullscreen=False)),
    dls.ThreeDots(
        html.Div(id='output-data-upload'),
        color="blue",
        speed_multiplier=1,
        width=150,
    )
])

CHIPPER_MARKER = 'window.phet.chipper.strings ='
FIELD_SEPARATOR = '{screenName}}'
goog_tr_url_st = "https://translate.google.com/?sl=en&tl=bn&text="
goog_tr_url_end = "&op=translate"


def google_link(word: str) -> str:
    link = goog_tr_url_st + urllib.parse.quote_plus(word.strip()) + goog_tr_url_end
    # return f"html.A(html.P('Link'),href=\"{link}\""
    return link

def create_translation_helper_file_json(chipper_string) -> pd.DataFrame:
    str = re.sub(CHIPPER_MARKER, "", chipper_string)
    str = re.sub(";", "", str)
    print("key\tvalue\tgoogle translate link\ttranslated text")
    ps = json.loads(str)
    kvs = ps['en']
    translator = google_translator()
    trans_cache = dict()
    rows = list()
    for key, val in kvs.items():
        row = list()
        val = re.sub('}};', '', val)
        if 'window' in key or 'JOIST' in key or 'SCENERY_PHET' in key or '{{' in val:
            continue
        if len(key) > 0 or key != '':
            row.append(key)
            row.append(val)
            tr_key = val.strip().lower()
            # load from trans cache if already seen else translate
            if tr_key in trans_cache:
                tr_text = trans_cache[tr_key]
                print('from cache')
            else:
                tr_text = translator.translate(val, lang_tgt='bn')
                trans_cache[tr_key] = tr_text
            print(f"{val} --> {tr_text}")
            row.append(tr_text)
            rows.append(row)
    print(rows)
    df = pd.DataFrame(rows)
    df.columns = ['key', 'value', 'suggested_trans']
    return df


def parse_contents(contents, filename, date):
    global lines
    global chipper_string

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'html' in filename:
            # Assume that the user uploaded an excel file
            content = io.StringIO(decoded.decode('utf-8'))
            # print(content.readlines())
            lines = content.readlines()
            for line in lines:
                if CHIPPER_MARKER in line:
                    chipper_string = line
                    break
            # print(chipper_string)
            df = create_translation_helper_file_json(chipper_string)
    except Exception as e:
        print(e)
        return html.Div([
            f'There was an error reading this file. {e}'
        ])

    return html.Div([
        html.Center(html.P(f"Successfully loaded and processed '{filename}'")),
        html.Center(html.P(f"Last updated {datetime.datetime.fromtimestamp(date)}")),

        dash_table.DataTable(
            id='table',
            data=df.to_dict('records'),
            # columns=[{'name': i, 'id': i} for i in df.columns],
            columns=[
                {'name': 'HTML_KEY', 'id': 'key', 'type': 'text', 'editable': False},
                {'name': 'English word', 'id': 'value', 'type': 'text', 'editable': False, 'selectable': True},
                {'name': 'Translated word', 'id': 'suggested_trans', 'type': 'text', 'editable': True,
                 "deletable": True, "selectable": True},
                # {'name': 'Automated translation', 'id': 'suggested', 'type': 'text','editable': False},
            ],
            style_header={
                'backgroundColor': 'blue',
                'color': 'white',
                'fontWeight': 'bold'
            },
            style_cell={
                #'width': '80px',
                #'minWidth': '00px',
                'textAlign': 'left',
                #'maxWidth': '90px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            style_data={  # overflow cells' content into multiple lines
                'whiteSpace': 'normal',
                'height': 'auto',
                'border': '2px light blue'
            },
            style_data_conditional=[
                {
                'if': {
                    'column_id': 'key',
                },
                'width': '80px',
                'minWidth': '80px',
                'textAlign': 'left',
                'maxWidth': '80px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                },
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
            editable=True,
            export_format='csv'
        ),
        html.Div([
            html.Hr(),  # horizontal line
            # For debugging, display the raw contents provided by the web browser
            html.Button("Download translated HTML", id="btn-download-txt", n_clicks=0,
                        style={'background-color': 'black',
                               'color': 'white',
                               'height': '60px',
                               'width': '400px',
                               'margin-top': '40px',
                               'margin-left': '40px'}
                        ),
            dcc.Download(id="download-text")
        ]
        )
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    State("table", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, data1):
    if n_clicks is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate
    translated_data = pd.DataFrame(data1)
    print(translated_data.head(30))
    trans_chipper = chipper_string
    for _, row in translated_data.iterrows():
        key = f'"{row["key"]}":"{row["value"]}"'
        sub = f'"{row["key"]}":"{row["suggested_trans"]}"'
        print(f"key:{key}\tsub:{sub}")
        trans_chipper = re.sub(key, sub, trans_chipper)

    final_lines = list()
    print(trans_chipper)
    for line in lines:
        if CHIPPER_MARKER in line:
            final_lines.append(trans_chipper)
        else:
            final_lines.append(line)
    content = ' '.join(final_lines)
    return dict(content=content, filename="translated_html_file.html")


if __name__ == '__main__':
    port = 8070
    app.run_server(port=port, debug=False)
