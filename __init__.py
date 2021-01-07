from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from json_interpreter import *
from api_caller import *

app = Flask(__name__)
app.secret_key = "supersecretkeyrighthere"
app.permanent_session_lifetime = timedelta(hours=1)  # enable if session is permanent below, this just sets time

# Just making it easy to keep track of state values
imperial = "imperial"
metric = "metric"
view_today = 0
view_5_day = 1
view_5_day_graph = 2


# Template must be in a "Template folder in the same dir as py file
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search", methods=["POST", "GET"])
def search_page():
    if request.method == "POST":
        session.permanent = True

        if "zip_code" not in session and "country_name" not in session:
            session["unit"] = imperial
            session["view"] = view_5_day

        print(request.form)

        zip_code = request.form["myZip"]
        session["zip_code"] = zip_code

        country_name = request.form["myCountry"]
        session["country_name"] = country_name

        return redirect(url_for("weather_home"))
    else:
        country_name = ""
        if "country_name" in session:
            country_name = session["country_name"]

        zip_code = ""
        if "zip_code" in session:
            zip_code = session["zip_code"]

        return render_template("search.html", zip_code=zip_code, country_name=country_name)


@app.route("/weather", methods=["POST", "GET"])
def weather_home():
    # if user hasn't provided location data, redirect to search page until they do
    if "country_name" not in session or "zip_code" not in session:
        flash("Enter your Zip and Country so we can find out what it's looking like out there", "info")
        return redirect(url_for("search_page"))
    else:

        temp_data = {}
        country_name = session["country_name"]
        zip_code = session["zip_code"]
        unit = session["unit"]
        view = session["view"]

        interpreter = json_interpreter()
        caller = api_caller()

        if view == view_5_day:
            if "last_update_today" not in session or "forecast_5_day" not in session or can_i_refresh(session["last_update_5_day"]) :
                interval_forecasts = interpreter.lazy_pass_in(caller.get_5_day_forecast(country_name, zip_code, unit))

                if interval_forecasts is not None:
                    for key in interval_forecasts.keys():
                        if key.split("@ ")[1] == "12:00:00":
                            temp_data[interval_forecasts[key]["timestamp_display"]] = interval_forecasts[key]
                    session["last_update_5_day"] = datetime.datetime.now()
                    session["forecast_5_day"] = temp_data
                else:
                    flash("Looks like there was some trouble connecting to OpenWeather to fetch forecasts. Make sure your "
                          + "API key is up to date, and servers are reachable.")
            else:
                temp_data = session["forecast_5_day"]

        elif view == view_today:
            if "forecast_today" not in session or "last_update_today" not in session or can_i_refresh(session["last_update_today"]):
                temp_data = interpreter.lazy_pass_in(caller.get_weather_today(country_name, zip_code, unit))

                if temp_data is None:
                    flash("Looks like there was some trouble connecting to OpenWeather to fetch forecasts. Make sure your "
                          + "API key is up to date, and servers are reachable.")
                else:
                    session["last_update_today"] = datetime.datetime.now()
                    session["forecast_today"] = temp_data
            else:
                temp_data = session["forecast_today"]

        else:
            if "graph_points" not in session or "last_update_graph" not in session or can_i_refresh(session["last_update_graph"]):
                api_return = caller.get_5_day_forecast(country_name, zip_code, unit)
                if api_return is None:
                    flash("Looks like there was some trouble connecting to OpenWeather to fetch forecasts. Make sure "
                          + "your API key is up to date, and servers are reachable.")
                else:
                    api_return["graph"] = True
                    temp_data = interpreter.lazy_pass_in(api_return)

                    session["last_update_graph"] = datetime.datetime.now()
                    session["graph_points"] = temp_data
            else:
                temp_data = session["graph_points"]

        # Allow switch between "Today" and "5 Day Forecast"
        return render_template("weather.html", unit=unit, temp_data=temp_data, view=view)


@app.route("/toggle_unit")
def toggle_unit():
    if "unit" in session:
        if session["unit"] == imperial:
            session["unit"] = metric
        else:
            session["unit"] = imperial

    return redirect(url_for("weather_home"))


@app.route("/toggle_view",  methods=["POST"])
def toggle_view():
    if request.method == "POST" and "new_view_id" in request.form:
        new_view_id = int(request.form["new_view_id"])
        if new_view_id == view_today:
            session["view"] = view_today
        elif new_view_id == view_5_day:
            session["view"] = view_5_day
        else:
            session["view"] = view_5_day_graph

    return redirect(url_for("weather_home"))


@app.route("/contact")
def contact_page():
    return redirect("https://github.com/jfarnsworth95")


@app.route("/clear_session")
def clear_session():
    session.pop("country_name", None)
    session.pop("zip_code", None)
    session.pop("unit", None)
    session.pop("view", None)
    session.pop("can_update", None)
    session.pop("last_update_5_day", None)
    session.pop("last_update_today", None)
    session.pop("last_update_graph", None)
    session.pop("forecast_today", None)
    session.pop("forecast_5_day", None)
    session.pop("graph_points", None)

    flash("Your session has been successfully purged... It had a family, you monster.")

    return redirect(url_for("home"))


# Just catches any unknown paths to provide a cleaner experience
@app.route("/<unknown>")
def unknown(unknown):
    return redirect(url_for("home"))

def can_i_refresh(last_updated):
    if last_updated is None:
        return True

    difference = datetime.datetime.now() - last_updated
    if difference.total_seconds() / 60 > 5:
        return True

    return False


if __name__ == "__main__":
    app.run(debug=True)  # debug=True will allow code to update once saved without requiring a restart
