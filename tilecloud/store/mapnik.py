import json

import mapnik

from tilecloud import TileStore



class MapnikTileStore(TileStore):

    def __init__(self, mapfile, **kwargs):
        TileStore.__init__(self, **kwargs)
        self.map = mapnik.Map(0, 0)
        mapnik.load_map(self.map, mapfile)

    def prepare_map(self, tile):
        # fixme: tile size
        tilesize = (256, 256)
        # fixme: tile coord in geo (mapfile) unit
        bounds = (-180.0, -90.0, 180.0, 90.0)

        self.map.width, self.map.height = tilesize
        self.map.zoom_to_box(mapnik.Box2d(*bounds))

    def get_one(self, tile):
        self.prepare_map(tile)
        image = mapnik.Image(self.map.width, self.map.height)
        mapnik.render(self.map, image)
        # fixme: content_type
        tile.data = image.tostring('png')


class UTFGridTileStore(MapnikTileStore):

    def __init__(self, mapfile, layer_idx=0, fields=None, **kwargs):
        MapnikTileStore.__init__(self, mapfile, **kwargs)
        self.layer_idx = layer_idx
        self.fields = fields

    def get_one(self, tile):
        self.prepare_map(tile)
        grid = mapnik.Grid(self.map.width, self.map.height)
        mapnik.render_layer(self.map, grid, layer=self.layer_idx, fields=self.fields)
        # fixme: content_type
        tile.data = json.encode(grid.encode())
