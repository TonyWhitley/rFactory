import urllib3
import json

# From https://simple.wikipedia.org/wiki/List_of_countries_by_continents
continent_countries = {
'Africa':
    {
    'Algeria': 'Algiers',
    'Angola': 'Luanda',

    'Benin': 'Porto Novo, Cotonou',

    'Botswana': 'Gaborone',

    'Burkina Faso': 'Ouagadougou',
    'Burundi': 'Gitega',
    'Cameroon': 'Yaoundé',
    'Cameroun': 'Yaoundé',
    'Cape Verde': 'Praia',
    'Central African Republic': 'Bangui',
    'Chad': 'N\'Djamena',
    'Tchad': 'N\'Djamena',

    'Comoros': 'Moroni',
    'Republic of the Congo': 'Brazzaville',
    'Democratic Republic of the Congo': 'Kinshasa',
    'Zaire': 'Kinshasa',

    'Côte d\'Ivoire': 'Yamoussoukro',
    'Ivory Coast': 'Yamoussoukro',

    'Djibouti': 'Djibouti',
    'Egypt': 'Cairo',
    'Misr': 'Cairo',

    'Equatorial Guinea': 'Malabo',
    'Eritrea': 'Asmara',
    'Ethiopia': 'Addis Ababa',
    'Abyssinia': 'Addis Ababa',

    'Gabon': 'Libreville',
    'The Gambia': 'Banjul',
    'Ghana': 'Accra',
    'Guinea': 'Conakry',
    'Guinea-Bissau': 'Bissau',
    'Kenya': 'Nairobi',
    'Lesotho': 'Maseru',
    'Liberia': 'Monrovia',
    'Libya': 'Tripoli',
    'Madagascar': 'Antananarivo',
    'Malawi': 'Lilongwe',
    'Mali': 'Bamako',
    'Mauritania': 'Nouakchott',
    'Mauritius': 'Port Louis',
    'Morocco': 'Rabat',
    'Al Maghrib': 'Rabat',

    'Mozambique': 'Maputo',
    'Namibia': 'Windhoek',
    'Niger': 'Niamey',
    'Nigeria': 'Abuja',
    'Rwanda': 'Kigali',
    'São Tomé and Príncipe': 'São Tomé',
    'Senegal': 'Dakar',
    'Seychelles': 'Victoria: Seychelles',
    'Sierra Leone': 'Freetown',
    'Somalia': 'Mogadishu',
    'South Africa': 'Pretoria',
    'South Sudan': 'Juba',
    'Sudan': 'Khartoum',
    'Swaziland': 'Mbabane',
    'Eswatini': 'Mbabane',

    'Tanzania': 'Dodoma',
    'Togo': 'Lome',
    'Tunisia': 'Tunis',
    'Uganda': 'Kampala',
    'Western Sahara': 'El Aaiún',
    'Zambia': 'Lusaka',
    'Zimbabwe': 'Harare',
    },

'Antarctica':
    {
    'Antarctica': 'South Pole!'
    },

'Asia':
    {
    'Afghanistan': 'Kabul',
    'Armenia': 'Yerevan',
    'Azerbaijan': 'Baku',
    'Bahrain': 'Manama',
    'Bangladesh': 'Dhaka',

    'Bhutan': 'Thimphu',
    'Brunei': 'Bandar Seri Begawan',
    'Cambodia': 'Phnom Penh',
    'Kampuchea': 'Phnom Penh',

    'China': 'Beijing',
    'Cyprus': 'Nicosia',
    'East Timor': 'Dili',
    'Timor Leste': 'Dili',

    'Georgia': 'Tbilisi',
    'Hong Kong': 'Hong Kong',
    'India': 'New Delhi',
    'Indonesia': 'Jakarta',
    'Iran': 'Tehran',
    'Iraq': 'Baghdad',
    'Israel': 'Jerusalem',
    'Japan': 'Tokyo',
    'Jordan': 'Amman',
    'Al Urdun': 'Amman',

    'Kazakhstan': 'nursultan',
    'Kuwait': 'Kuwait',
    'Kyrgyzstan': 'Bishkek',
    'Laos': 'Vientiane',
    'Lebanon': 'Beirut',
    'Lubnan': 'Beirut',

    'Malaysia': 'Kuala Lumpur',
    'Maldives': 'Malé',
    'Mongolia': 'Ulaanbaatar',
    'Myanmar': 'Naypyidaw',
    'Burma': 'Naypyidaw',

    'Nepal': 'Kathmandu',
    'North Korea': 'Pyongyang',
    'Oman': 'Muscat',
    'Pakistan': 'Islamabad',
    'Palestine': 'Jerusalem',
    'Philippines': 'Manila',
    'Qatar': 'Doha',
    'Russia': 'Moscow',
    'Saudi Arabia': 'Riyadh',
    'Singapore': 'Singapore',
    'South Korea': 'Seoul',
    'Sri Lanka': 'Sri Jayawardenapura Kotte',
    'Syria': 'Damascus',
    'Taiwan': 'Taipei',
    'Republic of China': 'Taipei',

    'Tajikistan': 'Dushanbe',
    'Thailand': 'Bangkok',
    'Muang Thai': 'Bangkok',

    'Turkey': 'Ankara',
    'Turkmenistan': 'Asgabat',
    'United Arab Emirates': 'Abu Dhabi',
    'Uzbekistan': 'Tashkent',
    'Vietnam': 'Hanoi',
    'Yemen': 'Sana\'a',
    },
'Europe':
    {


    'Albania': 'Tirana',
    'Shqipëria': 'Tirana',

    'Andorra': 'Andorra la Vella',
    'Austria': 'Vienna',
    'Österreich': 'Vienna',

    'Belarus': 'Minsk',

    'Belgium': 'Brussels',
    'België': 'Brussels',
    'Belgique': 'Brussels',
    'Belgien': 'Brussels',

    'Bosnia and Herzegovina': 'Sarajevo',
    'Bosna i Hercegovina': 'Sarajevo',

    'Bulgaria': 'Sofia',

    'Croatia': 'Zagreb',
    'Hrvatska': 'Zagreb',

    'Czech Republic': 'Prague',
    'Cesko': 'Prague',

    'Denmark': 'Copenhagen',
    'Danmark': 'Copenhagen',

    'Estonia': 'Tallinn',
    'Eesti': 'Tallinn',

    'Finland': 'Helsinki',
    'Suomi': 'Helsinki',

    'France': 'Paris',
    'Germany': 'Berlin',
    'Deutschland': 'Berlin',

    'Greece': 'Athens',

    'Hungary': 'Budapest',
    'Magyarország': 'Budapest',

    'Iceland': 'Reykjavik',
    'Island': 'Reykjavik',

    'Republic of Ireland': 'Dublin',
    'Ireland': 'Dublin',
    'Éire': 'Dublin',

    'Italy': 'Rome',
    'Italia': 'Rome',

    'Kosovo': 'Pristina',
    'Latvia': 'Riga',
    'Latvija': 'Riga',

    'Liechtenstein': 'Vaduz',
    'Lithuania': 'Vilnius',
    'Lietuva': 'Vilnius',

    'Luxembourg': 'Luxembourg City',
    'Macedonia': 'Skopje',

    'Malta': 'Valletta',
    'Moldova': 'Chisinau',
    'Monaco': 'Monte Carlo Quarter',
    'Montenegro': 'Podgorica',

    'Netherlands': 'Amsterdam',
    'Nederland': 'Amsterdam',

    'Norway': 'Oslo',
    'Norge': 'Oslo',

    'Poland': 'Warsaw',
    'Polska': 'Warsaw',

    'Portugal': 'Lisbon',
    'Romania': 'Bucharest',
    'Russia': 'Moscow',
    'San Marino': 'San Marino',
    'Serbia': 'Belgrade',

    'Slovakia': 'Bratislava',
    'Slovensko': 'Bratislava',

    'Slovenia': 'Ljubljana',
    'Slovenija': 'Ljubljana',

    'Spain': 'Madrid',
    'España': 'Madrid',

    'Sweden': 'Stockholm',
    'Sverige': 'Stockholm',

    'Switzerland': 'Bern',
    'Schweiz': 'Bern',
    'Suisse': 'Bern',
    'Svizzera': 'Bern',
    'Svizra': 'Bern',

    'Ukraine': 'Kiev',
    'Ukraine': 'Kyiv',

    'United Kingdom': 'London',
    'Great Britain': 'London',
    'England': 'London',
    'Scotland': 'Edinburgh',
    'Wales': 'Cardiff',
    'Northern Ireland': 'Belfast',
    'Vatican City': 'Vatican City',
    },

'North America':
    {

    'Antigua and Barbuda': 'St. John\'s',
    'Anguilla': 'The Valley',
    'Aruba': 'Oranjestad',
    'The Bahamas': 'Nassau',
    'Barbados': 'Bridgetown',
    'Belize': 'Belmopan',
    'Bermuda': 'Hamilton',
    'Bonaire': 'part of the Netherlands',
    'British Virgin Islands': 'Road Town',
    'Canada': 'Ottawa',
    'Cayman Islands': 'George Town',
    'Clipperton Island': 'n/a',
    'Costa Rica': 'San José',
    'Cuba': 'Havana',
    'Curaçao': 'Willemstad',
    'Dominica': 'Roseau',
    'Dominican Republic': 'Santo Domingo',
    'Republica Dominicana': 'Santo Domingo',

    'El Salvador': 'San Salvador',
    'Greenland': 'Nuuk',
    'Grenada': 'St George\'s',
    'Guadeloupe': 'n/a',
    'Guatemala': 'Guatemala',
    'Haiti': 'Port-au-Prince',
    'Honduras': 'Tegucigalpa',
    'Jamaica': 'Kingston',
    'Martinique': 'Fort-de-France Bay',
    'Mexico': 'Mexico City',
    'Montserrat': 'Plymouth: Brades: Little Bay',
    'Navassa Island': 'Washinton: D.C.',
    'Nicaragua': 'Managua',
    'Panama': 'Panama City',
    'Panamá': 'Panama City',

    'Puerto Rico': 'San Juan',
    'Saba': 'The Bottom',
    'Saint Barthelemy': 'Gustavia',
    'Saint Kitts and Nevis': 'Basseterre',
    'Saint Lucia': 'Castries',
    'Saint Martin': 'Marigot',
    'Saint Pierre and Miquelon': 'Saint-Pierre',
    'Saint Vincent and the Grenadines': 'Kingstown',
    'Sint Eustatius': 'Oranjestad',
    'Sint Maarten': 'Philipsburg',
    'Trinidad and Tobago': 'Port of Spain',
    'Turks and Caicos': 'Cockburn Town',
    'United States of America': 'Washington: District of Columbia',
    'United States': 'Washington: District of Columbia',
    'USA': 'Washington: District of Columbia',
    'US Virgin Islands': 'Charlotte Amalie',
    },
'South America':
    {
    'Argentina': 'Buenos Aires',
    'Bolivia': 'Sucré',
    'Brazil': 'Brasília',
    'Brasil': 'Brasília',

    'Chile': 'Santiago',
    'Colombia': 'Bogotá',
    'Ecuador': 'Quito',
    'Falkland Islands': 'Stanley',
    'French Guiana': 'Cayenne',
    'Guyana': 'Georgetown',
    'Paraguay': 'Asunción',
    'Peru': 'Lima',
    'South Georgia and the South Sandwich Islands': 'n/a',
    'Suriname': 'Paramaribo',
    'Uruguay': 'Montevideo',
    'Venezuela': 'Caracas',
    },
'Oceania':
    {
    'Australia': 'Canberra',
    'Federated States of Micronesia': 'Palikir',
    'Fiji': 'suva',
    'Kiribati': 'South Tarawa',
    'Marshall Islands': 'Majuro',
    'Nauru': 'no capital; biggest city is Yaren',
    'New Zealand': 'Wellington',
    'Palau': 'Melekeok',
    'Papua New Guinea': 'Port Moresby',
    'Samoa': 'Apia',
    'Solomon Islands': 'Honiara',
    'Tonga': 'Nuku\'alofa',
    'Tuvalu': 'Funafuti',
    'Vanuatu': 'Port Vila',

    'Flores': 'n/a',
    'Lombok': 'n/a',
    'Melanesia': 'n/a',
    'New Caledonia': 'n/a',
    'New Guinea': 'n/a',
    'Sulawesi': 'n/a',
    'Sumbawa': 'n/a',
    'Timor': 'n/a',
    }
}

