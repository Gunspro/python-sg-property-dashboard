import re

def transform_block_and_address(data):
    room_number_pattern = re.compile(r'\d+\s*Room\s+HDB\s+in\s+')
    transformed_data = room_number_pattern.sub('', data)
    return transformed_data

def transform_no_of_rooms(data):
    match = re.search(r'HDB \((\d+)\w*\)', data)
    if match:
        transformed_data = match.group(1)
        return transformed_data
    return None
