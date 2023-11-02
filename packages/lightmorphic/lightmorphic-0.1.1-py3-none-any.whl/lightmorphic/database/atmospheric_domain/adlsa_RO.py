#!/usr/bin/env python3

"""
===================================================
Created on Mon May 29 19:00:00 2023
===================================================
@author: ARXDE™
===================================================
This module contains the atmospheric domain functionality
for the lightmorphic signature analysis (adlsa)
===================================================
"""
from sys import path

path += ['Romania/Alba/Abrud', 'Romania/Alba/Aiud', 'Romania/Alba/Alba_Iulia', 'Romania/Alba/Baia_de_Aries', 'Romania/Alba/Blaj', 'Romania/Alba/Campeni', 'Romania/Alba/Cugir', 'Romania/Alba/Ocna_Mures', 'Romania/Alba/Sebes', 'Romania/Alba/Teius', 'Romania/Alba/Zlatna',
                'Romania/Arad/Arad', 'Romania/Arad/Chisineu_Cris', 'Romania/Arad/Curtici', 'Romania/Arad/Ineu', 'Romania/Arad/Lipova', 'Romania/Arad/Nadlac', 'Romania/Arad/Pancota', 'Romania/Arad/Pecica', 'Romania/Arad/Santana', 
                'Romania/Arges/Campulung', 'Romania/Arges/Costesti', 'Romania/Arges/Curtea_de_Arges', 'Romania/Arges/Mioveni', 'Romania/Arges/Pitesti', 'Romania/Arges/Stefanesti', 'Romania/Arges/Topoloveni', 
                'Romania/Bacau/Bacau', 'Romania/Bacau/Buhusi', 'Romania/Bacau/Comanesti', 'Romania/Bacau/Darmanesti', 'Romania/Bacau/Moinesti', 'Romania/Bacau/Onesti', 'Romania/Bacau/Slanic_Moldova', 'Romania/Bacau/Targu_Ocna', 
                'Romania/Bihor/Alesd', 'Romania/Bihor/Beius', 'Romania/Bihor/Marghita', 'Romania/Bihor/Nucet', 'Romania/Bihor/Oradea', 'Romania/Bihor/Sacueni', 'Romania/Bihor/Salonta', 'Romania/Bihor/Stei', 'Romania/Bihor/Valea_lui_Mihai', 'Romania/Bihor/Vascau', 
                'Romania/Bistrita_Nasaud/Beclean', 'Romania/Bistrita_Nasaud/Bistrita', 'Romania/Bistrita_Nasaud/Nasaud', 'Romania/Bistrita_Nasaud/Sangeorz_Bai', 
                'Romania/Botosani/Botosani', 'Romania/Botosani/Bucecea', 'Romania/Botosani/Darabani', 'Romania/Botosani/Dorohoi', 'Romania/Botosani/Flamanzi', 'Romania/Botosani/Saveni', 'Romania/Botosani/Stefanesti', 
                'Romania/Braila/Braila', 'Romania/Braila/Faurei', 'Romania/Braila/Ianca', 'Romania/Braila/Insuratei', 
                'Romania/Brasov/Brasov', 'Romania/Brasov/Codlea', 'Romania/Brasov/Fagaras', 'Romania/Brasov/Ghimbav', 'Romania/Brasov/Predeal', 'Romania/Brasov/Rasnov', 'Romania/Brasov/Rupea', 'Romania/Brasov/Sacele', 'Romania/Brasov/Victoria', 'Romania/Brasov/Zarnesti', 
                'Romania/Bucuresti', 
                'Romania/Buzau/Buzau', 'Romania/Buzau/Nehoiu', 'Romania/Buzau/Patarlagele', 'Romania/Buzau/Pogoanele', 'Romania/Buzau/Ramnicu_Sarat',
                'Romania/Calarasi/Budesti', 'Romania/Calarasi/Calarasi', 'Romania/Calarasi/Fundulea', 'Romania/Calarasi/Lehliu_Gara', 'Romania/Calarasi/Oltenita', 
                'Romania/Caras_Severin/Anina', 'Romania/Caras_Severin/Baile_Herculane', 'Romania/Caras_Severin/Bocsa', 'Romania/Caras_Severin/Caransebes', 'Romania/Caras_Severin/Moldova_Noua', 'Romania/Caras_Severin/Oravita', 'Romania/Caras_Severin/Otelu_Rosu', 'Romania/Caras_Severin/Resita', 
                'Romania/Cluj_Napoca/Campia_Turzii', 'Romania/Cluj_Napoca/Cluj_Napoca', 'Romania/Cluj_Napoca/Dej', 'Romania/Cluj_Napoca/Gherla', 'Romania/Cluj_Napoca/Huedin', 'Romania/Cluj_Napoca/Turda' , 
                'Romania/Constanta/Cernavoda', 'Romania/Constanta/Constanta', 'Romania/Constanta/Eforie', 'Romania/Constanta/Harsova', 'Romania/Constanta/Mangalia', 'Romania/Constanta/Medgidia', 'Romania/Constanta/Murfatlar', 'Romania/Constanta/Navodari', 'Romania/Constanta/Negru_Voda', 'Romania/Constanta/Ovidiu', 'Romania/Constanta/Techirghiol', 
                'Romania/Covasna/Baraolt', 'Romania/Covasna/Covasna', 'Romania/Covasna/Intorsura_Buzaului', 'Romania/Covasna/Sfantu_Gheorghe', 'Romania/Covasna/Targu_Secuiesc' , 
                'Romania/Dambovita/Fieni', 'Romania/Dambovita/Gaesti', 'Romania/Dambovita/Moreni', 'Romania/Dambovita/Pucioasa', 'Romania/Dambovita/Racari', 'Romania/Dambovita/Targoviste', 'Romania/Dambovita/Titu', 
                'Romania/Dolj/Bailesti', 'Romania/Dolj/Bechet', 'Romania/Dolj/Calafat', 'Romania/Dolj/Craiova', 'Romania/Dolj/Dabuleni', 'Romania/Dolj/Filiasi', 'Romania/Dolj/Segarcea', 
                'Romania/Galati/Beresti', 'Romania/Galati/Galati', 'Romania/Galati/Targu_Bujor', 'Romania/Galati/Tecuci', 
                'Romania/Giurgiu/Bolintin_Vale', 'Romania/Giurgiu/Giurgiu', 'Romania/Giurgiu/Mihailesti', 
                'Romania/Gorj/Bumbesti_Jiu', 'Romania/Gorj/Motru', 'Romania/Gorj/Novaci', 'Romania/Gorj/Rovinari', 'Romania/Gorj/Targu_Carbunesti', 'Romania/Gorj/Targu_Jiu', 'Romania/Gorj/Ticleni', 'Romania/Gorj/Tismana', 
                'Romania/Harghita/Baile_Tusnad', 'Romania/Harghita/Balan', 'Romania/Harghita/Borsec', 'Romania/Harghita/Cristuru_Secuiesc', 'Romania/Harghita/Gheorgheni', 'Romania/Harghita/Miercurea_Ciuc', 'Romania/Harghita/Odorheiu_Secuiesc', 'Romania/Harghita/Toplita', 'Romania/Harghita/Vlahita', 
                'Romania/Hunedoara/Deva', 'Romania/Hunedoara/Aninoasa', 'Romania/Hunedoara/Brad', 'Romania/Hunedoara/Calan','Romania/Hunedoara/Geoagiu', 'Romania/Hunedoara/Hateg', 'Romania/Hunedoara/Hunedoara', 'Romania/Hunedoara/Lupeni', 'Romania/Hunedoara/Orastie', 'Romania/Hunedoara/Petrila', 'Romania/Hunedoara/Petrosani', 'Romania/Hunedoara/Simeria', 'Romania/Hunedoara/Uricani', 'Romania/Hunedoara/Vulcan'
                'Romania/Ialomita/Amara', 'Romania/Ialomita/Cazanesti', 'Romania/Ialomita/Fetesti', 'Romania/Ialomita/Fierbinti_Targ', 'Romania/Ialomita/Slobozia', 'Romania/Ialomita/Tandarei', 'Romania/Ialomita/Urziceni',
                'Romania/Iasi/Harlau', 'Romania/Iasi/Iasi', 'Romania/Iasi/Pascani', 'Romania/Iasi/Podu_Iloaiei', 'Romania/Iasi/Targu_Frumos',
                'Romania/Ilfov/Bragadiru', 'Romania/Ilfov/Buftea', 'Romania/Ilfov/Chitila', 'Romania/Ilfov/Magurele', 'Romania/Ilfov/Otopeni', 'Romania/Ilfov/Pantelimon', 'Romania/Ilfov/Popesti_Leordeni', 'Romania/Ilfov/Voluntari',
                'Romania/Maramures/Baia_Mare', 'Romania/Maramures/Baia_Sprie', 'Romania/Maramures/Borsa', 'Romania/Maramures/Cavnic', 'Romania/Maramures/Dragomiresti', 'Romania/Maramures/Salistea_de_Sus', 'Romania/Maramures/Seini', 'Romania/Maramures/Sighetu_Marmatiei', 'Romania/Maramures/Somcuta_Mare', 'Romania/Maramures/Targu_Lapus', 'Romania/Maramures/Tautii_Magheraus', 'Romania/Maramures/Ulmeni', 'Romania/Maramures/Viseu_de_Sus',
                'Romania/Mehedinti/Baia_de_Arama', 'Romania/Mehedinti/Drobeta_Turnu_Severin', 'Romania/Mehedinti/Orsova', 'Romania/Mehedinti/Strehaia', 'Romania/Mehedinti/Vanju_Mare''Romania/Mehedinti/Baia_de_Arama', 'Romania/Mehedinti/Drobeta_Turnu_Severin', 'Romania/Mehedinti/Orsova', 'Romania/Mehedinti/Strehaia', 'Romania/Mehedinti/Vanju_Mare',
                'Romania/Mures/Iernut', 'Romania/Mures/Ludus', 'Romania/Mures/Miercurea_Nirajului', 'Romania/Mures/Reghin', 'Romania/Mures/Sangeorgiu_de_Padure', 'Romania/Mures/Sarmasu', 'Romania/Mures/Sighisoara', 'Romania/Mures/Sovata', 'Romania/Mures/Targu_Mures', 'Romania/Mures/Tarnaveni', 'Romania/Mures/Ungheni',
                 'Romania/Neamt/Bicaz', 'Romania/Neamt/Piatra_Neamt', 'Romania/Neamt/Roman', 'Romania/Neamt/Roznov', 'Romania/Neamt/Targu_Neamt',
                 'Romania/Olt/Bals', 'Romania/Olt/Caracal', 'Romania/Olt/Corabia', 'Romania/Olt/Draganesti_Olt', 'Romania/Olt/Piatra_Olt', 'Romania/Olt/Potcoava', 'Romania/Olt/Scornicesti', 'Romania/Olt/Slatina',
                 'Romania/Prahova/Azuga', 'Romania/Prahova/Baicoi', 'Romania/Prahova/Boldesti_Scaeni', 'Romania/Prahova/Breaza', 'Romania/Prahova/Busteni', 'Romania/Prahova/Campina', 'Romania/Prahova/Comarnic', 'Romania/Prahova/Mizil', 'Romania/Prahova/Ploiesti', 'Romania/Prahova/Plopeni', 'Romania/Prahova/Sinaia', 'Romania/Prahova/Slanic', 'Romania/Prahova/Urlati', 'Romania/Prahova/Valenii_de_Munte',
                 'Romania/Salaj/Cehu_Silvaniei', 'Romania/Salaj/Jibou', 'Romania/Salaj/Simleu_Silvaniei', 'Romania/Salaj/Zalau',
                 'Romania/Satu_Mare/Ardud', 'Romania/Satu_Mare/Carei', 'Romania/Satu_Mare/Livada', 'Romania/Satu_Mare/Negresti_Oas', 'Romania/Satu_Mare/Satu_Mare', 'Romania/Satu_Mare/Tasnad',
                 'Romania/Sibiu/Agnita', 'Romania/Sibiu/Avrig', 'Romania/Sibiu/Cisnadie', 'Romania/Sibiu/Copsa_Mica', 'Romania/Sibiu/Dumbraveni', 'Romania/Sibiu/Medias', 'Romania/Sibiu/Miercurea_Sibiului', 'Romania/Sibiu/Ocna_Sibiului', 'Romania/Sibiu/Saliste', 'Romania/Sibiu/Sibiu', 'Romania/Sibiu/Talmaciu',
                 'Romania/Suceava/Brosteni', 'Romania/Suceava/Cajvana', 'Romania/Suceava/Campulung_Moldovenesc', 'Romania/Suceava/Dolhasca', 'Romania/Suceava/Falticeni', 'Romania/Suceava/Frasin', 'Romania/Suceava/Gura_Humorului', 'Romania/Suceava/Liteni', 'Romania/Suceava/Milisauti', 'Romania/Suceava/Radauti', 'Romania/Suceava/Salcea', 'Romania/Suceava/Siret', 'Romania/Suceava/Solca', 'Romania/Suceava/Suceava', 'Romania/Suceava/Vatra_Dornei', 'Romania/Suceava/Vicovu_de_Sus',
                 'Romania/Teleorman/Alexandria', 'Romania/Teleorman/Rosiorii_de_Vede', 'Romania/Teleorman/Turnu_Magurele', 'Romania/Teleorman/Videle', 'Romania/Teleorman/Zimnicea',
                 'Romania/Timis/Buzias', 'Romania/Timis/Ciacova', 'Romania/Timis/Deta', 'Romania/Timis/Faget', 'Romania/Timis/Gataia', 'Romania/Timis/Jimbolia', 'Romania/Timis/Lugoj', 'Romania/Timis/Recas', 'Romania/Timis/Sannicolau_Mare', 'Romania/Timis/Timisoara',
                 'Romania/Tulcea/Babadag', 'Romania/Tulcea/Isaccea', 'Romania/Tulcea/Macin', 'Romania/Tulcea/Sulina', 'Romania/Tulcea/Tulcea',
                 'Romania/Valcea/Babeni', 'Romania/Valcea/Baile_Govora', 'Romania/Valcea/Baile_Olanesti', 'Romania/Valcea/Balcesti', 'Romania/Valcea/Berbesti', 'Romania/Valcea/Brezoi', 'Romania/Valcea/Calimanesti', 'Romania/Valcea/Dragasani', 'Romania/Valcea/Horezu', 'Romania/Valcea/Ocnele_Mari', 'Romania/Valcea/Ramnicu_Valcea',
                 'Romania/Vaslui/Barlad', 'Romania/Vaslui/Husi', 'Romania/Vaslui/Murgeni', 'Romania/Vaslui/Negresti', 'Romania/Vaslui/Vaslui',
                 'Romania/Vrancea/Adjud', 'Romania/Vrancea/Focsani', 'Romania/Vrancea/Marasesti', 'Romania/Vrancea/Odobesti', 'Romania/Vrancea/Panciu'         
                 ]

def error_msg(city):
        msg =  '''!!! Error!!!. Retry the call to the OpenWeather One Call API for {}. Or check if the call was done correctly in module adlsa_RO.'''.format(city)
        return msg

