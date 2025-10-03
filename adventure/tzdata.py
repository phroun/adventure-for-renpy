#!/usr/bin/env python3
"""
**************************************************************************
**
**   tzdata.py - Time Zone Data for Adventure
**
**   Version 1 revision 0
**
**************************************************************************
**
**   The IANA time zone database itself, which was used to source the
**   information in this module, as well as some reference source code,
**   is in the public domain.
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

"""
IANA Timezone Information Dictionary
Maps IANA timezone identifiers to UTC offsets and daylight saving time rules

Format:
"timezone_id": {
    "utc_offset_std": hours_offset_from_utc_in_standard_time,
    "utc_offset_dst": hours_offset_from_utc_in_daylight_time (or None if no DST),
    "dst_start": "DST start rule description",
    "dst_end": "DST end rule description",
    "dst_rule": None if no DST, otherwise brief description
}
"""

tzdata = {
    # AFRICA
    "Africa/Accra": {
        "utc_offset_std": 0,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Addis_Ababa": {
        "utc_offset_std": 3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Algiers": {
        "utc_offset_std": 1,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Bamako": {
        "utc_offset_std": 0,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Cairo": {
        "utc_offset_std": 2,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None  # Egypt discontinued DST in 2014
    },
    "Africa/Casablanca": {
        "utc_offset_std": 1,
        "utc_offset_dst": 0,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Reverse DST (UTC+1 -> UTC+0) during Ramadan period"
    },
    "Africa/Dakar": {
        "utc_offset_std": 0,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Dar_es_Salaam": {
        "utc_offset_std": 3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Gaborone": {
        "utc_offset_std": 2,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Harare": {
        "utc_offset_std": 2,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Johannesburg": {
        "utc_offset_std": 2,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Kampala": {
        "utc_offset_std": 3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Kigali": {
        "utc_offset_std": 2,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Kinshasa": {
        "utc_offset_std": 1,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Lagos": {
        "utc_offset_std": 1,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Luanda": {
        "utc_offset_std": 1,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Lusaka": {
        "utc_offset_std": 2,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Nairobi": {
        "utc_offset_std": 3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Tunis": {
        "utc_offset_std": 1,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Africa/Windhoek": {
        "utc_offset_std": 2,
        "utc_offset_dst": 1,
        "dst_start": "First Sunday in September",
        "dst_end": "First Sunday in April",
        "dst_rule": "Southern Hemisphere DST"
    },

    # AMERICAS
    "America/Anchorage": {
        "utc_offset_std": -9,
        "utc_offset_dst": -8,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Alaska Daylight Time (AKDT)"
    },
    "America/Argentina/Buenos_Aires": {
        "utc_offset_std": -3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None  # Argentina discontinued DST in 2009
    },
    "America/Asuncion": {
        "utc_offset_std": -3,
        "utc_offset_dst": -4,
        "dst_start": "First Sunday in October",
        "dst_end": "Fourth Sunday in March",
        "dst_rule": "Paraguay Summer Time (Southern Hemisphere)"
    },
    "America/Barbados": {
        "utc_offset_std": -4,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/Bogota": {
        "utc_offset_std": -5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/Cancun": {
        "utc_offset_std": -5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None  # Quintana Roo discontinued DST
    },
    "America/Caracas": {
        "utc_offset_std": -4,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/Chicago": {
        "utc_offset_std": -6,
        "utc_offset_dst": -5,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Central Daylight Time (CDT)"
    },
    "America/Costa_Rica": {
        "utc_offset_std": -6,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/Denver": {
        "utc_offset_std": -7,
        "utc_offset_dst": -6,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Mountain Daylight Time (MDT)"
    },
    "America/Edmonton": {
        "utc_offset_std": -7,
        "utc_offset_dst": -6,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Mountain Daylight Time (MDT)"
    },
    "America/Guatemala": {
        "utc_offset_std": -6,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/Guayaquil": {
        "utc_offset_std": -5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/Guyana": {
        "utc_offset_std": -4,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/Halifax": {
        "utc_offset_std": -4,
        "utc_offset_dst": -3,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Atlantic Daylight Time (ADT)"
    },
    "America/Havana": {
        "utc_offset_std": -5,
        "utc_offset_dst": -4,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Cuba Daylight Time (CDT)"
    },
    "America/Iqaluit": {
        "utc_offset_std": -5,
        "utc_offset_dst": -4,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Eastern Daylight Time (EDT)"
    },
    "America/Jamaica": {
        "utc_offset_std": -5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/La_Paz": {
        "utc_offset_std": -4,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/Lima": {
        "utc_offset_std": -5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/Los_Angeles": {
        "utc_offset_std": -8,
        "utc_offset_dst": -7,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Pacific Daylight Time (PDT)"
    },
    "America/Manaus": {
        "utc_offset_std": -4,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/Mexico_City": {
        "utc_offset_std": -6,
        "utc_offset_dst": -5,
        "dst_start": "First Sunday in April",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central Daylight Time (CDT)"
    },
    "America/Montevideo": {
        "utc_offset_std": -3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None  # Uruguay discontinued DST in 2015
    },
    "America/Nassau": {
        "utc_offset_std": -5,
        "utc_offset_dst": -4,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Eastern Daylight Time (EDT)"
    },
    "America/New_York": {
        "utc_offset_std": -5,
        "utc_offset_dst": -4,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Eastern Daylight Time (EDT)"
    },
    "America/Nuuk": {
        "utc_offset_std": -3,
        "utc_offset_dst": -2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "West Greenland Summer Time"
    },
    "America/Panama": {
        "utc_offset_std": -5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/Paramaribo": {
        "utc_offset_std": -3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/Phoenix": {
        "utc_offset_std": -7,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None  # Arizona does not observe DST
    },
    "America/Puerto_Rico": {
        "utc_offset_std": -4,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "America/Santiago": {
        "utc_offset_std": -3,
        "utc_offset_dst": -4,
        "dst_start": "First Sunday in September",
        "dst_end": "First Sunday in April",
        "dst_rule": "Chile Summer Time (Southern Hemisphere)"
    },
    "America/Sao_Paulo": {
        "utc_offset_std": -3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None  # Brazil discontinued DST in 2019
    },
    "America/St_Johns": {
        "utc_offset_std": -3.5,
        "utc_offset_dst": -2.5,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Newfoundland Daylight Time (NDT)"
    },
    "America/Tijuana": {
        "utc_offset_std": -8,
        "utc_offset_dst": -7,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Pacific Daylight Time (PDT)"
    },
    "America/Toronto": {
        "utc_offset_std": -5,
        "utc_offset_dst": -4,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Eastern Daylight Time (EDT)"
    },
    "America/Vancouver": {
        "utc_offset_std": -8,
        "utc_offset_dst": -7,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Pacific Daylight Time (PDT)"
    },
    "America/Whitehorse": {
        "utc_offset_std": -7,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None  # Yukon stopped DST in 2020
    },
    "America/Winnipeg": {
        "utc_offset_std": -6,
        "utc_offset_dst": -5,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Central Daylight Time (CDT)"
    },
    "America/Yellowknife": {
        "utc_offset_std": -7,
        "utc_offset_dst": -6,
        "dst_start": "Second Sunday in March",
        "dst_end": "First Sunday in November",
        "dst_rule": "Mountain Daylight Time (MDT)"
    },

    # ARCTIC
    "Arctic/Longyearbyen": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },

    # ASIA
    "Asia/Almaty": {
        "utc_offset_std": 6,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Amman": {
        "utc_offset_std": 2,
        "utc_offset_dst": 3,
        "dst_start": "Last Friday in March",
        "dst_end": "Last Friday in October",
        "dst_rule": "Arabia Summer Time"
    },
    "Asia/Ashgabat": {
        "utc_offset_std": 5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Baghdad": {
        "utc_offset_std": 3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Bahrain": {
        "utc_offset_std": 3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Bangkok": {
        "utc_offset_std": 7,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Beirut": {
        "utc_offset_std": 2,
        "utc_offset_dst": 3,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Eastern European Summer Time (EEST)"
    },
    "Asia/Bishkek": {
        "utc_offset_std": 6,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Brunei": {
        "utc_offset_std": 8,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Colombo": {
        "utc_offset_std": 5.5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Damascus": {
        "utc_offset_std": 2,
        "utc_offset_dst": 3,
        "dst_start": "Last Friday in March",
        "dst_end": "Last Friday in October",
        "dst_rule": "Eastern European Summer Time (EEST)"
    },
    "Asia/Dhaka": {
        "utc_offset_std": 6,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Dili": {
        "utc_offset_std": 9,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Dubai": {
        "utc_offset_std": 4,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Dushanbe": {
        "utc_offset_std": 5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Ho_Chi_Minh": {
        "utc_offset_std": 7,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Hong_Kong": {
        "utc_offset_std": 8,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Jakarta": {
        "utc_offset_std": 7,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Jerusalem": {
        "utc_offset_std": 2,
        "utc_offset_dst": 3,
        "dst_start": "Friday before last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Israel Daylight Time (IDT)"
    },
    "Asia/Kabul": {
        "utc_offset_std": 4.5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Karachi": {
        "utc_offset_std": 5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Kathmandu": {
        "utc_offset_std": 5.75,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Kolkata": {
        "utc_offset_std": 5.5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Kuala_Lumpur": {
        "utc_offset_std": 8,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Kuwait": {
        "utc_offset_std": 3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Macau": {
        "utc_offset_std": 8,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Makassar": {
        "utc_offset_std": 8,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Manila": {
        "utc_offset_std": 8,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Muscat": {
        "utc_offset_std": 4,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Nicosia": {
        "utc_offset_std": 2,
        "utc_offset_dst": 3,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Eastern European Summer Time (EEST)"
    },
    "Asia/Phnom_Penh": {
        "utc_offset_std": 7,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Pyongyang": {
        "utc_offset_std": 9,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Qatar": {
        "utc_offset_std": 3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Riyadh": {
        "utc_offset_std": 3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Seoul": {
        "utc_offset_std": 9,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Shanghai": {
        "utc_offset_std": 8,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Singapore": {
        "utc_offset_std": 8,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Taipei": {
        "utc_offset_std": 8,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Tashkent": {
        "utc_offset_std": 5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Tehran": {
        "utc_offset_std": 3.5,
        "utc_offset_dst": 4.5,
        "dst_start": "March 21 (Persian New Year)",
        "dst_end": "September 21 (Autumnal Equinox)",
        "dst_rule": "Iran Daylight Time (IRDT)"
    },
    "Asia/Thimphu": {
        "utc_offset_std": 6,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Tokyo": {
        "utc_offset_std": 9,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Ulaanbaatar": {
        "utc_offset_std": 8,
        "utc_offset_dst": 9,
        "dst_start": "Last Saturday in March",
        "dst_end": "Last Saturday in September",
        "dst_rule": "Ulaanbaatar Summer Time"
    },
    "Asia/Vientiane": {
        "utc_offset_std": 7,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Asia/Yangon": {
        "utc_offset_std": 6.5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },

    # ATLANTIC
    "Atlantic/Reykjavik": {
        "utc_offset_std": 0,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },

    # AUSTRALIA
    "Australia/Adelaide": {
        "utc_offset_std": 9.5,
        "utc_offset_dst": 10.5,
        "dst_start": "First Sunday in October",
        "dst_end": "First Sunday in April",
        "dst_rule": "Australian Central Daylight Time (Southern Hemisphere)"
    },
    "Australia/Brisbane": {
        "utc_offset_std": 10,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None  # Queensland does not observe DST
    },
    "Australia/Darwin": {
        "utc_offset_std": 9.5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None  # Northern Territory does not observe DST
    },
    "Australia/Hobart": {
        "utc_offset_std": 10,
        "utc_offset_dst": 11,
        "dst_start": "First Sunday in October",
        "dst_end": "First Sunday in April",
        "dst_rule": "Australian Eastern Daylight Time (Southern Hemisphere)"
    },
    "Australia/Melbourne": {
        "utc_offset_std": 10,
        "utc_offset_dst": 11,
        "dst_start": "First Sunday in October",
        "dst_end": "First Sunday in April",
        "dst_rule": "Australian Eastern Daylight Time (Southern Hemisphere)"
    },
    "Australia/Perth": {
        "utc_offset_std": 8,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None  # Western Australia does not observe DST
    },
    "Australia/Sydney": {
        "utc_offset_std": 10,
        "utc_offset_dst": 11,
        "dst_start": "First Sunday in October",
        "dst_end": "First Sunday in April",
        "dst_rule": "Australian Eastern Daylight Time (Southern Hemisphere)"
    },

    # EUROPE
    "Europe/Amsterdam": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Athens": {
        "utc_offset_std": 2,
        "utc_offset_dst": 3,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Eastern European Summer Time (EEST)"
    },
    "Europe/Belgrade": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Berlin": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Bratislava": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Brussels": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Bucharest": {
        "utc_offset_std": 2,
        "utc_offset_dst": 3,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Eastern European Summer Time (EEST)"
    },
    "Europe/Budapest": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Copenhagen": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Dublin": {
        "utc_offset_std": 0,
        "utc_offset_dst": 1,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Irish Standard Time (IST)"
    },
    "Europe/Helsinki": {
        "utc_offset_std": 2,
        "utc_offset_dst": 3,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Eastern European Summer Time (EEST)"
    },
    "Europe/Istanbul": {
        "utc_offset_std": 3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None  # Turkey discontinued DST in 2016
    },
    "Europe/Kiev": {
        "utc_offset_std": 2,
        "utc_offset_dst": 3,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Eastern European Summer Time (EEST)"
    },
    "Europe/Lisbon": {
        "utc_offset_std": 0,
        "utc_offset_dst": 1,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Western European Summer Time (WEST)"
    },
    "Europe/Ljubljana": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/London": {
        "utc_offset_std": 0,
        "utc_offset_dst": 1,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "British Summer Time (BST)"
    },
    "Europe/Luxembourg": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Madrid": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Malta": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Moscow": {
        "utc_offset_std": 3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None  # Russia discontinued DST in 2014
    },
    "Europe/Oslo": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Paris": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Prague": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Rome": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Sarajevo": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Sofia": {
        "utc_offset_std": 2,
        "utc_offset_dst": 3,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Eastern European Summer Time (EEST)"
    },
    "Europe/Stockholm": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Vienna": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Warsaw": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Zagreb": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },
    "Europe/Zurich": {
        "utc_offset_std": 1,
        "utc_offset_dst": 2,
        "dst_start": "Last Sunday in March",
        "dst_end": "Last Sunday in October",
        "dst_rule": "Central European Summer Time (CEST)"
    },

    # INDIAN OCEAN
    "Indian/Antananarivo": {
        "utc_offset_std": 3,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Indian/Mahe": {
        "utc_offset_std": 4,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Indian/Maldives": {
        "utc_offset_std": 5,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Indian/Mauritius": {
        "utc_offset_std": 4,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Indian/Reunion": {
        "utc_offset_std": 4,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },

    # PACIFIC
    "Pacific/Apia": {
        "utc_offset_std": 13,
        "utc_offset_dst": 14,
        "dst_start": "Last Sunday in September",
        "dst_end": "First Sunday in April",
        "dst_rule": "Samoa Summer Time (Southern Hemisphere)"
    },
    "Pacific/Auckland": {
        "utc_offset_std": 12,
        "utc_offset_dst": 13,
        "dst_start": "Last Sunday in September",
        "dst_end": "First Sunday in April",
        "dst_rule": "New Zealand Daylight Time (Southern Hemisphere)"
    },
    "Pacific/Efate": {
        "utc_offset_std": 11,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Pacific/Fiji": {
        "utc_offset_std": 12,
        "utc_offset_dst": 13,
        "dst_start": "First Sunday in November",
        "dst_end": "Third Sunday in January",
        "dst_rule": "Fiji Summer Time (Southern Hemisphere)"
    },
    "Pacific/Guam": {
        "utc_offset_std": 10,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Pacific/Honolulu": {
        "utc_offset_std": -10,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Pacific/Noumea": {
        "utc_offset_std": 11,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Pacific/Port_Moresby": {
        "utc_offset_std": 10,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Pacific/Tahiti": {
        "utc_offset_std": -10,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
    "Pacific/Tongatapu": {
        "utc_offset_std": 13,
        "utc_offset_dst": None,
        "dst_start": None,
        "dst_end": None,
        "dst_rule": None
    },
}