def country_to_continent(country):
    for continent, countries in continent_countries.items():
        if country in countries:
            return continent

class google_address:
    country = None
    city = None
    def __init__(self, lat, long):
        try:
            import google_api
            API_key = google_api.key
        except:
            try:
                import data.google_api
                API_key = data.google_api.key
            except Exception as e:
                print(e)
                self.country = 'google API key'
                self.city = 'not present'
                return
        http = urllib3.PoolManager()
        url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{long}&key={API_key}'.format()
        self.response = http.request('GET', url)
        if self.response.status == 200:
            # that's OK
            json_dict = json.loads(self.response.data.decode('utf-8'))
            if json_dict['status'] == 'OK':
                for result in json_dict['results']:
                    for a_c in result['address_components']:
                        for t in a_c['types']:
                            if t == 'country':
                                self.country = a_c['long_name']
                            if t == 'postal_town':
                                self.city = a_c['long_name']
                            if self.country and self.city:
                                return
    def get_country(self):
        if not self.country:
            return ''
        return self.country
    def get_city(self):
        if not self.city:
            return ''
        return self.city

if __name__ == '__main__':
    lat = 46    # Bremgarten
    long = 7
    lat = 52    # Birmingham
    long = -1.898575
    lat = 51.489444
    long = -2.21222
    address_o = google_address(lat, long)

    print(f'City: {address_o.get_city()}')
    print(f'Country: {address_o.get_country()}')
    continent = country_to_continent(address_o.get_country())
    print(f'Continent: {continent}')

    # print(json.dumps(j, indent=4))
    pass