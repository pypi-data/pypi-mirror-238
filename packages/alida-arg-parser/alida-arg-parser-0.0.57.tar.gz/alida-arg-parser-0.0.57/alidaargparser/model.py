from .assets_utils import get_asset_properties

class Model:
    def __init__(self, name=None, description=None, format=None):
        self.name = name
        self.description = description
        self.info = get_asset_properties(name)
        self.format=format