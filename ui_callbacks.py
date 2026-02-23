# astro_deck/callbacks/ui_callbacks.py
from dash import Input, Output, State, callback_context
from ui.styles import GLASS
from visualization.charts import chart_agency, chart_orbit


def register(app, db, stats):
    """Register UI control callbacks"""

    @app.callback(
        Output("control-content", "style"),
        Input("minimize-control", "n_clicks"),
    )
    def toggle_control(n):
        if n is None:
            return {"display": "block"}
        return {"display": "none"} if (n % 2 == 1) else {"display": "block"}

    @app.callback(
        Output("stats-content", "style"),
        Input("minimize-stats", "n_clicks"),
    )
    def toggle_stats_content(n):
        if n is None:
            return {"display": "block"}
        return {"display": "none"} if (n % 2 == 1) else {"display": "block"}

    @app.callback(
        Output("chat-content", "style"),
        Input("minimize-chat", "n_clicks"),
    )
    def toggle_chat_content(n):
        expanded = {"flex": "1", "display": "flex", "flexDirection": "column", "minHeight": "400px"}
        if n is None:
            return expanded
        return {"display": "none"} if (n % 2 == 1) else expanded

    @app.callback(
        Output("telemetry-content", "style"),
        Input("minimize-telemetry", "n_clicks"),
    )
    def toggle_telemetry_content(n):
        if n is None:
            return {"display": "block"}
        return {"display": "none"} if (n % 2 == 1) else {"display": "block"}

    @app.callback(
        Output("satellite-content", "style"),
        Input("minimize-satellite", "n_clicks"),
    )
    def toggle_satellite(n):
        if n is None:
            return {"display": "block"}
        return {"display": "none"} if (n % 2 == 1) else {"display": "block"}

    @app.callback(
        Output("rotation-state", "data"),
        Input("toggle-rotation", "n_clicks"),
        State("rotation-state", "data"),
    )
    def toggle_rotation(n_clicks, current_state):
        if not n_clicks:
            return bool(current_state) if current_state is not None else False
        return not (bool(current_state) if current_state is not None else False)

    @app.callback(
        Output("stats-panel-container", "style"),
        Output("chart-agency", "figure"),
        Output("chart-orbit", "figure"),
        Input("toggle-stats", "n_clicks"),
        Input("close-stats", "n_clicks"),
    )
    def toggle_stats(n1, n2):
        if not callback_context.triggered:
            hidden = {**GLASS, "top": "20px", "left": "340px", "width": "450px", "display": "none"}
            return hidden, chart_agency(stats), chart_orbit(stats)

        prop_id = callback_context.triggered[0]["prop_id"]

        if prop_id.startswith("toggle-stats"):
            s = db.stats()
            shown = {
                **GLASS,
                "top": "20px",
                "left": "340px",
                "width": "450px",
                "maxHeight": "90vh",
                "overflowY": "auto",
                "display": "block",
            }
            return shown, chart_agency(s), chart_orbit(s)

        hidden = {**GLASS, "top": "20px", "left": "340px", "width": "450px", "display": "none"}
        return hidden, chart_agency(stats), chart_orbit(stats)
