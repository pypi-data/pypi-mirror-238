
class LayerHandler:
    def __init__(self, handler, layer_or_file_name=None):
        self.layer_or_file_name = layer_or_file_name
        self.handler = handler
        self.type = handler.handler_type
        self._check_for_multiple_layers()

    def _check_for_multiple_layers(self):
        if self.handler.get_layer_count() > 1 and self.layer_or_file_name is None:
            raise Exception("no layer or file name provided")
        else:
            pass

    def get_dataframe(self):
        return self.handler.get_dataframe(
            self.layer_or_file_name
        )

    def get_feature_count(self):
        return self.handler.get_feature_count(
            self.layer_or_file_name)

    def get_schema(self):
        return self.handler.get_schema(self.layer_or_file_name)

    def get_layer_name(self):
        return self.layer_or_file_name

    def get_extent(self):
        return self.handler.get_extent(self.layer_or_file_name)

    def get_crs_code(self):
        return self.handler.get_crs_code(
            self.layer_or_file_name
        )

    def get_geom_type(self):
        return self.handler.get_geom_type(
            self.layer_or_file_name
        )

    def write_to_postgis_db(self, *args, **kwargs):
        return self.handler.write_to_postgis_db(
            self.layer_or_file_name, *args, **kwargs
        )
