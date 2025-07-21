def is_valid_item(item):
    return item.isdigit() and len(item) <= 12

def is_valid_quantity(qty):
    return qty.isdigit() and 1 <= int(qty) <= 99