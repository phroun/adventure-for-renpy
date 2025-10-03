#!/usr/bin/env python3
"""
**************************************************************************
**
**   locales.py - Locales for Adventure
**
**   Version 1 revision 0
**
**************************************************************************
This module is released under the MIT License:
==========================================================================

Copyright 2025 Jeffrey R. Day

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the “Software”),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

#*************************************************************************
"""

locales = {

    # UNITED STATES - Major Cities
    "Seattle": ("Seattle, Washington", 47.6061, -122.3328, "America/Los_Angeles"),
    "Portland": ("Portland, Oregon", 45.5152, -122.6784, "America/Los_Angeles"),
    "San Francisco": ("San Francisco, California", 37.7749, -122.4194, "America/Los_Angeles"),
    "Los Angeles": ("Los Angeles, California", 34.0522, -118.2437, "America/Los_Angeles"),
    "San Diego": ("San Diego, California", 32.7157, -117.1611, "America/Los_Angeles"),
    "Las Vegas": ("Las Vegas, Nevada", 36.1699, -115.1398, "America/Los_Angeles"),
    "Phoenix": ("Phoenix, Arizona", 33.4484, -112.0740, "America/Phoenix"),
    "Denver": ("Denver, Colorado", 39.7392, -104.9903, "America/Denver"),
    "Salt Lake City": ("Salt Lake City, Utah", 40.7608, -111.8910, "America/Denver"),
    "Albuquerque": ("Albuquerque, New Mexico", 35.0844, -106.6504, "America/Denver"),
    "Chicago": ("Chicago, Illinois", 41.8781, -87.6298, "America/Chicago"),
    "Dallas": ("Dallas, Texas", 32.7767, -96.7970, "America/Chicago"),
    "Houston": ("Houston, Texas", 29.7604, -95.3698, "America/Chicago"),
    "Austin": ("Austin, Texas", 30.2672, -97.7431, "America/Chicago"),
    "New Orleans": ("New Orleans, Louisiana", 29.9511, -90.0715, "America/Chicago"),
    "Nashville": ("Nashville, Tennessee", 36.1627, -86.7816, "America/Chicago"),
    "Minneapolis": ("Minneapolis, Minnesota", 44.9778, -93.2650, "America/Chicago"),
    "Kansas City": ("Kansas City, Missouri", 39.0997, -94.5786, "America/Chicago"),
    "Oklahoma City": ("Oklahoma City, Oklahoma", 35.4676, -97.5164, "America/Chicago"),
    "New York": ("New York City, New York", 40.7128, -74.0060, "America/New_York"),
    "Boston": ("Boston, Massachusetts", 42.3601, -71.0589, "America/New_York"),
    "Washington": ("Washington, D.C.", 38.9072, -77.0369, "America/New_York"),
    "Philadelphia": ("Philadelphia, Pennsylvania", 39.9526, -75.1652, "America/New_York"),
    "Atlanta": ("Atlanta, Georgia", 33.7490, -84.3880, "America/New_York"),
    "Miami": ("Miami, Florida", 25.7617, -80.1918, "America/New_York"),
    "Orlando": ("Orlando, Florida", 28.5383, -81.3792, "America/New_York"),
    "Tampa": ("Tampa, Florida", 27.9506, -82.4572, "America/New_York"),
    "Charlotte": ("Charlotte, North Carolina", 35.2271, -80.8431, "America/New_York"),
    "Detroit": ("Detroit, Michigan", 42.3314, -83.0458, "America/New_York"),
    "Cleveland": ("Cleveland, Ohio", 41.4993, -81.6944, "America/New_York"),
    "Pittsburgh": ("Pittsburgh, Pennsylvania", 40.4406, -79.9959, "America/New_York"),
    "Baltimore": ("Baltimore, Maryland", 39.2904, -76.6122, "America/New_York"),
    "Richmond": ("Richmond, Virginia", 37.5407, -77.4360, "America/New_York"),
    
    # UNITED STATES - States (using capital cities for coordinates)
    "Alaska": ("Alaska, USA", 61.2181, -149.9003, "America/Anchorage"),  # Anchorage
    "Hawaii": ("Hawaii, USA", 21.3099, -157.8581, "Pacific/Honolulu"),  # Honolulu
    "California": ("California, USA", 38.5816, -121.4944, "America/Los_Angeles"),  # Sacramento
    "Texas": ("Texas, USA", 30.2672, -97.7431, "America/Chicago"),  # Austin
    "Florida": ("Florida, USA", 30.4518, -84.2807, "America/New_York"),  # Tallahassee
    "New York State": ("New York State, USA", 42.6526, -73.7562, "America/New_York"),  # Albany

    # CANADA
    "Vancouver": ("Vancouver, British Columbia", 49.2827, -123.1207, "America/Vancouver"),
    "Calgary": ("Calgary, Alberta", 51.0447, -114.0719, "America/Edmonton"),
    "Edmonton": ("Edmonton, Alberta", 53.5461, -113.4938, "America/Edmonton"),
    "Winnipeg": ("Winnipeg, Manitoba", 49.8951, -97.1384, "America/Winnipeg"),
    "Toronto": ("Toronto, Ontario", 43.6532, -79.3832, "America/Toronto"),
    "Ottawa": ("Ottawa, Ontario", 45.4215, -75.6972, "America/Toronto"),
    "Montreal": ("Montreal, Quebec", 45.5017, -73.5673, "America/Toronto"),
    "Quebec City": ("Quebec City, Quebec", 46.8139, -71.2080, "America/Toronto"),
    "Halifax": ("Halifax, Nova Scotia", 44.6488, -63.5752, "America/Halifax"),
    "St. John's": ("St. John's, Newfoundland", 47.5615, -52.7126, "America/St_Johns"),
    
    # MEXICO
    "Mexico City": ("Mexico City, Mexico", 19.4326, -99.1332, "America/Mexico_City"),
    "Guadalajara": ("Guadalajara, Mexico", 20.6597, -103.3496, "America/Mexico_City"),
    "Cancun": ("Cancun, Mexico", 21.1619, -86.8515, "America/Cancun"),
    "Tijuana": ("Tijuana, Mexico", 32.5149, -117.0382, "America/Tijuana"),
    "Puerto Vallarta": ("Puerto Vallarta, Mexico", 20.6534, -105.2253, "America/Mexico_City"),
    
    # CENTRAL AMERICA & CARIBBEAN
    "Guatemala City": ("Guatemala City, Guatemala", 14.6349, -90.5069, "America/Guatemala"),
    "San Jose": ("San José, Costa Rica", 9.9281, -84.0907, "America/Costa_Rica"),
    "Panama City": ("Panama City, Panama", 8.9824, -79.5199, "America/Panama"),
    "Havana": ("Havana, Cuba", 23.1136, -82.3666, "America/Havana"),
    "Kingston": ("Kingston, Jamaica", 17.9712, -76.7936, "America/Jamaica"),
    "San Juan": ("San Juan, Puerto Rico", 18.4655, -66.1057, "America/Puerto_Rico"),
    "Nassau": ("Nassau, Bahamas", 25.0443, -77.3504, "America/Nassau"),
    "Barbados": ("Bridgetown, Barbados", 13.1939, -59.5432, "America/Barbados"),
    
    # SOUTH AMERICA
    "Bogota": ("Bogotá, Colombia", 4.7110, -74.0721, "America/Bogota"),
    "Caracas": ("Caracas, Venezuela", 10.4806, -66.9036, "America/Caracas"),
    "Georgetown": ("Georgetown, Guyana", 6.8013, -58.1551, "America/Guyana"),
    "Paramaribo": ("Paramaribo, Suriname", 5.8520, -55.2038, "America/Paramaribo"),
    "Quito": ("Quito, Ecuador", -0.1807, -78.4678, "America/Guayaquil"),
    "Lima": ("Lima, Peru", -12.0464, -77.0428, "America/Lima"),
    "La Paz": ("La Paz, Bolivia", -16.5000, -68.1500, "America/La_Paz"),
    "Santiago": ("Santiago, Chile", -33.4489, -70.6693, "America/Santiago"),
    "Buenos Aires": ("Buenos Aires, Argentina", -34.6118, -58.3960, "America/Argentina/Buenos_Aires"),
    "Montevideo": ("Montevideo, Uruguay", -34.9011, -56.1645, "America/Montevideo"),
    "Asuncion": ("Asunción, Paraguay", -25.2637, -57.5759, "America/Asuncion"),
    "Brasilia": ("Brasília, Brazil", -15.8267, -47.9218, "America/Sao_Paulo"),
    "Rio de Janeiro": ("Rio de Janeiro, Brazil", -22.9068, -43.1729, "America/Sao_Paulo"),
    "Sao Paulo": ("São Paulo, Brazil", -23.5505, -46.6333, "America/Sao_Paulo"),
    "Manaus": ("Manaus, Brazil", -3.1190, -60.0217, "America/Manaus"),
    
    # EUROPE - Western
    "London": ("London, United Kingdom", 51.5074, -0.1278, "Europe/London"),
    "Edinburgh": ("Edinburgh, Scotland", 55.9533, -3.1883, "Europe/London"),
    "Dublin": ("Dublin, Ireland", 53.3498, -6.2603, "Europe/Dublin"),
    "Paris": ("Paris, France", 48.8566, 2.3522, "Europe/Paris"),
    "Lyon": ("Lyon, France", 45.7640, 4.8357, "Europe/Paris"),
    "Nice": ("Nice, France", 43.7102, 7.2620, "Europe/Paris"),
    "Madrid": ("Madrid, Spain", 40.4168, -3.7038, "Europe/Madrid"),
    "Barcelona": ("Barcelona, Spain", 41.3851, 2.1734, "Europe/Madrid"),
    "Seville": ("Seville, Spain", 37.3891, -5.9845, "Europe/Madrid"),
    "Lisbon": ("Lisbon, Portugal", 38.7223, -9.1393, "Europe/Lisbon"),
    "Porto": ("Porto, Portugal", 41.1579, -8.6291, "Europe/Lisbon"),
    "Rome": ("Rome, Italy", 41.9028, 12.4964, "Europe/Rome"),
    "Milan": ("Milan, Italy", 45.4642, 9.1900, "Europe/Rome"),
    "Venice": ("Venice, Italy", 45.4408, 12.3155, "Europe/Rome"),
    "Florence": ("Florence, Italy", 43.7696, 11.2558, "Europe/Rome"),
    "Naples": ("Naples, Italy", 40.8518, 14.2681, "Europe/Rome"),
    "Amsterdam": ("Amsterdam, Netherlands", 52.3676, 4.9041, "Europe/Amsterdam"),
    "Brussels": ("Brussels, Belgium", 50.8503, 4.3517, "Europe/Brussels"),
    "Luxembourg": ("Luxembourg City, Luxembourg", 49.6116, 6.1319, "Europe/Luxembourg"),
    "Bern": ("Bern, Switzerland", 46.9481, 7.4474, "Europe/Zurich"),
    "Zurich": ("Zurich, Switzerland", 47.3769, 8.5417, "Europe/Zurich"),
    "Geneva": ("Geneva, Switzerland", 46.2044, 6.1432, "Europe/Zurich"),
    "Vienna": ("Vienna, Austria", 48.2082, 16.3738, "Europe/Vienna"),
    "Salzburg": ("Salzburg, Austria", 47.8095, 13.0550, "Europe/Vienna"),
    
    # EUROPE - Northern
    "Copenhagen": ("Copenhagen, Denmark", 55.6761, 12.5683, "Europe/Copenhagen"),
    "Stockholm": ("Stockholm, Sweden", 59.3293, 18.0686, "Europe/Stockholm"),
    "Oslo": ("Oslo, Norway", 59.9139, 10.7522, "Europe/Oslo"),
    "Bergen": ("Bergen, Norway", 60.3913, 5.3221, "Europe/Oslo"),
    "Helsinki": ("Helsinki, Finland", 60.1699, 24.9384, "Europe/Helsinki"),
    "Reykjavik": ("Reykjavík, Iceland", 64.1466, -21.9426, "Atlantic/Reykjavik"),
    
    # EUROPE - Central & Eastern
    "Berlin": ("Berlin, Germany", 52.5200, 13.4050, "Europe/Berlin"),
    "Munich": ("Munich, Germany", 48.1351, 11.5820, "Europe/Berlin"),
    "Hamburg": ("Hamburg, Germany", 53.5511, 9.9937, "Europe/Berlin"),
    "Frankfurt": ("Frankfurt, Germany", 50.1109, 8.6821, "Europe/Berlin"),
    "Prague": ("Prague, Czech Republic", 50.0755, 14.4378, "Europe/Prague"),
    "Budapest": ("Budapest, Hungary", 47.4979, 19.0402, "Europe/Budapest"),
    "Warsaw": ("Warsaw, Poland", 52.2297, 21.0122, "Europe/Warsaw"),
    "Krakow": ("Kraków, Poland", 50.0647, 19.9450, "Europe/Warsaw"),
    "Bratislava": ("Bratislava, Slovakia", 48.1486, 17.1077, "Europe/Bratislava"),
    "Ljubljana": ("Ljubljana, Slovenia", 46.0569, 14.5058, "Europe/Ljubljana"),
    "Zagreb": ("Zagreb, Croatia", 45.8150, 15.9819, "Europe/Zagreb"),
    "Belgrade": ("Belgrade, Serbia", 44.7866, 20.4489, "Europe/Belgrade"),
    "Sarajevo": ("Sarajevo, Bosnia and Herzegovina", 43.8486, 18.3564, "Europe/Sarajevo"),
    "Sofia": ("Sofia, Bulgaria", 42.6977, 23.3219, "Europe/Sofia"),
    "Bucharest": ("Bucharest, Romania", 44.4268, 26.1025, "Europe/Bucharest"),
    "Kiev": ("Kyiv, Ukraine", 50.4501, 30.5234, "Europe/Kiev"),
    "Moscow": ("Moscow, Russia", 55.7558, 37.6176, "Europe/Moscow"),
    "St. Petersburg": ("St. Petersburg, Russia", 59.9311, 30.3609, "Europe/Moscow"),
    
    # EUROPE - Mediterranean
    "Athens": ("Athens, Greece", 37.9838, 23.7275, "Europe/Athens"),
    "Thessaloniki": ("Thessaloniki, Greece", 40.6401, 22.9444, "Europe/Athens"),
    "Istanbul": ("Istanbul, Turkey", 41.0082, 28.9784, "Europe/Istanbul"),
    "Ankara": ("Ankara, Turkey", 39.9334, 32.8597, "Europe/Istanbul"),
    "Valletta": ("Valletta, Malta", 35.8989, 14.5146, "Europe/Malta"),
    "Nicosia": ("Nicosia, Cyprus", 35.1856, 33.3823, "Asia/Nicosia"),
    
    # AFRICA - North
    "Cairo": ("Cairo, Egypt", 30.0444, 31.2357, "Africa/Cairo"),
    "Alexandria": ("Alexandria, Egypt", 31.2001, 29.9187, "Africa/Cairo"),
    "Tunis": ("Tunis, Tunisia", 36.8065, 10.1815, "Africa/Tunis"),
    "Algiers": ("Algiers, Algeria", 36.7538, 3.0588, "Africa/Algiers"),
    "Rabat": ("Rabat, Morocco", 34.0209, -6.8416, "Africa/Casablanca"),
    "Casablanca": ("Casablanca, Morocco", 33.5731, -7.5898, "Africa/Casablanca"),
    "Marrakech": ("Marrakech, Morocco", 31.6295, -7.9811, "Africa/Casablanca"),
    
    # AFRICA - Sub-Saharan
    "Lagos": ("Lagos, Nigeria", 6.5244, 3.3792, "Africa/Lagos"),
    "Abuja": ("Abuja, Nigeria", 9.0579, 7.4951, "Africa/Lagos"),
    "Accra": ("Accra, Ghana", 5.6037, -0.1870, "Africa/Accra"),
    "Dakar": ("Dakar, Senegal", 14.7167, -17.4677, "Africa/Dakar"),
    "Bamako": ("Bamako, Mali", 12.6392, -8.0029, "Africa/Bamako"),
    "Addis Ababa": ("Addis Ababa, Ethiopia", 9.1450, 38.7451, "Africa/Addis_Ababa"),
    "Nairobi": ("Nairobi, Kenya", -1.2921, 36.8219, "Africa/Nairobi"),
    "Kampala": ("Kampala, Uganda", 0.3476, 32.5825, "Africa/Kampala"),
    "Dar es Salaam": ("Dar es Salaam, Tanzania", -6.7924, 39.2083, "Africa/Dar_es_Salaam"),
    "Kigali": ("Kigali, Rwanda", -1.9441, 30.0619, "Africa/Kigali"),
    "Kinshasa": ("Kinshasa, Democratic Republic of Congo", -4.4419, 15.2663, "Africa/Kinshasa"),
    "Luanda": ("Luanda, Angola", -8.8390, 13.2894, "Africa/Luanda"),
    "Johannesburg": ("Johannesburg, South Africa", -26.2041, 28.0473, "Africa/Johannesburg"),
    "Cape Town": ("Cape Town, South Africa", -33.9249, 18.4241, "Africa/Johannesburg"),
    "Durban": ("Durban, South Africa", -29.8587, 31.0218, "Africa/Johannesburg"),
    "Harare": ("Harare, Zimbabwe", -17.8252, 31.0335, "Africa/Harare"),
    "Lusaka": ("Lusaka, Zambia", -15.3875, 28.3228, "Africa/Lusaka"),
    "Gaborone": ("Gaborone, Botswana", -24.6282, 25.9231, "Africa/Gaborone"),
    "Windhoek": ("Windhoek, Namibia", -22.5597, 17.0832, "Africa/Windhoek"),
    "Antananarivo": ("Antananarivo, Madagascar", -18.8792, 47.5079, "Indian/Antananarivo"),
    
    # MIDDLE EAST
    "Riyadh": ("Riyadh, Saudi Arabia", 24.7136, 46.6753, "Asia/Riyadh"),
    "Jeddah": ("Jeddah, Saudi Arabia", 21.4858, 39.1925, "Asia/Riyadh"),
    "Mecca": ("Mecca, Saudi Arabia", 21.3891, 39.8579, "Asia/Riyadh"),
    "Dubai": ("Dubai, United Arab Emirates", 25.2769, 55.2962, "Asia/Dubai"),
    "Abu Dhabi": ("Abu Dhabi, United Arab Emirates", 24.4539, 54.3773, "Asia/Dubai"),
    "Doha": ("Doha, Qatar", 25.2854, 51.5310, "Asia/Qatar"),
    "Kuwait City": ("Kuwait City, Kuwait", 29.3117, 47.4818, "Asia/Kuwait"),
    "Manama": ("Manama, Bahrain", 26.0667, 50.5577, "Asia/Bahrain"),
    "Muscat": ("Muscat, Oman", 23.5880, 58.3829, "Asia/Muscat"),
    "Baghdad": ("Baghdad, Iraq", 33.3152, 44.3661, "Asia/Baghdad"),
    "Tehran": ("Tehran, Iran", 35.6892, 51.3890, "Asia/Tehran"),
    "Isfahan": ("Isfahan, Iran", 32.6546, 51.6680, "Asia/Tehran"),
    "Tel Aviv": ("Tel Aviv, Israel", 32.0853, 34.7818, "Asia/Jerusalem"),
    "Jerusalem": ("Jerusalem, Israel", 31.7683, 35.2137, "Asia/Jerusalem"),
    "Amman": ("Amman, Jordan", 31.9454, 35.9284, "Asia/Amman"),
    "Damascus": ("Damascus, Syria", 33.5138, 36.2765, "Asia/Damascus"),
    "Beirut": ("Beirut, Lebanon", 33.8938, 35.5018, "Asia/Beirut"),
    
    # SOUTH ASIA
    "Mumbai": ("Mumbai, India", 19.0760, 72.8777, "Asia/Kolkata"),
    "Delhi": ("Delhi, India", 28.7041, 77.1025, "Asia/Kolkata"),
    "Bangalore": ("Bangalore, India", 12.9716, 77.5946, "Asia/Kolkata"),
    "Chennai": ("Chennai, India", 13.0827, 80.2707, "Asia/Kolkata"),
    "Kolkata": ("Kolkata, India", 22.5726, 88.3639, "Asia/Kolkata"),
    "Hyderabad": ("Hyderabad, India", 17.3850, 78.4867, "Asia/Kolkata"),
    "Pune": ("Pune, India", 18.5204, 73.8567, "Asia/Kolkata"),
    "Jaipur": ("Jaipur, India", 26.9124, 75.7873, "Asia/Kolkata"),
    "Goa": ("Goa, India", 15.2993, 74.1240, "Asia/Kolkata"),
    "Karachi": ("Karachi, Pakistan", 24.8607, 67.0011, "Asia/Karachi"),
    "Lahore": ("Lahore, Pakistan", 31.5204, 74.3587, "Asia/Karachi"),
    "Islamabad": ("Islamabad, Pakistan", 33.6844, 73.0479, "Asia/Karachi"),
    "Dhaka": ("Dhaka, Bangladesh", 23.8103, 90.4125, "Asia/Dhaka"),
    "Chittagong": ("Chittagong, Bangladesh", 22.3569, 91.7832, "Asia/Dhaka"),
    "Colombo": ("Colombo, Sri Lanka", 6.9271, 79.8612, "Asia/Colombo"),
    "Kandy": ("Kandy, Sri Lanka", 7.2906, 80.6337, "Asia/Colombo"),
    "Kathmandu": ("Kathmandu, Nepal", 27.7172, 85.3240, "Asia/Kathmandu"),
    "Thimphu": ("Thimphu, Bhutan", 27.4728, 89.6390, "Asia/Thimphu"),
    
    # SOUTHEAST ASIA
    "Bangkok": ("Bangkok, Thailand", 13.7563, 100.5018, "Asia/Bangkok"),
    "Phuket": ("Phuket, Thailand", 7.8804, 98.3923, "Asia/Bangkok"),
    "Chiang Mai": ("Chiang Mai, Thailand", 18.7883, 98.9853, "Asia/Bangkok"),
    "Ho Chi Minh City": ("Ho Chi Minh City, Vietnam", 10.8231, 106.6297, "Asia/Ho_Chi_Minh"),
    "Hanoi": ("Hanoi, Vietnam", 21.0285, 105.8542, "Asia/Ho_Chi_Minh"),
    "Singapore": ("Singapore", 1.3521, 103.8198, "Asia/Singapore"),
    "Kuala Lumpur": ("Kuala Lumpur, Malaysia", 3.1390, 101.6869, "Asia/Kuala_Lumpur"),
    "Penang": ("Penang, Malaysia", 5.4164, 100.3327, "Asia/Kuala_Lumpur"),
    "Jakarta": ("Jakarta, Indonesia", -6.2088, 106.8456, "Asia/Jakarta"),
    "Bali": ("Bali, Indonesia", -8.4095, 115.1889, "Asia/Makassar"),
    "Yogyakarta": ("Yogyakarta, Indonesia", -7.7956, 110.3695, "Asia/Jakarta"),
    "Manila": ("Manila, Philippines", 14.5995, 120.9842, "Asia/Manila"),
    "Cebu": ("Cebu, Philippines", 10.3157, 123.8854, "Asia/Manila"),
    "Vientiane": ("Vientiane, Laos", 17.9757, 102.6331, "Asia/Vientiane"),
    "Phnom Penh": ("Phnom Penh, Cambodia", 11.5449, 104.8922, "Asia/Phnom_Penh"),
    "Yangon": ("Yangon, Myanmar", 16.8661, 96.1951, "Asia/Yangon"),
    "Naypyidaw": ("Naypyidaw, Myanmar", 19.7633, 96.0785, "Asia/Yangon"),
    "Bandar Seri Begawan": ("Bandar Seri Begawan, Brunei", 4.9031, 114.9398, "Asia/Brunei"),
    "Dili": ("Dili, East Timor", -8.5569, 125.5603, "Asia/Dili"),
    
    # EAST ASIA
    "Beijing": ("Beijing, China", 39.9042, 116.4074, "Asia/Shanghai"),
    "Shanghai": ("Shanghai, China", 31.2304, 121.4737, "Asia/Shanghai"),
    "Guangzhou": ("Guangzhou, China", 23.1291, 113.2644, "Asia/Shanghai"),
    "Shenzhen": ("Shenzhen, China", 22.5431, 114.0579, "Asia/Shanghai"),
    "Hong Kong": ("Hong Kong", 22.3193, 114.1694, "Asia/Hong_Kong"),
    "Macau": ("Macau", 22.1987, 113.5439, "Asia/Macau"),
    "Chengdu": ("Chengdu, China", 30.5728, 104.0668, "Asia/Shanghai"),
    "Xi'an": ("Xi'an, China", 34.3416, 108.9398, "Asia/Shanghai"),
    "Hangzhou": ("Hangzhou, China", 30.2741, 120.1551, "Asia/Shanghai"),
    "Tokyo": ("Tokyo, Japan", 35.6762, 139.6503, "Asia/Tokyo"),
    "Osaka": ("Osaka, Japan", 34.6937, 135.5023, "Asia/Tokyo"),
    "Kyoto": ("Kyoto, Japan", 35.0116, 135.7681, "Asia/Tokyo"),
    "Hiroshima": ("Hiroshima, Japan", 34.3853, 132.4553, "Asia/Tokyo"),
    "Nagoya": ("Nagoya, Japan", 35.1815, 136.9066, "Asia/Tokyo"),
    "Sapporo": ("Sapporo, Japan", 43.0642, 141.3469, "Asia/Tokyo"),
    "Seoul": ("Seoul, South Korea", 37.5665, 126.9780, "Asia/Seoul"),
    "Busan": ("Busan, South Korea", 35.1796, 129.0756, "Asia/Seoul"),
    "Incheon": ("Incheon, South Korea", 37.4563, 126.7052, "Asia/Seoul"),
    "Pyongyang": ("Pyongyang, North Korea", 39.0392, 125.7625, "Asia/Pyongyang"),
    "Taipei": ("Taipei, Taiwan", 25.0330, 121.5654, "Asia/Taipei"),
    "Kaohsiung": ("Kaohsiung, Taiwan", 22.6273, 120.3014, "Asia/Taipei"),
    "Ulaanbaatar": ("Ulaanbaatar, Mongolia", 47.8864, 106.9057, "Asia/Ulaanbaatar"),
    
    # OCEANIA
    "Sydney": ("Sydney, Australia", -33.8688, 151.2093, "Australia/Sydney"),
    "Melbourne": ("Melbourne, Australia", -37.8136, 144.9631, "Australia/Melbourne"),
    "Brisbane": ("Brisbane, Australia", -27.4698, 153.0251, "Australia/Brisbane"),
    "Perth": ("Perth, Australia", -31.9505, 115.8605, "Australia/Perth"),
    "Adelaide": ("Adelaide, Australia", -34.9285, 138.6007, "Australia/Adelaide"),
    "Canberra": ("Canberra, Australia", -35.2809, 149.1300, "Australia/Sydney"),
    "Darwin": ("Darwin, Australia", -12.4634, 130.8456, "Australia/Darwin"),
    "Hobart": ("Hobart, Australia", -42.8821, 147.3272, "Australia/Hobart"),
    "Gold Coast": ("Gold Coast, Australia", -28.0167, 153.4000, "Australia/Brisbane"),
    "Cairns": ("Cairns, Australia", -16.9203, 145.7781, "Australia/Brisbane"),
    "Auckland": ("Auckland, New Zealand", -36.8485, 174.7633, "Pacific/Auckland"),
    "Wellington": ("Wellington, New Zealand", -41.2865, 174.7762, "Pacific/Auckland"),
    "Christchurch": ("Christchurch, New Zealand", -43.5321, 172.6362, "Pacific/Auckland"),
    "Queenstown": ("Queenstown, New Zealand", -45.0312, 168.6626, "Pacific/Auckland"),
    "Suva": ("Suva, Fiji", -18.1248, 178.4501, "Pacific/Fiji"),
    "Nadi": ("Nadi, Fiji", -17.7765, 177.4162, "Pacific/Fiji"),
    "Port Moresby": ("Port Moresby, Papua New Guinea", -9.4438, 147.1803, "Pacific/Port_Moresby"),
    "Noumea": ("Nouméa, New Caledonia", -22.2758, 166.4581, "Pacific/Noumea"),
    "Papeete": ("Papeete, French Polynesia", -17.5516, -149.5585, "Pacific/Tahiti"),
    "Apia": ("Apia, Samoa", -13.8506, -171.7513, "Pacific/Apia"),
    "Nuku'alofa": ("Nuku'alofa, Tonga", -21.1789, -175.1982, "Pacific/Tongatapu"),
    "Port Vila": ("Port Vila, Vanuatu", -17.7334, 168.3273, "Pacific/Efate"),
    
    # CENTRAL ASIA
    "Almaty": ("Almaty, Kazakhstan", 43.2775, 76.8958, "Asia/Almaty"),
    "Nur-Sultan": ("Nur-Sultan, Kazakhstan", 51.1694, 71.4491, "Asia/Almaty"),
    "Tashkent": ("Tashkent, Uzbekistan", 41.2995, 69.2401, "Asia/Tashkent"),
    "Samarkand": ("Samarkand, Uzbekistan", 39.6270, 66.9750, "Asia/Tashkent"),
    "Ashgabat": ("Ashgabat, Turkmenistan", 37.9601, 58.3261, "Asia/Ashgabat"),
    "Bishkek": ("Bishkek, Kyrgyzstan", 42.8746, 74.5698, "Asia/Bishkek"),
    "Dushanbe": ("Dushanbe, Tajikistan", 38.5598, 68.7870, "Asia/Dushanbe"),
    "Kabul": ("Kabul, Afghanistan", 34.5553, 69.2075, "Asia/Kabul"),
    
    # ARCTIC & REMOTE
    "Anchorage": ("Anchorage, Alaska", 61.2181, -149.9003, "America/Anchorage"),
    "Fairbanks": ("Fairbanks, Alaska", 64.8378, -147.7164, "America/Anchorage"),
    "Whitehorse": ("Whitehorse, Yukon", 60.7212, -135.0568, "America/Whitehorse"),
    "Yellowknife": ("Yellowknife, Northwest Territories", 62.4540, -114.3718, "America/Yellowknife"),
    "Iqaluit": ("Iqaluit, Nunavut", 63.7467, -68.5170, "America/Iqaluit"),
    "Nuuk": ("Nuuk, Greenland", 64.1836, -51.7214, "America/Nuuk"),
    "Longyearbyen": ("Longyearbyen, Svalbard", 78.2232, 15.6267, "Arctic/Longyearbyen"),
    "Murmansk": ("Murmansk, Russia", 68.9585, 33.0827, "Europe/Moscow"),
    "Tromsø": ("Tromsø, Norway", 69.6496, 18.9560, "Europe/Oslo"),
    "Rovaniemi": ("Rovaniemi, Finland", 66.5039, 25.7294, "Europe/Helsinki"),
    
    # ISLAND NATIONS & TERRITORIES
    "Male": ("Malé, Maldives", 4.1755, 73.5093, "Indian/Maldives"),
    "Victoria": ("Victoria, Seychelles", -4.6197, 55.4500, "Indian/Mahe"),
    "Port Louis": ("Port Louis, Mauritius", -20.1609, 57.5012, "Indian/Mauritius"),
    "Saint Denis": ("Saint-Denis, Réunion", -20.8823, 55.4504, "Indian/Reunion"),
    "Honolulu": ("Honolulu, Hawaii", 21.3099, -157.8581, "Pacific/Honolulu"),
    "Guam": ("Hagåtña, Guam", 13.4745, 144.7504, "Pacific/Guam"),

} # adventure_locales
