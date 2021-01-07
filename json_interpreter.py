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
    json = {
        'cod': '200',
        'message': 0,
        'cnt': 40,
        'list': [
            {
                'dt': 1609902000,
                'main': {
                    'temp': 13.28,
                    'feels_like': 8.64,
                    'temp_min': 13.09,
                    'temp_max': 13.28,
                    'pressure': 1016,
                    'sea_level': 1016,
                    'grnd_level': 993,
                    'humidity': 51,
                    'temp_kf': 0.19
                },
                'weather': [
                    {
                        'id': 802,
                        'main': 'Clouds',
                        'description': 'scattered clouds',
                        'icon': '03n'
                    }
                ],
                'clouds': {
                    'all': 47
                },
                'wind': {
                    'speed': 4.58,
                    'deg': 148
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-06 03:00:00'
            },
            {
                'dt': 1609912800,
                'main': {
                    'temp': 12.97,
                    'feels_like': 7.94,
                    'temp_min': 12.83,
                    'temp_max': 12.97,
                    'pressure': 1016,
                    'sea_level': 1016,
                    'grnd_level': 992,
                    'humidity': 62,
                    'temp_kf': 0.14
                },
                'weather': [
                    {
                        'id': 803,
                        'main': 'Clouds',
                        'description': 'broken clouds',
                        'icon': '04n'
                    }
                ],
                'clouds': {
                    'all': 76
                },
                'wind': {
                    'speed': 5.83,
                    'deg': 158
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-06 06:00:00'
            },
            {
                'dt': 1609923600,
                'main': {
                    'temp': 13,
                    'feels_like': 8.77,
                    'temp_min': 12.97,
                    'temp_max': 13,
                    'pressure': 1014,
                    'sea_level': 1014,
                    'grnd_level': 991,
                    'humidity': 77,
                    'temp_kf': 0.03
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04n'
                    }
                ],
                'clouds': {
                    'all': 91
                },
                'wind': {
                    'speed': 5.76,
                    'deg': 162
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-06 09:00:00'
            },
            {
                'dt': 1609934400,
                'main': {
                    'temp': 12.69,
                    'feels_like': 8.79,
                    'temp_min': 12.68,
                    'temp_max': 12.69,
                    'pressure': 1013,
                    'sea_level': 1013,
                    'grnd_level': 990,
                    'humidity': 87,
                    'temp_kf': 0.01
                },
                'weather': [
                    {
                        'id': 500,
                        'main': 'Rain',
                        'description': 'light rain',
                        'icon': '10n'
                    }
                ],
                'clouds': {
                    'all': 98
                },
                'wind': {
                    'speed': 5.87,
                    'deg': 158
                },
                'visibility': 10000,
                'pop': 0.67,
                'rain': {
                    '3h': 0.75
                },
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-06 12:00:00'
            },
            {
                'dt': 1609945200,
                'main': {
                    'temp': 12.8,
                    'feels_like': 8.95,
                    'temp_min': 12.8,
                    'temp_max': 12.8,
                    'pressure': 1013,
                    'sea_level': 1013,
                    'grnd_level': 990,
                    'humidity': 91,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 500,
                        'main': 'Rain',
                        'description': 'light rain',
                        'icon': '10d'
                    }
                ],
                'clouds': {
                    'all': 100
                },
                'wind': {
                    'speed': 6.12,
                    'deg': 156
                },
                'visibility': 9730,
                'pop': 1,
                'rain': {
                    '3h': 1.46
                },
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-06 15:00:00'
            },
            {
                'dt': 1609956000,
                'main': {
                    'temp': 14.35,
                    'feels_like': 11.68,
                    'temp_min': 14.35,
                    'temp_max': 14.35,
                    'pressure': 1012,
                    'sea_level': 1012,
                    'grnd_level': 989,
                    'humidity': 79,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 501,
                        'main': 'Rain',
                        'description': 'moderate rain',
                        'icon': '10d'
                    }
                ],
                'clouds': {
                    'all': 96
                },
                'wind': {
                    'speed': 4.18,
                    'deg': 236
                },
                'visibility': 10000,
                'pop': 1,
                'rain': {
                    '3h': 4.91
                },
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-06 18:00:00'
            },
            {
                'dt': 1609966800,
                'main': {
                    'temp': 12.77,
                    'feels_like': 5.39,
                    'temp_min': 12.77,
                    'temp_max': 12.77,
                    'pressure': 1011,
                    'sea_level': 1011,
                    'grnd_level': 987,
                    'humidity': 59,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 801,
                        'main': 'Clouds',
                        'description': 'few clouds',
                        'icon': '02d'
                    }
                ],
                'clouds': {
                    'all': 20
                },
                'wind': {
                    'speed': 8.92,
                    'deg': 301
                },
                'visibility': 10000,
                'pop': 0.25,
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-06 21:00:00'
            },
            {
                'dt': 1609977600,
                'main': {
                    'temp': 9.37,
                    'feels_like': 1.41,
                    'temp_min': 9.37,
                    'temp_max': 9.37,
                    'pressure': 1012,
                    'sea_level': 1012,
                    'grnd_level': 989,
                    'humidity': 66,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 802,
                        'main': 'Clouds',
                        'description': 'scattered clouds',
                        'icon': '03n'
                    }
                ],
                'clouds': {
                    'all': 42
                },
                'wind': {
                    'speed': 9.31,
                    'deg': 302
                },
                'visibility': 10000,
                'pop': 0.21,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-07 00:00:00'
            },
            {
                'dt': 1609988400,
                'main': {
                    'temp': 8.19,
                    'feels_like': 0.02,
                    'temp_min': 8.19,
                    'temp_max': 8.19,
                    'pressure': 1013,
                    'sea_level': 1013,
                    'grnd_level': 989,
                    'humidity': 76,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 500,
                        'main': 'Rain',
                        'description': 'light rain',
                        'icon': '10n'
                    }
                ],
                'clouds': {
                    'all': 100
                },
                'wind': {
                    'speed': 9.85,
                    'deg': 307
                },
                'visibility': 10000,
                'pop': 0.76,
                'rain': {
                    '3h': 0.81
                },
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-07 03:00:00'
            },
            {
                'dt': 1609999200,
                'main': {
                    'temp': 8.17,
                    'feels_like': 0.04,
                    'temp_min': 8.17,
                    'temp_max': 8.17,
                    'pressure': 1013,
                    'sea_level': 1013,
                    'grnd_level': 989,
                    'humidity': 78,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 500,
                        'main': 'Rain',
                        'description': 'light rain',
                        'icon': '10n'
                    }
                ],
                'clouds': {
                    'all': 100
                },
                'wind': {
                    'speed': 9.89,
                    'deg': 317
                },
                'visibility': 10000,
                'pop': 0.73,
                'rain': {
                    '3h': 0.94
                },
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-07 06:00:00'
            },
            {
                'dt': 1610010000,
                'main': {
                    'temp': 8.53,
                    'feels_like': 1.59,
                    'temp_min': 8.53,
                    'temp_max': 8.53,
                    'pressure': 1014,
                    'sea_level': 1014,
                    'grnd_level': 991,
                    'humidity': 79,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04n'
                    }
                ],
                'clouds': {
                    'all': 99
                },
                'wind': {
                    'speed': 8.34,
                    'deg': 326
                },
                'visibility': 10000,
                'pop': 0.03,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-07 09:00:00'
            },
            {
                'dt': 1610020800,
                'main': {
                    'temp': 8.26,
                    'feels_like': 1.7,
                    'temp_min': 8.26,
                    'temp_max': 8.26,
                    'pressure': 1017,
                    'sea_level': 1017,
                    'grnd_level': 993,
                    'humidity': 78,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04n'
                    }
                ],
                'clouds': {
                    'all': 99
                },
                'wind': {
                    'speed': 7.67,
                    'deg': 328
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-07 12:00:00'
            },
            {
                'dt': 1610031600,
                'main': {
                    'temp': 8.38,
                    'feels_like': 2.33,
                    'temp_min': 8.38,
                    'temp_max': 8.38,
                    'pressure': 1019,
                    'sea_level': 1019,
                    'grnd_level': 995,
                    'humidity': 77,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04d'
                    }
                ],
                'clouds': {
                    'all': 94
                },
                'wind': {
                    'speed': 6.92,
                    'deg': 332
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-07 15:00:00'
            },
            {
                'dt': 1610042400,
                'main': {
                    'temp': 9.73,
                    'feels_like': 4.11,
                    'temp_min': 9.73,
                    'temp_max': 9.73,
                    'pressure': 1020,
                    'sea_level': 1020,
                    'grnd_level': 996,
                    'humidity': 71,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04d'
                    }
                ],
                'clouds': {
                    'all': 93
                },
                'wind': {
                    'speed': 6.34,
                    'deg': 345
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-07 18:00:00'
            },
            {
                'dt': 1610053200,
                'main': {
                    'temp': 10.21,
                    'feels_like': 4.69,
                    'temp_min': 10.21,
                    'temp_max': 10.21,
                    'pressure': 1020,
                    'sea_level': 1020,
                    'grnd_level': 996,
                    'humidity': 64,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04d'
                    }
                ],
                'clouds': {
                    'all': 100
                },
                'wind': {
                    'speed': 5.92,
                    'deg': 345
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-07 21:00:00'
            },
            {
                'dt': 1610064000,
                'main': {
                    'temp': 8.57,
                    'feels_like': 2.77,
                    'temp_min': 8.57,
                    'temp_max': 8.57,
                    'pressure': 1021,
                    'sea_level': 1021,
                    'grnd_level': 997,
                    'humidity': 66,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04n'
                    }
                ],
                'clouds': {
                    'all': 100
                },
                'wind': {
                    'speed': 6.04,
                    'deg': 358
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-08 00:00:00'
            },
            {
                'dt': 1610074800,
                'main': {
                    'temp': 6.65,
                    'feels_like': 1.54,
                    'temp_min': 6.65,
                    'temp_max': 6.65,
                    'pressure': 1023,
                    'sea_level': 1023,
                    'grnd_level': 999,
                    'humidity': 71,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04n'
                    }
                ],
                'clouds': {
                    'all': 90
                },
                'wind': {
                    'speed': 4.86,
                    'deg': 13
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-08 03:00:00'
            },
            {
                'dt': 1610085600,
                'main': {
                    'temp': 4.76,
                    'feels_like': 0.55,
                    'temp_min': 4.76,
                    'temp_max': 4.76,
                    'pressure': 1025,
                    'sea_level': 1025,
                    'grnd_level': 1001,
                    'humidity': 78,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 803,
                        'main': 'Clouds',
                        'description': 'broken clouds',
                        'icon': '04n'
                    }
                ],
                'clouds': {
                    'all': 51
                },
                'wind': {
                    'speed': 3.45,
                    'deg': 1
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-08 06:00:00'
            },
            {
                'dt': 1610096400,
                'main': {
                    'temp': 4.11,
                    'feels_like': -0.19,
                    'temp_min': 4.11,
                    'temp_max': 4.11,
                    'pressure': 1025,
                    'sea_level': 1025,
                    'grnd_level': 1000,
                    'humidity': 82,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 800,
                        'main': 'Clear',
                        'description': 'clear sky',
                        'icon': '01n'
                    }
                ],
                'clouds': {
                    'all': 0
                },
                'wind': {
                    'speed': 3.6,
                    'deg': 358
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-08 09:00:00'
            },
            {
                'dt': 1610107200,
                'main': {
                    'temp': 3.63,
                    'feels_like': -0.19,
                    'temp_min': 3.63,
                    'temp_max': 3.63,
                    'pressure': 1026,
                    'sea_level': 1026,
                    'grnd_level': 1002,
                    'humidity': 87,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 800,
                        'main': 'Clear',
                        'description': 'clear sky',
                        'icon': '01n'
                    }
                ],
                'clouds': {
                    'all': 0
                },
                'wind': {
                    'speed': 2.99,
                    'deg': 12
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-08 12:00:00'
            },
            {
                'dt': 1610118000,
                'main': {
                    'temp': 4.55,
                    'feels_like': 0.45,
                    'temp_min': 4.55,
                    'temp_max': 4.55,
                    'pressure': 1028,
                    'sea_level': 1028,
                    'grnd_level': 1003,
                    'humidity': 83,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 800,
                        'main': 'Clear',
                        'description': 'clear sky',
                        'icon': '01d'
                    }
                ],
                'clouds': {
                    'all': 1
                },
                'wind': {
                    'speed': 3.44,
                    'deg': 354
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-08 15:00:00'
            },
            {
                'dt': 1610128800,
                'main': {
                    'temp': 7.65,
                    'feels_like': 3.13,
                    'temp_min': 7.65,
                    'temp_max': 7.65,
                    'pressure': 1027,
                    'sea_level': 1027,
                    'grnd_level': 1003,
                    'humidity': 65,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 801,
                        'main': 'Clouds',
                        'description': 'few clouds',
                        'icon': '02d'
                    }
                ],
                'clouds': {
                    'all': 17
                },
                'wind': {
                    'speed': 3.95,
                    'deg': 347
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-08 18:00:00'
            },
            {
                'dt': 1610139600,
                'main': {
                    'temp': 9.76,
                    'feels_like': 5.17,
                    'temp_min': 9.76,
                    'temp_max': 9.76,
                    'pressure': 1025,
                    'sea_level': 1025,
                    'grnd_level': 1001,
                    'humidity': 50,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 802,
                        'main': 'Clouds',
                        'description': 'scattered clouds',
                        'icon': '03d'
                    }
                ],
                'clouds': {
                    'all': 46
                },
                'wind': {
                    'speed': 3.69,
                    'deg': 348
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-08 21:00:00'
            },
            {
                'dt': 1610150400,
                'main': {
                    'temp': 7.79,
                    'feels_like': 3.57,
                    'temp_min': 7.79,
                    'temp_max': 7.79,
                    'pressure': 1025,
                    'sea_level': 1025,
                    'grnd_level': 1001,
                    'humidity': 57,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 801,
                        'main': 'Clouds',
                        'description': 'few clouds',
                        'icon': '02n'
                    }
                ],
                'clouds': {
                    'all': 23
                },
                'wind': {
                    'speed': 3.15,
                    'deg': 2
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-09 00:00:00'
            },
            {
                'dt': 1610161200,
                'main': {
                    'temp': 6.01,
                    'feels_like': 2.15,
                    'temp_min': 6.01,
                    'temp_max': 6.01,
                    'pressure': 1026,
                    'sea_level': 1026,
                    'grnd_level': 1002,
                    'humidity': 64,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 800,
                        'main': 'Clear',
                        'description': 'clear sky',
                        'icon': '01n'
                    }
                ],
                'clouds': {
                    'all': 1
                },
                'wind': {
                    'speed': 2.62,
                    'deg': 26
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-09 03:00:00'
            },
            {
                'dt': 1610172000,
                'main': {
                    'temp': 4.81,
                    'feels_like': 1.63,
                    'temp_min': 4.81,
                    'temp_max': 4.81,
                    'pressure': 1026,
                    'sea_level': 1026,
                    'grnd_level': 1002,
                    'humidity': 70,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 800,
                        'main': 'Clear',
                        'description': 'clear sky',
                        'icon': '01n'
                    }
                ],
                'clouds': {
                    'all': 0
                },
                'wind': {
                    'speed': 1.67,
                    'deg': 29
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-09 06:00:00'
            },
            {
                'dt': 1610182800,
                'main': {
                    'temp': 3.78,
                    'feels_like': 0.57,
                    'temp_min': 3.78,
                    'temp_max': 3.78,
                    'pressure': 1025,
                    'sea_level': 1025,
                    'grnd_level': 1000,
                    'humidity': 75,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 800,
                        'main': 'Clear',
                        'description': 'clear sky',
                        'icon': '01n'
                    }
                ],
                'clouds': {
                    'all': 7
                },
                'wind': {
                    'speed': 1.7,
                    'deg': 46
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-09 09:00:00'
            },
            {
                'dt': 1610193600,
                'main': {
                    'temp': 3.34,
                    'feels_like': 0.11,
                    'temp_min': 3.34,
                    'temp_max': 3.34,
                    'pressure': 1025,
                    'sea_level': 1025,
                    'grnd_level': 1001,
                    'humidity': 77,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 802,
                        'main': 'Clouds',
                        'description': 'scattered clouds',
                        'icon': '03n'
                    }
                ],
                'clouds': {
                    'all': 35
                },
                'wind': {
                    'speed': 1.71,
                    'deg': 49
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-09 12:00:00'
            },
            {
                'dt': 1610204400,
                'main': {
                    'temp': 3.92,
                    'feels_like': 0.45,
                    'temp_min': 3.92,
                    'temp_max': 3.92,
                    'pressure': 1026,
                    'sea_level': 1026,
                    'grnd_level': 1002,
                    'humidity': 73,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04d'
                    }
                ],
                'clouds': {
                    'all': 100
                },
                'wind': {
                    'speed': 2.03,
                    'deg': 62
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-09 15:00:00'
            },
            {
                'dt': 1610215200,
                'main': {
                    'temp': 7.16,
                    'feels_like': 3.99,
                    'temp_min': 7.16,
                    'temp_max': 7.16,
                    'pressure': 1025,
                    'sea_level': 1025,
                    'grnd_level': 1001,
                    'humidity': 59,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04d'
                    }
                ],
                'clouds': {
                    'all': 91
                },
                'wind': {
                    'speed': 1.63,
                    'deg': 62
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-09 18:00:00'
            },
            {
                'dt': 1610226000,
                'main': {
                    'temp': 9.18,
                    'feels_like': 4.96,
                    'temp_min': 9.18,
                    'temp_max': 9.18,
                    'pressure': 1022,
                    'sea_level': 1022,
                    'grnd_level': 998,
                    'humidity': 51,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 801,
                        'main': 'Clouds',
                        'description': 'few clouds',
                        'icon': '02d'
                    }
                ],
                'clouds': {
                    'all': 13
                },
                'wind': {
                    'speed': 3.1,
                    'deg': 73
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-09 21:00:00'
            },
            {
                'dt': 1610236800,
                'main': {
                    'temp': 7.3,
                    'feels_like': 2.82,
                    'temp_min': 7.3,
                    'temp_max': 7.3,
                    'pressure': 1022,
                    'sea_level': 1022,
                    'grnd_level': 998,
                    'humidity': 59,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 803,
                        'main': 'Clouds',
                        'description': 'broken clouds',
                        'icon': '04n'
                    }
                ],
                'clouds': {
                    'all': 55
                },
                'wind': {
                    'speed': 3.52,
                    'deg': 66
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-10 00:00:00'
            },
            {
                'dt': 1610247600,
                'main': {
                    'temp': 5.93,
                    'feels_like': 1.59,
                    'temp_min': 5.93,
                    'temp_max': 5.93,
                    'pressure': 1024,
                    'sea_level': 1024,
                    'grnd_level': 1000,
                    'humidity': 64,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04n'
                    }
                ],
                'clouds': {
                    'all': 100
                },
                'wind': {
                    'speed': 3.29,
                    'deg': 70
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-10 03:00:00'
            },
            {
                'dt': 1610258400,
                'main': {
                    'temp': 5.27,
                    'feels_like': 0.74,
                    'temp_min': 5.27,
                    'temp_max': 5.27,
                    'pressure': 1025,
                    'sea_level': 1025,
                    'grnd_level': 1000,
                    'humidity': 67,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04n'
                    }
                ],
                'clouds': {
                    'all': 100
                },
                'wind': {
                    'speed': 3.56,
                    'deg': 54
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-10 06:00:00'
            },
            {
                'dt': 1610269200,
                'main': {
                    'temp': 4.12,
                    'feels_like': -1.49,
                    'temp_min': 4.12,
                    'temp_max': 4.12,
                    'pressure': 1026,
                    'sea_level': 1026,
                    'grnd_level': 1001,
                    'humidity': 72,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04n'
                    }
                ],
                'clouds': {
                    'all': 100
                },
                'wind': {
                    'speed': 5.08,
                    'deg': 26
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-10 09:00:00'
            },
            {
                'dt': 1610280000,
                'main': {
                    'temp': 2.89,
                    'feels_like': -1.96,
                    'temp_min': 2.89,
                    'temp_max': 2.89,
                    'pressure': 1027,
                    'sea_level': 1027,
                    'grnd_level': 1003,
                    'humidity': 80,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 500,
                        'main': 'Rain',
                        'description': 'light rain',
                        'icon': '10n'
                    }
                ],
                'clouds': {
                    'all': 100
                },
                'wind': {
                    'speed': 4.05,
                    'deg': 51
                },
                'visibility': 10000,
                'pop': 0.4,
                'rain': {
                    '3h': 0.25
                },
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-10 12:00:00'
            },
            {
                'dt': 1610290800,
                'main': {
                    'temp': 3.11,
                    'feels_like': -1.53,
                    'temp_min': 3.11,
                    'temp_max': 3.11,
                    'pressure': 1030,
                    'sea_level': 1030,
                    'grnd_level': 1005,
                    'humidity': 78,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 600,
                        'main': 'Snow',
                        'description': 'light snow',
                        'icon': '13d'
                    }
                ],
                'clouds': {
                    'all': 100
                },
                'wind': {
                    'speed': 3.72,
                    'deg': 17
                },
                'visibility': 10000,
                'pop': 0.49,
                'snow': {
                    '3h': 0.33
                },
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-10 15:00:00'
            },
            {
                'dt': 1610301600,
                'main': {
                    'temp': 5.58,
                    'feels_like': 0.77,
                    'temp_min': 5.58,
                    'temp_max': 5.58,
                    'pressure': 1030,
                    'sea_level': 1030,
                    'grnd_level': 1005,
                    'humidity': 65,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04d'
                    }
                ],
                'clouds': {
                    'all': 100
                },
                'wind': {
                    'speed': 3.94,
                    'deg': 0
                },
                'visibility': 10000,
                'pop': 0.17,
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-10 18:00:00'
            },
            {
                'dt': 1610312400,
                'main': {
                    'temp': 6.99,
                    'feels_like': 2.09,
                    'temp_min': 6.99,
                    'temp_max': 6.99,
                    'pressure': 1028,
                    'sea_level': 1028,
                    'grnd_level': 1004,
                    'humidity': 59,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 804,
                        'main': 'Clouds',
                        'description': 'overcast clouds',
                        'icon': '04d'
                    }
                ],
                'clouds': {
                    'all': 91
                },
                'wind': {
                    'speed': 4.07,
                    'deg': 353
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'd'
                },
                'dt_txt': '2021-01-10 21:00:00'
            },
            {
                'dt': 1610323200,
                'main': {
                    'temp': 5.46,
                    'feels_like': 1.01,
                    'temp_min': 5.46,
                    'temp_max': 5.46,
                    'pressure': 1029,
                    'sea_level': 1029,
                    'grnd_level': 1005,
                    'humidity': 64,
                    'temp_kf': 0
                },
                'weather': [
                    {
                        'id': 803,
                        'main': 'Clouds',
                        'description': 'broken clouds',
                        'icon': '04n'
                    }
                ],
                'clouds': {
                    'all': 53
                },
                'wind': {
                    'speed': 3.36,
                    'deg': 18
                },
                'visibility': 10000,
                'pop': 0,
                'sys': {
                    'pod': 'n'
                },
                'dt_txt': '2021-01-11 00:00:00'
            }
        ],
        'city': {
            'id': 0,
            'name': 'Dallas',
            'coord': {
                'lat': 33.0005,
                'lon': -96.8314
            },
            'country': 'US',
            'population': 0,
            'timezone': -21600,
            'sunrise': 1609853451,
            'sunset': 1609889672
        },
        'unit': 'metric'
    }

    json_interpreter = json_interpreter()
    json_interpreter.lazy_pass_in(json)
