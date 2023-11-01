import sys
import os

def replace_dashes(string):
    key = string.split("=")[0]
    value = string.replace(key, "")
    return "--" + key.replace("-", "_")[2:] + value

# Get specific property related to an asset
def get_asset_property_from_args(asset_name, property=None):
    
    to_find = "--" + asset_name.replace("-", "_")
    if property is not None:
        to_find = to_find + "." + property

    args = sys.argv[1:]

    # Replace all dashes in the mid of a word with underscores
    args = [replace_dashes(arg) for arg in args]
    
    for arg in args:
        if arg.split("=")[0] == to_find:
            return "=".join(arg.split("=")[1:])

def get_asset_property(asset_name, property=None):
    
    if os.getenv('GET_PROPERTIES_FROM_ENV'):
        if str(os.getenv('GET_PROPERTIES_FROM_ENV')).lower()=="true" or str(os.getenv('GET_PROPERTIES_FROM_ENV'))=="1":
            return get_asset_property_from_env(asset_name=asset_name, property=property)
    
    return get_asset_property_from_args(asset_name=asset_name, property=property)


def get_asset_property_from_env(asset_name, property=None):
    prop = None

    to_find = asset_name.replace("-", "_")
    
    if property is not None:
        to_find = to_find + "." + property

    if os.getenv(to_find):
        prop = os.getenv(to_find)
    if prop is None:
        if os.getenv(to_find.upper()):
            prop = os.getenv(to_find.upper())
    return prop

# Get all properties related to an asset
def get_asset_properties(asset_name):
    
    to_find = "--" + asset_name.replace("-", "_")
  
    args = sys.argv[1:]

    # Replace all dashes in the mid of a word with underscores
    args = [replace_dashes(arg) for arg in args]
    
    props = {}

    for arg in args:
        if to_find in arg.split("=")[0]:
            if len(arg.split("=")[0].split("."))>1:
                props[arg.split("=")[0].split(".")[-1]] ="=".join(arg.split("=")[1:])
            else:
                props["main"] ="=".join(arg.split("=")[1:])
    return props