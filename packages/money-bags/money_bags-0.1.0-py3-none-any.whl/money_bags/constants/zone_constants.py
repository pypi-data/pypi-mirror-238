from enum import Enum


class RegionIssuance(Enum):
    NORTH_AMERICA = "North America"
    EUROZONE = "EuroZone"
    NON_EUROZONE = "Non-EuroZone"
    CROSS_ZONE = "Cross-Zone"
    APAC = "APAC"
    UNKNOWN = "UNKNOWN"


NON_EURO_COUNTRIES = ["GB", "SE", "NO", "DK"]
NON_EUROZONE_INSTRUMENT_GROUP = ["SSA", "SAS"]
XS_COUNTRY_CODES = ["XS"]
