import requests

class api_caller():
    # Hey there, good chance if you were just running this, you got an error about the line below. If not, congrats on
    # looking at the code in advance! To get your own API key (for free), go to
    # "https://home.openweathermap.org/api_keys". Sign in if you have an account, or just make one. All APIs called
    # here use the free tier as of Jan 4th 2021.
    open_weather_api_key = ""

    country_ISO_3166_dic = {"Afghanistan": "AF", "Åland Islands": "AX", "Albania": "AL", "Algeria": "DZ",
                            "American Samoa": "AS", "Andorra": "AD", "Angola": "AO", "Anguilla": "AI",
                            "Antarctica": "AQ",
                            "Antigua and Barbuda": "AG", "Argentina": "AR", "Armenia": "AM", "Aruba": "AW",
                            "Australia": "AU", "Austria": "AT", "Azerbaijan": "AZ", "The Bahamas": "BS",
                            "Bahrain": "BH",
                            "Bangladesh": "BD", "Barbados": "BB", "Belarus": "BY", "Belgium": "BE", "Belize": "BZ",
                            "Benin": "BJ", "Bermuda": "BM", "Bhutan": "BT", "Plurinational State of Bolivia": "BO",
                            "Bonaire": "BQ", "Saba": "BQ", "Sint Eustatius": "BQ", "Bosnia and Herzegovina": "BA",
                            "Botswana": "BW", "Bouvet Island": "BV", "Brazil": "BR",
                            "The British Indian Ocean Territory": "IO", "Brunei Darussalam": "BN", "Bulgaria": "BG",
                            "Burkina Faso": "BF", "Burundi": "BI", "Cabo Verde": "CV", "Cambodia": "KH",
                            "Cameroon": "CM",
                            "Canada": "CA", "The Cayman Islands": "KY", "The Central African Republic": "CF",
                            "Chad": "TD",
                            "Chile": "CL", "China": "CN", "Christmas Island": "CX", "The Cocos (Keeling) Islands": "CC",
                            "Colombia": "CO", "The Comoros": "KM", "The Democratic Republic of the Congo": "CD",
                            "The Congo": "CG", "The Cook Islands": "CK", "Costa Rica": "CR", "Côte d'Ivoire": "CI",
                            "Croatia": "HR", "Cuba": "CU", "Curaçao": "CW", "Cyprus": "CY", "Czechia": "CZ",
                            "Denmark": "DK", "Djibouti": "DJ", "Dominica": "DM", "The Dominican Republic": "DO",
                            "Ecuador": "EC", "Egypt": "EG", "El Salvador": "SV", "Equatorial Guinea": "GQ",
                            "Eritrea": "ER",
                            "Estonia": "EE", "Eswatini": "SZ", "Ethiopia": "ET",
                            "The Falkland Islands [Malvinas]": "FK",
                            "The Faroe Islands": "FO", "Fiji": "FJ", "Finland": "FI", "France": "FR",
                            "French Guiana": "GF",
                            "French Polynesia": "PF", "The French Southern Territories": "TF", "Gabon": "GA",
                            "The Gambia": "GM", "Georgia": "GE", "Germany": "DE", "Ghana": "GH", "Gibraltar": "GI",
                            "Greece": "GR", "Greenland": "GL", "Grenada": "GD", "Guadeloupe": "GP", "Guam": "GU",
                            "Guatemala": "GT", "Guernsey": "GG", "Guinea": "GN", "Guinea-Bissau": "GW", "Guyana": "GY",
                            "Haiti": "HT", "Heard Island and McDonald Islands": "HM", "The Holy See": "VA",
                            "Honduras": "HN", "Hong Kong": "HK", "Hungary": "HU", "Iceland": "IS", "India": "IN",
                            "Indonesia": "ID", "Islamic Republic of Iran": "IR", "Iraq": "IQ", "Ireland": "IE",
                            "Isle of Man": "IM", "Israel": "IL", "Italy": "IT", "Jamaica": "JM", "Japan": "JP",
                            "Jersey": "JE", "Jordan": "JO", "Kazakhstan": "KZ", "Kenya": "KE", "Kiribati": "KI",
                            "The Democratic People's Republic of Korea": "KP", "The Republic of Korea": "KR",
                            "Kuwait": "KW", "Kyrgyzstan": "KG", "The Lao People's Democratic Republic": "LA",
                            "Latvia": "LV", "Lebanon": "LB", "Lesotho": "LS", "Liberia": "LR", "Libya": "LY",
                            "Liechtenstein": "LI", "Lithuania": "LT", "Luxembourg": "LU", "Macao": "MO",
                            "North Macedonia": "MK", "Madagascar": "MG", "Malawi": "MW", "Malaysia": "MY",
                            "Maldives": "MV",
                            "Mali": "ML", "Malta": "MT", "The Marshall Islands": "MH", "Martinique": "MQ",
                            "Mauritania": "MR", "Mauritius": "MU", "Mayotte": "YT", "Mexico": "MX",
                            "Federated States of Micronesia": "FM", "The Republic of Moldova": "MD", "Monaco": "MC",
                            "Mongolia": "MN", "Montenegro": "ME", "Montserrat": "MS", "Morocco": "MA",
                            "Mozambique": "MZ",
                            "Myanmar": "MM", "Namibia": "NA", "Nauru": "NR", "Nepal": "NP", "The Netherlands": "NL",
                            "New Caledonia": "NC", "New Zealand": "NZ", "Nicaragua": "NI", "The Niger": "NE",
                            "Nigeria": "NG", "Niue": "NU", "Norfolk Island": "NF", "The Northern Mariana Islands": "MP",
                            "Norway": "NO", "Oman": "OM", "Pakistan": "PK", "Palau": "PW", "State of Palestine": "PS",
                            "Panama": "PA", "Papua New Guinea": "PG", "Paraguay": "PY", "Peru": "PE",
                            "The Philippines": "PH", "Pitcairn": "PN", "Poland": "PL", "Portugal": "PT",
                            "Puerto Rico": "PR", "Qatar": "QA", "Réunion": "RE", "Romania": "RO",
                            "The Russian Federation": "RU", "Rwanda": "RW", "Saint Barthélemy": "BL",
                            "Saint Kitts and Nevis": "KN", "Saint Lucia": "LC", "Saint Martin (French part)": "MF",
                            "Saint Pierre and Miquelon": "PM", "Saint Vincent and the Grenadines": "VC",
                            "Saint Helena": "SH", "Ascension Island": "SH", "Tristan da Cunha": "SH", "Samoa": "WS",
                            "San Marino": "SM", "Sao Tome and Principe": "ST", "Saudi Arabia": "SA", "Senegal": "SN",
                            "Serbia": "RS", "Seychelles": "SC", "Sierra Leone": "SL", "Singapore": "SG",
                            "Sint Maarten (Dutch part)": "SX", "Slovakia": "SK", "Slovenia": "SI",
                            "Solomon Islands": "SB",
                            "Somalia": "SO", "South Africa": "ZA", "South Georgia and the South Sandwich Islands": "GS",
                            "South Sudan": "SS", "Spain": "ES", "Sri Lanka": "LK", "The Sudan": "SD", "Suriname": "SR",
                            "Svalbard": "SJ", "Jan Mayen": "SJ", "Sweden": "SE", "Switzerland": "CH",
                            "The Syrian Arab Republic": "SY", "Taiwan": "TW", "Tajikistan": "TJ",
                            "The United Republic of Tanzania": "TZ", "Thailand": "TH", "Timor-Leste": "TL",
                            "Togo": "TG",
                            "Tokelau": "TK", "Tonga": "TO", "Trinidad and Tobago": "TT", "Tunisia": "TN",
                            "Turkey": "TR",
                            "Turkmenistan": "TM", "The Turks and Caicos Islands": "TC", "Tuvalu": "TV", "Uganda": "UG",
                            "Ukraine": "UA", "United Arab Emirates": "AE",
                            "The United Kingdom of Great Britain and Northern Ireland": "GB",
                            "The United States Minor Outlying Islands": "UM", "The United States of America": "US",
                            "USA": "US", "Uruguay": "UY", "Uzbekistan": "UZ", "Vanuatu": "VU",
                            "Bolivarian Republic of Venezuela": "VE", "Viet Nam": "VN",
                            "Virgin Islands (British)": "VG",
                            "Virgin Islands (U.S.)": "VI", "Wallis and Futuna": "WF", "Western Sahara": "EH",
                            "Yemen": "YE",
                            "Zambia": "ZM", "Zimbabwe": "ZW"}

    def __init__(self):
        pass

    def convert_country_to_iso_3166(self, country_name):
        return self.country_ISO_3166_dic[country_name]

    def get_weather_today(self, country_name, zip_code, unit):
        country_code = self.convert_country_to_iso_3166(country_name)
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={self.open_weather_api_key}&units={unit}"
        response = requests.get(url)
        # print(f"API Call: '{url}'")
        # print("Response Code: " + str(response.status_code))
        # print(response.json())
        return self.response_handler(response, unit)

    def get_5_day_forecast(self, country_name, zip_code, unit):
        country_code = self.convert_country_to_iso_3166(country_name)
        url = f"http://api.openweathermap.org/data/2.5/forecast?zip={zip_code},{country_code}&appid={self.open_weather_api_key}&units={unit}"
        response = requests.get(url)
        # print(f"API Call: '{url}'")
        # print("Response Code: " + str(response.status_code))
        # print(response.json())
        return self.response_handler(response, unit)

    def response_handler(self, response, unit):
        if response.status_code == 200:
            json = response.json()
            json["unit"] = unit
            return json
        else:
            return None


if __name__ == "__main__":
    api_caller = api_caller()

    print("//Current Weather Data")
    print(api_caller.get_weather_today("USA", 75287, True))
    print("")

    print("//5 Day Forecast")
    print(api_caller.get_5_day_forecast("USA", 75287, True))
    print()
