import datetime


class json_interpreter():

    def __init__(self):
        pass

    def lazy_pass_in(self, json):
        if json is None:
            print("Error, no json returned. Check your API key.")
            return None
        elif "cnt" in json:
            return self.convert_json_list(json)
        else:
            return self.convert_current_data(json, json["name"], json["sys"]["sunrise"], json["sys"]["sunset"], json["unit"])

    def convert_current_data(self, json, city, sunrise, sunset, unit):

        if json is None:
            print("Bad JSON return")
            return None
        elif "cnt" in json:
            print("Wrong JSON file. Shouldn't have a count 'cnt' value")
            return None

        translation_dic = {"city": city,
                           "sunrise": sunrise,
                           "sunset": sunset,
                           "weather_condition": json["weather"][0]["main"],
                           "weather_description": json["weather"][0]["description"],
                           "weather_icon_id": json["weather"][0]["icon"],
                           "humidity": json["main"]["humidity"],
                           "wind_speed": json["wind"]["speed"],
                           "cloud_percent": json["clouds"]["all"],
                           "timestamp": json["dt"],
                           "timestamp_display": datetime.datetime.fromtimestamp(json["dt"]).strftime(
                               "%A %B %d %Y"),
                           "timestamp_adjusted": datetime.datetime.fromtimestamp(json["dt"]).strftime(
                               "%A %B %d %Y @ %H:%M:%S")}

        if translation_dic["sunrise"]:
            translation_dic["sunrise_display"] = datetime.datetime.fromtimestamp(translation_dic["sunrise"]).strftime("%H:%M")
        if translation_dic["sunset"]:
            translation_dic["sunset_display"] = datetime.datetime.fromtimestamp(translation_dic["sunset"]).strftime("%H:%M")

        # create
        temp_dics = self.generate_c_vs_f_temps(json, unit)
        translation_dic["temp_f"] = temp_dics["temp_f"]
        translation_dic["temp_c"] = temp_dics["temp_c"]

        return translation_dic

    def convert_json_list(self, json_list):

        if json_list is None:
            print("Bad JSON return")
            return None
        elif "cod" not in json_list or "cnt" not in json_list or "list" not in json_list:
            print("Unknown return")
            return None

        if "graph" not in json_list:
            translation_dic_collection = {}
            city = json_list["city"]["name"]
            unit = json_list["unit"]
            for json in json_list["list"]:
                translation_dic = self.convert_current_data(json, city, None, None, unit)
                translation_dic_collection[translation_dic["timestamp"]] = translation_dic

            return translation_dic_collection

        else:
            graph_points = {}

            unit = json_list["unit"]
            graph_points_c = {}
            graph_points_f = {}
            for dic in json_list["list"]:
                ts = dic["dt"] * 1000

                if unit == "imperial":
                    temperature_f = round(dic["main"]["temp"], 1)
                    graph_points_f[ts] = temperature_f

                    temperature_c = round(self.toggle_c_and_f(temperature_f, True), 1)
                    graph_points_c[ts] = temperature_c
                else:
                    temperature_c = round(dic["main"]["temp"], 1)
                    graph_points_c[ts] = temperature_c

                    temperature_f = round(self.toggle_c_and_f(temperature_c, False), 1)
                    graph_points_f[ts] = temperature_f

            graph_points["F"] = graph_points_f
            graph_points["C"] = graph_points_c

            return graph_points


    def generate_c_vs_f_temps(self, json, unit):
        # I don't have to put these here, but it provides me some peace of mind
        temp_c = {}
        temp_f = {}

        temp = round(json["main"]["temp"], 1)
        feels_like = round(json["main"]["feels_like"], 1)
        temp_low = round(json["main"]["temp_min"], 1)
        temp_high = round(json["main"]["temp_max"], 1)

        if unit == "metric":
            temp_c = {"temp": temp, "feels_like": feels_like, "temp_low": temp_low, "temp_high": temp_high}

            # C -> F : (°C * 9/5) + 32
            temp_f_convert = round(self.toggle_c_and_f(temp, False), 1)
            feels_like_f_convert = round(self.toggle_c_and_f(feels_like, False), 1)
            temp_low_f_convert = round(self.toggle_c_and_f(temp_low, False), 1)
            temp_high_f_convert = round(self.toggle_c_and_f(temp_high, False), 1)

            temp_f = {"temp": temp_f_convert, "feels_like": feels_like_f_convert, "temp_low": temp_low_f_convert,
                      "temp_high": temp_high_f_convert}

        else:
            temp_f = {"temp": temp, "feels_like": feels_like, "temp_low": temp_low, "temp_high": temp_high}

            # F -> C : (°F − 32) * 5/9
            temp_c_convert = round(self.toggle_c_and_f(temp, True), 1)
            feels_like_c_convert = round(self.toggle_c_and_f(feels_like, True), 1)
            temp_low_c_convert = round(self.toggle_c_and_f(temp_low, True), 1)
            temp_high_c_convert = round(self.toggle_c_and_f(temp_high, True), 1)

            temp_c = {"temp": temp_c_convert, "feels_like": feels_like_c_convert, "temp_low": temp_low_c_convert,
                      "temp_high": temp_high_c_convert}

        return {"temp_c": temp_c, "temp_f": temp_f}

    def toggle_c_and_f(self, temp, toggle_to_celsius):
        if toggle_to_celsius:
            return (temp - 32) * 5 / 9
        else:
            return (temp * 9 / 5) + 32


if __name__ == "__main__":
    pass
    #json_interpreter = json_interpreter()
    #json_interpreter.lazy_pass_in(json)