def atmospheric_data(city, appid):
        if city in ['Deva', 'deva']:
                try:
                        get_atmospheric_data_HD_Deva('https://api.openweathermap.org/data/2.5/onecall?lat=45.866257&lon=22.914374&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Aninoasa', 'aninoasa']:
                try:
                        get_atmospheric_data_HD_Aninoasa('https://api.openweathermap.org/data/2.5/onecall?lat=45.409241&lon=23.31505&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Brad', 'brad']:
                try:
                        get_atmospheric_data_HD_Brad('https://api.openweathermap.org/data/2.5/onecall?lat=46.133331&lon=22.783331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Calan', 'calan']:
                try:
                        get_atmospheric_data_HD_Calan('https://api.openweathermap.org/data/2.5/onecall?lat=45.73333&lon=22.98333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Geoagiu', 'geoagiu']:
                try:
                        get_atmospheric_data_HD_Geoagiu('https://api.openweathermap.org/data/2.5/onecall?lat=45.9191&lon=23.202&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Hateg', 'hateg']:
                try:
                        get_atmospheric_data_HD_Hateg('https://api.openweathermap.org/data/2.5/onecall?lat=45.6027&lon=22.9526&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Hunedoara', 'hunedoara']:
                try:
                        get_atmospheric_data_HD_Hunedoara('https://api.openweathermap.org/data/2.5/onecall?lat=45.75&lon=23.0&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Lupeni', 'lupeni']:
                try:
                        get_atmospheric_data_HD_Lupeni('https://api.openweathermap.org/data/2.5/onecall?lat=46.383331&lon=25.216669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Orastie', 'orastie']:
                try:
                        get_atmospheric_data_HD_Orastie('https://api.openweathermap.org/data/2.5/onecall?lat=45.8324&lon=23.1965&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Petrila', 'petrila']:
                try:
                        get_atmospheric_data_HD_Petrila('https://api.openweathermap.org/data/2.5/onecall?lat=45.450001&lon=23.41667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Petrosani', 'petrosani']:
                try:
                        get_atmospheric_data_HD_Petrosani('https://api.openweathermap.org/data/2.5/onecall?lat=45.4084&lon=23.3815&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Simeria', 'simeria']:
                try:
                        get_atmospheric_data_HD_Simeria('https://api.openweathermap.org/data/2.5/onecall?lat=45.849998&lon=23.01667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Uricani', 'uricani']:
                try:
                        get_atmospheric_data_HD_Uricani('https://api.openweathermap.org/data/2.5/onecall?lat=45.337311&lon=23.152399&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Vulcan', 'vulcan']:
                try:
                        get_atmospheric_data_HD_Vulcan('https://api.openweathermap.org/data/2.5/onecall?lat=45.383331&lon=23.26667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Abrud', 'abrud']:
                try:
                        get_atmospheric_data_AB_Abrud('https://api.openweathermap.org/data/2.5/onecall?lat=46.26667&lon=23.066669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Aiud', 'aiud']:
                try:
                        get_atmospheric_data_AB_Aiud('https://api.openweathermap.org/data/2.5/onecall?lat=46.299999&lon=23.716669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Alba Iulia', 'alba iulia']:
                try:
                        get_atmospheric_data_AB_Alba_Iulia('https://api.openweathermap.org/data/2.5/onecall?lat=46.066669&lon=23.58333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Baia de Aries', 'baia de aries']:
                try:
                        get_atmospheric_data_AB_Baia_de_Aries('https://api.openweathermap.org/data/2.5/onecall?lat=46.3807&lon=23.2823&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Blaj', 'blaj']:
                try:
                        get_atmospheric_data_AB_Blaj('https://api.openweathermap.org/data/2.5/onecall?lat=46.183331&lon=23.91667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Campeni', 'campeni']:
                try:
                        get_atmospheric_data_AB_Campeni('https://api.openweathermap.org/data/2.5/onecall?lat=46.366669&lon=23.049999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Cugir', 'cugir']:
                try:
                        get_atmospheric_data_AB_Cugir('https://api.openweathermap.org/data/2.5/onecall?lat=45.833328&lon=23.366671&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ocna Mures', 'ocna mures']:
                try:
                        get_atmospheric_data_AB_Ocna_Mures('https://api.openweathermap.org/data/2.5/onecall?lat=46.3824&lon=23.8638&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sebes', 'sebes']:
                try:
                        get_atmospheric_data_AB_Sebes('https://api.openweathermap.org/data/2.5/onecall?lat=45.9553&lon=23.5737&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Teius', 'teius']:
                try:
                        get_atmospheric_data_AB_Teius('https://api.openweathermap.org/data/2.5/onecall?lat=46.2021&lon=23.6697&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Zlatna', 'zlatna']:
                try:
                        get_atmospheric_data_AB_Zlatna('https://api.openweathermap.org/data/2.5/onecall?lat=46.2021&lon=23.6697&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Arad', 'arad']:
                try:
                        get_atmospheric_data_AR_Arad('https://api.openweathermap.org/data/2.5/onecall?lat=46.333328&lon=21.75&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Chisineu Cris', 'chisineu cris']:
                try:
                        get_atmospheric_data_AR_Chisineu_Cris('https://api.openweathermap.org/data/2.5/onecall?lat=46.5242&lon=21.5199&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Curtici', 'curtici']:
                try:
                        get_atmospheric_data_AR_Curtici('https://api.openweathermap.org/data/2.5/onecall?lat=46.349998&lon=21.299999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ineu', 'ineu']:
                try:
                        get_atmospheric_data_AR_Ineu('https://api.openweathermap.org/data/2.5/onecall?lat=46.433331&lon=21.85&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Lipova', 'lipova']:
                try:
                        get_atmospheric_data_AR_Lipova('https://api.openweathermap.org/data/2.5/onecall?lat=46.083328&lon=21.700001&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Nadlac', 'nadlac']:
                try:
                        get_atmospheric_data_AR_Nadlac('https://api.openweathermap.org/data/2.5/onecall?lat=46.166672&lon=20.75&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Pancota', 'pancota']:
                try:
                        get_atmospheric_data_AR_Pancota('https://api.openweathermap.org/data/2.5/onecall?lat=46.333328&lon=21.700001&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Pecica', 'pecica']:
                try:
                        get_atmospheric_data_AR_Pecica('https://api.openweathermap.org/data/2.5/onecall?lat=46.166672&lon=21.066669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Santana', 'santana']:
                try:
                        get_atmospheric_data_AR_Santana('https://api.openweathermap.org/data/2.5/onecall?lat=46.349998&lon=21.5&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Campulung', 'campulung']:
                try:
                        get_atmospheric_data_AG_Campulung('https://api.openweathermap.org/data/2.5/onecall?lat=45.26667&lon=25.049999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Costesti', 'costesti']:
                try:
                        get_atmospheric_data_AG_Costesti('https://api.openweathermap.org/data/2.5/onecall?lat=44.661&lon=24.8794&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Curtea de Arges', 'curtea de arges']:
                try:
                        get_atmospheric_data_AG_Curtea_de_Arges('https://api.openweathermap.org/data/2.5/onecall?lat=45.1406&lon=24.6685&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Mioveni', 'mioveni']:
                try:
                        get_atmospheric_data_AG_Mioveni('https://api.openweathermap.org/data/2.5/onecall?lat=44.9571&lon=24.9472&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Pitesti', 'pitesti']:
                try:
                        get_atmospheric_data_AG_Pitesti('https://api.openweathermap.org/data/2.5/onecall?lat=44.85&lon=24.8667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Stefanesti(AG)', 'stefanesti(ag)']:
                try:
                        get_atmospheric_data_AG_Stefanesti('https://api.openweathermap.org/data/2.5/onecall?lat=44.8733&lon=24.964&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Topoloveni', 'topoloveni']:
                try:
                        get_atmospheric_data_AG_Topoloveni('https://api.openweathermap.org/data/2.5/onecall?lat=44.816669&lon=25.08333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Bacau', 'bacau']:
                try:
                        get_atmospheric_data_BC_Bacau('https://api.openweathermap.org/data/2.5/onecall?lat=46.566669&lon=26.09&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Buhusi', 'buhusi']:
                try:
                        get_atmospheric_data_BC_Buhusi('https://api.openweathermap.org/data/2.5/onecall?lat=46.71&lon=26.7048&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Comanesti', 'comanesti']:
                try:
                        get_atmospheric_data_BC_Comanesti('https://api.openweathermap.org/data/2.5/onecall?lat=46.421&lon=26.4398&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Darmanesti', 'darmanesti']:
                try:
                        get_atmospheric_data_BC_Darmanesti('https://api.openweathermap.org/data/2.5/onecall?lat=46.3679&lon=26.473&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Moinesti', 'moinesti']:
                try:
                        get_atmospheric_data_BC_Moinesti('https://api.openweathermap.org/data/2.5/onecall?lat=46.4701&lon=26.4859&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Onesti', 'onesti']:
                try:
                        get_atmospheric_data_BC_Onesti('https://api.openweathermap.org/data/2.5/onecall?lat=46.2493&lon=26.7768&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Slanic Moldova', 'slanic moldova']:
                try:
                        get_atmospheric_data_BC_Slanic_Moldova('https://api.openweathermap.org/data/2.5/onecall?lat=46.2041&lon=26.4392&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Targu Ocna', 'targu ocna']:
                try:
                        get_atmospheric_data_BC_Targu_Ocna('https://api.openweathermap.org/data/2.5/onecall?lat=46.2041&lon=26.4392&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Alesd', 'alesd']:
                try:
                        get_atmospheric_data_BH_Alesd('https://api.openweathermap.org/data/2.5/onecall?lat=47.0590&lon=22.3981&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Beius', 'beius']:
                try:
                        get_atmospheric_data_BH_Beius('https://api.openweathermap.org/data/2.5/onecall?lat=46.6624&lon=22.3531&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Marghita', 'marghita']:
                try:
                        get_atmospheric_data_BH_Marghita('https://api.openweathermap.org/data/2.5/onecall?lat=47.349998&lon=22.33333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Nucet', 'nucet']:
                try:
                        get_atmospheric_data_BH_Nucet('https://api.openweathermap.org/data/2.5/onecall?lat=46.466671&lon=22.58333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Oradea', 'oradea']:
                try:
                        get_atmospheric_data_BH_Oradea('https://api.openweathermap.org/data/2.5/onecall?lat=47.066669&lon=21.933331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sacueni', 'sacueni']:
                try:
                        get_atmospheric_data_BH_Sacueni('https://api.openweathermap.org/data/2.5/onecall?lat=47.349998&lon=22.1&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Salonta', 'salonta']:
                try:
                        get_atmospheric_data_BH_Salonta('https://api.openweathermap.org/data/2.5/onecall?lat=46.799999&lon=21.65&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Stei', 'stei']:
                try:
                        get_atmospheric_data_BH_Stei('https://api.openweathermap.org/data/2.5/onecall?lat=46.532&lon=22.4469&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Valea lui Mihai', 'valea lui mihai']:
                try:
                        get_atmospheric_data_BH_Valea_lui_Mihai('https://api.openweathermap.org/data/2.5/onecall?lat=47.51667&lon=22.15&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Vascau', 'vascau']:
                try:
                        get_atmospheric_data_BH_Vascau('https://api.openweathermap.org/data/2.5/onecall?lat=46.4691&lon=22.4784&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Beclean', 'beclean']:
                try:
                        get_atmospheric_data_BN_Beclean('https://api.openweathermap.org/data/2.5/onecall?lat=47.183331&lon=24.183331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Bistrita', 'bistrita']:
                try:
                        get_atmospheric_data_BN_Bistrita('https://api.openweathermap.org/data/2.5/onecall?lat=47.1288&lon=24.4997&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Nasaud', 'nasaud']:
                try:
                        get_atmospheric_data_BN_Nasaud('https://api.openweathermap.org/data/2.5/onecall?lat=47.283329&lon=24.4&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sangeorz Bai', 'sangeorz bai']:
                try:
                        get_atmospheric_data_BN_Sangeorz_Bai('https://api.openweathermap.org/data/2.5/onecall?lat=47.3649&lon=24.6719&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Botosani', 'botosani']:
                try:
                        get_atmospheric_data_BT_Botosani('https://api.openweathermap.org/data/2.5/onecall?lat=47.7349&lon=26.6539&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Bucecea', 'bucecea']:
                try:
                        get_atmospheric_data_BT_Bucecea('https://api.openweathermap.org/data/2.5/onecall?lat=47.7349&lon=26.6539&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Darabani', 'darabani']:
                try:
                        get_atmospheric_data_BT_Darabani('https://api.openweathermap.org/data/2.5/onecall?lat=48.183331&lon=26.58333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Dorohoi', 'dorohoi']:
                try:
                        get_atmospheric_data_BT_Dorohoi('https://api.openweathermap.org/data/2.5/onecall?lat=47.950001&lon=26.4&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Flamanzi', 'flamanzi']:
                try:
                        get_atmospheric_data_BT_Flamanzi('https://api.openweathermap.org/data/2.5/onecall?lat=47.5554&lon=26.8902&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Saveni', 'saveni']:
                try:
                        get_atmospheric_data_BT_Saveni('https://api.openweathermap.org/data/2.5/onecall?lat=47.950001&lon=26.866671&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Stefanesti(BT)', 'stefanesti(bt)']:
                try:
                        get_atmospheric_data_BT_Stefanesti('https://api.openweathermap.org/data/2.5/onecall?lat=47.7877&lon=27.1958&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Braila', 'braila']:
                try:
                        get_atmospheric_data_BR_Braila('https://api.openweathermap.org/data/2.5/onecall?lat=45.26667&lon=27.98333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Faurei', 'faurei']:
                try:
                        get_atmospheric_data_BR_Faurei('https://api.openweathermap.org/data/2.5/onecall?lat=45.083328&lon=27.26667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ianca', 'ianca']:
                try:
                        get_atmospheric_data_BR_Ianca('https://api.openweathermap.org/data/2.5/onecall?lat=45.083328&lon=27.26667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Insuratei', 'insuratei']:
                try:
                        get_atmospheric_data_BR_Insuratei('https://api.openweathermap.org/data/2.5/onecall?lat=44.9064&lon=27.6014&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Brasov', 'brasov']:
                try:
                        get_atmospheric_data_BV_Brasov('https://api.openweathermap.org/data/2.5/onecall?lat=45.71&lon=25.3441&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Codlea', 'codlea']:
                try:
                        get_atmospheric_data_BV_Codlea('https://api.openweathermap.org/data/2.5/onecall?lat=45.6935&lon=25.4488&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Fagaras', 'fagaras']:
                try:
                        get_atmospheric_data_BV_Fagaras('https://api.openweathermap.org/data/2.5/onecall?lat=45.849998&lon=24.966669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ghimbav', 'ghimbav']:
                try:
                        get_atmospheric_data_BV_Ghimbav('https://api.openweathermap.org/data/2.5/onecall?lat=45.666672&lon=25.5&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Predeal', 'predeal']:
                try:
                        get_atmospheric_data_BV_Predeal('https://api.openweathermap.org/data/2.5/onecall?lat=45.5&lon=25.566669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Rasnov', 'rasnov']:
                try:
                        get_atmospheric_data_BV_Rasnov('https://api.openweathermap.org/data/2.5/onecall?lat=45.5746&lon=25.4540&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Rupea', 'rupea']:
                try:
                        get_atmospheric_data_BV_Rupea('https://api.openweathermap.org/data/2.5/onecall?lat=46.033329&lon=25.216669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sacele', 'sacele']:
                try:
                        get_atmospheric_data_BV_Sacele('https://api.openweathermap.org/data/2.5/onecall?lat=45.617401&lon=25.694269&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Victoria', 'victoria']:
                try:
                        get_atmospheric_data_BV_Victoria('https://api.openweathermap.org/data/2.5/onecall?lat=45.73333&lon=24.683331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Zarnesti', 'zarnesti']:
                try:
                        get_atmospheric_data_BV_Zarnesti('https://api.openweathermap.org/data/2.5/onecall?lat=45.549999&lon=25.299999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Bucuresti', 'bucuresti']:
                try:
                        get_atmospheric_data_B_Bucuresti('https://api.openweathermap.org/data/2.5/onecall?lat=44.43278&lon=26.10389&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Buzau', 'buzau']:
                try:
                        get_atmospheric_data_BZ_Buzau('https://api.openweathermap.org/data/2.5/onecall?lat=45.416672&lon=26.75&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Nehoiu', 'nehoiu']:
                try:
                        get_atmospheric_data_BZ_Nehoiu('https://api.openweathermap.org/data/2.5/onecall?lat=45.416672&lon=26.75&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Patarlagele', 'patarlagele']:
                try:
                        get_atmospheric_data_BZ_Patarlagele('https://api.openweathermap.org/data/2.5/onecall?lat=45.3186&lon=26.3649&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Pogoanele', 'pogoanele']:
                try:
                        get_atmospheric_data_BZ_Pogoanele('https://api.openweathermap.org/data/2.5/onecall?lat=45.3186&lon=26.3649&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ramnicu Sarat', 'ramnicu sarat']:
                try:
                        get_atmospheric_data_BZ_Ramnicu_Sarat('https://api.openweathermap.org/data/2.5/onecall?lat=45.383331&lon=27.049999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Budesti', 'budesti']:
                try:
                        get_atmospheric_data_CL_Budesti('https://api.openweathermap.org/data/2.5/onecall?lat=44.227&lon=26.4655&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Calarasi', 'calarasi']:
                try:
                        get_atmospheric_data_CL_Calarasi('https://api.openweathermap.org/data/2.5/onecall?lat=44.1834&lon=27.3281&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Fundulea', 'fundulea']:
                try:
                        get_atmospheric_data_CL_Fundulea('https://api.openweathermap.org/data/2.5/onecall?lat=44.466671&lon=26.51667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Lehliu Gara', 'lehliu gara']:
                try:
                        get_atmospheric_data_CL_Lehliu_Gara('https://api.openweathermap.org/data/2.5/onecall?lat=44.4371&lon=26.8545&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Oltenita', 'oltenita']:
                try:
                        get_atmospheric_data_CL_Oltenita('https://api.openweathermap.org/data/2.5/onecall?lat=44.0847&lon=26.6424&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Anina', 'anina']:
                try:
                        get_atmospheric_data_CS_Anina('https://api.openweathermap.org/data/2.5/onecall?lat=45.079441&lon=21.856939&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Baile Herculane', 'baile herculane']:
                try:
                        get_atmospheric_data_CS_Baile_Herculane('https://api.openweathermap.org/data/2.5/onecall?lat=44.879719&lon=22.4125&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Bocsa', 'bocsa']:
                try:
                        get_atmospheric_data_CS_Bocsa('https://api.openweathermap.org/data/2.5/onecall?lat=45.3735&lon=21.7293&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Caransebes', 'caransebes']:
                try:
                        get_atmospheric_data_CS_Caransebes('https://api.openweathermap.org/data/2.5/onecall?lat=45.4084&lon=22.2242&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Moldova Noua', 'moldova noua']:
                try:
                        get_atmospheric_data_CS_Moldova_Noua('https://api.openweathermap.org/data/2.5/onecall?lat=44.737499&lon=21.666941&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Oravita', 'oravita']:
                try:
                        get_atmospheric_data_CS_Oravita('https://api.openweathermap.org/data/2.5/onecall?lat=45.0335&lon=21.6891&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Otelu Rosu', 'otelu rosu']:
                try:
                        get_atmospheric_data_CS_Otelu_Rosu('https://api.openweathermap.org/data/2.5/onecall?lat=45.5177&lon=22.3596&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Resita', 'resita']:
                try:
                        get_atmospheric_data_CS_Resita('https://api.openweathermap.org/data/2.5/onecall?lat=45.286&lon=21.8917&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Campia Turzii', 'campia turzii']:
                try:
                        get_atmospheric_data_CJ_Campia_Turzii('https://api.openweathermap.org/data/2.5/onecall?lat=46.549999&lon=23.883329&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Cluj Napoca', 'cluj napoca']:
                try:
                        get_atmospheric_data_CJ_Cluj_Napoca('https://api.openweathermap.org/data/2.5/onecall?lat=46.76667&lon=23.6&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Dej', 'dej']:
                try:
                        get_atmospheric_data_CJ_Dej('https://api.openweathermap.org/data/2.5/onecall?lat=47.150002&lon=23.866671&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Gherla', 'gherla']:
                try:
                        get_atmospheric_data_CJ_Gherla('https://api.openweathermap.org/data/2.5/onecall?lat=47.033329&lon=23.91667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Huedin', 'huedin']:
                try:
                        get_atmospheric_data_CJ_Huedin('https://api.openweathermap.org/data/2.5/onecall?lat=46.866669&lon=23.049999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Turda', 'turda']:
                try:
                        get_atmospheric_data_CJ_Turda('https://api.openweathermap.org/data/2.5/onecall?lat=46.566669&lon=23.783331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Cernavoda', 'cernavoda']:
                try:
                        get_atmospheric_data_CT_Cernavoda('https://api.openweathermap.org/data/2.5/onecall?lat=44.366669&lon=28.01667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Constanta', 'constanta']:
                try:
                        get_atmospheric_data_CT_Constanta('https://api.openweathermap.org/data/2.5/onecall?lat=44.25&lon=28.33333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Eforie', 'eforie']:
                try:
                        get_atmospheric_data_CT_Eforie('https://api.openweathermap.org/data/2.5/onecall?lat=44.0491&lon=28.6527&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Harsova', 'harsova']:
                try:
                        get_atmospheric_data_CT_Harsova('https://api.openweathermap.org/data/2.5/onecall?lat=44.6831&lon=27.9539&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Mangalia', 'mangalia']:
                try:
                        get_atmospheric_data_CT_Mangalia('https://api.openweathermap.org/data/2.5/onecall?lat=43.799999&lon=28.58333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Medgidia', 'medgidia']:
                try:
                        get_atmospheric_data_CT_Medgidia('https://api.openweathermap.org/data/2.5/onecall?lat=44.25&lon=28.283331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Murfatlar', 'murfatlar']:
                try:
                        get_atmospheric_data_CT_Murfatlar('https://api.openweathermap.org/data/2.5/onecall?lat=44.183331&lon=28.41667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Navodari', 'navodari']:
                try:
                        get_atmospheric_data_CT_Navodari('https://api.openweathermap.org/data/2.5/onecall?lat=44.316669&lon=28.6&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Negru Voda', 'negru voda']:
                try:
                        get_atmospheric_data_CT_Negru_Voda('https://api.openweathermap.org/data/2.5/onecall?lat=43.816669&lon=28.200001&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ovidiu', 'ovidiu']:
                try:
                        get_atmospheric_data_CT_Ovidiu('https://api.openweathermap.org/data/2.5/onecall?lat=44.26667&lon=28.566669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Techirghiol', 'techirghiol']:
                try:
                        get_atmospheric_data_CT_Techirghiol('https://api.openweathermap.org/data/2.5/onecall?lat=44.049999&lon=28.6&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Baraolt', 'baraolt']:
                try:
                        get_atmospheric_data_CV_Baraolt('https://api.openweathermap.org/data/2.5/onecall?lat=46.075142&lon=25.60029&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Covasna', 'covasna']:
                try:
                        get_atmospheric_data_CV_Covasna('https://api.openweathermap.org/data/2.5/onecall?lat=45.849998&lon=26.183331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Intorsura Buzaului', 'intorsura buzaului']:
                try:
                        get_atmospheric_data_CV_Intorsura_Buzaului('https://api.openweathermap.org/data/2.5/onecall?lat=45.683331&lon=26.033331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sfantu Gheorghe', 'sfantu gheorghe']:
                try:
                        get_atmospheric_data_CV_Sfantu_Gheorghe('https://api.openweathermap.org/data/2.5/onecall?lat=45.866669&lon=25.783331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Targu Secuiesc', 'targu secuiesc']:
                try:
                        get_atmospheric_data_CV_Targu_Secuiesc('https://api.openweathermap.org/data/2.5/onecall?lat=46.0&lon=26.133329&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Fieni', 'fieni']:
                try:
                        get_atmospheric_data_DB_Fieni('https://api.openweathermap.org/data/2.5/onecall?lat=45.133331&lon=25.41667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Gaesti', 'gaesti']:
                try:
                        get_atmospheric_data_DB_Gaesti('https://api.openweathermap.org/data/2.5/onecall?lat=44.7169&lon=25.3236&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Moreni', 'moreni']:
                try:
                        get_atmospheric_data_DB_Moreni('https://api.openweathermap.org/data/2.5/onecall?lat=44.98333&lon=25.65&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Pucioasa', 'pucioasa']:
                try:
                        get_atmospheric_data_DB_Pucioasa('https://api.openweathermap.org/data/2.5/onecall?lat=45.083328&lon=25.41667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Racari', 'racari']:
                try:
                        get_atmospheric_data_DB_Racari('https://api.openweathermap.org/data/2.5/onecall?lat=44.633331&lon=25.73333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Targoviste', 'targoviste']:
                try:
                        get_atmospheric_data_DB_Targoviste('https://api.openweathermap.org/data/2.5/onecall?lat=44.9172&lon=25.461&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Titu', 'titu']:
                try:
                        get_atmospheric_data_DB_Titu('https://api.openweathermap.org/data/2.5/onecall?lat=44.650002&lon=25.533331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Bailesti', 'bailesti']:
                try:
                        get_atmospheric_data_DJ_Bailesti('https://api.openweathermap.org/data/2.5/onecall?lat=44.0269&lon=23.3454&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Bechet', 'bechet']:
                try:
                        get_atmospheric_data_DJ_Bechet('https://api.openweathermap.org/data/2.5/onecall?lat=43.76667&lon=23.950001&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Calafat', 'calafat']:
                try:
                        get_atmospheric_data_DJ_Calafat('https://api.openweathermap.org/data/2.5/onecall?lat=43.991112&lon=22.932779&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Craiova', 'craiova']:
                try:
                        get_atmospheric_data_DJ_Craiova('https://api.openweathermap.org/data/2.5/onecall?lat=44.316669&lon=23.799999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Dabuleni', 'dabuleni']:
                try:
                        get_atmospheric_data_DJ_Dabuleni('https://api.openweathermap.org/data/2.5/onecall?lat=43.799999&lon=24.08333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Filiasi', 'filiasi']:
                try:
                        get_atmospheric_data_DJ_Filiasi('https://api.openweathermap.org/data/2.5/onecall?lat=44.5533&lon=23.5247&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Segarcea', 'segarcea']:
                try:
                        get_atmospheric_data_DJ_Segarcea('https://api.openweathermap.org/data/2.5/onecall?lat=44.099998&lon=23.75&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Beresti', 'beresti']:
                try:
                        get_atmospheric_data_GL_Beresti('https://api.openweathermap.org/data/2.5/onecall?lat=46.1013&lon=27.8846&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Galati', 'galati']:
                try:
                        get_atmospheric_data_GL_Galati('https://api.openweathermap.org/data/2.5/onecall?lat=45.44&lon=28.04&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Targu Bujor', 'targu bujor']:
                try:
                        get_atmospheric_data_GL_Targu_Bujor('https://api.openweathermap.org/data/2.5/onecall?lat=45.866669&lon=27.9&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Tecuci', 'tecuci']:
                try:
                        get_atmospheric_data_GL_Tecuci('https://api.openweathermap.org/data/2.5/onecall?lat=45.849731&lon=27.43441&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Bolintin Vale', 'bolintin vale']:
                try:
                        get_atmospheric_data_GR_Bolintin_Vale('https://api.openweathermap.org/data/2.5/onecall?lat=44.4475&lon=25.7647&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Giurgiu', 'giurgiu']:
                try:
                        get_atmospheric_data_GR_Giurgiu('https://api.openweathermap.org/data/2.5/onecall?lat=43.883331&lon=25.966669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Mihailesti', 'mihailesti']:
                try:
                        get_atmospheric_data_GR_Mihailesti('https://api.openweathermap.org/data/2.5/onecall?lat=44.3214&lon=25.9124&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Bumbesti Jiu', 'bumbesti jiu']:
                try:
                        get_atmospheric_data_GJ_Bumbesti_Jiu('https://api.openweathermap.org/data/2.5/onecall?lat=45.179&lon=23.3793&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Motru', 'motru']:
                try:
                        get_atmospheric_data_GJ_Motru('https://api.openweathermap.org/data/2.5/onecall?lat=44.803329&lon=22.971939&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Novaci', 'novaci']:
                try:
                        get_atmospheric_data_GJ_Novaci('https://api.openweathermap.org/data/2.5/onecall?lat=45.183331&lon=23.66667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Rovinari', 'rovinari']:
                try:
                        get_atmospheric_data_GJ_Rovinari('https://api.openweathermap.org/data/2.5/onecall?lat=44.916672&lon=23.183331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Targu Carbunesti', 'targu carbunesti']:
                try:
                        get_atmospheric_data_GJ_Targu_Carbunesti('https://api.openweathermap.org/data/2.5/onecall?lat=44.9573&lon=23.5093&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Targu Jiu', 'targu jiu']:
                try:
                        get_atmospheric_data_GJ_Targu_Jiu('https://api.openweathermap.org/data/2.5/onecall?lat=45.049999&lon=23.283331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ticleni', 'ticleni']:
                try:
                        get_atmospheric_data_GJ_Ticleni('https://api.openweathermap.org/data/2.5/onecall?lat=44.8869&lon=23.3976&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Tismana', 'tismana']:
                try:
                        get_atmospheric_data_GJ_Tismana('https://api.openweathermap.org/data/2.5/onecall?lat=45.049999&lon=22.966669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Baile Tusnad', 'baile tusnad']:
                try:
                        get_atmospheric_data_HR_Baile_Tusnad('https://api.openweathermap.org/data/2.5/onecall?lat=46.1433&lon=25.8622&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Balan', 'balan']:
                try:
                        get_atmospheric_data_HR_Balan('https://api.openweathermap.org/data/2.5/onecall?lat=46.650501&lon=25.80834&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Borsec', 'borsec']:
                try:
                        get_atmospheric_data_HR_Borsec('https://api.openweathermap.org/data/2.5/onecall?lat=46.950001&lon=25.566669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Cristuru Secuiesc', 'cristuru secuiesc']:
                try:
                        get_atmospheric_data_HR_Cristuru_Secuiesc('https://api.openweathermap.org/data/2.5/onecall?lat=46.283329&lon=25.033331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Gheorgheni', 'gheorgheni']:
                try:
                        get_atmospheric_data_HR_Gheorgheni('https://api.openweathermap.org/data/2.5/onecall?lat=46.7189&lon=25.603&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Miercurea Ciuc', 'miercurea ciuc']:
                try:
                        get_atmospheric_data_HR_Miercurea_Ciuc('https://api.openweathermap.org/data/2.5/onecall?lat=46.357948&lon=25.80405&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Odorheiu Secuiesc', 'odorheiu secuiesc']:
                try:
                        get_atmospheric_data_HR_Odorheiu_Secuiesc('https://api.openweathermap.org/data/2.5/onecall?lat=46.299999&lon=25.299999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Toplita', 'toplita']:
                try:
                        get_atmospheric_data_HR_Toplita('https://api.openweathermap.org/data/2.5/onecall?lat=46.9118&lon=25.3594&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Vlahita', 'vlahita']:
                try:
                        get_atmospheric_data_HR_Vlahita('https://api.openweathermap.org/data/2.5/onecall?lat=46.3267&lon=25.5148&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Amara', 'amara']:
                try:
                        get_atmospheric_data_IL_Amara('https://api.openweathermap.org/data/2.5/onecall?lat=44.616669&lon=27.316669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Cazanesti', 'cazanesti']:
                try:
                        get_atmospheric_data_IL_Cazanesti('https://api.openweathermap.org/data/2.5/onecall?lat=44.6196&lon=27.0058&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Fetesti', 'fetesti']:
                try:
                        get_atmospheric_data_IL_Fetesti('https://api.openweathermap.org/data/2.5/onecall?lat=47.700001&lon=26.33333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Fierbinti Targ', 'fierbinti targ']:
                try:
                        get_atmospheric_data_IL_Fierbinti_Targ('https://api.openweathermap.org/data/2.5/onecall?lat=44.6813&lon=26.3826&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Slobozia', 'slobozia']:
                try:
                        get_atmospheric_data_IL_Slobozia('https://api.openweathermap.org/data/2.5/onecall?lat=44.51667&lon=25.23333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Tandarei', 'tandarei']:
                try:
                        get_atmospheric_data_IL_Tandarei('https://api.openweathermap.org/data/2.5/onecall?lat=44.6385&lon=27.6478&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Urziceni', 'urziceni']:
                try:
                        get_atmospheric_data_IL_Urziceni('https://api.openweathermap.org/data/2.5/onecall?lat=44.716671&lon=26.633329&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Harlau', 'harlau']:
                try:
                        get_atmospheric_data_IS_Harlau('https://api.openweathermap.org/data/2.5/onecall?lat=47.426&lon=26.9024&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Iasi', 'iasi']:
                try:
                        get_atmospheric_data_IS_Iasi('https://api.openweathermap.org/data/2.5/onecall?lat=47.17&lon=27.57&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Pascani', 'pascani']:
                try:
                        get_atmospheric_data_IS_Pascani('https://api.openweathermap.org/data/2.5/onecall?lat=47.245&lon=26.7261&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Podu Iloaiei', 'podu iloaiei']:
                try:
                        get_atmospheric_data_IS_Podu_Iloaiei('https://api.openweathermap.org/data/2.5/onecall?lat=47.216671&lon=27.26667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Targu Frumos', 'targu frumos']:
                try:
                        get_atmospheric_data_IS_Targu_Frumos('https://api.openweathermap.org/data/2.5/onecall?lat=47.200001&lon=27.0&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Bragadiru', 'bragadiru']:
                try:
                        get_atmospheric_data_IF_Bragadiru('https://api.openweathermap.org/data/2.5/onecall?lat=44.371109&lon=25.977501&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Buftea', 'buftea']:
                try:
                        get_atmospheric_data_IF_Buftea('https://api.openweathermap.org/data/2.5/onecall?lat=44.56139&lon=25.948891&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Chitila', 'chitila']:
                try:
                        get_atmospheric_data_IF_Chitila('https://api.openweathermap.org/data/2.5/onecall?lat=44.50806&lon=25.98222&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Magurele', 'magurele']:
                try:
                        get_atmospheric_data_IF_Magurele('https://api.openweathermap.org/data/2.5/onecall?lat=45.099998&lon=26.033331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Otopeni', 'otopeni']:
                try:
                        get_atmospheric_data_IF_Otopeni('https://api.openweathermap.org/data/2.5/onecall?lat=44.549999&lon=26.066669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Pantelimon', 'pantelimon']:
                try:
                        get_atmospheric_data_IF_Pantelimon('https://api.openweathermap.org/data/2.5/onecall?lat=44.450001&lon=26.200001&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Popesti Leordeni', 'popesti leordeni']:
                try:
                        get_atmospheric_data_IF_Popesti_Leordeni('https://api.openweathermap.org/data/2.5/onecall?lat=44.3786&lon=26.1697&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Voluntari', 'voluntari']:
                try:
                        get_atmospheric_data_IF_Voluntari('https://api.openweathermap.org/data/2.5/onecall?lat=44.466671&lon=26.133329&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Baia Mare', 'baia mare']:
                try:
                        get_atmospheric_data_MM_Baia_Mare('https://api.openweathermap.org/data/2.5/onecall?lat=47.653309&lon=23.579491&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Baia Sprie', 'baia sprie']:
                try:
                        get_atmospheric_data_MM_Baia_Sprie('https://api.openweathermap.org/data/2.5/onecall?lat=47.661888&lon=23.69215&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Borsa', 'borsa']:
                try:
                        get_atmospheric_data_MM_Borsa('https://api.openweathermap.org/data/2.5/onecall?lat=47.6538&lon=24.6632&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Cavnic', 'cavnic']:
                try:
                        get_atmospheric_data_MM_Cavnic('https://api.openweathermap.org/data/2.5/onecall?lat=47.666672&lon=23.866671&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Dragomiresti', 'dragomiresti']:
                try:
                        get_atmospheric_data_MM_Dragomiresti('https://api.openweathermap.org/data/2.5/onecall?lat=47.6657&lon=24.2948&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Salistea de Sus', 'salistea de sus']:
                try:
                        get_atmospheric_data_MM_Salistea_de_Sus('https://api.openweathermap.org/data/2.5/onecall?lat=47.6576&lon=24.3525&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Seini', 'seini']:
                try:
                        get_atmospheric_data_MM_Seini('https://api.openweathermap.org/data/2.5/onecall?lat=47.75&lon=23.283331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sighetu Marmatiei', 'sighetu marmatiei']:
                try:
                        get_atmospheric_data_MM_Sighetu_Marmatiei('https://api.openweathermap.org/data/2.5/onecall?lat=47.9277&lon=23.8977&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Somcuta Mare', 'somcuta mare']:
                try:
                        get_atmospheric_data_MM_Somcuta_Mare('https://api.openweathermap.org/data/2.5/onecall?lat=47.5039&lon=23.4634&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Targu Lapus', 'targu lapus']:
                try:
                        get_atmospheric_data_MM_Targu_Lapus('https://api.openweathermap.org/data/2.5/onecall?lat=47.4486&lon=23.8576&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Tautii Magheraus', 'tautii magheraus']:
                try:
                        get_atmospheric_data_MM_Tautii_Magheraus('https://api.openweathermap.org/data/2.5/onecall?lat=47.650002&lon=23.48333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ulmeni', 'Ulmeni']:
                try:
                        get_atmospheric_data_MM_Ulmeni('https://api.openweathermap.org/data/2.5/onecall?lat=47.466671&lon=23.299999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Viseu de Sus', 'viseu de sus']:
                try:
                        get_atmospheric_data_MM_Viseu_de_Sus('https://api.openweathermap.org/data/2.5/onecall?lat=47.7167&lon=24.4333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Baia de Arama', 'baia de arama']:
                try:
                        get_atmospheric_data_MH_Baia_de_Arama('https://api.openweathermap.org/data/2.5/onecall?lat=45.0&lon=22.806669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Drobeta Turnu Severin', 'drobeta turnu severin']:
                try:
                        get_atmospheric_data_MH_Drobeta_Turnu_Severin('https://api.openweathermap.org/data/2.5/onecall?lat=44.631939&lon=22.656111&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Orsova', 'orsova']:
                try:
                        get_atmospheric_data_MH_Orsova('https://api.openweathermap.org/data/2.5/onecall?lat=44.7172&lon=22.3979&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Strehaia', 'strehaia']:
                try:
                        get_atmospheric_data_MH_Strehaia('https://api.openweathermap.org/data/2.5/onecall?lat=44.616669&lon=23.200001&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Vanju Mare', 'vanju mare']:
                try:
                        get_atmospheric_data_MH_Vanju_Mare('https://api.openweathermap.org/data/2.5/onecall?lat=44.4232&lon=22.8662&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Iernut', 'iernut']:
                try:
                        get_atmospheric_data_MS_Iernut('https://api.openweathermap.org/data/2.5/onecall?lat=46.450001&lon=24.25&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ludus', 'ludus']:
                try:
                        get_atmospheric_data_MS_Ludus('https://api.openweathermap.org/data/2.5/onecall?lat=46.4761&lon=24.0934&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Miercurea Nirajului', 'miercurea nirajului']:
                try:
                        get_atmospheric_data_MS_Miercurea_Nirajului('https://api.openweathermap.org/data/2.5/onecall?lat=46.533329&lon=24.799999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Reghin', 'reghin']:
                try:
                        get_atmospheric_data_MS_Reghin('https://api.openweathermap.org/data/2.5/onecall?lat=46.7742&lon=24.70216&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sangeorgiu de Padure', 'sangeorgiu de padure']:
                try:
                        get_atmospheric_data_MS_Sangeorgiu_de_Padure('https://api.openweathermap.org/data/2.5/onecall?lat=46.4288&lon=24.8401&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sarmasu', 'sarmasu']:
                try:
                        get_atmospheric_data_MS_Sarmasu('https://api.openweathermap.org/data/2.5/onecall?lat=46.7512&lon=24.1656&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sighisoara', 'sighisoara']:
                try:
                        get_atmospheric_data_MS_Sighisoara('https://api.openweathermap.org/data/2.5/onecall?lat=46.2151&lon=24.801&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sovata', 'sovata']:
                try:
                        get_atmospheric_data_MS_Sovata('https://api.openweathermap.org/data/2.5/onecall?lat=46.583328&lon=25.066669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Targu Mures', 'targu mures']:
                try:
                        get_atmospheric_data_MS_Targu_Mures('https://api.openweathermap.org/data/2.5/onecall?lat=46.5326&lon=24.5671&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Tarnaveni', 'tarnaveni']:
                try:
                        get_atmospheric_data_MS_Tarnaveni('https://api.openweathermap.org/data/2.5/onecall?lat=46.3333&lon=24.2833&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ungheni', 'ungheni']:
                try:
                        get_atmospheric_data_MS_Ungheni('https://api.openweathermap.org/data/2.5/onecall?lat=46.48333&lon=24.466669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Bicaz', 'bicaz']:
                try:
                        get_atmospheric_data_NT_Bicaz('https://api.openweathermap.org/data/2.5/onecall?lat=46.916672&lon=26.066669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Piatra Neamt', 'piatra neamt']:
                try:
                        get_atmospheric_data_NT_Piatra_Neamt('https://api.openweathermap.org/data/2.5/onecall?lat=46.9245&lon=26.3703&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Roman', 'roman']:
                try:
                        get_atmospheric_data_NT_Roman('https://api.openweathermap.org/data/2.5/onecall?lat=46.916672&lon=26.91667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Roznov', 'roznov']:
                try:
                        get_atmospheric_data_NT_Roznov('https://api.openweathermap.org/data/2.5/onecall?lat=46.833328&lon=26.51667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Targu Neamt', 'targu neamt']:
                try:
                        get_atmospheric_data_NT_Targu_Neamt('https://api.openweathermap.org/data/2.5/onecall?lat=47.200001&lon=26.3667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Bals', 'bals']:
                try:
                        get_atmospheric_data_OT_Bals('https://api.openweathermap.org/data/2.5/onecall?lat=44.3498&lon=24.103&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Caracal', 'caracal']:
                try:
                        get_atmospheric_data_OT_Caracal('https://api.openweathermap.org/data/2.5/onecall?lat=44.116669&lon=24.35&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Corabia', 'corabia']:
                try:
                        get_atmospheric_data_OT_Corabia('https://api.openweathermap.org/data/2.5/onecall?lat=43.783329&lon=24.5&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Draganesti Olt', 'draganesti olt']:
                try:
                        get_atmospheric_data_OT_Draganesti_Olt('https://api.openweathermap.org/data/2.5/onecall?lat=44.1654&lon=24.5272&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Piatra Olt', 'piatra olt']:
                try:
                        get_atmospheric_data_OT_Piatra_Olt('https://api.openweathermap.org/data/2.5/onecall?lat=44.3699&lon=24.2607&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Potcoava', 'potcoava']:
                try:
                        get_atmospheric_data_OT_Potcoava('https://api.openweathermap.org/data/2.5/onecall?lat=44.48333&lon=24.65&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Scornicesti', 'scornicesti']:
                try:
                        get_atmospheric_data_OT_Scornicesti('https://api.openweathermap.org/data/2.5/onecall?lat=44.5818&lon=24.5494&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Slatina', 'slatina']:
                try:
                        get_atmospheric_data_OT_Slatina('https://api.openweathermap.org/data/2.5/onecall?lat=44.433331&lon=24.366671&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Azuga', 'azuga']:
                try:
                        get_atmospheric_data_PH_Azuga('https://api.openweathermap.org/data/2.5/onecall?lat=45.450001&lon=25.549999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Baicoi', 'baicoi']:
                try:
                        get_atmospheric_data_PH_Baicoi('https://api.openweathermap.org/data/2.5/onecall?lat=45.033329&lon=25.85&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Boldesti Scaeni', 'boldesti scaeni']:
                try:
                        get_atmospheric_data_PH_Boldesti_Scaeni('https://api.openweathermap.org/data/2.5/onecall?lat=45.0275&lon=26.0276&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Breaza', 'breaza']:
                try:
                        get_atmospheric_data_PH_Breaza('https://api.openweathermap.org/data/2.5/onecall?lat=45.183331&lon=25.66667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Busteni', 'busteni']:
                try:
                        get_atmospheric_data_PH_Busteni('https://api.openweathermap.org/data/2.5/onecall?lat=45.4097&lon=25.5342&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Campina', 'campina']:
                try:
                        get_atmospheric_data_PH_Campina('https://api.openweathermap.org/data/2.5/onecall?lat=45.133331&lon=25.73333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Comarnic', 'comarnic']:
                try:
                        get_atmospheric_data_PH_Comarnic('https://api.openweathermap.org/data/2.5/onecall?lat=45.25&lon=25.633329&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Mizil', 'mizil']:
                try:
                        get_atmospheric_data_PH_Mizil('https://api.openweathermap.org/data/2.5/onecall?lat=45.01667&lon=26.450001&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ploiesti', 'ploiesti']:
                try:
                        get_atmospheric_data_PH_Ploiesti('https://api.openweathermap.org/data/2.5/onecall?lat=44.9367&lon=26.0129&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Plopeni', 'plopeni']:
                try:
                        get_atmospheric_data_PH_Plopeni('https://api.openweathermap.org/data/2.5/onecall?lat=45.066669&lon=25.98333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sinaia', 'sinaia']:
                try:
                        get_atmospheric_data_PH_Sinaia('https://api.openweathermap.org/data/2.5/onecall?lat=45.349998&lon=25.549999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Slanic', 'slanic']:
                try:
                        get_atmospheric_data_PH_Slanic('https://api.openweathermap.org/data/2.5/onecall?lat=45.25&lon=25.933331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Urlati', 'urlati']:
                try:
                        get_atmospheric_data_PH_Urlati('https://api.openweathermap.org/data/2.5/onecall?lat=44.9888&lon=26.2375&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Valenii de Munte', 'valenii de Munte']:
                try:
                        get_atmospheric_data_PH_Valenii_de_Munte('https://api.openweathermap.org/data/2.5/onecall?lat=45.183331&lon=26.033331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Cehu Silvaniei', 'cehu silvaniei']:
                try:
                        get_atmospheric_data_SJ_Cehu_Silvaniei('https://api.openweathermap.org/data/2.5/onecall?lat=47.4105&lon=23.1747&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Jibou', 'jibou']:
                try:
                        get_atmospheric_data_SJ_Jibou('https://api.openweathermap.org/data/2.5/onecall?lat=47.26667&lon=23.25&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Simleu Silvaniei', 'simleu silvaniei']:
                try:
                        get_atmospheric_data_SJ_Simleu_Silvaniei('https://api.openweathermap.org/data/2.5/onecall?lat=47.2273&lon=22.7913&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Zalau', 'zalau']:
                try:
                        get_atmospheric_data_SJ_Zalau('https://api.openweathermap.org/data/2.5/onecall?lat=47.200001&lon=23.049999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ardud', 'ardud']:
                try:
                        get_atmospheric_data_SM_Ardud('https://api.openweathermap.org/data/2.5/onecall?lat=47.633331&lon=22.883329&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Carei', 'carei']:
                try:
                        get_atmospheric_data_SM_Carei('https://api.openweathermap.org/data/2.5/onecall?lat=47.683331&lon=22.466669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Livada', 'livada']:
                try:
                        get_atmospheric_data_SM_Livada('https://api.openweathermap.org/data/2.5/onecall?lat=47.866669&lon=23.133329&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Negresti Oas', 'negresti oas']:
                try:
                        get_atmospheric_data_SM_Negresti_Oas('https://api.openweathermap.org/data/2.5/onecall?lat=47.8709&lon=23.4303&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Satu Mare', 'satu mare']:
                try:
                        get_atmospheric_data_SM_Satu_Mare('https://api.openweathermap.org/data/2.5/onecall?lat=47.799999&lon=22.883329&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Tasnad', 'tasnad']:
                try:
                        get_atmospheric_data_SM_Tasnad('https://api.openweathermap.org/data/2.5/onecall?lat=47.4784&lon=22.5817&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Agnita', 'agnita']:
                try:
                        get_atmospheric_data_SB_Agnita('https://api.openweathermap.org/data/2.5/onecall?lat=45.966671&lon=24.616671&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Avrig', 'avrig']:
                try:
                        get_atmospheric_data_SB_Avrig('https://api.openweathermap.org/data/2.5/onecall?lat=45.716671&lon=24.383329&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Cisnadie', 'cisnadie']:
                try:
                        get_atmospheric_data_SB_Cisnadie('https://api.openweathermap.org/data/2.5/onecall?lat=45.716671&lon=24.15&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Copsa Mica', 'copsa mica']:
                try:
                        get_atmospheric_data_SB_Copsa_Mica('https://api.openweathermap.org/data/2.5/onecall?lat=46.1109&lon=24.2299&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Dumbraveni', 'dumbraveni']:
                try:
                        get_atmospheric_data_SB_Dumbraveni('https://api.openweathermap.org/data/2.5/onecall?lat=46.23333&lon=24.566669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Medias', 'medias']:
                try:
                        get_atmospheric_data_SB_Medias('https://api.openweathermap.org/data/2.5/onecall?lat=46.1573&lon=24.3472&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Miercurea Sibiului', 'miercurea sibiului']:
                try:
                        get_atmospheric_data_SB_Miercurea_Sibiului('https://api.openweathermap.org/data/2.5/onecall?lat=45.883331&lon=23.799999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ocna Sibiului', 'ocna sibiului']:
                try:
                        get_atmospheric_data_SB_Ocna_Sibiului('https://api.openweathermap.org/data/2.5/onecall?lat=45.883331&lon=24.049999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Saliste', 'saliste']:
                try:
                        get_atmospheric_data_SB_Saliste('https://api.openweathermap.org/data/2.5/onecall?lat=45.7945&lon=23.8748&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sibiu', 'sibiu']:
                try:
                        get_atmospheric_data_SB_Sibiu('https://api.openweathermap.org/data/2.5/onecall?lat=45.784279&lon=24.143829&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Talmaciu', 'talmaciu']:
                try:
                        get_atmospheric_data_SB_Talmaciu('https://api.openweathermap.org/data/2.5/onecall?lat=45.6647&lon=24.2606&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Brosteni', 'brosteni']:
                try:
                        get_atmospheric_data_SV_Brosteni('https://api.openweathermap.org/data/2.5/onecall?lat=47.2403&lon=25.6977&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Cajvana', 'cajvana']:
                try:
                        get_atmospheric_data_SV_Cajvana('https://api.openweathermap.org/data/2.5/onecall?lat=47.700001&lon=25.966669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Campulung Moldovenesc', 'campulung moldovenesc']:
                try:
                        get_atmospheric_data_SV_Campulung_Moldovenesc('https://api.openweathermap.org/data/2.5/onecall?lat=47.533329&lon=25.566669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Dolhasca', 'dolhasca']:
                try:
                        get_atmospheric_data_SV_Dolhasca('https://api.openweathermap.org/data/2.5/onecall?lat=47.433331&lon=26.69&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Falticeni', 'falticeni']:
                try:
                        get_atmospheric_data_SV_Falticeni('https://api.openweathermap.org/data/2.5/onecall?lat=47.450001&lon=26.299999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Frasin', 'frasin']:
                try:
                        get_atmospheric_data_SV_Frasin('https://api.openweathermap.org/data/2.5/onecall?lat=47.533329&lon=25.799999&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Gura Humorului', 'gura humorului']:
                try:
                        get_atmospheric_data_SV_Gura_Humorului('https://api.openweathermap.org/data/2.5/onecall?lat=47.5525&lon=25.8856&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Liteni', 'liteni']:
                try:
                        get_atmospheric_data_SV_Liteni('https://api.openweathermap.org/data/2.5/onecall?lat=47.566669&lon=26.200001&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Milisauti', 'milisauti']:
                try:
                        get_atmospheric_data_SV_Milisauti('https://api.openweathermap.org/data/2.5/onecall?lat=47.7857&lon=25.9996&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Radauti', 'radauti']:
                try:
                        get_atmospheric_data_SV_Radauti('https://api.openweathermap.org/data/2.5/onecall?lat=47.849998&lon=25.91667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Salcea', 'salcea']:
                try:
                        get_atmospheric_data_SV_Salcea('https://api.openweathermap.org/data/2.5/onecall?lat=47.650002&lon=26.366671&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Siret', 'siret']:
                try:
                        get_atmospheric_data_SV_Siret('https://api.openweathermap.org/data/2.5/onecall?lat=47.950001&lon=26.066669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Solca', 'solca']:
                try:
                        get_atmospheric_data_SV_Solca('https://api.openweathermap.org/data/2.5/onecall?lat=47.700001&lon=25.85&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Suceava', 'suceava']:
                try:
                        get_atmospheric_data_SV_Suceava('https://api.openweathermap.org/data/2.5/onecall?lat=47.633331&lon=26.25&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Vatra Dornei', 'vatra dornei']:
                try:
                        get_atmospheric_data_SV_Vatra_Dornei('https://api.openweathermap.org/data/2.5/onecall?lat=47.349998&lon=25.366671&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Vicovu de Sus', 'vicovu de sus']:
                try:
                        get_atmospheric_data_SV_Vicovu_de_Sus('https://api.openweathermap.org/data/2.5/onecall?lat=47.933331&lon=25.683331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Alexandria', 'alexandria']:
                try:
                        get_atmospheric_data_TR_Alexandria('https://api.openweathermap.org/data/2.5/onecall?lat=43.98333&lon=25.33333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Rosiorii de Vede', 'rosiorii de vede']:
                try:
                        get_atmospheric_data_TR_Rosiorii_de_Vede('https://api.openweathermap.org/data/2.5/onecall?lat=44.116669&lon=24.98333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Turnu Magurele', 'turnu magurele']:
                try:
                        get_atmospheric_data_TR_Turnu_Magurele('https://api.openweathermap.org/data/2.5/onecall?lat=43.75&lon=24.866671&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Videle', 'videle']:
                try:
                        get_atmospheric_data_TR_Videle('https://api.openweathermap.org/data/2.5/onecall?lat=44.278061&lon=25.524441&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Zimnicea', 'zimnicea']:
                try:
                        get_atmospheric_data_TR_Zimnicea('https://api.openweathermap.org/data/2.5/onecall?lat=43.666672&lon=25.366671&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Buzias', 'buzias']:
                try:
                        get_atmospheric_data_TM_Buzias('https://api.openweathermap.org/data/2.5/onecall?lat=45.6487&lon=21.6062&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ciacova', 'ciacova']:
                try:
                        get_atmospheric_data_TM_Ciacova('https://api.openweathermap.org/data/2.5/onecall?lat=45.50806&lon=21.128611&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Deta', 'deta']:
                try:
                        get_atmospheric_data_TM_Deta('https://api.openweathermap.org/data/2.5/onecall?lat=45.388889&lon=21.22444&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Faget', 'faget']:
                try:
                        get_atmospheric_data_TM_Faget('https://api.openweathermap.org/data/2.5/onecall?lat=45.849998&lon=22.183331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Gataia', 'gataia']:
                try:
                        get_atmospheric_data_TM_Gataia('https://api.openweathermap.org/data/2.5/onecall?lat=45.4296&lon=21.4318&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Jimbolia', 'jimbolia']:
                try:
                        get_atmospheric_data_TM_Jimbolia('https://api.openweathermap.org/data/2.5/onecall?lat=45.791389&lon=20.71722&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Lugoj', 'lugoj']:
                try:
                        get_atmospheric_data_TM_Lugoj('https://api.openweathermap.org/data/2.5/onecall?lat=45.68861&lon=21.903061&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Recas', 'recas']:
                try:
                        get_atmospheric_data_TM_Recas('https://api.openweathermap.org/data/2.5/onecall?lat=45.8012&lon=21.5119&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sannicolau Mare', 'sannicolau mare']:
                try:
                        get_atmospheric_data_TM_Sannicolau_Mare('https://api.openweathermap.org/data/2.5/onecall?lat=46.083328&lon=20.633329&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Timisoara', 'timisoara']:
                try:
                        get_atmospheric_data_TM_Timisoara('https://api.openweathermap.org/data/2.5/onecall?lat=45.7494&lon=21.2272&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Babadag', 'babadag']:
                try:
                        get_atmospheric_data_TL_Babadag('https://api.openweathermap.org/data/2.5/onecall?lat=45.174&lon=28.8001&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Isaccea', 'isaccea']:
                try:
                        get_atmospheric_data_TL_Isaccea('https://api.openweathermap.org/data/2.5/onecall?lat=45.26667&lon=28.466669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Macin', 'macin']:
                try:
                        get_atmospheric_data_TL_Macin('https://api.openweathermap.org/data/2.5/onecall?lat=45.24371&lon=28.135639&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Sulina', 'sulina']:
                try:
                        get_atmospheric_data_TL_Sulina('https://api.openweathermap.org/data/2.5/onecall?lat=45.155899&lon=29.653561&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Tulcea', 'tulcea']:
                try:
                        get_atmospheric_data_TL_Tulcea('https://api.openweathermap.org/data/2.5/onecall?lat=45.01&lon=28.83333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Babeni', 'babeni']:
                try:
                        get_atmospheric_data_VL_Babeni('https://api.openweathermap.org/data/2.5/onecall?lat=44.966671&lon=24.23333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Baile Govora', 'baile govora']:
                try:
                        get_atmospheric_data_VL_Baile_Govora('https://api.openweathermap.org/data/2.5/onecall?lat=45.083328&lon=24.183331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Baile Olanesti', 'baile olanesti']:
                try:
                        get_atmospheric_data_VL_Baile_Olanesti('https://api.openweathermap.org/data/2.5/onecall?lat=45.2028&lon=24.2411&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Balcesti', 'balcesti']:
                try:
                        get_atmospheric_data_VL_Balcesti('https://api.openweathermap.org/data/2.5/onecall?lat=44.6214&lon=23.9384&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Berbesti', 'berbesti']:
                try:
                        get_atmospheric_data_VL_Berbesti('https://api.openweathermap.org/data/2.5/onecall?lat=44.5114&lon=24.0625&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Brezoi', 'brezoi']:
                try:
                        get_atmospheric_data_VL_Brezoi('https://api.openweathermap.org/data/2.5/onecall?lat=45.337971&lon=24.248631&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Calimanesti', 'calimanesti']:
                try:
                        get_atmospheric_data_VL_Calimanesti('https://api.openweathermap.org/data/2.5/onecall?lat=45.2391&lon=24.3399&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Dragasani', 'dragasani']:
                try:
                        get_atmospheric_data_VL_Dragasani('https://api.openweathermap.org/data/2.5/onecall?lat=44.652&lon=24.2659&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Horezu', 'horezu']:
                try:
                        get_atmospheric_data_VL_Horezu('https://api.openweathermap.org/data/2.5/onecall?lat=45.150002&lon=24.01667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ocnele Mari', 'ocnele mari']:
                try:
                        get_atmospheric_data_VL_Ocnele_Mari('https://api.openweathermap.org/data/2.5/onecall?lat=45.083328&lon=24.316669&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Ramnicu Valcea', 'ramnicu valcea']:
                try:
                        get_atmospheric_data_VL_Ramnicu_Valcea('https://api.openweathermap.org/data/2.5/onecall?lat=45.099998&lon=24.366671&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Barlad', 'barlad']:
                try:
                        get_atmospheric_data_VS_Barlad('https://api.openweathermap.org/data/2.5/onecall?lat=46.23333&lon=27.66667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Husi', 'husi']:
                try:
                        get_atmospheric_data_VS_Husi('https://api.openweathermap.org/data/2.5/onecall?lat=46.6678&lon=28.0641&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Murgeni', 'murgeni']:
                try:
                        get_atmospheric_data_VS_Murgeni('https://api.openweathermap.org/data/2.5/onecall?lat=46.204441&lon=28.01972&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Negresti', 'negresti']:
                try:
                        get_atmospheric_data_VS_Negresti('https://api.openweathermap.org/data/2.5/onecall?lat=46.8321&lon=27.4641&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Vaslui', 'vaslui']:
                try:
                        get_atmospheric_data_VS_Vaslui('https://api.openweathermap.org/data/2.5/onecall?lat=46.633331&lon=27.73333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Adjud', 'adjud']:
                try:
                        get_atmospheric_data_VN_Adjud('https://api.openweathermap.org/data/2.5/onecall?lat=46.099998&lon=27.16667&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Focsani', 'focsani']:
                try:
                        get_atmospheric_data_VN_Focsani('https://api.openweathermap.org/data/2.5/onecall?lat=45.700001&lon=27.183331&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Marasesti', 'marasesti']:
                try:
                        get_atmospheric_data_VN_Marasesti('https://api.openweathermap.org/data/2.5/onecall?lat=45.883331&lon=27.23333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Odobesti', 'odobesti']:
                try:
                        get_atmospheric_data_VN_Odobesti('https://api.openweathermap.org/data/2.5/onecall?lat=45.7581&lon=27.0698&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        elif city in ['Panciu', 'panciu']:
                try:
                        get_atmospheric_data_VN_Panciu('https://api.openweathermap.org/data/2.5/onecall?lat=45.900002&lon=27.08333&exclude=minutely,hourly&units=metric&'+appid)
                except:
                        print(error_msg(city))
        else:
                print('\n {}: !!! Error!!!. Check if city name was written correctly!'.format(city))

if __name__ == "__main__": # absolute import
        from Romania.Alba.Abrud.AB_Abrud import get_atmospheric_data_AB_Abrud
        from Romania.Alba.Aiud.AB_Aiud import get_atmospheric_data_AB_Aiud
        from Romania.Alba.Alba_Iulia.AB_Alba_Iulia import get_atmospheric_data_AB_Alba_Iulia
        from Romania.Alba.Baia_de_Aries.AB_Baia_de_Aries import get_atmospheric_data_AB_Baia_de_Aries
        from Romania.Alba.Blaj.AB_Blaj import get_atmospheric_data_AB_Blaj
        from Romania.Alba.Campeni.AB_Campeni import get_atmospheric_data_AB_Campeni
        from Romania.Alba.Cugir.AB_Cugir import get_atmospheric_data_AB_Cugir
        from Romania.Alba.Ocna_Mures.AB_Ocna_Mures import get_atmospheric_data_AB_Ocna_Mures
        from Romania.Alba.Sebes.AB_Sebes import get_atmospheric_data_AB_Sebes
        from Romania.Alba.Teius.AB_Teius import get_atmospheric_data_AB_Teius
        from Romania.Alba.Zlatna.AB_Zlatna import get_atmospheric_data_AB_Zlatna
        from Romania.Arad.Arad.AR_Arad import get_atmospheric_data_AR_Arad
        from Romania.Arad.Chisineu_Cris.AR_Chisineu_Cris import get_atmospheric_data_AR_Chisineu_Cris
        from Romania.Arad.Curtici.AR_Curtici import get_atmospheric_data_AR_Curtici
        from Romania.Arad.Ineu.AR_Ineu import get_atmospheric_data_AR_Ineu
        from Romania.Arad.Lipova.AR_Lipova import get_atmospheric_data_AR_Lipova
        from Romania.Arad.Nadlac.AR_Nadlac import get_atmospheric_data_AR_Nadlac
        from Romania.Arad.Pancota.AR_Pancota import get_atmospheric_data_AR_Pancota
        from Romania.Arad.Pecica.AR_Pecica import get_atmospheric_data_AR_Pecica
        from Romania.Arad.Santana.AR_Santana import get_atmospheric_data_AR_Santana
        from Romania.Arges.Campulung.AG_Campulung import get_atmospheric_data_AG_Campulung
        from Romania.Arges.Costesti.AG_Costesti import get_atmospheric_data_AG_Costesti
        from Romania.Arges.Curtea_de_Arges.AG_Curtea_de_Arges import get_atmospheric_data_AG_Curtea_de_Arges
        from Romania.Arges.Mioveni.AG_Mioveni import get_atmospheric_data_AG_Mioveni
        from Romania.Arges.Pitesti.AG_Pitesti import get_atmospheric_data_AG_Pitesti
        from Romania.Arges.Stefanesti.AG_Stefanesti import get_atmospheric_data_AG_Stefanesti
        from Romania.Arges.Topoloveni.AG_Topoloveni import get_atmospheric_data_AG_Topoloveni
        from Romania.Bacau.Bacau.BC_Bacau import get_atmospheric_data_BC_Bacau
        from Romania.Bacau.Buhusi.BC_Buhusi import get_atmospheric_data_BC_Buhusi
        from Romania.Bacau.Comanesti.BC_Comanesti import get_atmospheric_data_BC_Comanesti
        from Romania.Bacau.Darmanesti.BC_Darmanesti import get_atmospheric_data_BC_Darmanesti
        from Romania.Bacau.Moinesti.BC_Moinesti import get_atmospheric_data_BC_Moinesti
        from Romania.Bacau.Onesti.BC_Onesti import get_atmospheric_data_BC_Onesti
        from Romania.Bacau.Slanic_Moldova.BC_Slanic_Moldova import get_atmospheric_data_BC_Slanic_Moldova
        from Romania.Bacau.Targu_Ocna.BC_Targu_Ocna import get_atmospheric_data_BC_Targu_Ocna
        from Romania.Bihor.Alesd.BH_Alesd import get_atmospheric_data_BH_Alesd
        from Romania.Bihor.Beius.BH_Beius import get_atmospheric_data_BH_Beius
        from Romania.Bihor.Marghita.BH_Marghita import get_atmospheric_data_BH_Marghita
        from Romania.Bihor.Nucet.BH_Nucet import get_atmospheric_data_BH_Nucet
        from Romania.Bihor.Oradea.BH_Oradea import get_atmospheric_data_BH_Oradea
        from Romania.Bihor.Sacueni.BH_Sacueni import get_atmospheric_data_BH_Sacueni
        from Romania.Bihor.Salonta.BH_Salonta import get_atmospheric_data_BH_Salonta
        from Romania.Bihor.Stei.BH_Stei import get_atmospheric_data_BH_Stei
        from Romania.Bihor.Valea_lui_Mihai.BH_Valea_lui_Mihai import get_atmospheric_data_BH_Valea_lui_Mihai
        from Romania.Bihor.Vascau.BH_Vascau import get_atmospheric_data_BH_Vascau
        from Romania.Bistrita_Nasaud.Beclean.BN_Beclean import get_atmospheric_data_BN_Beclean
        from Romania.Bistrita_Nasaud.Bistrita.BN_Bistrita import get_atmospheric_data_BN_Bistrita
        from Romania.Bistrita_Nasaud.Nasaud.BN_Nasaud import get_atmospheric_data_BN_Nasaud
        from Romania.Bistrita_Nasaud.Sangeorz_Bai.BN_Sangeorz_Bai import get_atmospheric_data_BN_Sangeorz_Bai
        from Romania.Botosani.Botosani.BT_Botosani import get_atmospheric_data_BT_Botosani
        from Romania.Botosani.Bucecea.BT_Bucecea import get_atmospheric_data_BT_Bucecea
        from Romania.Botosani.Darabani.BT_Darabani import get_atmospheric_data_BT_Darabani
        from Romania.Botosani.Dorohoi.BT_Dorohoi import get_atmospheric_data_BT_Dorohoi
        from Romania.Botosani.Flamanzi.BT_Flamanzi import get_atmospheric_data_BT_Flamanzi
        from Romania.Botosani.Saveni.BT_Saveni import get_atmospheric_data_BT_Saveni
        from Romania.Botosani.Stefanesti.BT_Stefanesti import get_atmospheric_data_BT_Stefanesti
        from Romania.Braila.Braila.BR_Braila import get_atmospheric_data_BR_Braila
        from Romania.Braila.Faurei.BR_Faurei import get_atmospheric_data_BR_Faurei
        from Romania.Braila.Ianca.BR_Ianca import get_atmospheric_data_BR_Ianca
        from Romania.Braila.Insuratei.BR_Insuratei import get_atmospheric_data_BR_Insuratei
        from Romania.Brasov.Brasov.BV_Brasov import get_atmospheric_data_BV_Brasov
        from Romania.Brasov.Codlea.BV_Codlea import get_atmospheric_data_BV_Codlea
        from Romania.Brasov.Fagaras.BV_Fagaras import get_atmospheric_data_BV_Fagaras
        from Romania.Brasov.Ghimbav.BV_Ghimbav import get_atmospheric_data_BV_Ghimbav
        from Romania.Brasov.Predeal.BV_Predeal import get_atmospheric_data_BV_Predeal
        from Romania.Brasov.Rasnov.BV_Rasnov import get_atmospheric_data_BV_Rasnov
        from Romania.Brasov.Rupea.BV_Rupea import get_atmospheric_data_BV_Rupea
        from Romania.Brasov.Sacele.BV_Sacele import get_atmospheric_data_BV_Sacele
        from Romania.Brasov.Victoria.BV_Victoria import get_atmospheric_data_BV_Victoria
        from Romania.Brasov.Zarnesti.BV_Zarnesti import get_atmospheric_data_BV_Zarnesti
        from Romania.Bucuresti.B_Bucuresti import get_atmospheric_data_B_Bucuresti
        from Romania.Buzau.Buzau.BZ_Buzau import get_atmospheric_data_BZ_Buzau
        from Romania.Buzau.Nehoiu.BZ_Nehoiu import get_atmospheric_data_BZ_Nehoiu
        from Romania.Buzau.Patarlagele.BZ_Patarlagele import get_atmospheric_data_BZ_Patarlagele
        from Romania.Buzau.Pogoanele.BZ_Pogoanele import get_atmospheric_data_BZ_Pogoanele
        from Romania.Buzau.Ramnicu_Sarat.BZ_Ramnicu_Sarat import get_atmospheric_data_BZ_Ramnicu_Sarat
        from Romania.Calarasi.Budesti.CL_Budesti import get_atmospheric_data_CL_Budesti
        from Romania.Calarasi.Calarasi.CL_Calarasi import get_atmospheric_data_CL_Calarasi
        from Romania.Calarasi.Fundulea.CL_Fundulea import get_atmospheric_data_CL_Fundulea
        from Romania.Calarasi.Lehliu_Gara.CL_Lehliu_Gara import get_atmospheric_data_CL_Lehliu_Gara
        from Romania.Calarasi.Oltenita.CL_Oltenita import get_atmospheric_data_CL_Oltenita
        from Romania.Caras_Severin.Anina.CS_Anina import get_atmospheric_data_CS_Anina
        from Romania.Caras_Severin.Baile_Herculane.CS_Baile_Herculane import get_atmospheric_data_CS_Baile_Herculane
        from Romania.Caras_Severin.Bocsa.CS_Bocsa import get_atmospheric_data_CS_Bocsa
        from Romania.Caras_Severin.Caransebes.CS_Caransebes import get_atmospheric_data_CS_Caransebes
        from Romania.Caras_Severin.Moldova_Noua.CS_Moldova_Noua import get_atmospheric_data_CS_Moldova_Noua
        from Romania.Caras_Severin.Oravita.CS_Oravita import get_atmospheric_data_CS_Oravita
        from Romania.Caras_Severin.Otelu_Rosu.CS_Otelu_Rosu import get_atmospheric_data_CS_Otelu_Rosu
        from Romania.Caras_Severin.Resita.CS_Resita import get_atmospheric_data_CS_Resita
        from Romania.Cluj_Napoca.Campia_Turzii.CJ_Campia_Turzii import get_atmospheric_data_CJ_Campia_Turzii
        from Romania.Cluj_Napoca.Cluj_Napoca.CJ_Cluj_Napoca import get_atmospheric_data_CJ_Cluj_Napoca
        from Romania.Cluj_Napoca.Dej.CJ_Dej import get_atmospheric_data_CJ_Dej
        from Romania.Cluj_Napoca.Gherla.CJ_Gherla import get_atmospheric_data_CJ_Gherla
        from Romania.Cluj_Napoca.Huedin.CJ_Huedin import get_atmospheric_data_CJ_Huedin
        from Romania.Cluj_Napoca.Turda.CJ_Turda import get_atmospheric_data_CJ_Turda
        from Romania.Constanta.Cernavoda.CT_Cernavoda import get_atmospheric_data_CT_Cernavoda
        from Romania.Constanta.Constanta.CT_Constanta import get_atmospheric_data_CT_Constanta
        from Romania.Constanta.Eforie.CT_Eforie import get_atmospheric_data_CT_Eforie
        from Romania.Constanta.Harsova.CT_Harsova import get_atmospheric_data_CT_Harsova
        from Romania.Constanta.Mangalia.CT_Mangalia import get_atmospheric_data_CT_Mangalia
        from Romania.Constanta.Medgidia.CT_Medgidia import get_atmospheric_data_CT_Medgidia
        from Romania.Constanta.Murfatlar.CT_Murfatlar import get_atmospheric_data_CT_Murfatlar
        from Romania.Constanta.Navodari.CT_Navodari import get_atmospheric_data_CT_Navodari
        from Romania.Constanta.Negru_Voda.CT_Negru_Voda import get_atmospheric_data_CT_Negru_Voda
        from Romania.Constanta.Ovidiu.CT_Ovidiu import get_atmospheric_data_CT_Ovidiu
        from Romania.Constanta.Techirghiol.CT_Techirghiol import get_atmospheric_data_CT_Techirghiol
        from Romania.Covasna.Baraolt.CV_Baraolt import get_atmospheric_data_CV_Baraolt
        from Romania.Covasna.Covasna.CV_Covasna import get_atmospheric_data_CV_Covasna
        from Romania.Covasna.Intorsura_Buzaului.CV_Intorsura_Buzaului import get_atmospheric_data_CV_Intorsura_Buzaului
        from Romania.Covasna.Sfantu_Gheorghe.CV_Sfantu_Gheorghe import get_atmospheric_data_CV_Sfantu_Gheorghe
        from Romania.Covasna.Targu_Secuiesc.CV_Targu_Secuiesc import get_atmospheric_data_CV_Targu_Secuiesc
        from Romania.Dambovita.Fieni.DB_Fieni import get_atmospheric_data_DB_Fieni
        from Romania.Dambovita.Gaesti.DB_Gaesti import get_atmospheric_data_DB_Gaesti
        from Romania.Dambovita.Moreni.DB_Moreni import get_atmospheric_data_DB_Moreni
        from Romania.Dambovita.Pucioasa.DB_Pucioasa import get_atmospheric_data_DB_Pucioasa
        from Romania.Dambovita.Racari.DB_Racari import get_atmospheric_data_DB_Racari
        from Romania.Dambovita.Targoviste.DB_Targoviste import get_atmospheric_data_DB_Targoviste
        from Romania.Dambovita.Titu.DB_Titu import get_atmospheric_data_DB_Titu
        from Romania.Dolj.Bailesti.DJ_Bailesti import get_atmospheric_data_DJ_Bailesti
        from Romania.Dolj.Bechet.DJ_Bechet import get_atmospheric_data_DJ_Bechet
        from Romania.Dolj.Calafat.DJ_Calafat import get_atmospheric_data_DJ_Calafat
        from Romania.Dolj.Craiova.DJ_Craiova import get_atmospheric_data_DJ_Craiova
        from Romania.Dolj.Dabuleni.DJ_Dabuleni import get_atmospheric_data_DJ_Dabuleni
        from Romania.Dolj.Filiasi.DJ_Filiasi import get_atmospheric_data_DJ_Filiasi
        from Romania.Dolj.Segarcea.DJ_Segarcea import get_atmospheric_data_DJ_Segarcea
        from Romania.Galati.Beresti.GL_Beresti import get_atmospheric_data_GL_Beresti
        from Romania.Galati.Galati.GL_Galati import get_atmospheric_data_GL_Galati
        from Romania.Galati.Targu_Bujor.GL_Targu_Bujor import get_atmospheric_data_GL_Targu_Bujor
        from Romania.Galati.Tecuci.GL_Tecuci import get_atmospheric_data_GL_Tecuci
        from Romania.Giurgiu.Bolintin_Vale.GR_Bolintin_Vale import get_atmospheric_data_GR_Bolintin_Vale
        from Romania.Giurgiu.Giurgiu.GR_Giurgiu import get_atmospheric_data_GR_Giurgiu
        from Romania.Giurgiu.Mihailesti.GR_Mihailesti import get_atmospheric_data_GR_Mihailesti
        from Romania.Gorj.Bumbesti_Jiu.GJ_Bumbesti_Jiu import get_atmospheric_data_GJ_Bumbesti_Jiu
        from Romania.Gorj.Motru.GJ_Motru import get_atmospheric_data_GJ_Motru
        from Romania.Gorj.Novaci.GJ_Novaci import get_atmospheric_data_GJ_Novaci
        from Romania.Gorj.Rovinari.GJ_Rovinari import get_atmospheric_data_GJ_Rovinari
        from Romania.Gorj.Targu_Carbunesti.GJ_Targu_Carbunesti import get_atmospheric_data_GJ_Targu_Carbunesti
        from Romania.Gorj.Targu_Jiu.GJ_Targu_Jiu import get_atmospheric_data_GJ_Targu_Jiu
        from Romania.Gorj.Ticleni.GJ_Ticleni import get_atmospheric_data_GJ_Ticleni
        from Romania.Gorj.Tismana.GJ_Tismana import get_atmospheric_data_GJ_Tismana
        from Romania.Harghita.Baile_Tusnad.HR_Baile_Tusnad import get_atmospheric_data_HR_Baile_Tusnad
        from Romania.Harghita.Balan.HR_Balan import get_atmospheric_data_HR_Balan
        from Romania.Harghita.Borsec.HR_Borsec import get_atmospheric_data_HR_Borsec
        from Romania.Harghita.Cristuru_Secuiesc.HR_Cristuru_Secuiesc import get_atmospheric_data_HR_Cristuru_Secuiesc
        from Romania.Harghita.Gheorgheni.HR_Gheorgheni import get_atmospheric_data_HR_Gheorgheni
        from Romania.Harghita.Miercurea_Ciuc.HR_Miercurea_Ciuc import get_atmospheric_data_HR_Miercurea_Ciuc
        from Romania.Harghita.Odorheiu_Secuiesc.HR_Odorheiu_Secuiesc import get_atmospheric_data_HR_Odorheiu_Secuiesc
        from Romania.Harghita.Toplita.HR_Toplita import get_atmospheric_data_HR_Toplita
        from Romania.Harghita.Vlahita.HR_Vlahita import get_atmospheric_data_HR_Vlahita
        from Romania.Hunedoara.Deva.HD_Deva import get_atmospheric_data_HD_Deva  
        from Romania.Hunedoara.Aninoasa.HD_Aninoasa import get_atmospheric_data_HD_Aninoasa
        from Romania.Hunedoara.Brad.HD_Brad import get_atmospheric_data_HD_Brad
        from Romania.Hunedoara.Calan.HD_Calan import get_atmospheric_data_HD_Calan
        from Romania.Hunedoara.Geoagiu.HD_Geoagiu import get_atmospheric_data_HD_Geoagiu
        from Romania.Hunedoara.Hateg.HD_Hateg import get_atmospheric_data_HD_Hateg
        from Romania.Hunedoara.Hunedoara.HD_Hunedoara import get_atmospheric_data_HD_Hunedoara
        from Romania.Hunedoara.Lupeni.HD_Lupeni import get_atmospheric_data_HD_Lupeni
        from Romania.Hunedoara.Orastie.HD_Orastie import get_atmospheric_data_HD_Orastie
        from Romania.Hunedoara.Petrila.HD_Petrila import get_atmospheric_data_HD_Petrila
        from Romania.Hunedoara.Petrosani.HD_Petrosani import get_atmospheric_data_HD_Petrosani
        from Romania.Hunedoara.Simeria.HD_Simeria import get_atmospheric_data_HD_Simeria
        from Romania.Hunedoara.Uricani.HD_Uricani import get_atmospheric_data_HD_Uricani
        from Romania.Hunedoara.Vulcan.HD_Vulcan import get_atmospheric_data_HD_Vulcan
        from Romania.Ialomita.Amara.IL_Amara import get_atmospheric_data_IL_Amara
        from Romania.Ialomita.Cazanesti.IL_Cazanesti import get_atmospheric_data_IL_Cazanesti
        from Romania.Ialomita.Fetesti.IL_Fetesti import get_atmospheric_data_IL_Fetesti
        from Romania.Ialomita.Fierbinti_Targ.IL_Fierbinti_Targ import get_atmospheric_data_IL_Fierbinti_Targ
        from Romania.Ialomita.Slobozia.IL_Slobozia import get_atmospheric_data_IL_Slobozia
        from Romania.Ialomita.Tandarei.IL_Tandarei import get_atmospheric_data_IL_Tandarei
        from Romania.Ialomita.Urziceni.IL_Urziceni import get_atmospheric_data_IL_Urziceni
        from Romania.Iasi.Harlau.IS_Harlau import get_atmospheric_data_IS_Harlau
        from Romania.Iasi.Iasi.IS_Iasi import get_atmospheric_data_IS_Iasi
        from Romania.Iasi.Pascani.IS_Pascani import get_atmospheric_data_IS_Pascani
        from Romania.Iasi.Podu_Iloaiei.IS_Podu_Iloaiei import get_atmospheric_data_IS_Podu_Iloaiei
        from Romania.Iasi.Targu_Frumos.IS_Targu_Frumos import get_atmospheric_data_IS_Targu_Frumos
        from Romania.Ilfov.Bragadiru.IF_Bragadiru import get_atmospheric_data_IF_Bragadiru
        from Romania.Ilfov.Buftea.IF_Buftea import get_atmospheric_data_IF_Buftea
        from Romania.Ilfov.Chitila.IF_Chitila import get_atmospheric_data_IF_Chitila
        from Romania.Ilfov.Magurele.IF_Magurele import get_atmospheric_data_IF_Magurele
        from Romania.Ilfov.Otopeni.IF_Otopeni import get_atmospheric_data_IF_Otopeni
        from Romania.Ilfov.Pantelimon.IF_Pantelimon import get_atmospheric_data_IF_Pantelimon
        from Romania.Ilfov.Popesti_Leordeni.IF_Popesti_Leordeni import get_atmospheric_data_IF_Popesti_Leordeni
        from Romania.Ilfov.Voluntari.IF_Voluntari import get_atmospheric_data_IF_Voluntari
        from Romania.Maramures.Baia_Mare.MM_Baia_Mare import get_atmospheric_data_MM_Baia_Mare
        from Romania.Maramures.Baia_Sprie.MM_Baia_Sprie import get_atmospheric_data_MM_Baia_Sprie
        from Romania.Maramures.Borsa.MM_Borsa import get_atmospheric_data_MM_Borsa
        from Romania.Maramures.Cavnic.MM_Cavnic import get_atmospheric_data_MM_Cavnic
        from Romania.Maramures.Dragomiresti.MM_Dragomiresti import get_atmospheric_data_MM_Dragomiresti
        from Romania.Maramures.Salistea_de_Sus.MM_Salistea_de_Sus import get_atmospheric_data_MM_Salistea_de_Sus
        from Romania.Maramures.Seini.MM_Seini import get_atmospheric_data_MM_Seini
        from Romania.Maramures.Sighetu_Marmatiei.MM_Sighetu_Marmatiei import get_atmospheric_data_MM_Sighetu_Marmatiei
        from Romania.Maramures.Somcuta_Mare.MM_Somcuta_Mare import get_atmospheric_data_MM_Somcuta_Mare
        from Romania.Maramures.Targu_Lapus.MM_Targu_Lapus import get_atmospheric_data_MM_Targu_Lapus
        from Romania.Maramures.Tautii_Magheraus.MM_Tautii_Magheraus import get_atmospheric_data_MM_Tautii_Magheraus
        from Romania.Maramures.Ulmeni.MM_Ulmeni import get_atmospheric_data_MM_Ulmeni
        from Romania.Maramures.Viseu_de_Sus.MM_Viseu_de_Sus import get_atmospheric_data_MM_Viseu_de_Sus
        from Romania.Mehedinti.Baia_de_Arama.MH_Baia_de_Arama import get_atmospheric_data_MH_Baia_de_Arama
        from Romania.Mehedinti.Drobeta_Turnu_Severin.MH_Drobeta_Turnu_Severin import get_atmospheric_data_MH_Drobeta_Turnu_Severin
        from Romania.Mehedinti.Orsova.MH_Orsova import get_atmospheric_data_MH_Orsova
        from Romania.Mehedinti.Strehaia.MH_Strehaia import get_atmospheric_data_MH_Strehaia
        from Romania.Mehedinti.Vanju_Mare.MH_Vanju_Mare import get_atmospheric_data_MH_Vanju_Mare
        from Romania.Mures.Iernut.MS_Iernut import get_atmospheric_data_MS_Iernut
        from Romania.Mures.Ludus.MS_Ludus import get_atmospheric_data_MS_Ludus
        from Romania.Mures.Miercurea_Nirajului.MS_Miercurea_Nirajului import get_atmospheric_data_MS_Miercurea_Nirajului
        from Romania.Mures.Reghin.MS_Reghin import get_atmospheric_data_MS_Reghin
        from Romania.Mures.Sangeorgiu_de_Padure.MS_Sangeorgiu_de_Padure import get_atmospheric_data_MS_Sangeorgiu_de_Padure
        from Romania.Mures.Sarmasu.MS_Sarmasu import get_atmospheric_data_MS_Sarmasu
        from Romania.Mures.Sighisoara.MS_Sighisoara import get_atmospheric_data_MS_Sighisoara
        from Romania.Mures.Sovata.MS_Sovata import get_atmospheric_data_MS_Sovata
        from Romania.Mures.Targu_Mures.MS_Targu_Mures import get_atmospheric_data_MS_Targu_Mures
        from Romania.Mures.Tarnaveni.MS_Tarnaveni import get_atmospheric_data_MS_Tarnaveni
        from Romania.Mures.Ungheni.MS_Ungheni import get_atmospheric_data_MS_Ungheni
        from Romania.Neamt.Bicaz.NT_Bicaz import get_atmospheric_data_NT_Bicaz
        from Romania.Neamt.Piatra_Neamt.NT_Piatra_Neamt import get_atmospheric_data_NT_Piatra_Neamt
        from Romania.Neamt.Roman.NT_Roman import get_atmospheric_data_NT_Roman
        from Romania.Neamt.Roznov.NT_Roznov import get_atmospheric_data_NT_Roznov
        from Romania.Neamt.Targu_Neamt.NT_Targu_Neamt import get_atmospheric_data_NT_Targu_Neamt
        from Romania.Olt.Bals.OT_Bals import get_atmospheric_data_OT_Bals
        from Romania.Olt.Caracal.OT_Caracal import get_atmospheric_data_OT_Caracal
        from Romania.Olt.Corabia.OT_Corabia import get_atmospheric_data_OT_Corabia
        from Romania.Olt.Draganesti_Olt.OT_Draganesti_Olt import get_atmospheric_data_OT_Draganesti_Olt
        from Romania.Olt.Piatra_Olt.OT_Piatra_Olt import get_atmospheric_data_OT_Piatra_Olt
        from Romania.Olt.Potcoava.OT_Potcoava import get_atmospheric_data_OT_Potcoava
        from Romania.Olt.Scornicesti.OT_Scornicesti import get_atmospheric_data_OT_Scornicesti
        from Romania.Olt.Slatina.OT_Slatina import get_atmospheric_data_OT_Slatina
        from Romania.Prahova.Azuga.PH_Azuga import get_atmospheric_data_PH_Azuga
        from Romania.Prahova.Baicoi.PH_Baicoi import get_atmospheric_data_PH_Baicoi
        from Romania.Prahova.Boldesti_Scaeni.PH_Boldesti_Scaeni import get_atmospheric_data_PH_Boldesti_Scaeni
        from Romania.Prahova.Breaza.PH_Breaza import get_atmospheric_data_PH_Breaza
        from Romania.Prahova.Busteni.PH_Busteni import get_atmospheric_data_PH_Busteni
        from Romania.Prahova.Campina.PH_Campina import get_atmospheric_data_PH_Campina
        from Romania.Prahova.Comarnic.PH_Comarnic import get_atmospheric_data_PH_Comarnic
        from Romania.Prahova.Mizil.PH_Mizil import get_atmospheric_data_PH_Mizil
        from Romania.Prahova.Ploiesti.PH_Ploiesti import get_atmospheric_data_PH_Ploiesti
        from Romania.Prahova.Plopeni.PH_Plopeni import get_atmospheric_data_PH_Plopeni
        from Romania.Prahova.Sinaia.PH_Sinaia import get_atmospheric_data_PH_Sinaia
        from Romania.Prahova.Slanic.PH_Slanic import get_atmospheric_data_PH_Slanic
        from Romania.Prahova.Urlati.PH_Urlati import get_atmospheric_data_PH_Urlati
        from Romania.Prahova.Valenii_de_Munte.PH_Valenii_de_Munte import get_atmospheric_data_PH_Valenii_de_Munte
        from Romania.Salaj.Cehu_Silvaniei.SJ_Cehu_Silvaniei import get_atmospheric_data_SJ_Cehu_Silvaniei
        from Romania.Salaj.Jibou.SJ_Jibou import get_atmospheric_data_SJ_Jibou
        from Romania.Salaj.Simleu_Silvaniei.SJ_Simleu_Silvaniei import get_atmospheric_data_SJ_Simleu_Silvaniei
        from Romania.Salaj.Zalau.SJ_Zalau import get_atmospheric_data_SJ_Zalau
        from Romania.Satu_Mare.Ardud.SM_Ardud import get_atmospheric_data_SM_Ardud
        from Romania.Satu_Mare.Carei.SM_Carei import get_atmospheric_data_SM_Carei
        from Romania.Satu_Mare.Livada.SM_Livada import get_atmospheric_data_SM_Livada
        from Romania.Satu_Mare.Negresti_Oas.SM_Negresti_Oas import get_atmospheric_data_SM_Negresti_Oas
        from Romania.Satu_Mare.Satu_Mare.SM_Satu_Mare import get_atmospheric_data_SM_Satu_Mare
        from Romania.Satu_Mare.Tasnad.SM_Tasnad import get_atmospheric_data_SM_Tasnad
        from Romania.Sibiu.Agnita.SB_Agnita import get_atmospheric_data_SB_Agnita
        from Romania.Sibiu.Avrig.SB_Avrig import get_atmospheric_data_SB_Avrig
        from Romania.Sibiu.Cisnadie.SB_Cisnadie import get_atmospheric_data_SB_Cisnadie
        from Romania.Sibiu.Copsa_Mica.SB_Copsa_Mica import get_atmospheric_data_SB_Copsa_Mica
        from Romania.Sibiu.Dumbraveni.SB_Dumbraveni import get_atmospheric_data_SB_Dumbraveni
        from Romania.Sibiu.Medias.SB_Medias import get_atmospheric_data_SB_Medias
        from Romania.Sibiu.Miercurea_Sibiului.SB_Miercurea_Sibiului import get_atmospheric_data_SB_Miercurea_Sibiului
        from Romania.Sibiu.Ocna_Sibiului.SB_Ocna_Sibiului import get_atmospheric_data_SB_Ocna_Sibiului
        from Romania.Sibiu.Saliste.SB_Saliste import get_atmospheric_data_SB_Saliste
        from Romania.Sibiu.Sibiu.SB_Sibiu import get_atmospheric_data_SB_Sibiu
        from Romania.Sibiu.Talmaciu.SB_Talmaciu import get_atmospheric_data_SB_Talmaciu
        from Romania.Suceava.Brosteni.SV_Brosteni import get_atmospheric_data_SV_Brosteni
        from Romania.Suceava.Cajvana.SV_Cajvana import get_atmospheric_data_SV_Cajvana
        from Romania.Suceava.Campulung_Moldovenesc.SV_Campulung_Moldovenesc import get_atmospheric_data_SV_Campulung_Moldovenesc
        from Romania.Suceava.Dolhasca.SV_Dolhasca import get_atmospheric_data_SV_Dolhasca
        from Romania.Suceava.Falticeni.SV_Falticeni import get_atmospheric_data_SV_Falticeni
        from Romania.Suceava.Frasin.SV_Frasin import get_atmospheric_data_SV_Frasin
        from Romania.Suceava.Gura_Humorului.SV_Gura_Humorului import get_atmospheric_data_SV_Gura_Humorului
        from Romania.Suceava.Liteni.SV_Liteni import get_atmospheric_data_SV_Liteni
        from Romania.Suceava.Milisauti.SV_Milisauti import get_atmospheric_data_SV_Milisauti
        from Romania.Suceava.Radauti.SV_Radauti import get_atmospheric_data_SV_Radauti
        from Romania.Suceava.Salcea.SV_Salcea import get_atmospheric_data_SV_Salcea
        from Romania.Suceava.Siret.SV_Siret import get_atmospheric_data_SV_Siret
        from Romania.Suceava.Solca.SV_Solca import get_atmospheric_data_SV_Solca
        from Romania.Suceava.Suceava.SV_Suceava import get_atmospheric_data_SV_Suceava
        from Romania.Suceava.Vatra_Dornei.SV_Vatra_Dornei import get_atmospheric_data_SV_Vatra_Dornei
        from Romania.Suceava.Vicovu_de_Sus.SV_Vicovu_de_Sus import get_atmospheric_data_SV_Vicovu_de_Sus
        from Romania.Teleorman.Alexandria.TR_Alexandria import get_atmospheric_data_TR_Alexandria
        from Romania.Teleorman.Rosiorii_de_Vede.TR_Rosiorii_de_Vede import get_atmospheric_data_TR_Rosiorii_de_Vede
        from Romania.Teleorman.Turnu_Magurele.TR_Turnu_Magurele import get_atmospheric_data_TR_Turnu_Magurele
        from Romania.Teleorman.Videle.TR_Videle import get_atmospheric_data_TR_Videle
        from Romania.Teleorman.Zimnicea.TR_Zimnicea import get_atmospheric_data_TR_Zimnicea
        from Romania.Timis.Buzias.TM_Buzias import get_atmospheric_data_TM_Buzias
        from Romania.Timis.Ciacova.TM_Ciacova import get_atmospheric_data_TM_Ciacova
        from Romania.Timis.Deta.TM_Deta import get_atmospheric_data_TM_Deta
        from Romania.Timis.Faget.TM_Faget import get_atmospheric_data_TM_Faget
        from Romania.Timis.Gataia.TM_Gataia import get_atmospheric_data_TM_Gataia
        from Romania.Timis.Jimbolia.TM_Jimbolia import get_atmospheric_data_TM_Jimbolia
        from Romania.Timis.Lugoj.TM_Lugoj import get_atmospheric_data_TM_Lugoj
        from Romania.Timis.Recas.TM_Recas import get_atmospheric_data_TM_Recas
        from Romania.Timis.Sannicolau_Mare.TM_Sannicolau_Mare import get_atmospheric_data_TM_Sannicolau_Mare
        from Romania.Timis.Timisoara.TM_Timisoara import get_atmospheric_data_TM_Timisoara
        from Romania.Tulcea.Babadag.TL_Babadag import get_atmospheric_data_TL_Babadag
        from Romania.Tulcea.Isaccea.TL_Isaccea import get_atmospheric_data_TL_Isaccea
        from Romania.Tulcea.Macin.TL_Macin import get_atmospheric_data_TL_Macin
        from Romania.Tulcea.Sulina.TL_Sulina import get_atmospheric_data_TL_Sulina
        from Romania.Tulcea.Tulcea.TL_Tulcea import get_atmospheric_data_TL_Tulcea
        from Romania.Valcea.Babeni.VL_Babeni import get_atmospheric_data_VL_Babeni
        from Romania.Valcea.Baile_Govora.VL_Baile_Govora import get_atmospheric_data_VL_Baile_Govora
        from Romania.Valcea.Baile_Olanesti.VL_Baile_Olanesti import get_atmospheric_data_VL_Baile_Olanesti
        from Romania.Valcea.Balcesti.VL_Balcesti import get_atmospheric_data_VL_Balcesti
        from Romania.Valcea.Berbesti.VL_Berbesti import get_atmospheric_data_VL_Berbesti
        from Romania.Valcea.Brezoi.VL_Brezoi import get_atmospheric_data_VL_Brezoi
        from Romania.Valcea.Calimanesti.VL_Calimanesti import get_atmospheric_data_VL_Calimanesti
        from Romania.Valcea.Dragasani.VL_Dragasani import get_atmospheric_data_VL_Dragasani
        from Romania.Valcea.Horezu.VL_Horezu import get_atmospheric_data_VL_Horezu
        from Romania.Valcea.Ocnele_Mari.VL_Ocnele_Mari import get_atmospheric_data_VL_Ocnele_Mari
        from Romania.Valcea.Ramnicu_Valcea.VL_Ramnicu_Valcea import get_atmospheric_data_VL_Ramnicu_Valcea
        from Romania.Vaslui.Barlad.VS_Barlad import get_atmospheric_data_VS_Barlad
        from Romania.Vaslui.Husi.VS_Husi import get_atmospheric_data_VS_Husi
        from Romania.Vaslui.Murgeni.VS_Murgeni import get_atmospheric_data_VS_Murgeni
        from Romania.Vaslui.Negresti.VS_Negresti import get_atmospheric_data_VS_Negresti
        from Romania.Vaslui.Vaslui.VS_Vaslui import get_atmospheric_data_VS_Vaslui
        from Romania.Vrancea.Adjud.VN_Adjud import get_atmospheric_data_VN_Adjud
        from Romania.Vrancea.Focsani.VN_Focsani import get_atmospheric_data_VN_Focsani
        from Romania.Vrancea.Marasesti.VN_Marasesti import get_atmospheric_data_VN_Marasesti
        from Romania.Vrancea.Odobesti.VN_Odobesti import get_atmospheric_data_VN_Odobesti
        from Romania.Vrancea.Panciu.VN_Panciu import get_atmospheric_data_VN_Panciu
        print("The atmospheric domain module (adlsa) is running.")
else: # relative import
        from .Romania.Alba.Abrud.AB_Abrud import get_atmospheric_data_AB_Abrud
        from .Romania.Alba.Aiud.AB_Aiud import get_atmospheric_data_AB_Aiud
        from .Romania.Alba.Alba_Iulia.AB_Alba_Iulia import get_atmospheric_data_AB_Alba_Iulia
        from .Romania.Alba.Baia_de_Aries.AB_Baia_de_Aries import get_atmospheric_data_AB_Baia_de_Aries
        from .Romania.Alba.Blaj.AB_Blaj import get_atmospheric_data_AB_Blaj
        from .Romania.Alba.Campeni.AB_Campeni import get_atmospheric_data_AB_Campeni
        from .Romania.Alba.Cugir.AB_Cugir import get_atmospheric_data_AB_Cugir
        from .Romania.Alba.Ocna_Mures.AB_Ocna_Mures import get_atmospheric_data_AB_Ocna_Mures
        from .Romania.Alba.Sebes.AB_Sebes import get_atmospheric_data_AB_Sebes
        from .Romania.Alba.Teius.AB_Teius import get_atmospheric_data_AB_Teius
        from .Romania.Alba.Zlatna.AB_Zlatna import get_atmospheric_data_AB_Zlatna
        from .Romania.Arad.Arad.AR_Arad import get_atmospheric_data_AR_Arad
        from .Romania.Arad.Chisineu_Cris.AR_Chisineu_Cris import get_atmospheric_data_AR_Chisineu_Cris
        from .Romania.Arad.Curtici.AR_Curtici import get_atmospheric_data_AR_Curtici
        from .Romania.Arad.Ineu.AR_Ineu import get_atmospheric_data_AR_Ineu
        from .Romania.Arad.Lipova.AR_Lipova import get_atmospheric_data_AR_Lipova
        from .Romania.Arad.Nadlac.AR_Nadlac import get_atmospheric_data_AR_Nadlac
        from .Romania.Arad.Pancota.AR_Pancota import get_atmospheric_data_AR_Pancota
        from .Romania.Arad.Pecica.AR_Pecica import get_atmospheric_data_AR_Pecica
        from .Romania.Arad.Santana.AR_Santana import get_atmospheric_data_AR_Santana
        from .Romania.Arges.Campulung.AG_Campulung import get_atmospheric_data_AG_Campulung
        from .Romania.Arges.Costesti.AG_Costesti import get_atmospheric_data_AG_Costesti
        from .Romania.Arges.Curtea_de_Arges.AG_Curtea_de_Arges import get_atmospheric_data_AG_Curtea_de_Arges
        from .Romania.Arges.Mioveni.AG_Mioveni import get_atmospheric_data_AG_Mioveni
        from .Romania.Arges.Pitesti.AG_Pitesti import get_atmospheric_data_AG_Pitesti
        from .Romania.Arges.Stefanesti.AG_Stefanesti import get_atmospheric_data_AG_Stefanesti
        from .Romania.Arges.Topoloveni.AG_Topoloveni import get_atmospheric_data_AG_Topoloveni
        from .Romania.Bacau.Bacau.BC_Bacau import get_atmospheric_data_BC_Bacau
        from .Romania.Bacau.Buhusi.BC_Buhusi import get_atmospheric_data_BC_Buhusi
        from .Romania.Bacau.Comanesti.BC_Comanesti import get_atmospheric_data_BC_Comanesti
        from .Romania.Bacau.Darmanesti.BC_Darmanesti import get_atmospheric_data_BC_Darmanesti
        from .Romania.Bacau.Moinesti.BC_Moinesti import get_atmospheric_data_BC_Moinesti
        from .Romania.Bacau.Onesti.BC_Onesti import get_atmospheric_data_BC_Onesti
        from .Romania.Bacau.Slanic_Moldova.BC_Slanic_Moldova import get_atmospheric_data_BC_Slanic_Moldova
        from .Romania.Bacau.Targu_Ocna.BC_Targu_Ocna import get_atmospheric_data_BC_Targu_Ocna
        from .Romania.Bihor.Alesd.BH_Alesd import get_atmospheric_data_BH_Alesd
        from .Romania.Bihor.Beius.BH_Beius import get_atmospheric_data_BH_Beius
        from .Romania.Bihor.Marghita.BH_Marghita import get_atmospheric_data_BH_Marghita
        from .Romania.Bihor.Nucet.BH_Nucet import get_atmospheric_data_BH_Nucet
        from .Romania.Bihor.Oradea.BH_Oradea import get_atmospheric_data_BH_Oradea
        from .Romania.Bihor.Sacueni.BH_Sacueni import get_atmospheric_data_BH_Sacueni
        from .Romania.Bihor.Salonta.BH_Salonta import get_atmospheric_data_BH_Salonta
        from .Romania.Bihor.Stei.BH_Stei import get_atmospheric_data_BH_Stei
        from .Romania.Bihor.Valea_lui_Mihai.BH_Valea_lui_Mihai import get_atmospheric_data_BH_Valea_lui_Mihai
        from .Romania.Bihor.Vascau.BH_Vascau import get_atmospheric_data_BH_Vascau
        from .Romania.Bistrita_Nasaud.Beclean.BN_Beclean import get_atmospheric_data_BN_Beclean
        from .Romania.Bistrita_Nasaud.Bistrita.BN_Bistrita import get_atmospheric_data_BN_Bistrita
        from .Romania.Bistrita_Nasaud.Nasaud.BN_Nasaud import get_atmospheric_data_BN_Nasaud
        from .Romania.Bistrita_Nasaud.Sangeorz_Bai.BN_Sangeorz_Bai import get_atmospheric_data_BN_Sangeorz_Bai
        from .Romania.Botosani.Botosani.BT_Botosani import get_atmospheric_data_BT_Botosani
        from .Romania.Botosani.Bucecea.BT_Bucecea import get_atmospheric_data_BT_Bucecea
        from .Romania.Botosani.Darabani.BT_Darabani import get_atmospheric_data_BT_Darabani
        from .Romania.Botosani.Dorohoi.BT_Dorohoi import get_atmospheric_data_BT_Dorohoi
        from .Romania.Botosani.Flamanzi.BT_Flamanzi import get_atmospheric_data_BT_Flamanzi
        from .Romania.Botosani.Saveni.BT_Saveni import get_atmospheric_data_BT_Saveni
        from .Romania.Botosani.Stefanesti.BT_Stefanesti import get_atmospheric_data_BT_Stefanesti
        from .Romania.Braila.Braila.BR_Braila import get_atmospheric_data_BR_Braila
        from .Romania.Braila.Faurei.BR_Faurei import get_atmospheric_data_BR_Faurei
        from .Romania.Braila.Ianca.BR_Ianca import get_atmospheric_data_BR_Ianca
        from .Romania.Braila.Insuratei.BR_Insuratei import get_atmospheric_data_BR_Insuratei
        from .Romania.Brasov.Brasov.BV_Brasov import get_atmospheric_data_BV_Brasov
        from .Romania.Brasov.Codlea.BV_Codlea import get_atmospheric_data_BV_Codlea
        from .Romania.Brasov.Fagaras.BV_Fagaras import get_atmospheric_data_BV_Fagaras
        from .Romania.Brasov.Ghimbav.BV_Ghimbav import get_atmospheric_data_BV_Ghimbav
        from .Romania.Brasov.Predeal.BV_Predeal import get_atmospheric_data_BV_Predeal
        from .Romania.Brasov.Rasnov.BV_Rasnov import get_atmospheric_data_BV_Rasnov
        from .Romania.Brasov.Rupea.BV_Rupea import get_atmospheric_data_BV_Rupea
        from .Romania.Brasov.Sacele.BV_Sacele import get_atmospheric_data_BV_Sacele
        from .Romania.Brasov.Victoria.BV_Victoria import get_atmospheric_data_BV_Victoria
        from .Romania.Brasov.Zarnesti.BV_Zarnesti import get_atmospheric_data_BV_Zarnesti
        from .Romania.Bucuresti.B_Bucuresti import get_atmospheric_data_B_Bucuresti
        from .Romania.Buzau.Buzau.BZ_Buzau import get_atmospheric_data_BZ_Buzau
        from .Romania.Buzau.Nehoiu.BZ_Nehoiu import get_atmospheric_data_BZ_Nehoiu
        from .Romania.Buzau.Patarlagele.BZ_Patarlagele import get_atmospheric_data_BZ_Patarlagele
        from .Romania.Buzau.Pogoanele.BZ_Pogoanele import get_atmospheric_data_BZ_Pogoanele
        from .Romania.Buzau.Ramnicu_Sarat.BZ_Ramnicu_Sarat import get_atmospheric_data_BZ_Ramnicu_Sarat
        from .Romania.Calarasi.Budesti.CL_Budesti import get_atmospheric_data_CL_Budesti
        from .Romania.Calarasi.Calarasi.CL_Calarasi import get_atmospheric_data_CL_Calarasi
        from .Romania.Calarasi.Fundulea.CL_Fundulea import get_atmospheric_data_CL_Fundulea
        from .Romania.Calarasi.Lehliu_Gara.CL_Lehliu_Gara import get_atmospheric_data_CL_Lehliu_Gara
        from .Romania.Calarasi.Oltenita.CL_Oltenita import get_atmospheric_data_CL_Oltenita
        from .Romania.Caras_Severin.Anina.CS_Anina import get_atmospheric_data_CS_Anina
        from .Romania.Caras_Severin.Baile_Herculane.CS_Baile_Herculane import get_atmospheric_data_CS_Baile_Herculane
        from .Romania.Caras_Severin.Bocsa.CS_Bocsa import get_atmospheric_data_CS_Bocsa
        from .Romania.Caras_Severin.Caransebes.CS_Caransebes import get_atmospheric_data_CS_Caransebes
        from .Romania.Caras_Severin.Moldova_Noua.CS_Moldova_Noua import get_atmospheric_data_CS_Moldova_Noua
        from .Romania.Caras_Severin.Oravita.CS_Oravita import get_atmospheric_data_CS_Oravita
        from .Romania.Caras_Severin.Otelu_Rosu.CS_Otelu_Rosu import get_atmospheric_data_CS_Otelu_Rosu
        from .Romania.Caras_Severin.Resita.CS_Resita import get_atmospheric_data_CS_Resita
        from .Romania.Cluj_Napoca.Campia_Turzii.CJ_Campia_Turzii import get_atmospheric_data_CJ_Campia_Turzii
        from .Romania.Cluj_Napoca.Cluj_Napoca.CJ_Cluj_Napoca import get_atmospheric_data_CJ_Cluj_Napoca
        from .Romania.Cluj_Napoca.Dej.CJ_Dej import get_atmospheric_data_CJ_Dej
        from .Romania.Cluj_Napoca.Gherla.CJ_Gherla import get_atmospheric_data_CJ_Gherla
        from .Romania.Cluj_Napoca.Huedin.CJ_Huedin import get_atmospheric_data_CJ_Huedin
        from .Romania.Cluj_Napoca.Turda.CJ_Turda import get_atmospheric_data_CJ_Turda
        from .Romania.Constanta.Cernavoda.CT_Cernavoda import get_atmospheric_data_CT_Cernavoda
        from .Romania.Constanta.Constanta.CT_Constanta import get_atmospheric_data_CT_Constanta
        from .Romania.Constanta.Eforie.CT_Eforie import get_atmospheric_data_CT_Eforie
        from .Romania.Constanta.Harsova.CT_Harsova import get_atmospheric_data_CT_Harsova
        from .Romania.Constanta.Mangalia.CT_Mangalia import get_atmospheric_data_CT_Mangalia
        from .Romania.Constanta.Medgidia.CT_Medgidia import get_atmospheric_data_CT_Medgidia
        from .Romania.Constanta.Murfatlar.CT_Murfatlar import get_atmospheric_data_CT_Murfatlar
        from .Romania.Constanta.Navodari.CT_Navodari import get_atmospheric_data_CT_Navodari
        from .Romania.Constanta.Negru_Voda.CT_Negru_Voda import get_atmospheric_data_CT_Negru_Voda
        from .Romania.Constanta.Ovidiu.CT_Ovidiu import get_atmospheric_data_CT_Ovidiu
        from .Romania.Constanta.Techirghiol.CT_Techirghiol import get_atmospheric_data_CT_Techirghiol
        from .Romania.Covasna.Baraolt.CV_Baraolt import get_atmospheric_data_CV_Baraolt
        from .Romania.Covasna.Covasna.CV_Covasna import get_atmospheric_data_CV_Covasna
        from .Romania.Covasna.Intorsura_Buzaului.CV_Intorsura_Buzaului import get_atmospheric_data_CV_Intorsura_Buzaului
        from .Romania.Covasna.Sfantu_Gheorghe.CV_Sfantu_Gheorghe import get_atmospheric_data_CV_Sfantu_Gheorghe
        from .Romania.Covasna.Targu_Secuiesc.CV_Targu_Secuiesc import get_atmospheric_data_CV_Targu_Secuiesc
        from .Romania.Dambovita.Fieni.DB_Fieni import get_atmospheric_data_DB_Fieni
        from .Romania.Dambovita.Gaesti.DB_Gaesti import get_atmospheric_data_DB_Gaesti
        from .Romania.Dambovita.Moreni.DB_Moreni import get_atmospheric_data_DB_Moreni
        from .Romania.Dambovita.Pucioasa.DB_Pucioasa import get_atmospheric_data_DB_Pucioasa
        from .Romania.Dambovita.Racari.DB_Racari import get_atmospheric_data_DB_Racari
        from .Romania.Dambovita.Targoviste.DB_Targoviste import get_atmospheric_data_DB_Targoviste
        from .Romania.Dambovita.Titu.DB_Titu import get_atmospheric_data_DB_Titu
        from .Romania.Dolj.Bailesti.DJ_Bailesti import get_atmospheric_data_DJ_Bailesti
        from .Romania.Dolj.Bechet.DJ_Bechet import get_atmospheric_data_DJ_Bechet
        from .Romania.Dolj.Calafat.DJ_Calafat import get_atmospheric_data_DJ_Calafat
        from .Romania.Dolj.Craiova.DJ_Craiova import get_atmospheric_data_DJ_Craiova
        from .Romania.Dolj.Dabuleni.DJ_Dabuleni import get_atmospheric_data_DJ_Dabuleni
        from .Romania.Dolj.Filiasi.DJ_Filiasi import get_atmospheric_data_DJ_Filiasi
        from .Romania.Dolj.Segarcea.DJ_Segarcea import get_atmospheric_data_DJ_Segarcea
        from .Romania.Galati.Beresti.GL_Beresti import get_atmospheric_data_GL_Beresti
        from .Romania.Galati.Galati.GL_Galati import get_atmospheric_data_GL_Galati
        from .Romania.Galati.Targu_Bujor.GL_Targu_Bujor import get_atmospheric_data_GL_Targu_Bujor
        from .Romania.Galati.Tecuci.GL_Tecuci import get_atmospheric_data_GL_Tecuci
        from .Romania.Giurgiu.Bolintin_Vale.GR_Bolintin_Vale import get_atmospheric_data_GR_Bolintin_Vale
        from .Romania.Giurgiu.Giurgiu.GR_Giurgiu import get_atmospheric_data_GR_Giurgiu
        from .Romania.Giurgiu.Mihailesti.GR_Mihailesti import get_atmospheric_data_GR_Mihailesti
        from .Romania.Gorj.Bumbesti_Jiu.GJ_Bumbesti_Jiu import get_atmospheric_data_GJ_Bumbesti_Jiu
        from .Romania.Gorj.Motru.GJ_Motru import get_atmospheric_data_GJ_Motru
        from .Romania.Gorj.Novaci.GJ_Novaci import get_atmospheric_data_GJ_Novaci
        from .Romania.Gorj.Rovinari.GJ_Rovinari import get_atmospheric_data_GJ_Rovinari
        from .Romania.Gorj.Targu_Carbunesti.GJ_Targu_Carbunesti import get_atmospheric_data_GJ_Targu_Carbunesti
        from .Romania.Gorj.Targu_Jiu.GJ_Targu_Jiu import get_atmospheric_data_GJ_Targu_Jiu
        from .Romania.Gorj.Ticleni.GJ_Ticleni import get_atmospheric_data_GJ_Ticleni
        from .Romania.Gorj.Tismana.GJ_Tismana import get_atmospheric_data_GJ_Tismana
        from .Romania.Harghita.Baile_Tusnad.HR_Baile_Tusnad import get_atmospheric_data_HR_Baile_Tusnad
        from .Romania.Harghita.Balan.HR_Balan import get_atmospheric_data_HR_Balan
        from .Romania.Harghita.Borsec.HR_Borsec import get_atmospheric_data_HR_Borsec
        from .Romania.Harghita.Cristuru_Secuiesc.HR_Cristuru_Secuiesc import get_atmospheric_data_HR_Cristuru_Secuiesc
        from .Romania.Harghita.Gheorgheni.HR_Gheorgheni import get_atmospheric_data_HR_Gheorgheni
        from .Romania.Harghita.Miercurea_Ciuc.HR_Miercurea_Ciuc import get_atmospheric_data_HR_Miercurea_Ciuc
        from .Romania.Harghita.Odorheiu_Secuiesc.HR_Odorheiu_Secuiesc import get_atmospheric_data_HR_Odorheiu_Secuiesc
        from .Romania.Harghita.Toplita.HR_Toplita import get_atmospheric_data_HR_Toplita
        from .Romania.Harghita.Vlahita.HR_Vlahita import get_atmospheric_data_HR_Vlahita
        from .Romania.Hunedoara.Deva.HD_Deva import get_atmospheric_data_HD_Deva  
        from .Romania.Hunedoara.Aninoasa.HD_Aninoasa import get_atmospheric_data_HD_Aninoasa
        from .Romania.Hunedoara.Brad.HD_Brad import get_atmospheric_data_HD_Brad
        from .Romania.Hunedoara.Calan.HD_Calan import get_atmospheric_data_HD_Calan
        from .Romania.Hunedoara.Geoagiu.HD_Geoagiu import get_atmospheric_data_HD_Geoagiu
        from .Romania.Hunedoara.Hateg.HD_Hateg import get_atmospheric_data_HD_Hateg
        from .Romania.Hunedoara.Hunedoara.HD_Hunedoara import get_atmospheric_data_HD_Hunedoara
        from .Romania.Hunedoara.Lupeni.HD_Lupeni import get_atmospheric_data_HD_Lupeni
        from .Romania.Hunedoara.Orastie.HD_Orastie import get_atmospheric_data_HD_Orastie
        from .Romania.Hunedoara.Petrila.HD_Petrila import get_atmospheric_data_HD_Petrila
        from .Romania.Hunedoara.Petrosani.HD_Petrosani import get_atmospheric_data_HD_Petrosani
        from .Romania.Hunedoara.Simeria.HD_Simeria import get_atmospheric_data_HD_Simeria
        from .Romania.Hunedoara.Uricani.HD_Uricani import get_atmospheric_data_HD_Uricani
        from .Romania.Hunedoara.Vulcan.HD_Vulcan import get_atmospheric_data_HD_Vulcan
        from .Romania.Ialomita.Amara.IL_Amara import get_atmospheric_data_IL_Amara
        from .Romania.Ialomita.Cazanesti.IL_Cazanesti import get_atmospheric_data_IL_Cazanesti
        from .Romania.Ialomita.Fetesti.IL_Fetesti import get_atmospheric_data_IL_Fetesti
        from .Romania.Ialomita.Fierbinti_Targ.IL_Fierbinti_Targ import get_atmospheric_data_IL_Fierbinti_Targ
        from .Romania.Ialomita.Slobozia.IL_Slobozia import get_atmospheric_data_IL_Slobozia
        from .Romania.Ialomita.Tandarei.IL_Tandarei import get_atmospheric_data_IL_Tandarei
        from .Romania.Ialomita.Urziceni.IL_Urziceni import get_atmospheric_data_IL_Urziceni
        from .Romania.Iasi.Harlau.IS_Harlau import get_atmospheric_data_IS_Harlau
        from .Romania.Iasi.Iasi.IS_Iasi import get_atmospheric_data_IS_Iasi
        from .Romania.Iasi.Pascani.IS_Pascani import get_atmospheric_data_IS_Pascani
        from .Romania.Iasi.Podu_Iloaiei.IS_Podu_Iloaiei import get_atmospheric_data_IS_Podu_Iloaiei
        from .Romania.Iasi.Targu_Frumos.IS_Targu_Frumos import get_atmospheric_data_IS_Targu_Frumos
        from .Romania.Ilfov.Bragadiru.IF_Bragadiru import get_atmospheric_data_IF_Bragadiru
        from .Romania.Ilfov.Buftea.IF_Buftea import get_atmospheric_data_IF_Buftea
        from .Romania.Ilfov.Chitila.IF_Chitila import get_atmospheric_data_IF_Chitila
        from .Romania.Ilfov.Magurele.IF_Magurele import get_atmospheric_data_IF_Magurele
        from .Romania.Ilfov.Otopeni.IF_Otopeni import get_atmospheric_data_IF_Otopeni
        from .Romania.Ilfov.Pantelimon.IF_Pantelimon import get_atmospheric_data_IF_Pantelimon
        from .Romania.Ilfov.Popesti_Leordeni.IF_Popesti_Leordeni import get_atmospheric_data_IF_Popesti_Leordeni
        from .Romania.Ilfov.Voluntari.IF_Voluntari import get_atmospheric_data_IF_Voluntari
        from .Romania.Maramures.Baia_Mare.MM_Baia_Mare import get_atmospheric_data_MM_Baia_Mare
        from .Romania.Maramures.Baia_Sprie.MM_Baia_Sprie import get_atmospheric_data_MM_Baia_Sprie
        from .Romania.Maramures.Borsa.MM_Borsa import get_atmospheric_data_MM_Borsa
        from .Romania.Maramures.Cavnic.MM_Cavnic import get_atmospheric_data_MM_Cavnic
        from .Romania.Maramures.Dragomiresti.MM_Dragomiresti import get_atmospheric_data_MM_Dragomiresti
        from .Romania.Maramures.Salistea_de_Sus.MM_Salistea_de_Sus import get_atmospheric_data_MM_Salistea_de_Sus
        from .Romania.Maramures.Seini.MM_Seini import get_atmospheric_data_MM_Seini
        from .Romania.Maramures.Sighetu_Marmatiei.MM_Sighetu_Marmatiei import get_atmospheric_data_MM_Sighetu_Marmatiei
        from .Romania.Maramures.Somcuta_Mare.MM_Somcuta_Mare import get_atmospheric_data_MM_Somcuta_Mare
        from .Romania.Maramures.Targu_Lapus.MM_Targu_Lapus import get_atmospheric_data_MM_Targu_Lapus
        from .Romania.Maramures.Tautii_Magheraus.MM_Tautii_Magheraus import get_atmospheric_data_MM_Tautii_Magheraus
        from .Romania.Maramures.Ulmeni.MM_Ulmeni import get_atmospheric_data_MM_Ulmeni
        from .Romania.Maramures.Viseu_de_Sus.MM_Viseu_de_Sus import get_atmospheric_data_MM_Viseu_de_Sus
        from .Romania.Mehedinti.Baia_de_Arama.MH_Baia_de_Arama import get_atmospheric_data_MH_Baia_de_Arama
        from .Romania.Mehedinti.Drobeta_Turnu_Severin.MH_Drobeta_Turnu_Severin import get_atmospheric_data_MH_Drobeta_Turnu_Severin
        from .Romania.Mehedinti.Orsova.MH_Orsova import get_atmospheric_data_MH_Orsova
        from .Romania.Mehedinti.Strehaia.MH_Strehaia import get_atmospheric_data_MH_Strehaia
        from .Romania.Mehedinti.Vanju_Mare.MH_Vanju_Mare import get_atmospheric_data_MH_Vanju_Mare
        from .Romania.Mures.Iernut.MS_Iernut import get_atmospheric_data_MS_Iernut
        from .Romania.Mures.Ludus.MS_Ludus import get_atmospheric_data_MS_Ludus
        from .Romania.Mures.Miercurea_Nirajului.MS_Miercurea_Nirajului import get_atmospheric_data_MS_Miercurea_Nirajului
        from .Romania.Mures.Reghin.MS_Reghin import get_atmospheric_data_MS_Reghin
        from .Romania.Mures.Sangeorgiu_de_Padure.MS_Sangeorgiu_de_Padure import get_atmospheric_data_MS_Sangeorgiu_de_Padure
        from .Romania.Mures.Sarmasu.MS_Sarmasu import get_atmospheric_data_MS_Sarmasu
        from .Romania.Mures.Sighisoara.MS_Sighisoara import get_atmospheric_data_MS_Sighisoara
        from .Romania.Mures.Sovata.MS_Sovata import get_atmospheric_data_MS_Sovata
        from .Romania.Mures.Targu_Mures.MS_Targu_Mures import get_atmospheric_data_MS_Targu_Mures
        from .Romania.Mures.Tarnaveni.MS_Tarnaveni import get_atmospheric_data_MS_Tarnaveni
        from .Romania.Mures.Ungheni.MS_Ungheni import get_atmospheric_data_MS_Ungheni
        from .Romania.Neamt.Bicaz.NT_Bicaz import get_atmospheric_data_NT_Bicaz
        from .Romania.Neamt.Piatra_Neamt.NT_Piatra_Neamt import get_atmospheric_data_NT_Piatra_Neamt
        from .Romania.Neamt.Roman.NT_Roman import get_atmospheric_data_NT_Roman
        from .Romania.Neamt.Roznov.NT_Roznov import get_atmospheric_data_NT_Roznov
        from .Romania.Neamt.Targu_Neamt.NT_Targu_Neamt import get_atmospheric_data_NT_Targu_Neamt
        from .Romania.Olt.Bals.OT_Bals import get_atmospheric_data_OT_Bals
        from .Romania.Olt.Caracal.OT_Caracal import get_atmospheric_data_OT_Caracal
        from .Romania.Olt.Corabia.OT_Corabia import get_atmospheric_data_OT_Corabia
        from .Romania.Olt.Draganesti_Olt.OT_Draganesti_Olt import get_atmospheric_data_OT_Draganesti_Olt
        from .Romania.Olt.Piatra_Olt.OT_Piatra_Olt import get_atmospheric_data_OT_Piatra_Olt
        from .Romania.Olt.Potcoava.OT_Potcoava import get_atmospheric_data_OT_Potcoava
        from .Romania.Olt.Scornicesti.OT_Scornicesti import get_atmospheric_data_OT_Scornicesti
        from .Romania.Olt.Slatina.OT_Slatina import get_atmospheric_data_OT_Slatina
        from .Romania.Prahova.Azuga.PH_Azuga import get_atmospheric_data_PH_Azuga
        from .Romania.Prahova.Baicoi.PH_Baicoi import get_atmospheric_data_PH_Baicoi
        from .Romania.Prahova.Boldesti_Scaeni.PH_Boldesti_Scaeni import get_atmospheric_data_PH_Boldesti_Scaeni
        from .Romania.Prahova.Breaza.PH_Breaza import get_atmospheric_data_PH_Breaza
        from .Romania.Prahova.Busteni.PH_Busteni import get_atmospheric_data_PH_Busteni
        from .Romania.Prahova.Campina.PH_Campina import get_atmospheric_data_PH_Campina
        from .Romania.Prahova.Comarnic.PH_Comarnic import get_atmospheric_data_PH_Comarnic
        from .Romania.Prahova.Mizil.PH_Mizil import get_atmospheric_data_PH_Mizil
        from .Romania.Prahova.Ploiesti.PH_Ploiesti import get_atmospheric_data_PH_Ploiesti
        from .Romania.Prahova.Plopeni.PH_Plopeni import get_atmospheric_data_PH_Plopeni
        from .Romania.Prahova.Sinaia.PH_Sinaia import get_atmospheric_data_PH_Sinaia
        from .Romania.Prahova.Slanic.PH_Slanic import get_atmospheric_data_PH_Slanic
        from .Romania.Prahova.Urlati.PH_Urlati import get_atmospheric_data_PH_Urlati
        from .Romania.Prahova.Valenii_de_Munte.PH_Valenii_de_Munte import get_atmospheric_data_PH_Valenii_de_Munte
        from .Romania.Salaj.Cehu_Silvaniei.SJ_Cehu_Silvaniei import get_atmospheric_data_SJ_Cehu_Silvaniei
        from .Romania.Salaj.Jibou.SJ_Jibou import get_atmospheric_data_SJ_Jibou
        from .Romania.Salaj.Simleu_Silvaniei.SJ_Simleu_Silvaniei import get_atmospheric_data_SJ_Simleu_Silvaniei
        from .Romania.Salaj.Zalau.SJ_Zalau import get_atmospheric_data_SJ_Zalau
        from .Romania.Satu_Mare.Ardud.SM_Ardud import get_atmospheric_data_SM_Ardud
        from .Romania.Satu_Mare.Carei.SM_Carei import get_atmospheric_data_SM_Carei
        from .Romania.Satu_Mare.Livada.SM_Livada import get_atmospheric_data_SM_Livada
        from .Romania.Satu_Mare.Negresti_Oas.SM_Negresti_Oas import get_atmospheric_data_SM_Negresti_Oas
        from .Romania.Satu_Mare.Satu_Mare.SM_Satu_Mare import get_atmospheric_data_SM_Satu_Mare
        from .Romania.Satu_Mare.Tasnad.SM_Tasnad import get_atmospheric_data_SM_Tasnad
        from .Romania.Sibiu.Agnita.SB_Agnita import get_atmospheric_data_SB_Agnita
        from .Romania.Sibiu.Avrig.SB_Avrig import get_atmospheric_data_SB_Avrig
        from .Romania.Sibiu.Cisnadie.SB_Cisnadie import get_atmospheric_data_SB_Cisnadie
        from .Romania.Sibiu.Copsa_Mica.SB_Copsa_Mica import get_atmospheric_data_SB_Copsa_Mica
        from .Romania.Sibiu.Dumbraveni.SB_Dumbraveni import get_atmospheric_data_SB_Dumbraveni
        from .Romania.Sibiu.Medias.SB_Medias import get_atmospheric_data_SB_Medias
        from .Romania.Sibiu.Miercurea_Sibiului.SB_Miercurea_Sibiului import get_atmospheric_data_SB_Miercurea_Sibiului
        from .Romania.Sibiu.Ocna_Sibiului.SB_Ocna_Sibiului import get_atmospheric_data_SB_Ocna_Sibiului
        from .Romania.Sibiu.Saliste.SB_Saliste import get_atmospheric_data_SB_Saliste
        from .Romania.Sibiu.Sibiu.SB_Sibiu import get_atmospheric_data_SB_Sibiu
        from .Romania.Sibiu.Talmaciu.SB_Talmaciu import get_atmospheric_data_SB_Talmaciu
        from .Romania.Suceava.Brosteni.SV_Brosteni import get_atmospheric_data_SV_Brosteni
        from .Romania.Suceava.Cajvana.SV_Cajvana import get_atmospheric_data_SV_Cajvana
        from .Romania.Suceava.Campulung_Moldovenesc.SV_Campulung_Moldovenesc import get_atmospheric_data_SV_Campulung_Moldovenesc
        from .Romania.Suceava.Dolhasca.SV_Dolhasca import get_atmospheric_data_SV_Dolhasca
        from .Romania.Suceava.Falticeni.SV_Falticeni import get_atmospheric_data_SV_Falticeni
        from .Romania.Suceava.Frasin.SV_Frasin import get_atmospheric_data_SV_Frasin
        from .Romania.Suceava.Gura_Humorului.SV_Gura_Humorului import get_atmospheric_data_SV_Gura_Humorului
        from .Romania.Suceava.Liteni.SV_Liteni import get_atmospheric_data_SV_Liteni
        from .Romania.Suceava.Milisauti.SV_Milisauti import get_atmospheric_data_SV_Milisauti
        from .Romania.Suceava.Radauti.SV_Radauti import get_atmospheric_data_SV_Radauti
        from .Romania.Suceava.Salcea.SV_Salcea import get_atmospheric_data_SV_Salcea
        from .Romania.Suceava.Siret.SV_Siret import get_atmospheric_data_SV_Siret
        from .Romania.Suceava.Solca.SV_Solca import get_atmospheric_data_SV_Solca
        from .Romania.Suceava.Suceava.SV_Suceava import get_atmospheric_data_SV_Suceava
        from .Romania.Suceava.Vatra_Dornei.SV_Vatra_Dornei import get_atmospheric_data_SV_Vatra_Dornei
        from .Romania.Suceava.Vicovu_de_Sus.SV_Vicovu_de_Sus import get_atmospheric_data_SV_Vicovu_de_Sus
        from .Romania.Teleorman.Alexandria.TR_Alexandria import get_atmospheric_data_TR_Alexandria
        from .Romania.Teleorman.Rosiorii_de_Vede.TR_Rosiorii_de_Vede import get_atmospheric_data_TR_Rosiorii_de_Vede
        from .Romania.Teleorman.Turnu_Magurele.TR_Turnu_Magurele import get_atmospheric_data_TR_Turnu_Magurele
        from .Romania.Teleorman.Videle.TR_Videle import get_atmospheric_data_TR_Videle
        from .Romania.Teleorman.Zimnicea.TR_Zimnicea import get_atmospheric_data_TR_Zimnicea
        from .Romania.Timis.Buzias.TM_Buzias import get_atmospheric_data_TM_Buzias
        from .Romania.Timis.Ciacova.TM_Ciacova import get_atmospheric_data_TM_Ciacova
        from .Romania.Timis.Deta.TM_Deta import get_atmospheric_data_TM_Deta
        from .Romania.Timis.Faget.TM_Faget import get_atmospheric_data_TM_Faget
        from .Romania.Timis.Gataia.TM_Gataia import get_atmospheric_data_TM_Gataia
        from .Romania.Timis.Jimbolia.TM_Jimbolia import get_atmospheric_data_TM_Jimbolia
        from .Romania.Timis.Lugoj.TM_Lugoj import get_atmospheric_data_TM_Lugoj
        from .Romania.Timis.Recas.TM_Recas import get_atmospheric_data_TM_Recas
        from .Romania.Timis.Sannicolau_Mare.TM_Sannicolau_Mare import get_atmospheric_data_TM_Sannicolau_Mare
        from .Romania.Timis.Timisoara.TM_Timisoara import get_atmospheric_data_TM_Timisoara
        from .Romania.Tulcea.Babadag.TL_Babadag import get_atmospheric_data_TL_Babadag
        from .Romania.Tulcea.Isaccea.TL_Isaccea import get_atmospheric_data_TL_Isaccea
        from .Romania.Tulcea.Macin.TL_Macin import get_atmospheric_data_TL_Macin
        from .Romania.Tulcea.Sulina.TL_Sulina import get_atmospheric_data_TL_Sulina
        from .Romania.Tulcea.Tulcea.TL_Tulcea import get_atmospheric_data_TL_Tulcea
        from .Romania.Valcea.Babeni.VL_Babeni import get_atmospheric_data_VL_Babeni
        from .Romania.Valcea.Baile_Govora.VL_Baile_Govora import get_atmospheric_data_VL_Baile_Govora
        from .Romania.Valcea.Baile_Olanesti.VL_Baile_Olanesti import get_atmospheric_data_VL_Baile_Olanesti
        from .Romania.Valcea.Balcesti.VL_Balcesti import get_atmospheric_data_VL_Balcesti
        from .Romania.Valcea.Berbesti.VL_Berbesti import get_atmospheric_data_VL_Berbesti
        from .Romania.Valcea.Brezoi.VL_Brezoi import get_atmospheric_data_VL_Brezoi
        from .Romania.Valcea.Calimanesti.VL_Calimanesti import get_atmospheric_data_VL_Calimanesti
        from .Romania.Valcea.Dragasani.VL_Dragasani import get_atmospheric_data_VL_Dragasani
        from .Romania.Valcea.Horezu.VL_Horezu import get_atmospheric_data_VL_Horezu
        from .Romania.Valcea.Ocnele_Mari.VL_Ocnele_Mari import get_atmospheric_data_VL_Ocnele_Mari
        from .Romania.Valcea.Ramnicu_Valcea.VL_Ramnicu_Valcea import get_atmospheric_data_VL_Ramnicu_Valcea
        from .Romania.Vaslui.Barlad.VS_Barlad import get_atmospheric_data_VS_Barlad
        from .Romania.Vaslui.Husi.VS_Husi import get_atmospheric_data_VS_Husi
        from .Romania.Vaslui.Murgeni.VS_Murgeni import get_atmospheric_data_VS_Murgeni
        from .Romania.Vaslui.Negresti.VS_Negresti import get_atmospheric_data_VS_Negresti
        from .Romania.Vaslui.Vaslui.VS_Vaslui import get_atmospheric_data_VS_Vaslui
        from .Romania.Vrancea.Adjud.VN_Adjud import get_atmospheric_data_VN_Adjud
        from .Romania.Vrancea.Focsani.VN_Focsani import get_atmospheric_data_VN_Focsani
        from .Romania.Vrancea.Marasesti.VN_Marasesti import get_atmospheric_data_VN_Marasesti
        from .Romania.Vrancea.Odobesti.VN_Odobesti import get_atmospheric_data_VN_Odobesti
        from .Romania.Vrancea.Panciu.VN_Panciu import get_atmospheric_data_VN_Panciu
