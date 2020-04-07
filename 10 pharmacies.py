from business import find_businesses
from geocoder import get_coordinates
from mapapi import show_map
import sys


def main():
    toponym_to_find = " ".join(sys.argv[1:])
    if not toponym_to_find:
        print('No data')
        exit(1)
    lat, lon = get_coordinates(toponym_to_find)
    address_ll = "{0},{1}".format(lat, lon)
    delta = 0.01
    organizations = []
    while delta < 100 and len(organizations) < 10:
        delta *= 2.0
        span = "{0},{1}".format(delta, delta)
        organizations = find_businesses(address_ll, span, "аптека")
    farmacies_with_time = []
    for org in organizations:
        point = org["geometry"]["coordinates"]
        hours = org["properties"]["CompanyMetaData"].get("Hours", None)
        if hours:
            available = hours["Availabilities"][0]
            is_24x7 = available.get("Everyday", False) and available.get("TwentyFourHours", False)
        else:
            is_24x7 = None
        farmacies_with_time.append((point, is_24x7))
    points_param = "pt=" + "~".join([
        "{0},{1},pm2{2}l".format(point[0], point[1], "gn" if is_24x7 else ("lb" if is_24x7 == False else "gr"))
        for point, is_24x7 in farmacies_with_time])
    show_map(map_type="map", add_params=points_param)


if __name__ == "__main__":
    main()
