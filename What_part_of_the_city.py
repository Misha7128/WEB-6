from geocoder import get_coordinates, get_nearest_object

import sys


def main():
    address = ''
    try:
        address = " ".join(sys.argv[1:])
    except:
        print('No data')
        exit(1)

    if not address:
        print('No data')
        exit(1)
    address_point = get_coordinates(address)
    district_name = get_nearest_object(address_point, "district")
    print(district_name)


if __name__ == "__main__":
    main()
