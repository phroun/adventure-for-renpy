init python:
     """
**************************************************************************
**
**   adventure-time.rpy - Time Module for Adventure (for Ren'Py)
**
**   See adventure.rpy for version information.
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

**************************************************************************
"""

# <init>
init python:

    import math
    import re
    from datetime import datetime, date
    import word_numbers as word_numbers
    adventure_parse_number_tokens = word_numbers.parse_number_tokens
    
    # <class>
    class AdventureTimeStore(object):
        # <def>
        def __init__(self):
            self.initialized = False
        # </def>
    # </class>

    adventure_t = AdventureTimeStore()
    import locales as adventure_time_locales
    import tzdata as adventure_tzdata
    adventure_t.locales = adventure_time_locales.locales
    adventure_t.zone_info = adventure_tzdata.tzdata

    adventure_t.locale = None
    adventure_t.base_locale = None
    adventure_t.default_locale = 'Seattle'
    adventure_t.game_day = 1
    adventure_t.locale_set = False
    adventure_t.year_known = False
    adventure_t.base_year = 2025 # Default Year
    adventure_t.base_month = 9 # September
    adventure_t.base_day = 21 # 21st (Day before Autumn Equinox)
    adventure_t.base_dow = 1 # Sunday 
    adventure_t.dow_offset = 0 # Matches the Real World
    adventure_t.date_set = False
    adventure_t.year  = adventure_t.base_year
    adventure_t.month = adventure_t.base_month
    adventure_t.day   = adventure_t.base_day
    adventure_t.dow   = adventure_t.base_dow

    # <def>
    def adventure_get_timezone_info(iana_timezone):
        """Get timezone information for a given IANA timezone identifier"""
        return timezone_info.get(iana_timezone, None)
    # </def adventure_get_timezone_info>

    # <def>
    def adventure_get_current_offset(iana_timezone, is_dst_active=False):
        """Get the current UTC offset for a timezone based on DST status"""
        tz_info = timezone_info.get(iana_timezone)
        # <if>
        if not tz_info:
            return None
        # </if>
        
        # <if>
        if is_dst_active and tz_info["utc_offset_dst"] is not None:
            return tz_info["utc_offset_dst"]
        else:
            return tz_info["utc_offset_std"]
        # </if>
    # </def adventure_get_current_offset>

    # <def>
    def adventure_has_dst(iana_timezone):
        """Check if a timezone observes daylight saving time"""
        tz_info = timezone_info.get(iana_timezone)
        return tz_info and tz_info["utc_offset_dst"] is not None
    # </def adventure_has_dst>

    # Example usage function
    def adventure_get_locale_info(key):
        """Get locale information by key"""
        # <if>
        if key in adventure_t.locales:
            return adventure_t.locales[key]
        else:
            return None
        # </if>
    # </def adventure_get_locale_info>

    # <def>
    def adventure_search_locales(search_term):
        """Search for locales containing the search term"""
        results = []
        search_lower = search_term.lower()
        
        # <for>
        for key, (full_name, lat, lon, tz) in adventure_t.locales.items():
            # <if>
            if (search_lower in key.lower() or 
                search_lower in full_name.lower()):
                results.append((key, full_name, lat, lon, tz))
            # </if>
        # </for>
        
        return results
    # </def adventure_search_locales>

    # <def>
    def adventure_calculate_sun_times(latitude, longitude, day_of_year, meridian=None, debug=False):
        """
        Calculate approximate sunrise and sunset times for a given location and day.
        
        Args:
            latitude (float): Latitude in decimal degrees (positive = North, negative = South)
            longitude (float): Longitude in decimal degrees (positive = East, negative = West)
            day_of_year (int): Day number in the year (1-365/366)
        
        Returns:
            tuple: (sunrise_hour, sunset_hour) as decimal hours in local solar time
                   Returns (None, None) if sun doesn't rise/set (polar day/night)
        """
        # <def>
        def dbg(*args, **kwargs):
            # <if>
            if debug:
                print(*args, **kwargs)
            # </if>
        # </def dbg>
        meridian = meridian or longitude
        lat_rad = math.radians(latitude)
        fractional_day = day_of_year - 1 + (12.0 - 12) / 24.0
        gamma_decl = 2 * math.pi / 365 * (day_of_year - 1)
        declination_rad = 0.006918 - 0.399912 * math.cos(gamma_decl) + 0.070257 * math.sin(gamma_decl) \
                        - 0.006758 * math.cos(2 * gamma_decl) + 0.000907 * math.sin(2 * gamma_decl) \
                        - 0.002697 * math.cos(3 * gamma_decl) + 0.00148 * math.sin(3 * gamma_decl)
        dbg(meridian, "day_of_year", day_of_year)
        dbg(meridian, "declination rad", declination_rad)
        cos_hour_angle = (math.sin(math.radians(-0.833)) - 
                          math.sin(lat_rad) * math.sin(declination_rad)) / \
                         (math.cos(lat_rad) * math.cos(declination_rad))
        dbg(meridian, "cos hour angle", cos_hour_angle)
        # Check for polar day/night conditions
        # <if>
        if cos_hour_angle > 1:
            # Polar night - sun never rises
            return (None, True)
        elif cos_hour_angle < -1:
            # Polar day - sun never sets
            return (True, None)
        # </if>
        hour_angle_rad = math.acos(cos_hour_angle)
        hour_angle_hours = math.degrees(hour_angle_rad) / 15  # 15 degrees per hour
        dbg(meridian, "hour_angle_rad: ", hour_angle_rad)
        dbg(meridian, "hour_angle_hours: ", hour_angle_hours)
        gamma_eot = 2 * math.pi / 365 * (day_of_year - 1)
        equation_of_time = 229.18 * (0.000075 + 0.001868 * math.cos(gamma_eot)
                         - 0.032077 * math.sin(gamma_eot)
                         - 0.014615 * math.cos(2 * gamma_eot)
                         - 0.040849 * math.sin(2 * gamma_eot))
        equation_of_time_hours = equation_of_time / 60  # Convert minutes to hours
        # Calculate longitude correction (4 minutes per degree from standard meridian)
        # Assuming standard meridian is at longitude 0° for simplicity
        longitude_correction_hours = (longitude - meridian) / 15
        # Solar noon in local solar time (12:00 + corrections)
        solar_noon = 12 - longitude_correction_hours + equation_of_time_hours
        dbg(meridian, "solar_noon:", solar_noon)
        dbg(meridian, "equation_of_time_hours: ", equation_of_time_hours)
        dbg(meridian, "longitude_correction_hours: ", longitude_correction_hours)
        # Calculate sunrise and sunset times
        sunrise = solar_noon - hour_angle_hours
        sunset = solar_noon + hour_angle_hours
        dbg(meridian, f"About to return: sunrise={sunrise}, sunset={sunset}")
        return (sunrise, sunset)
    # </def adventure_calculate_sun_times>

    # <def>
    def adventure_format_time(decimal_hour):
        # <if>
        if decimal_hour in [None, False, True]:
            return "N/A"
        # </if>
        hours = int(decimal_hour)
        minutes = int((decimal_hour - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"
    # </def adventure_format_time>

    # <def>
    def adventure_calc_locale(locale, type=""):
        res = adventure_search_locales(locale)
        ltyp = type.strip()
        # <if>
        if ltyp != "":
            ltyp = ltyp + " ";
        # </if>
        rtz = []
        rlat = []
        rlong = []
        # <for>
        for r in res:
            # <if>
            if not r[4] in rtz:
                rtz.append(r[4])
                rlat.append(r[2])
                rlong.append(r[3])
            # </if>
        # </for>
        # <if>
        if len(rtz) == 1:
            # <if>
            if len(res) == 1:
                rlocale = res[0][0]
                lat = res[0][2]
                long = res[0][3]
            else:
                rlocale = locale
            # </if>
            tz = rtz[0]
            lat = sum(rlat) / len(rlat)
            long = sum(rlong) / len(rlong)
        elif len(res):
            # <for>
            for r in res:
                print(r[1])
            # </for>
            raise ValueError('Specified ' + ltyp + 'locale "' + locale + '" not specific enough to select timezone.')
        else:
            raise ValueError('Specified ' + ltyp + 'locale "' + locale + '" matched no results.')
        # </if>
        # <try>
        try:
            zone = adventure_t.zone_info[tz]
            meridian = zone["utc_offset_std"] * 15
        except:
            meridian = long
        # </try>
        
        return (rlocale, tz, lat, long, meridian)
    # </def adventure_calc_locale>

    # <def>
    def adventure_story_base_locale(locale):
        """
        Set the base locale for the story.
        
        Args:
            See locales.py for list.
        """
        rlocale, tz, lat, long, meridian = adventure_calc_locale(locale)
        adventure_t.base_locale = rlocale
        adventure_t.base_tz = tz
        adventure_t.base_lat = lat
        adventure_t.base_long = long
        adventure_t.base_meridian = meridian
        base_date = datetime(adventure_t.base_year, adventure_t.base_month, adventure_t.base_day)
        time_tuple = base_date.timetuple()
        doy = time_tuple.tm_yday
        rise, set = adventure_calculate_sun_times(lat, long, doy, meridian)
        adventure_t.base_sunset = set
        adventure_t.base_sunrise = rise
        dlocale = adventure_t.base_locale or adventure_t.default_locale
        # <if>
        if adventure_t.locale_set and adventure_t.locale:
            dlocale = adventure_t.locale
        # </if>
        adventure_locale(dlocale, system_set=True)
    # </def>

    # <def>
    def adventure_locale(locale, system_set=False):
        rlocale, tz, lat, long, meridian = adventure_calc_locale(locale)
        # <if>
        if system_set == False:
            adventure_t.locale_set = True
        # </if>
        adventure_t.locale = rlocale
        adventure_t.tz = tz
        adventure_t.lat = lat
        adventure_t.long = long
        adventure_t.meridian = meridian
        base_date = datetime(adventure_t.base_year, adventure_t.base_month, adventure_t.base_day)
        time_tuple = base_date.timetuple()
        doy = time_tuple.tm_yday
        rise, set = adventure_calculate_sun_times(lat, long, doy, meridian)
        adventure_t.sunset = set
        adventure_t.sunrise = rise
    # </def>

    # <def>
    def adventure_wrap_day_of_week(day):
        return (day - 1) % 7 + 1
    # </def>

    # <class>
    class AdventureParsedTime:
        # <def>
        def __init__(self):
            self.initialized = False
            self.flash_back = False
            self.flash_forward = False

            # example: Thursday, September 14th, 1989

            self.weekday_prefix = None       # Range: None or 1-7.  Example: 5 for Thursday
            self.exact_day_of_week = None    # 5 for "Thursday" (when exact date is detected)
            self.exact_month = None          # 9 for "September"
            self.exact_day_of_month = None   # 14 for "September 14th"
            self.year_known = False          # True or False
            self.exact_year = None           # 1989
            self.exact_year_era = None       # CE
            self.standard_year = None        # Year mapped by era data
            self.standard_day_of_week = None # Day of week, using real world calculation
            
            self.exact_hour = None           # 14 (2:30PM, 1430)
            self.exact_minute = None         # 30

            self.next_day_of_week = None     # next Tuesday
            self.days_later = 0              # 2 days later, 2:30pm the next day
            self.hours_later = 0             # 3 hours later
            self.minutes_later = 0           # 15 minutes later
        # </def>
        
        # <def>
        def __str__(self):
            # This is called by print() and str()
            p = "AdventureParsedTime(flash_back=" + str(self.flash_back)
            p += ", flash_forward=" + str(self.flash_forward)
            p += ", year_known=" + str(self.year_known) + "\n"
            p += ", weekday_prefix=" + str(self.weekday_prefix) + "\n"
            p += ", exact_day_of_week=" + str(self.exact_day_of_week)
            p += ", standard_day_of_week=" + str(self.standard_day_of_week)
            p += ", standard_year=" + str(self.standard_year) + "\n"
            p += ", exact_month=" + str(self.exact_month)
            p += ", exact_day_of_month=" + str(self.exact_day_of_month)
            p += ", exact_year=" + str(self.exact_year)
            p += ", exact_year_era='" + str(self.exact_year_era) + "'\n"
            p += ", exact_hour=" + str(self.exact_hour)
            p += ", exact_minute=" + str(self.exact_minute) + "\n"
            p += ", next_day_of_week=" + str(self.next_day_of_week)
            p += ", days_later=" + str(self.days_later)
            p += ", hours_later=" + str(self.hours_later)
            p += ", minutes_later=" + str(self.minutes_later)
            p += ")"
            return p
        # </def>
    # </class>

    adventure_t.prefix = ('next', 'this')
    adventure_t.single_units = ('minute', 'hour', 'day', 'night', 'morning', 'afternoon', 'evening', 'week', 'month')
    adventure_t_plural_units = ('minutes', 'hours', 'days', 'nights', 'mornings', 'afternoons', 'evenings', 'weeks', 'months')
    adventure_t.digits = ('1','2','3','4','5','6','7','8','9','0')
    adventure_t.eras = ('bce', 'ce')
    adventure_t.era_offsets = {
        'ce': 0,
        'bce': 1,
    }
    adventure_t.inverted_eras = ('bce')   # lower numbers are later
    adventure_t.months = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'sept': 9, 'oct': 10, 'nov': 11, 'dec': 12,
        'january': 1, 'february': 2, 'march': 3, 'april': 4, 'june': 6,
        'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
    }
    adventure_t.weekdays = {
        'sun': 1,
        'sunday': 1,
        'mon': 2,
        'monday': 2,
        'tue': 3,
        'tues': 3,
        'tuesday': 3,
        'wed': 4,
        'wednesday': 4,
        'thu': 5,
        'thur': 5,
        'thurs': 5,
        'thursday': 5,
        'fri': 6,
        'friday': 6,
        'sat': 7,
        'saturday': 7,
    }
    adventure_t.plural_weekdays = {
        'sundays': 1,
        'mondays': 2,
        'tuesdays': 3,
        'wednesdays': 4,
        'thursdays': 5,
        'fridays': 6,
        'saturdays': 7,
    }
    
    # <def>
    def adventure_tupeek(t, offset=0):
        # <try>
        try:
            return t[offset]
        except IndexError:
            return ""
        # </try>
    # <def>

    # <def>
    def adventure_time_extract_year(tokens):
        era_found = None
        nval = None
        done = False
        year_comma_eaten = False
        n = 0
        while len(tokens):
            n += 1
            consider = tokens[0:n]
            inner_comma_eaten = False
            # <if>
            if consider[-1].endswith(','):
                new_last_token = consider[-1][:-1]
                consider = consider[0:-1] + (consider[-1][:-1],)
                inner_comma_eaten = True
            # </if>
            
            # <if>
            if consider[-1] == ',':
                done = True
            else:
                # <try>
                try:
                    ntype, nval, _fmt, _sep = adventure_parse_number_tokens(consider, True)
                    error = ntype == 'ordinal'
                    # <if>
                    if error:
                        raise ValueError('Unexpected Ordinal in Year')
                    # </if>
                    date_comma_eaten = inner_comma_eaten
                    # <if>
                    if date_comma_eaten:
                        done = True
                    # </if>
                except:
                    n -= 1
                    done = True
                # </try>
            # </if>
            # <if>
            if n == len(tokens):
                done = True
            # </if>
            # <if>
            if done:
                break
            # </if>
        # </while do-until loop>
        tokens = tokens[n:]
        era_considered = adventure_tupeek(tokens).replace('.','').lower()
        # <if>
        if era_found is None and era_considered in adventure_t.eras:
           era_found = era_considered
           tokens = tokens[1:]
        # </if>
        return (nval, era_found, tokens)
    # </def adventure_time_extract_year>

    # <def>
    def adventure_time_extract_day_number(tokens):
        first_tok = adventure_tupeek(tokens)
        exact_day_of_month = None
        # <if>
        if first_tok.startswith(adventure_t.digits):
            # <try>
            try:
                # <if>
                if first_tok.endswith(','):
                    first_tok = first_tok[:-1]                    
                # </if>
                _ntype, exact_day_of_month, _fmt, _sep = adventure_parse_number_tokens((first_tok,), True)
                tokens = tokens[1:]
            except Exception as e:
                print("Exception:", str(e))
                pass
            # </try>
        else:
            # <while>
            n = 0
            nval = None
            done = False
            date_comma_eaten = False
            while True:
                n += 1
                consider = tokens[0:n]
                inner_comma_eaten = False
                # <if>
                if consider[-1].endswith(','):
                    consider = consider[0:-1] + (consider[-1][:-1],)
                    inner_comma_eaten = True
                # </if>
                done = False
                # <try>
                try:
                    ntype, nval, _fmt, _sep = adventure_parse_number_tokens(consider, True)
                    done = ntype == 'ordinal'
                    date_comma_eaten = inner_comma_eaten
                    # <if>
                    if date_comma_eaten:
                        done = True
                    # </if>
                except:
                    n -= 1
                    done = True
                # </try>
                # <if>
                if n == len(tokens):
                    done = True
                # </if>
                # <if>
                if done:
                    break
                # </if>
            # </while do-until loop>
            tokens = tokens[n:]
            # <if>
            if adventure_tupeek(tokens, 0) == ',' and not date_comma_eaten:
                tokens = tokens[1:]
            # </if>
            exact_day_of_month = nval
        # </if>
        return (exact_day_of_month, tokens)
    # </def adventure_time_extract_day_number>
    
    # <def>
    def adventure_parse_tokens(tokens):
        # <if>
        if not tokens:
            raise ValueError("Empty token list")
        # </if>

        res = AdventureParsedTime()
        
        if not len(tokens):
            return res
        
        # Convert all tokens to cardinal equivalents and check for ordinal indicators
        cardinal_tokens = []
        is_ordinal = False
        last_ordinal_position = -1
        
        first_tok = adventure_tupeek(tokens).replace('.','').lower()
        comma_eaten = False
        # <if>
        if first_tok.endswith(','):
            first_tok = first_tok[:-1]
            comma_eaten = True
        # </if>
        res.weekday_prefix = adventure_t.weekdays.get(first_tok)
        
        # <if>
        if res.weekday_prefix:
            tokens = tokens[1:]
            # <if>
            if adventure_tupeek(tokens) == ',' and not comma_eaten:
                # consume the optional comma
                tokens = tokens[1:]
                comma_eaten = True
            # </if>
        # </if>

        date_found = False
        first_tok = adventure_tupeek(tokens)
        # <if>
        if len(first_tok) == 10:
            # <if>
            if first_tok[4] == first_tok[7] and first_tok[4] in ['/','-','.']:
                components = first_tok.split(first_tok[4])
                # <if>
                if components[0].isdigit() and components[1].isdigit() and components[2].isdigit():
                    # <try>
                    try:
                        res.exact_year = int(components[0])
                        res.exact_month = int(components[1])
                        res.exact_day_of_month = int(components[2])
                        # <if>
                        if res.exact_year == 0 or res.exact_month == 0 or res.exact_day_of_month == 0:
                            raise ValueError('Invalid date component in "' + first_tok + '"')
                        # </if>
                        tokens = tokens[1:]
                        date_found = True
                        # <if>
                        if res.weekday_prefix:
                            res.exact_day_of_week = res.weekday_prefix
                        # </if>
                    except:
                        raise ValueError('Invalid date component in "' + first_tok + '"')
                    # </try>
                # </if>
            # </if>
        # </if>
        
        # <if>        
        if not date_found:
            first_tok = first_tok.replace('.','').lower()
            res.exact_month = adventure_t.months.get(first_tok)
            # <if>
            if res.exact_month:
                res.exact_day_of_week = res.weekday_prefix # might still be None
                tokens = tokens[1:]
                res.exact_day_of_month, tokens = adventure_time_extract_day_number(tokens)
                res.exact_year, res.exact_year_era, tokens = adventure_time_extract_year(tokens)
            else:
                # check for "[the] X [day] [of] Y"
                ctokens = tokens
                # <if>
                if adventure_tupeek(ctokens).lower() == 'the':
                    ctokens = ctokens[1:]
                # </if>
                cday_of_month, ctokens = adventure_time_extract_day_number(ctokens)
                # <if>
                if cday_of_month:
                    # <if>
                    if adventure_tupeek(ctokens).lower() == 'day':
                        ctokens = ctokens[1:]
                    # </if>
                    # <if>
                    if adventure_tupeek(ctokens).lower() == 'of':
                        ctokens = ctokens[1:]
                    # </if>
                    date_comma_eaten = False
                    inner_comma_eaten = False
                    first_tok = adventure_tupeek(ctokens).replace('.','').lower()
                    # <if>
                    if first_tok.endswith(','):
                        first_tok = first_tok[:-1]
                        inner_comma_eaten = True
                    # </if considered month had comma>
                    cmonth = adventure_t.months.get(first_tok)
                    # <if>
                    if cmonth:
                        tokens = ctokens[1:]
                        res.exact_month = cmonth
                        res.exact_day_of_month = cday_of_month
                        date_comma_eaten = inner_comma_eaten
                        # <if>
                        if adventure_tupeek(tokens) == ',' and not date_comma_eaten:
                            # consume the optional comma
                            tokens = tokens[1:]
                            date_comma_eaten = True
                        # </if comma token after month>
                    # </if cmonth>
                    res.exact_year, res.exact_year_era, tokens = adventure_time_extract_year(tokens)
                # </if cday_of_month>
            # </if>
        # </if>
        
        # <for>
        for i, token in enumerate(tokens):
            print('extra token', token)
        # </for>
        
        # <if>
        if res.exact_year and res.exact_year_era:
            res.standard_year = res.exact_yaer
            # <if>
            if res.exact_year_era in adventure_t.inverted_eras:
                res.standard_year = -res.exact_yaer
            # </if>
            # <if>
            if res.exact_year_era in adventure_t.era_offsets:
                res.standard_year += adventure_t.era_offsets[res.exact_year_era]
            # </if>
        # </if>

        # <if>
        if res.standard_year and res.exact_month and res.exact_day_of_month:
            cdate = datetime(res.standard_year, res.exact_month, res.exact_day_of_month)
            res.standard_day_of_week = adventure_wrap_day_of_week(cdate.isoweekday() + 1)
        # </if>

        return res
    # </def>
    
    # <def>
    def adventure_story_base_date(s):
        tokens = s.split()
        res = adventure_parse_tokens(tuple(tokens))

        # the following allows story DOWs to be desynchronized from
        # DOWs in reality if specified as such in the base date:
        if res.exact_day_of_week is None:
           res.exact_day_of_week = res.standard_day_of_week
        if res.standard_day_of_week is not None:
           adventure_t.dow_offset = res.exact_day_of_week - res.standard_day_of_week
        if res.exact_year is not None:
            adventure_t.base_year = res.exact_year
            adventure_t.year_known = True
        adventure_t.base_month = res.exact_month
        adventure_t.base_day = res.exact_day_of_month
        # <if>
        if not adventure_t.date_set:
            adventure_t.year = adventure_t.base_year
            adventure_t.month = adventure_t.base_month
            adventure_t.day = adventure_t.base_day
        # </if>
        dlocale = adventure_t.base_locale or adventure_t.default_locale
        # <if>
        if adventure_t.locale_set and adventure_t.locale:
            dlocale = adventure_t.locale
        # </if>
        adventure_locale(dlocale, True)
    # </def>
    
    # <def>
    def adventure_get_setting():
        res = { "base_locale": adventure_t.base_locale }
        try:
            res["base_date"] = datetime(adventure_t.base_year, adventure_t.base_month, adventure_t.base_day).strftime("%Y-%m-%d")
        except:
            res["base_date"] = None
        try:
            res["base_sunrise"] = adventure_format_time(adventure_t.base_sunrise)
        except:
            res["base_sunrise"] = None
        try:
            res["base_sunset"] = adventure_format_time(adventure_t.base_sunset)
        except:
            res["base_sunset"] = None
        res["locale"] = adventure_t.locale
        try:
            res["date"] = datetime(adventure_t.year, adventure_t.month, adventure_t.day).strftime("%Y-%m-%d")
        except:
            res["date"] = None
        try:
            res["sunrise"] = adventure_format_time(adventure_t.sunrise)
        except:
            res["sunrise"] = None
        try:
            res["sunset"] = adventure_format_time(adventure_t.sunset)
        except:
            res["sunset"] = None
        return res
    # </def>
    
    # <def>
    def adventure_test_suntimes():
        test_cases = [

            # Seattle year-round test cases - ALL IN STANDARD TIME (PST, UTC-8)
            # Data sourced from timeanddate.com, converted to PST by subtracting 1 hour from PDT dates
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-01-15", 15, 7.867, 16.750),   # Mid-January (PST in effect)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-02-15", 46, 7.233, 17.550),   # Mid-February (PST in effect)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-03-15", 74, 6.350, 18.250),   # Mid-March (PDT -1hr = PST)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-04-15", 105, 5.317, 18.983),  # Mid-April (PDT -1hr = PST)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-05-15", 135, 4.517, 19.667),  # Mid-May (PDT -1hr = PST)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-06-15", 166, 4.183, 20.150),  # Mid-June (PDT -1hr = PST)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-07-15", 196, 4.450, 20.033),  # Mid-July (PDT -1hr = PST)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-08-15", 227, 5.083, 19.333),  # Mid-August (PDT -1hr = PST)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-09-15", 258, 5.783, 18.333),  # Mid-September (PDT -1hr = PST)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-09-28", 271, 6.067, 17.883),  # Late September (PDT -1hr = PST)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-10-15", 288, 6.467, 17.333),  # Mid-October (PDT -1hr = PST)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-11-15", 319, 7.250, 16.533),  # Mid-November (PST in effect)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-12-15", 349, 7.850, 16.300),  # Mid-December (PST in effect)

            # Mid-latitude cities - September (Fall/Spring)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-09-28", 271, 6.09, 17.89),
            ("New York, NY", 40.7128, -74.0060, -5, "2025-09-28", 271, 5.82, 17.70),
            ("London, UK", 51.5074, -0.1278, 0, "2025-09-28", 271, 5.95, 17.74),
            ("Tokyo, Japan", 35.6762, 139.6503, 9, "2025-09-28", 271, 5.55, 17.48),
            ("Sydney, Australia", -33.8688, 151.2093, 10, "2025-09-28", 271, 5.61, 17.92),
            
            # Summer solstice tests (June/July)
            ("Los Angeles, CA", 34.0522, -118.2437, -8, "2025-07-28", 209, 5.03, 18.94),
            ("London, UK", 51.5074, -0.1278, 0, "2025-06-21", 172, 3.72, 20.35),
            ("Sydney, Australia", -33.8688, 151.2093, 10, "2025-06-21", 172, 7.00, 16.88),
            ("Fairbanks, AK", 64.8378, -147.7164, -9, "2025-06-21", 172, 1.95, 23.78),
            
            # Winter tests (December/January)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-12-21", 355, 7.85, 16.37),
            ("New York, NY", 40.7128, -74.0060, -5, "2025-12-21", 355, 7.28, 16.53),
            ("Sydney, Australia", -33.8688, 151.2093, 10, "2025-12-21", 355, 4.68, 19.09),
            
            # Equinox tests (March 20, September 22)
            ("Seattle, WA", 47.6061, -122.3328, -8, "2025-03-20", 79, 6.19, 18.37),
            ("Miami, FL", 25.7617, -80.1918, -5, "2025-03-20", 79, 6.41, 18.53),
            ("London, UK", 51.5074, -0.1278, 0, "2025-09-22", 265, 5.79, 17.97),
            
            # Tropical location
            ("Honolulu, HI", 21.3099, -157.8581, -10, "2025-06-21", 172, 5.84, 19.27),
            ("Honolulu, HI", 21.3099, -157.8581, -10, "2025-12-21", 355, 7.08, 17.91),
            
            # Southern hemisphere variety
            ("Buenos Aires, Argentina", -34.6037, -58.3816, -3, "2025-06-21", 172, 8.01, 17.84),
            ("Cape Town, South Africa", -33.9249, 18.4241, 2, "2025-12-21", 355, 5.54, 19.95),
        ]

        results = []
        
        # <for>
        for city, lat, lon, utc_offset, date_str, day, exp_sunrise, exp_sunset in test_cases:
        
            calc_sunrise, calc_sunset = adventure_calculate_sun_times(lat, lon, day, utc_offset * 15)
            
            sunrise_error_minutes = (calc_sunrise - exp_sunrise) * 60
            sunset_error_minutes = (calc_sunset - exp_sunset) * 60
            
            results.append({
                'city': city,
                'date': date_str,
                'sunrise_error_min': round(sunrise_error_minutes, 1),
                'sunset_error_min': round(sunset_error_minutes, 1),
                'max_error_min': round(max(abs(sunrise_error_minutes), abs(sunset_error_minutes)), 1)
            })
            
            print(f"{city:30} {date_str}: Sunrise err: {sunrise_error_minutes:+6.1f} min, Sunset err: {sunset_error_minutes:+6.1f} min")
        # </for>
    # </def>
    
    adventure_locale(adventure_t.default_locale, system_set=True)

# </init>
