import re
import datetime
from difflib import SequenceMatcher

def transform_timestamp(data):
    return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

def transform_price(all_data, blk_address, price, num_of_rooms):
    prices = []
    similar_properties = [p for p in all_data if blk_address in p.block_and_address]
    prices = [int(p.price) if p.price != "Make an offer" else 0 for p in similar_properties if p.price]    
    if prices:
        if 0 in prices:
            prices = [p for p in prices if p != 0]
        return (sum(prices) / len(prices))
    else:
        similar_rooms = [p for p in all_data if num_of_rooms == p.number_of_rooms]
        prices = [int(p.price) for p in similar_rooms if p.price]
        return (sum(prices) / len(prices))

def transform_block_and_address(data):
    room_number_pattern = re.compile(r'\d+\s*Room\s+HDB\s+in\s+')
    transformed_data = room_number_pattern.sub('', data)
    return transformed_data

def transform_no_of_rooms(data):
    match = re.search(r'HDB \((\d+)\w*\)', data)
    if match:
        transformed_data = match.group(1)
        return transformed_data
    return 5

def transform_yearbuilt(data):
    year = datetime.date.today().year
    build_age = int(year) - int(data)
    return build_age

def assign_location(data):
    areas = {
    "Central": [
        "Bukit Merah", "Bukit Timah", "Downtown Core", "Geylang", "Kallang",
        "Marina East", "Marina South", "Marine Parade", "Museum", "Newton",
        "Novena", "Orchard", "Outram", "Queenstown", "River Valley", 
        "Rochor", "Singapore River", "Straits View", "Tanglin", "Toa Payoh", "Telok Blangah",
        "Queenstown", "Commonwealth", "Limau"
    ],
    
    "East": [
        "Bedok", "Changi", "Changi Bay", "Pasir Ris", "Paya Lebar", "Tampines"
    ],
    
    "North": [
        "Admiralty", "Kranji", "Marsiling", "Sembawang", "Woodlands", "Yishun", "Canberra",     
        "Ang Mo Kio", "Hougang", "North-Eastern Islands", "Punggol",
        "Seletar", "Sengkang", "Serangoon"
    ],
    
    "West": [
        "Boon Lay", "Bukit Batok", "Bukit Panjang", "Choa Chu Kang",
        "Clementi", "Jurong East", "Jurong West", "Pioneer", "Tengah",
        "Tuas", "Western Islands", "Western Water Catchment", "Jurong East", "Jurong West",
        "Clementi", "Choa Chu Kang"
    ]
    }

    for key, val in areas.items():
        for planning_area in val:
            if planning_area in data:
                return key
    return "Not found"
    