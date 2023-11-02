#!/usr/bin/env python3
from .database.atmospheric_domain.adlsa_RO import *
from .database.db_keys import appid

def get_cities():
    """
    Description:
    ==========
    Currently available countries: Romania
    Returns the user specified locations. 
       
    References:
    ==========
    """
    cities = [item for item in input('''Currently available countries: Romania.\n
Enter the cities, in travelling order, separated by a comma and a space. (Example: city1, city2) \n
Also, you can enter the country code followed by the regional abbreviation. (Example: RO-B) \n
Or the country code to update data for all the cities in that country. (Example: RO) \n
Your input: ''').split(', ')]
    print('~'*100)
    if 'RO-B' in cities:
        return ['Bucuresti']
    if 'RO-AB' in cities:
        return ['Abrud', 'Aiud',  'Alba Iulia',  'Baia de Aries',  'Blaj',  'Campeni',  'Cugir',  'Ocna Mures',  'Sebes',  'Teius', 'Zlatna']
    if 'RO-AR' in cities:
        return ['Arad', 'Chisineu Cris', 'Curtici', 'Ineu', 'Lipova', 'Nadlac', 'Pancota', 'Pecica', 'Santana']
    if 'RO-AG' in cities:
        return ['Campulung', 'Costesti', 'Curtea de Arges', 'Mioveni', 'Pitesti', 'Stefanesti(AG)', 'Topoloveni']
    if 'RO-BC' in cities:
        return ['Bacau', 'Buhusi', 'Comanesti', 'Darmanesti', 'Moinesti', 'Onesti', 'Slanic Moldova', 'Targu Ocna']
    if 'RO-BH' in cities:
        return ['Alesd', 'Beius', 'Marghita', 'Nucet', 'Oradea', 'Sacueni', 'Salonta', 'Stei', 'Valea lui Mihai', 'Vascau']
    if 'RO-BN' in cities:
        return ['Beclean', 'Bistrita', 'Nasaud', 'Sangeorz Bai']
    if 'RO-BT' in cities:
        return ['Botosani', 'Bucecea', 'Darabani', 'Dorohoi', 'Flamanzi', 'Saveni', 'Stefanesti(BT)']
    if 'RO-BR' in cities:
        return ['Braila', 'Faurei', 'Ianca', 'Insuratei']
    if 'RO-BV' in cities:
        return ['Brasov', 'Codlea', 'Fagaras', 'Ghimbav', 'Predeal', 'Rasnov', 'Rupea', 'Sacele', 'Victoria', 'Zarnesti']
    if 'RO-BZ' in cities:
        return ['Buzau', 'Nehoiu', 'Patarlagele', 'Pogoanele', 'Ramnicu Sarat']
    if 'RO-CL' in cities:
        return ['Budesti', 'Calarasi', 'Fundulea', 'Lehliu Gara', 'Oltenita']
    if 'RO-CS' in cities:
        return ['Anina', 'Baile Herculane', 'Bocsa', 'Caransebes', 'Moldova Noua', 'Oravita', 'Otelu Rosu', 'Resita']
    if 'RO-CJ' in cities:
        return ['Campia Turzii', 'Cluj Napoca', 'Dej', 'Gherla', 'Huedin', 'Turda']
    if 'RO-CT' in cities:
        return ['Cernavoda', 'Constanta', 'Eforie', 'Harsova', 'Mangalia', 'Medgidia', 'Murfatlar', 'Navodari', 'Negru Voda', 'Ovidiu', 'Techirghiol']
    if 'RO-CV' in cities:
        return ['Baraolt', 'Covasna', 'Intorsura Buzaului', 'Sfantu Gheorghe', 'Targu Secuiesc']
    if 'RO-DB' in cities:
        return ['Fieni', 'Gaesti', 'Moreni', 'Pucioasa', 'Racari', 'Targoviste', 'Titu']
    if 'RO-DJ' in cities:
        return ['Bailesti', 'Bechet', 'Calafat', 'Craiova', 'Dabuleni', 'Filiasi', 'Segarcea']
    if 'RO-GL' in cities:
        return ['Beresti', 'Galati', 'Targu Bujor', 'Tecuci']
    if 'RO-GR' in cities:
        return ['Bolintin Vale', 'Giurgiu', 'Mihailesti']
    if 'RO-GJ' in cities:
        return ['Bumbesti Jiu', 'Motru', 'Novaci', 'Rovinari', 'Targu Carbunesti', 'Targu Jiu', 'Ticleni', 'Tismana']
    if 'RO-HR' in cities:
        return ['Baile Tusnad', 'Balan', 'Borsec', 'Cristuru Secuiesc', 'Gheorgheni', 'Miercurea Ciuc', 'Odorheiu Secuiesc', 'Toplita', 'Vlahita']
    if 'RO-HD' in cities:
        return ['Deva', 'Aninoasa', 'Brad', 'Calan', 'Geoagiu', 'Hateg', 'Hunedoara', 'Lupeni', 'Orastie', 'Petrila', 'Petrosani', 'Simeria', 'Uricani', 'Vulcan']
    if 'RO-IL' in cities:
        return ['Amara', 'Cazanesti', 'Fetesti', 'Fierbinti Targ', 'Slobozia', 'Tandarei', 'Urziceni']
    if 'RO-IS' in cities:
        return ['Harlau', 'Iasi', 'Pascani', 'Podu Iloaiei', 'Targu Frumos']
    if 'RO-IF' in cities:
        return ['Bragadiru', 'Buftea', 'Chitila', 'Magurele', 'Otopeni', 'Pantelimon', 'Popesti Leordeni', 'Voluntari']
    if 'RO-MM' in cities:
        return ['Baia Mare', 'Baia Sprie', 'Borsa', 'Cavnic', 'Dragomiresti', 'Salistea de Sus', 'Seini', 'Sighetu Marmatiei', 'Somcuta Mare', 'Targu Lapus', 'Tautii Magheraus', 'Ulmeni', 'Viseu de Sus']
    if 'RO-MH' in cities:
        return ['Baia de Arama', 'Drobeta Turnu Severin', 'Orsova', 'Strehaia', 'Vanju Mare', 'Baia de Arama', 'Drobeta Turnu Severin', 'Orsova', 'Strehaia', 'Vanju Mare']
    if 'RO-MS' in cities:
        return ['Iernut', 'Ludus', 'Miercurea Nirajului', 'Reghin', 'Sangeorgiu de Padure', 'Sarmasu', 'Sighisoara', 'Sovata', 'Targu Mures', 'Tarnaveni', 'Ungheni']
    if 'RO-NT' in cities:
        return ['Bicaz', 'Piatra Neamt', 'Roman', 'Roznov', 'Targu Neamt']
    if 'RO-OT' in cities:
        return ['Bals', 'Caracal', 'Corabia', 'Draganesti Olt', 'Piatra Olt', 'Potcoava', 'Scornicesti', 'Slatina']
    if 'RO-PH' in cities:
        return ['Azuga', 'Baicoi', 'Boldesti Scaeni', 'Breaza', 'Busteni', 'Campina', 'Comarnic', 'Mizil', 'Ploiesti', 'Plopeni', 'Sinaia', 'Slanic', 'Urlati', 'Valenii de Munte']
    if 'RO-SJ' in cities:
        return ['Cehu Silvaniei', 'Jibou', 'Simleu Silvaniei', 'Zalau']
    if 'RO-SM' in cities:
        return ['Ardud', 'Carei', 'Livada', 'Negresti Oas', 'Satu Mare', 'Tasnad']
    if 'RO-SB' in cities:
        return ['Agnita', 'Avrig', 'Cisnadie', 'Copsa Mica', 'Dumbraveni', 'Medias', 'Miercurea Sibiului', 'Ocna Sibiului', 'Saliste', 'Sibiu', 'Talmaciu']
    if 'RO-SV' in cities:
        return ['Brosteni', 'Cajvana', 'Campulung Moldovenesc', 'Dolhasca', 'Falticeni', 'Frasin', 'Gura Humorului', 'Liteni', 'Milisauti', 'Radauti', 'Salcea', 'Siret', 'Solca', 'Suceava', 'Vatra Dornei', 'Vicovu de Sus']
    if 'RO-TR' in cities:
        return ['Alexandria', 'Rosiorii de Vede', 'Turnu Magurele', 'Videle', 'Zimnicea']
    if 'RO-TM' in cities:
        return ['Buzias', 'Ciacova', 'Deta', 'Faget', 'Gataia', 'Jimbolia', 'Lugoj', 'Recas', 'Sannicolau Mare', 'Timisoara']
    if 'RO-TL' in cities:
        return ['Babadag', 'Isaccea', 'Macin', 'Sulina', 'Tulcea']
    if 'RO-VL' in cities:
        return ['Babeni', 'Baile Govora', 'Baile Olanesti', 'Balcesti', 'Berbesti', 'Brezoi', 'Calimanesti', 'Dragasani', 'Horezu', 'Ocnele Mari', 'Ramnicu Valcea']
    if 'RO-VS' in cities:
        return ['Barlad', 'Husi', 'Murgeni', 'Negresti', 'Vaslui']
    if 'RO-VN' in cities:
        return ['Adjud', 'Focsani', 'Marasesti', 'Odobesti', 'Panciu']
    if 'RO' in cities:
        return ['Bucuresti', 'Abrud', 'Aiud',  'Alba Iulia',  'Baia de Aries',  'Blaj',  'Campeni',  'Cugir',  'Ocna Mures',  'Sebes',  'Teius', 'Zlatna',
                'Arad', 'Chisineu Cris', 'Curtici', 'Ineu', 'Lipova', 'Nadlac', 'Pancota', 'Pecica', 'Santana', 'Campulung', 'Costesti', 'Curtea de Arges', 'Mioveni', 'Pitesti', 'Stefanesti(AG)', 'Topoloveni',
                'Bacau', 'Buhusi', 'Comanesti', 'Darmanesti', 'Moinesti', 'Onesti', 'Slanic Moldova', 'Targu Ocna', 'Alesd', 'Beius', 'Marghita', 'Nucet', 'Oradea', 'Sacueni', 'Salonta', 'Stei', 'Valea lui Mihai', 'Vascau',
                'Beclean', 'Bistrita', 'Nasaud', 'Sangeorz Bai', 'Botosani', 'Bucecea', 'Darabani', 'Dorohoi', 'Flamanzi', 'Saveni', 'Stefanesti(BT)', 'Braila', 'Faurei', 'Ianca', 'Insuratei',
                'Brasov', 'Codlea', 'Fagaras', 'Ghimbav', 'Predeal', 'Rasnov', 'Rupea', 'Sacele', 'Victoria', 'Zarnesti', 'Buzau', 'Nehoiu', 'Patarlagele', 'Pogoanele', 'Ramnicu Sarat',
                'Budesti', 'Calarasi', 'Fundulea', 'Lehliu Gara', 'Oltenita', 'Anina', 'Baile Herculane', 'Bocsa', 'Caransebes', 'Moldova Noua', 'Oravita', 'Otelu Rosu', 'Resita',
                'Campia Turzii', 'Cluj Napoca', 'Dej', 'Gherla', 'Huedin', 'Turda', 'Cernavoda', 'Constanta', 'Eforie', 'Harsova', 'Mangalia', 'Medgidia', 'Murfatlar', 'Navodari', 'Negru Voda', 'Ovidiu', 'Techirghiol',
                'Baraolt', 'Covasna', 'Intorsura Buzaului', 'Sfantu Gheorghe', 'Targu Secuiesc', 'Fieni', 'Gaesti', 'Moreni', 'Pucioasa', 'Racari', 'Targoviste', 'Titu', 'Bailesti', 'Bechet', 'Calafat', 'Craiova', 'Dabuleni', 'Filiasi', 'Segarcea',
                'Beresti', 'Galati', 'Targu Bujor', 'Tecuci', 'Bolintin Vale', 'Giurgiu', 'Mihailesti', 'Bumbesti Jiu', 'Motru', 'Novaci', 'Rovinari', 'Targu Carbunesti', 'Targu Jiu', 'Ticleni', 'Tismana',
                'Baile Tusnad', 'Balan', 'Borsec', 'Cristuru Secuiesc', 'Gheorgheni', 'Miercurea Ciuc', 'Odorheiu Secuiesc', 'Toplita', 'Vlahita', 'Deva', 'Aninoasa', 'Brad', 'Calan', 'Geoagiu', 'Hateg', 'Hunedoara', 'Lupeni', 'Orastie', 'Petrila', 'Petrosani', 'Simeria', 'Uricani', 'Vulcan',
                'Amara', 'Cazanesti', 'Fetesti', 'Fierbinti Targ', 'Slobozia', 'Tandarei', 'Urziceni', 'Harlau', 'Iasi', 'Pascani', 'Podu Iloaiei', 'Targu Frumos', 'Bragadiru', 'Buftea', 'Chitila', 'Magurele', 'Otopeni', 'Pantelimon', 'Popesti Leordeni', 'Voluntari',
                'Baia Mare', 'Baia Sprie', 'Borsa', 'Cavnic', 'Dragomiresti', 'Salistea de Sus', 'Seini', 'Sighetu Marmatiei', 'Somcuta Mare', 'Targu Lapus', 'Tautii Magheraus', 'Ulmeni', 'Viseu de Sus',
                'Baia de Arama', 'Drobeta Turnu Severin', 'Orsova', 'Strehaia', 'Vanju Mare', 'Baia de Arama', 'Drobeta Turnu Severin', 'Orsova', 'Strehaia', 'Vanju Mare',
                'Iernut', 'Ludus', 'Miercurea Nirajului', 'Reghin', 'Sangeorgiu de Padure', 'Sarmasu', 'Sighisoara', 'Sovata', 'Targu Mures', 'Tarnaveni', 'Ungheni',
                'Bicaz', 'Piatra Neamt', 'Roman', 'Roznov', 'Targu Neamt', 'Bals', 'Caracal', 'Corabia', 'Draganesti Olt', 'Piatra Olt', 'Potcoava', 'Scornicesti', 'Slatina', 'Azuga', 'Baicoi', 'Boldesti Scaeni', 'Breaza', 'Busteni', 'Campina', 'Comarnic', 'Mizil', 'Ploiesti', 'Plopeni', 'Sinaia', 'Slanic', 'Urlati', 'Valenii de Munte',
                'Cehu Silvaniei', 'Jibou', 'Simleu Silvaniei', 'Zalau', 'Ardud', 'Carei', 'Livada', 'Negresti Oas', 'Satu Mare', 'Tasnad', 'Agnita', 'Avrig', 'Cisnadie', 'Copsa Mica', 'Dumbraveni', 'Medias', 'Miercurea Sibiului', 'Ocna Sibiului', 'Saliste', 'Sibiu', 'Talmaciu', 'Brosteni', 'Cajvana', 'Campulung Moldovenesc', 'Dolhasca', 'Falticeni', 'Frasin', 'Gura Humorului', 'Liteni', 'Milisauti', 'Radauti', 'Salcea', 'Siret', 'Solca', 'Suceava', 'Vatra Dornei', 'Vicovu de Sus',
                'Alexandria', 'Rosiorii de Vede', 'Turnu Magurele', 'Videle', 'Zimnicea', 'Buzias', 'Ciacova', 'Deta', 'Faget', 'Gataia', 'Jimbolia', 'Lugoj', 'Recas', 'Sannicolau Mare', 'Timisoara',
                'Babadag', 'Isaccea', 'Macin', 'Sulina', 'Tulcea', 'Babeni', 'Baile Govora', 'Baile Olanesti', 'Balcesti', 'Berbesti', 'Brezoi', 'Calimanesti', 'Dragasani', 'Horezu', 'Ocnele Mari', 'Ramnicu Valcea',
                'Barlad', 'Husi', 'Murgeni', 'Negresti', 'Vaslui', 'Adjud', 'Focsani', 'Marasesti', 'Odobesti', 'Panciu']
    else:
        return cities

   
if (m:=input('Do you wish to add data for the atmospheric domain (y/n): '))=='y' or m=='Y':
    print('~'*100)
    appid = appid()
    print('~'*100)
    candidates = get_cities()
    for city in candidates:
        atmospheric_data(city, appid)
    print('~'*100)
else:
    print('~'*100, '\n Using the already archived data.')
    print('~'*100)
    pass

if (q:=input('Do you wish to add data from the ARXDE\u2122 (y/n): '))=='y' or q=='Y':
    print('~'*100, '\nData from ARXDE\u2122 not available. Using the already archived data instead.')
    print('~'*100)
else:
    print('~'*100, '\n Using the already archived data from ARXDE\u2122.')    
    print('~'*100)
    pass
        
if __name__ == '__main__':
    print("The lightmorphic's main module is running")
else:
    pass
