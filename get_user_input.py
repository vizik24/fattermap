# get_user_input.py

def get_user_input():
    lat = float(input("Enter latitude: "))
    lon = float(input("Enter longitude: "))
    group_size = int(input("Enter group size: "))
    return lat, lon, group_size
