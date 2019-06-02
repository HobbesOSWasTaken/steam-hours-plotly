import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import os
import requests

app = dash.Dash()
server = app.server

key = *STEAM_API_KEY_HERE*
steam64id_hardcode = *STEAM64ID_HERE*

def gameNames(steam64id):
    steam_games_pararmeters = {"format": "json", "steamid": steam64id, "include_appinfo": 1, "key": key}
    steam_games_response = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/", params=steam_games_pararmeters)
    try:
        steam_game_data = steam_games_response.json()
        steam_games = []
        for i in range(steam_game_data["response"]["game_count"]):
            steam_game_name = steam_game_data["response"]["games"][i]["name"]
            steam_games.append(steam_game_name)

    except KeyError:
        return "Key Error Encountered: Please try again"
    except IndexError:
        return "No results found"
    except ValueError:
        return "Invalid Steam64 ID"
    return steam_games

def gameTime(steam64id):
    steam_games_pararmeters = {"format": "json", "steamid": steam64id, "include_appinfo": 1, "key": key}
    steam_games_response = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/", params=steam_games_pararmeters)
    try:
        steam_game_data = steam_games_response.json()
        steam_games_time = []
        for i in range(steam_game_data["response"]["game_count"]):
            steam_game_time = steam_game_data["response"]["games"][i]["playtime_forever"] / 60
            steam_games_time.append(round(steam_game_time, 2))

    except KeyError:
        return "Key Error Encountered: Please try again"
    except IndexError:
        return "No results found"
    except ValueError:
        return "Invalid Steam64 ID"
    return steam_games_time

def steam_user(steam64id):
    steam_userinfo_parameters = {"format": "json", "steamids": steam64id, "key": key}
    steam_userinfo_response = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/", params=steam_userinfo_parameters)
    try:
        steam_userinfo_data = steam_userinfo_response.json()
        steam_userinfo_name = steam_userinfo_data["response"]["players"][0]["personaname"]
    except KeyError:
        return "Key Error Encountered: Please try again"
    except IndexError:
        return "No results found"
    except ValueError:
        return "Invalid Steam64 ID"
    return steam_userinfo_name

colors = {
    "background": "#111111",
    "text": '#7FDBFF'
}
app.layout = html.Div(style={"backgroundColor": colors["background"], "width": 1800, "height": 1000}, children=[
    html.H1(
        children='Summary of Games',
        style={
            "textAlign": "center",
            "color": colors["text"]
        }
    ),

    html.Div(children='User - ' + steam_user(steam64id_hardcode), style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(style={"width": 1800, "height": 800},
        id='example-graph-2',
        figure={
            'data': [
                {'x': gameNames(steam64id_hardcode), 'y': gameTime(steam64id_hardcode), 'type': 'bar', 'name': 'Steam'},
            ],
            'layout': {
                "title": "Steam Games",
                'yaxis': {
                    'title': 'Time played in Hours'
                },
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        },
        config={
            "displayModeBar": False
        }
    )
])

@server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(server.root_path, 'static'),
                                     'favicon.ico')

if __name__ == '__main__':
    app.run_server(debug=True)
