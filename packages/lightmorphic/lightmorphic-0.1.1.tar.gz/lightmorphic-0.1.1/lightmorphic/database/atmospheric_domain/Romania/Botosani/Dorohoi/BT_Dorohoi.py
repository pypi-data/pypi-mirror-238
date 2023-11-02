import requests, json, datetime, locale
locale.setlocale(locale.LC_TIME, "ro_RO.utf8")

import datetime, unicodedata

def get_atmospheric_data_BT_Dorohoi(adress):
    try:
        res = requests.get(adress)
        weather_data = res.json()
        A = weather_data["current"]
        timp= datetime.datetime.fromtimestamp(int(A["dt"])).strftime('%W \ %A \ %d:%-m:%Y \ %H:%M:%S')
        now_winds = A["wind_speed"]
        now_winddg = A["wind_deg"]
        rasarit= datetime.datetime.fromtimestamp(int(A["sunrise"])).strftime('%H:%M:%S')
        apus= datetime.datetime.fromtimestamp(int(A["sunset"])).strftime('%H:%M:%S')
        now_temp = A["temp"]
        now_pressure = A["pressure"]
        now_humid = A["humidity"]
        now_uvi = A["uvi"]
        now_winds = A["wind_speed"]
        now_winddg = A["wind_deg"]
        now_condition_icon = A["weather"][0]['icon']
        now_condition_en = A["weather"][0]['description']
        now_condition_description = now_condition_en.replace('clear sky', 'cer senin').replace('few clouds', 'nori 10-25%')\
        .replace('scattered clouds', 'nori 25-50%').replace('broken clouds', 'nori 50-85%').replace('overcast clouds', 'nori 85-100%')\
        .replace('light rain', 'ploaie ușoară').replace('moderate rain', 'ploaie moderată').replace('heavy intensity rain', 'ploaie intensă')\
        .replace('very heavy rain', 'ploaie foarte \n puternică').replace('extreme rain', 'ploaie extremă').replace('freezing rain', 'ploaie înghețată')\
        .replace('light intensity shower rain', 'ploaie torențială \n de intensitate mică').replace('shower rain', 'ploaie torențială')\
        .replace('heavy intensity shower rain', 'ploaie torențială \n de intensitate mare').replace('ragged shower rain', 'ploaie torențială \n intermitentă')\
        .replace('thunderstorm with light rain', 'furtună cu \n ploaie slabă').replace('thunderstorm with rain', 'furtună cu ploaie')\
        .replace('thunderstorm with heavy rain', 'furtună cu \n ploaie puternică').replace('light thunderstorm', 'furtună ușoară')\
        .replace('thunderstorm', 'furtună').replace('heavy thunderstorm', 'furtună puternică').replace('ragged thunderstorm', 'furtună intermitentă')\
        .replace('thunderstorm with light drizzle', 'furtună cu \n burniță slabă').replace('thunderstorm with drizzle', 'furtună cu \n burniță')\
        .replace('thunderstorm with heavy drizzle', 'furtună cu \n burniță puternică').replace('light snow', 'zăpadă slabă')\
        .replace('Snow', 'zăpadă').replace('Heavy snow', 'zăpadă puternică').replace('Sleet', 'lapoviță')\
        .replace('Light shower sleet', 'lapoviță \n torențială slabă').replace('Shower sleet', 'lapoviță \n torențială')\
        .replace('Light rain and snow', 'zăpadă și \n ploaie slabă').replace('Rain and snow', 'zăpadă și ploaie')\
        .replace('Light shower snow', 'zăpadă torențială \n slabă').replace('Shower snow', 'zăpadă \n torențială')\
        .replace('Heavy shower snow', 'zăpadă \n torențială puternică').replace('mist', 'ceață')\
        .replace('Smoke', 'ceață').replace('Haze', 'ceață').replace('sand/ dust whirls', 'nisip')\
        .replace('fog', 'ceață').replace('sand', 'nisip').replace('dust', 'praf')\
        .replace('volcanic ash', 'cenușă vulcanică').replace('squalls', 'rafală')\
        .replace('tornado', 'tornadă').replace('light intensity drizzle', 'ploaie maruntă')\
        .replace('drizzle', 'burniță').replace('heavy intensity drizzle', 'burniță \n puternică')\
        .replace('light intensity drizzle rain', 'burniță și \n ploaie slabă').replace('drizzle rain', 'burniță și ploaie')\
        .replace('heavy intensity drizzle rain', 'burniță și \n ploaie puternică').replace('shower rain and drizzle', 'burniță și \n ploaie torențială')\
        .replace('heavy shower rain and drizzle', 'burniță și \n ploaie torențială puternică').replace('shower drizzle', 'burniță torențială')
        
        B = weather_data['daily']
        timp0= datetime.datetime.fromtimestamp(int(B[0]["dt"])).strftime('%W \ %A \ %d:%-m:%Y')
        rasarit0= datetime.datetime.fromtimestamp(int(B[0]["sunrise"])).strftime('%H:%M:%S')
        apus0= datetime.datetime.fromtimestamp(int(B[0]["sunset"])).strftime('%H:%M:%S')
        now_temp_min_0 = B[0]["temp"]['min']
        now_temp_max_0 = B[0]["temp"]['max']
        now_pressure0 = B[0]["pressure"]
        now_humid0 = B[0]["humidity"]
        now_uvi0 = B[0]["uvi"]
        now_condition_icon0 = B[0]["weather"][0]['icon']
        now_condition_en0 = B[0]["weather"][0]['description']
        now_condition_description0 = now_condition_en0.replace('clear sky', 'cer senin').replace('few clouds', 'nori 10-25%')\
        .replace('scattered clouds', 'nori 25-50%').replace('broken clouds', 'nori 50-85%').replace('overcast clouds', 'nori 85-100%')\
        .replace('light rain', 'ploaie ușoară').replace('moderate rain', 'ploaie moderată').replace('heavy intensity rain', 'ploaie intensă')\
        .replace('very heavy rain', 'ploaie foarte \n puternică').replace('extreme rain', 'ploaie extremă').replace('freezing rain', 'ploaie înghețată')\
        .replace('light intensity shower rain', 'ploaie torențială \n de intensitate mică').replace('shower rain', 'ploaie torențială')\
        .replace('heavy intensity shower rain', 'ploaie torențială \n de intensitate mare').replace('ragged shower rain', 'ploaie torențială \n intermitentă')\
        .replace('thunderstorm with light rain', 'furtună cu \n ploaie slabă').replace('thunderstorm with rain', 'furtună cu ploaie')\
        .replace('thunderstorm with heavy rain', 'furtună cu \n ploaie puternică').replace('light thunderstorm', 'furtună ușoară')\
        .replace('thunderstorm', 'furtună').replace('heavy thunderstorm', 'furtună puternică').replace('ragged thunderstorm', 'furtună intermitentă')\
        .replace('thunderstorm with light drizzle', 'furtună cu \n burniță slabă').replace('thunderstorm with drizzle', 'furtună cu \n burniță')\
        .replace('thunderstorm with heavy drizzle', 'furtună cu \n burniță puternică').replace('light snow', 'zăpadă slabă')\
        .replace('Snow', 'zăpadă').replace('Heavy snow', 'zăpadă puternică').replace('Sleet', 'lapoviță')\
        .replace('Light shower sleet', 'lapoviță \n torențială slabă').replace('Shower sleet', 'lapoviță \n torențială')\
        .replace('Light rain and snow', 'zăpadă și \n ploaie slabă').replace('Rain and snow', 'zăpadă și ploaie')\
        .replace('Light shower snow', 'zăpadă torențială \n slabă').replace('Shower snow', 'zăpadă \n torențială')\
        .replace('Heavy shower snow', 'zăpadă \n torențială puternică').replace('mist', 'ceață')\
        .replace('Smoke', 'ceață').replace('Haze', 'ceață').replace('sand/ dust whirls', 'nisip')\
        .replace('fog', 'ceață').replace('sand', 'nisip').replace('dust', 'praf')\
        .replace('volcanic ash', 'cenușă vulcanică').replace('squalls', 'rafală')\
        .replace('tornado', 'tornadă').replace('light intensity drizzle', 'ploaie maruntă')\
        .replace('drizzle', 'burniță').replace('heavy intensity drizzle', 'burniță \n puternică')\
        .replace('light intensity drizzle rain', 'burniță și \n ploaie slabă').replace('drizzle rain', 'burniță și ploaie')\
        .replace('heavy intensity drizzle rain', 'burniță și \n ploaie puternică').replace('shower rain and drizzle', 'burniță și \n ploaie torențială')\
        .replace('heavy shower rain and drizzle', 'burniță și \n ploaie torențială puternică').replace('shower drizzle', 'burniță torențială')

        timp1= datetime.datetime.fromtimestamp(int(B[1]["dt"])).strftime('%W \ %A \ %d:%-m:%Y')
        rasarit1= datetime.datetime.fromtimestamp(int(B[1]["sunrise"])).strftime('%H:%M:%S')
        apus1= datetime.datetime.fromtimestamp(int(B[1]["sunset"])).strftime('%H:%M:%S')
        now_temp_min_1 = B[1]["temp"]['min']
        now_temp_max_1 = B[1]["temp"]['max']
        now_pressure1 = B[1]["pressure"]
        now_humid1 = B[1]["humidity"]
        now_uvi1 = B[1]["uvi"]
        now_condition_icon1 = B[1]["weather"][0]['icon']
        now_condition_en1 = B[1]["weather"][0]['description']
        now_condition_description1 = now_condition_en1.replace('clear sky', 'cer senin').replace('few clouds', 'nori 10-25%')\
        .replace('scattered clouds', 'nori 25-50%').replace('broken clouds', 'nori 50-85%').replace('overcast clouds', 'nori 85-100%')\
        .replace('light rain', 'ploaie ușoară').replace('moderate rain', 'ploaie moderată').replace('heavy intensity rain', 'ploaie intensă')\
        .replace('very heavy rain', 'ploaie foarte \n puternică').replace('extreme rain', 'ploaie extremă').replace('freezing rain', 'ploaie înghețată')\
        .replace('light intensity shower rain', 'ploaie torențială \n de intensitate mică').replace('shower rain', 'ploaie torențială')\
        .replace('heavy intensity shower rain', 'ploaie torențială \n de intensitate mare').replace('ragged shower rain', 'ploaie torențială \n intermitentă')\
        .replace('thunderstorm with light rain', 'furtună cu \n ploaie slabă').replace('thunderstorm with rain', 'furtună cu ploaie')\
        .replace('thunderstorm with heavy rain', 'furtună cu \n ploaie puternică').replace('light thunderstorm', 'furtună ușoară')\
        .replace('thunderstorm', 'furtună').replace('heavy thunderstorm', 'furtună puternică').replace('ragged thunderstorm', 'furtună intermitentă')\
        .replace('thunderstorm with light drizzle', 'furtună cu \n burniță slabă').replace('thunderstorm with drizzle', 'furtună cu \n burniță')\
        .replace('thunderstorm with heavy drizzle', 'furtună cu \n burniță puternică').replace('light snow', 'zăpadă slabă')\
        .replace('Snow', 'zăpadă').replace('Heavy snow', 'zăpadă puternică').replace('Sleet', 'lapoviță')\
        .replace('Light shower sleet', 'lapoviță \n torențială slabă').replace('Shower sleet', 'lapoviță \n torențială')\
        .replace('Light rain and snow', 'zăpadă și \n ploaie slabă').replace('Rain and snow', 'zăpadă și ploaie')\
        .replace('Light shower snow', 'zăpadă torențială \n slabă').replace('Shower snow', 'zăpadă \n torențială')\
        .replace('Heavy shower snow', 'zăpadă \n torențială puternică').replace('mist', 'ceață')\
        .replace('Smoke', 'ceață').replace('Haze', 'ceață').replace('sand/ dust whirls', 'nisip')\
        .replace('fog', 'ceață').replace('sand', 'nisip').replace('dust', 'praf')\
        .replace('volcanic ash', 'cenușă vulcanică').replace('squalls', 'rafală')\
        .replace('tornado', 'tornadă').replace('light intensity drizzle', 'ploaie maruntă')\
        .replace('drizzle', 'burniță').replace('heavy intensity drizzle', 'burniță \n puternică')\
        .replace('light intensity drizzle rain', 'burniță și \n ploaie slabă').replace('drizzle rain', 'burniță și ploaie')\
        .replace('heavy intensity drizzle rain', 'burniță și \n ploaie puternică').replace('shower rain and drizzle', 'burniță și \n ploaie torențială')\
        .replace('heavy shower rain and drizzle', 'burniță și \n ploaie torențială puternică').replace('shower drizzle', 'burniță torențială')

        timp2= datetime.datetime.fromtimestamp(int(B[2]["dt"])).strftime('%W \ %A \ %d:%-m:%Y')
        rasarit2= datetime.datetime.fromtimestamp(int(B[2]["sunrise"])).strftime('%H:%M:%S')
        apus2= datetime.datetime.fromtimestamp(int(B[2]["sunset"])).strftime('%H:%M:%S')
        now_temp_min_2 = B[2]["temp"]['min']
        now_temp_max_2 = B[2]["temp"]['max']
        now_pressure2 = B[2]["pressure"]
        now_humid2 = B[2]["humidity"]
        now_uvi2 = B[2]["uvi"]
        now_condition_icon2 = B[2]["weather"][0]['icon']
        now_condition_en2 = B[2]["weather"][0]['description']
        now_condition_description2 = now_condition_en2.replace('clear sky', 'cer senin').replace('few clouds', 'nori 10-25%')\
        .replace('scattered clouds', 'nori 25-50%').replace('broken clouds', 'nori 50-85%').replace('overcast clouds', 'nori 85-100%')\
        .replace('light rain', 'ploaie ușoară').replace('moderate rain', 'ploaie moderată').replace('heavy intensity rain', 'ploaie intensă')\
        .replace('very heavy rain', 'ploaie foarte \n puternică').replace('extreme rain', 'ploaie extremă').replace('freezing rain', 'ploaie înghețată')\
        .replace('light intensity shower rain', 'ploaie torențială \n de intensitate mică').replace('shower rain', 'ploaie torențială')\
        .replace('heavy intensity shower rain', 'ploaie torențială \n de intensitate mare').replace('ragged shower rain', 'ploaie torențială \n intermitentă')\
        .replace('thunderstorm with light rain', 'furtună cu \n ploaie slabă').replace('thunderstorm with rain', 'furtună cu ploaie')\
        .replace('thunderstorm with heavy rain', 'furtună cu \n ploaie puternică').replace('light thunderstorm', 'furtună ușoară')\
        .replace('thunderstorm', 'furtună').replace('heavy thunderstorm', 'furtună puternică').replace('ragged thunderstorm', 'furtună intermitentă')\
        .replace('thunderstorm with light drizzle', 'furtună cu \n burniță slabă').replace('thunderstorm with drizzle', 'furtună cu \n burniță')\
        .replace('thunderstorm with heavy drizzle', 'furtună cu \n burniță puternică').replace('light snow', 'zăpadă slabă')\
        .replace('Snow', 'zăpadă').replace('Heavy snow', 'zăpadă puternică').replace('Sleet', 'lapoviță')\
        .replace('Light shower sleet', 'lapoviță \n torențială slabă').replace('Shower sleet', 'lapoviță \n torențială')\
        .replace('Light rain and snow', 'zăpadă și \n ploaie slabă').replace('Rain and snow', 'zăpadă și ploaie')\
        .replace('Light shower snow', 'zăpadă torențială \n slabă').replace('Shower snow', 'zăpadă \n torențială')\
        .replace('Heavy shower snow', 'zăpadă \n torențială puternică').replace('mist', 'ceață')\
        .replace('Smoke', 'ceață').replace('Haze', 'ceață').replace('sand/ dust whirls', 'nisip')\
        .replace('fog', 'ceață').replace('sand', 'nisip').replace('dust', 'praf')\
        .replace('volcanic ash', 'cenușă vulcanică').replace('squalls', 'rafală')\
        .replace('tornado', 'tornadă').replace('light intensity drizzle', 'ploaie maruntă')\
        .replace('drizzle', 'burniță').replace('heavy intensity drizzle', 'burniță \n puternică')\
        .replace('light intensity drizzle rain', 'burniță și \n ploaie slabă').replace('drizzle rain', 'burniță și ploaie')\
        .replace('heavy intensity drizzle rain', 'burniță și \n ploaie puternică').replace('shower rain and drizzle', 'burniță și \n ploaie torențială')\
        .replace('heavy shower rain and drizzle', 'burniță și \n ploaie torențială puternică').replace('shower drizzle', 'burniță torențială')

        timp3= datetime.datetime.fromtimestamp(int(B[3]["dt"])).strftime('%W \ %A \ %d:%-m:%Y')
        rasarit3= datetime.datetime.fromtimestamp(int(B[3]["sunrise"])).strftime('%H:%M:%S')
        apus3= datetime.datetime.fromtimestamp(int(B[3]["sunset"])).strftime('%H:%M:%S')
        now_temp_min_3 = B[3]["temp"]['min']
        now_temp_max_3 = B[3]["temp"]['max']
        now_pressure3 = B[3]["pressure"]
        now_humid3 = B[3]["humidity"]
        now_uvi3 = B[3]["uvi"]
        now_condition_icon3 = B[3]["weather"][0]['icon']
        now_condition_en3 = B[3]["weather"][0]['description']
        now_condition_description3 = now_condition_en3.replace('clear sky', 'cer senin').replace('few clouds', 'nori 10-25%')\
        .replace('scattered clouds', 'nori 25-50%').replace('broken clouds', 'nori 50-85%').replace('overcast clouds', 'nori 85-100%')\
        .replace('light rain', 'ploaie ușoară').replace('moderate rain', 'ploaie moderată').replace('heavy intensity rain', 'ploaie intensă')\
        .replace('very heavy rain', 'ploaie foarte \n puternică').replace('extreme rain', 'ploaie extremă').replace('freezing rain', 'ploaie înghețată')\
        .replace('light intensity shower rain', 'ploaie torențială \n de intensitate mică').replace('shower rain', 'ploaie torențială')\
        .replace('heavy intensity shower rain', 'ploaie torențială \n de intensitate mare').replace('ragged shower rain', 'ploaie torențială \n intermitentă')\
        .replace('thunderstorm with light rain', 'furtună cu \n ploaie slabă').replace('thunderstorm with rain', 'furtună cu ploaie')\
        .replace('thunderstorm with heavy rain', 'furtună cu \n ploaie puternică').replace('light thunderstorm', 'furtună ușoară')\
        .replace('thunderstorm', 'furtună').replace('heavy thunderstorm', 'furtună puternică').replace('ragged thunderstorm', 'furtună intermitentă')\
        .replace('thunderstorm with light drizzle', 'furtună cu \n burniță slabă').replace('thunderstorm with drizzle', 'furtună cu \n burniță')\
        .replace('thunderstorm with heavy drizzle', 'furtună cu \n burniță puternică').replace('light snow', 'zăpadă slabă')\
        .replace('Snow', 'zăpadă').replace('Heavy snow', 'zăpadă puternică').replace('Sleet', 'lapoviță')\
        .replace('Light shower sleet', 'lapoviță \n torențială slabă').replace('Shower sleet', 'lapoviță \n torențială')\
        .replace('Light rain and snow', 'zăpadă și \n ploaie slabă').replace('Rain and snow', 'zăpadă și ploaie')\
        .replace('Light shower snow', 'zăpadă torențială \n slabă').replace('Shower snow', 'zăpadă \n torențială')\
        .replace('Heavy shower snow', 'zăpadă \n torențială puternică').replace('mist', 'ceață')\
        .replace('Smoke', 'ceață').replace('Haze', 'ceață').replace('sand/ dust whirls', 'nisip')\
        .replace('fog', 'ceață').replace('sand', 'nisip').replace('dust', 'praf')\
        .replace('volcanic ash', 'cenușă vulcanică').replace('squalls', 'rafală')\
        .replace('tornado', 'tornadă').replace('light intensity drizzle', 'ploaie maruntă')\
        .replace('drizzle', 'burniță').replace('heavy intensity drizzle', 'burniță \n puternică')\
        .replace('light intensity drizzle rain', 'burniță și \n ploaie slabă').replace('drizzle rain', 'burniță și ploaie')\
        .replace('heavy intensity drizzle rain', 'burniță și \n ploaie puternică').replace('shower rain and drizzle', 'burniță și \n ploaie torențială')\
        .replace('heavy shower rain and drizzle', 'burniță și \n ploaie torențială puternică').replace('shower drizzle', 'burniță torențială')

        timp4= datetime.datetime.fromtimestamp(int(B[4]["dt"])).strftime('%W \ %A \ %d:%-m:%Y')
        rasarit4= datetime.datetime.fromtimestamp(int(B[4]["sunrise"])).strftime('%H:%M:%S')
        apus4= datetime.datetime.fromtimestamp(int(B[4]["sunset"])).strftime('%H:%M:%S')
        now_temp_min_4 = B[4]["temp"]['min']
        now_temp_max_4 = B[4]["temp"]['max']
        now_pressure4 = B[4]["pressure"]
        now_humid4 = B[4]["humidity"]
        now_uvi4 = B[4]["uvi"]
        now_condition_icon4 = B[4]["weather"][0]['icon']
        now_condition_en4 = B[4]["weather"][0]['description']
        now_condition_description4 = now_condition_en4.replace('clear sky', 'cer senin').replace('few clouds', 'nori 10-25%')\
        .replace('scattered clouds', 'nori 25-50%').replace('broken clouds', 'nori 50-85%').replace('overcast clouds', 'nori 85-100%')\
        .replace('light rain', 'ploaie ușoară').replace('moderate rain', 'ploaie moderată').replace('heavy intensity rain', 'ploaie intensă')\
        .replace('very heavy rain', 'ploaie foarte \n puternică').replace('extreme rain', 'ploaie extremă').replace('freezing rain', 'ploaie înghețată')\
        .replace('light intensity shower rain', 'ploaie torențială \n de intensitate mică').replace('shower rain', 'ploaie torențială')\
        .replace('heavy intensity shower rain', 'ploaie torențială \n de intensitate mare').replace('ragged shower rain', 'ploaie torențială \n intermitentă')\
        .replace('thunderstorm with light rain', 'furtună cu \n ploaie slabă').replace('thunderstorm with rain', 'furtună cu ploaie')\
        .replace('thunderstorm with heavy rain', 'furtună cu \n ploaie puternică').replace('light thunderstorm', 'furtună ușoară')\
        .replace('thunderstorm', 'furtună').replace('heavy thunderstorm', 'furtună puternică').replace('ragged thunderstorm', 'furtună intermitentă')\
        .replace('thunderstorm with light drizzle', 'furtună cu \n burniță slabă').replace('thunderstorm with drizzle', 'furtună cu \n burniță')\
        .replace('thunderstorm with heavy drizzle', 'furtună cu \n burniță puternică').replace('light snow', 'zăpadă slabă')\
        .replace('Snow', 'zăpadă').replace('Heavy snow', 'zăpadă puternică').replace('Sleet', 'lapoviță')\
        .replace('Light shower sleet', 'lapoviță \n torențială slabă').replace('Shower sleet', 'lapoviță \n torențială')\
        .replace('Light rain and snow', 'zăpadă și \n ploaie slabă').replace('Rain and snow', 'zăpadă și ploaie')\
        .replace('Light shower snow', 'zăpadă torențială \n slabă').replace('Shower snow', 'zăpadă \n torențială')\
        .replace('Heavy shower snow', 'zăpadă \n torențială puternică').replace('mist', 'ceață')\
        .replace('Smoke', 'ceață').replace('Haze', 'ceață').replace('sand/ dust whirls', 'nisip')\
        .replace('fog', 'ceață').replace('sand', 'nisip').replace('dust', 'praf')\
        .replace('volcanic ash', 'cenușă vulcanică').replace('squalls', 'rafală')\
        .replace('tornado', 'tornadă').replace('light intensity drizzle', 'ploaie maruntă')\
        .replace('drizzle', 'burniță').replace('heavy intensity drizzle', 'burniță \n puternică')\
        .replace('light intensity drizzle rain', 'burniță și \n ploaie slabă').replace('drizzle rain', 'burniță și ploaie')\
        .replace('heavy intensity drizzle rain', 'burniță și \n ploaie puternică').replace('shower rain and drizzle', 'burniță și \n ploaie torențială')\
        .replace('heavy shower rain and drizzle', 'burniță și \n ploaie torențială puternică').replace('shower drizzle', 'burniță torențială')

        timp5= datetime.datetime.fromtimestamp(int(B[5]["dt"])).strftime('%W \ %A \ %d:%-m:%Y')
        rasarit5= datetime.datetime.fromtimestamp(int(B[5]["sunrise"])).strftime('%H:%M:%S')
        apus5= datetime.datetime.fromtimestamp(int(B[5]["sunset"])).strftime('%H:%M:%S')
        now_temp_min_5 = B[5]["temp"]['min']
        now_temp_max_5 = B[5]["temp"]['max']
        now_pressure5 = B[5]["pressure"]
        now_humid5 = B[5]["humidity"]
        now_uvi5 = B[5]["uvi"]
        now_condition_icon5 = B[5]["weather"][0]['icon']
        now_condition_en5 = B[5]["weather"][0]['description']
        now_condition_description5 = now_condition_en5.replace('clear sky', 'cer senin').replace('few clouds', 'nori 10-25%')\
        .replace('scattered clouds', 'nori 25-50%').replace('broken clouds', 'nori 50-85%').replace('overcast clouds', 'nori 85-100%')\
        .replace('light rain', 'ploaie ușoară').replace('moderate rain', 'ploaie moderată').replace('heavy intensity rain', 'ploaie intensă')\
        .replace('very heavy rain', 'ploaie foarte \n puternică').replace('extreme rain', 'ploaie extremă').replace('freezing rain', 'ploaie înghețată')\
        .replace('light intensity shower rain', 'ploaie torențială \n de intensitate mică').replace('shower rain', 'ploaie torențială')\
        .replace('heavy intensity shower rain', 'ploaie torențială \n de intensitate mare').replace('ragged shower rain', 'ploaie torențială \n intermitentă')\
        .replace('thunderstorm with light rain', 'furtună cu \n ploaie slabă').replace('thunderstorm with rain', 'furtună cu ploaie')\
        .replace('thunderstorm with heavy rain', 'furtună cu \n ploaie puternică').replace('light thunderstorm', 'furtună ușoară')\
        .replace('thunderstorm', 'furtună').replace('heavy thunderstorm', 'furtună puternică').replace('ragged thunderstorm', 'furtună intermitentă')\
        .replace('thunderstorm with light drizzle', 'furtună cu \n burniță slabă').replace('thunderstorm with drizzle', 'furtună cu \n burniță')\
        .replace('thunderstorm with heavy drizzle', 'furtună cu \n burniță puternică').replace('light snow', 'zăpadă slabă')\
        .replace('Snow', 'zăpadă').replace('Heavy snow', 'zăpadă puternică').replace('Sleet', 'lapoviță')\
        .replace('Light shower sleet', 'lapoviță \n torențială slabă').replace('Shower sleet', 'lapoviță \n torențială')\
        .replace('Light rain and snow', 'zăpadă și \n ploaie slabă').replace('Rain and snow', 'zăpadă și ploaie')\
        .replace('Light shower snow', 'zăpadă torențială \n slabă').replace('Shower snow', 'zăpadă \n torențială')\
        .replace('Heavy shower snow', 'zăpadă \n torențială puternică').replace('mist', 'ceață')\
        .replace('Smoke', 'ceață').replace('Haze', 'ceață').replace('sand/ dust whirls', 'nisip')\
        .replace('fog', 'ceață').replace('sand', 'nisip').replace('dust', 'praf')\
        .replace('volcanic ash', 'cenușă vulcanică').replace('squalls', 'rafală')\
        .replace('tornado', 'tornadă').replace('light intensity drizzle', 'ploaie maruntă')\
        .replace('drizzle', 'burniță').replace('heavy intensity drizzle', 'burniță \n puternică')\
        .replace('light intensity drizzle rain', 'burniță și \n ploaie slabă').replace('drizzle rain', 'burniță și ploaie')\
        .replace('heavy intensity drizzle rain', 'burniță și \n ploaie puternică').replace('shower rain and drizzle', 'burniță și \n ploaie torențială')\
        .replace('heavy shower rain and drizzle', 'burniță și \n ploaie torențială puternică').replace('shower drizzle', 'burniță torențială')

        timp6= datetime.datetime.fromtimestamp(int(B[6]["dt"])).strftime('%W \ %A \ %d:%-m:%Y')
        rasarit6= datetime.datetime.fromtimestamp(int(B[6]["sunrise"])).strftime('%H:%M:%S')
        apus6= datetime.datetime.fromtimestamp(int(B[6]["sunset"])).strftime('%H:%M:%S')
        now_temp_min_6 = B[6]["temp"]['min']
        now_temp_max_6 = B[6]["temp"]['max']
        now_pressure6 = B[6]["pressure"]
        now_humid6 = B[6]["humidity"]
        now_uvi6 = B[6]["uvi"]
        now_condition_icon6 = B[6]["weather"][0]['icon']
        now_condition_en6 = B[6]["weather"][0]['description']
        now_condition_description6 = now_condition_en6.replace('clear sky', 'cer senin').replace('few clouds', 'nori 10-25%')\
        .replace('scattered clouds', 'nori 25-50%').replace('broken clouds', 'nori 50-85%').replace('overcast clouds', 'nori 85-100%')\
        .replace('light rain', 'ploaie ușoară').replace('moderate rain', 'ploaie moderată').replace('heavy intensity rain', 'ploaie intensă')\
        .replace('very heavy rain', 'ploaie foarte \n puternică').replace('extreme rain', 'ploaie extremă').replace('freezing rain', 'ploaie înghețată')\
        .replace('light intensity shower rain', 'ploaie torențială \n de intensitate mică').replace('shower rain', 'ploaie torențială')\
        .replace('heavy intensity shower rain', 'ploaie torențială \n de intensitate mare').replace('ragged shower rain', 'ploaie torențială \n intermitentă')\
        .replace('thunderstorm with light rain', 'furtună cu \n ploaie slabă').replace('thunderstorm with rain', 'furtună cu ploaie')\
        .replace('thunderstorm with heavy rain', 'furtună cu \n ploaie puternică').replace('light thunderstorm', 'furtună ușoară')\
        .replace('thunderstorm', 'furtună').replace('heavy thunderstorm', 'furtună puternică').replace('ragged thunderstorm', 'furtună intermitentă')\
        .replace('thunderstorm with light drizzle', 'furtună cu \n burniță slabă').replace('thunderstorm with drizzle', 'furtună cu \n burniță')\
        .replace('thunderstorm with heavy drizzle', 'furtună cu \n burniță puternică').replace('light snow', 'zăpadă slabă')\
        .replace('Snow', 'zăpadă').replace('Heavy snow', 'zăpadă puternică').replace('Sleet', 'lapoviță')\
        .replace('Light shower sleet', 'lapoviță \n torențială slabă').replace('Shower sleet', 'lapoviță \n torențială')\
        .replace('Light rain and snow', 'zăpadă și \n ploaie slabă').replace('Rain and snow', 'zăpadă și ploaie')\
        .replace('Light shower snow', 'zăpadă torențială \n slabă').replace('Shower snow', 'zăpadă \n torențială')\
        .replace('Heavy shower snow', 'zăpadă \n torențială puternică').replace('mist', 'ceață')\
        .replace('Smoke', 'ceață').replace('Haze', 'ceață').replace('sand/ dust whirls', 'nisip')\
        .replace('fog', 'ceață').replace('sand', 'nisip').replace('dust', 'praf')\
        .replace('volcanic ash', 'cenușă vulcanică').replace('squalls', 'rafală')\
        .replace('tornado', 'tornadă').replace('light intensity drizzle', 'ploaie maruntă')\
        .replace('drizzle', 'burniță').replace('heavy intensity drizzle', 'burniță \n puternică')\
        .replace('light intensity drizzle rain', 'burniță și \n ploaie slabă').replace('drizzle rain', 'burniță și ploaie')\
        .replace('heavy intensity drizzle rain', 'burniță și \n ploaie puternică').replace('shower rain and drizzle', 'burniță și \n ploaie torențială')\
        .replace('heavy shower rain and drizzle', 'burniță și \n ploaie torențială puternică').replace('shower drizzle', 'burniță torențială')

        timp7= datetime.datetime.fromtimestamp(int(B[7]["dt"])).strftime('%W \ %A \ %d:%-m:%Y')
        rasarit7= datetime.datetime.fromtimestamp(int(B[7]["sunrise"])).strftime('%H:%M:%S')
        apus7= datetime.datetime.fromtimestamp(int(B[7]["sunset"])).strftime('%H:%M:%S')
        now_temp_min_7 = B[7]["temp"]['min']
        now_temp_max_7 = B[7]["temp"]['max']
        now_pressure7 = B[7]["pressure"]
        now_humid7 = B[7]["humidity"]
        now_uvi7 = B[7]["uvi"]
        now_condition_icon7 = B[7]["weather"][0]['icon']
        now_condition_en7 = B[7]["weather"][0]['description']
        now_condition_description7 = now_condition_en7.replace('clear sky', 'cer senin').replace('few clouds', 'nori 10-25%')\
        .replace('scattered clouds', 'nori 25-50%').replace('broken clouds', 'nori 50-85%').replace('overcast clouds', 'nori 85-100%')\
        .replace('light rain', 'ploaie ușoară').replace('moderate rain', 'ploaie moderată').replace('heavy intensity rain', 'ploaie intensă')\
        .replace('very heavy rain', 'ploaie foarte \n puternică').replace('extreme rain', 'ploaie extremă').replace('freezing rain', 'ploaie înghețată')\
        .replace('light intensity shower rain', 'ploaie torențială \n de intensitate mică').replace('shower rain', 'ploaie torențială')\
        .replace('heavy intensity shower rain', 'ploaie torențială \n de intensitate mare').replace('ragged shower rain', 'ploaie torențială \n intermitentă')\
        .replace('thunderstorm with light rain', 'furtună cu \n ploaie slabă').replace('thunderstorm with rain', 'furtună cu ploaie')\
        .replace('thunderstorm with heavy rain', 'furtună cu \n ploaie puternică').replace('light thunderstorm', 'furtună ușoară')\
        .replace('thunderstorm', 'furtună').replace('heavy thunderstorm', 'furtună puternică').replace('ragged thunderstorm', 'furtună intermitentă')\
        .replace('thunderstorm with light drizzle', 'furtună cu \n burniță slabă').replace('thunderstorm with drizzle', 'furtună cu \n burniță')\
        .replace('thunderstorm with heavy drizzle', 'furtună cu \n burniță puternică').replace('light snow', 'zăpadă slabă')\
        .replace('Snow', 'zăpadă').replace('Heavy snow', 'zăpadă puternică').replace('Sleet', 'lapoviță')\
        .replace('Light shower sleet', 'lapoviță \n torențială slabă').replace('Shower sleet', 'lapoviță \n torențială')\
        .replace('Light rain and snow', 'zăpadă și \n ploaie slabă').replace('Rain and snow', 'zăpadă și ploaie')\
        .replace('Light shower snow', 'zăpadă torențială \n slabă').replace('Shower snow', 'zăpadă \n torențială')\
        .replace('Heavy shower snow', 'zăpadă \n torențială puternică').replace('mist', 'ceață')\
        .replace('Smoke', 'ceață').replace('Haze', 'ceață').replace('sand/ dust whirls', 'nisip')\
        .replace('fog', 'ceață').replace('sand', 'nisip').replace('dust', 'praf')\
        .replace('volcanic ash', 'cenușă vulcanică').replace('squalls', 'rafală')\
        .replace('tornado', 'tornadă').replace('light intensity drizzle', 'ploaie maruntă')\
        .replace('drizzle', 'burniță').replace('heavy intensity drizzle', 'burniță \n puternică')\
        .replace('light intensity drizzle rain', 'burniță și \n ploaie slabă').replace('drizzle rain', 'burniță și ploaie')\
        .replace('heavy intensity drizzle rain', 'burniță și \n ploaie puternică').replace('shower rain and drizzle', 'burniță și \n ploaie torențială')\
        .replace('heavy shower rain and drizzle', 'burniță și \n ploaie torențială puternică').replace('shower drizzle', 'burniță torențială')

        var0 = str(timp0)+"\n Răsarit = "+str(rasarit0)+"\n Apus = "+str(apus0)+"\n Min (°C) = "+str(now_temp_min_0)+ "\n Max (°C) ="+str(now_temp_max_0)+"\n Presiune = "+str(now_pressure0)+"\n Umiditate (%) = "+str(now_humid0)+"\n Index UV = "+str(now_uvi0)+"\n Stare = "+str(now_condition_description0)
        var1 = str(timp1)+"\n Răsarit = "+str(rasarit1)+"\n Apus = "+str(apus1)+"\n Min (°C) = "+str(now_temp_min_1)+ "\n Max (°C) ="+str(now_temp_max_1)+"\n Presiune = "+str(now_pressure1)+"\n Umiditate (%) = "+str(now_humid1)+"\n Index UV = "+str(now_uvi1)+"\n Stare = "+str(now_condition_description1)
        var2 = str(timp2)+"\n Răsarit = "+str(rasarit2)+"\n Apus = "+str(apus2)+"\n Min (°C) = "+str(now_temp_min_2)+ "\n Max (°C) ="+str(now_temp_max_2)+"\n Presiune = "+str(now_pressure2)+"\n Umiditate (%) = "+str(now_humid2)+"\n Index UV = "+str(now_uvi2)+"\n Stare = "+str(now_condition_description2)
        var3 = str(timp3)+"\n Răsarit = "+str(rasarit3)+"\n Apus = "+str(apus3)+"\n Min (°C) = "+str(now_temp_min_3)+ "\n Max (°C) ="+str(now_temp_max_3)+"\n Presiune = "+str(now_pressure3)+"\n Umiditate (%) = "+str(now_humid3)+"\n Index UV = "+str(now_uvi3)+"\n Stare = "+str(now_condition_description3)
        var4 = str(timp4)+"\n Răsarit = "+str(rasarit4)+"\n Apus = "+str(apus4)+"\n Min (°C) = "+str(now_temp_min_4)+ "\n Max (°C) ="+str(now_temp_max_4)+"\n Presiune = "+str(now_pressure4)+"\n Umiditate (%) = "+str(now_humid4)+"\n Index UV = "+str(now_uvi4)+"\n Stare = "+str(now_condition_description4)
        var5 = str(timp5)+"\n Răsarit = "+str(rasarit5)+"\n Apus = "+str(apus5)+"\n Min (°C) = "+str(now_temp_min_5)+ "\n Max (°C) ="+str(now_temp_max_5)+"\n Presiune = "+str(now_pressure5)+"\n Umiditate (%) = "+str(now_humid5)+"\n Index UV = "+str(now_uvi5)+"\n Stare = "+str(now_condition_description5)
        var6 = str(timp6)+"\n Răsarit = "+str(rasarit6)+"\n Apus = "+str(apus6)+"\n Min (°C) = "+str(now_temp_min_6)+ "\n Max (°C) ="+str(now_temp_max_6)+"\n Presiune = "+str(now_pressure6)+"\n Umiditate (%) = "+str(now_humid6)+"\n Index UV = "+str(now_uvi6)+"\n Stare = "+str(now_condition_description6)
        var7 = str(timp7)+"\n Răsarit = "+str(rasarit7)+"\n Apus = "+str(apus7)+"\n Min (°C) = "+str(now_temp_min_7)+ "\n Max (°C) ="+str(now_temp_max_7)+"\n Presiune = "+str(now_pressure7)+"\n Umiditate (%) = "+str(now_humid7)+"\n Index UV = "+str(now_uvi7)+"\n Stare = "+str(now_condition_description7)
        
        varX= str(["{:<3}".format(" Răsarit = " + str(rasarit) + \
                " Apus = " + str(apus) + " Min (°C) = " + str(now_temp_min_0) + " Max (°C) =" + str(now_temp_max_0) + " Presiune = " + str(now_pressure) + \
                " Umiditate (%) = " + str(now_humid) + " Index UV = " + str(now_uvi) + " Viteza vântului = " + str(now_winds) + " Unghiul vântului = " + str(now_winddg) + \
                " Stare = " + str(now_condition_description))])
#************************************************************
        with open('lightmorphic/database/atmospheric_domain/Romania/Botosani/Dorohoi/Dorohoi_atmospheric_domain_archive_all.txt', 'a') as data_all:
                Y = ["Dorohoi: ", str(timp),"\n", str(weather_data), "\n","\n"]
                data_all.writelines(Y)

        with open('lightmorphic/database/atmospheric_domain/Romania/Botosani/Dorohoi/Dorohoi_atmospheric_domain_archive.txt', 'a') as data_file:
                X = ["Dorohoi: ", str(timp),"\n", varX, "\n"]
                data_file.writelines(X)
#************************************************************
        print('{}: successfully retrieved the atmospheric data.'.format('Dorohoi'))
    except Exception:
        print('\n !!!Error!!! \n Didn\'t retrieve the atmospheric data for Dorohoi. Check if the appid is correct. ')
#************************************************************
if __name__ == "__main__":
        print("The atmospheric data for Dorohoi is running.")
else:
        pass

        
