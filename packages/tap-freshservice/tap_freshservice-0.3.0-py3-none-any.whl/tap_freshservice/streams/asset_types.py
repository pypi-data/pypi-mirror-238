"""Stream type classes for tap-freshservice."""
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_freshservice.client import FreshserviceStream

class AssetTypesStream(FreshserviceStream):
    name = "asset_types"
    path = "/asset_types"
    records_jsonpath="$.asset_types[*]"

    def get_url(self, context: dict):
        url = super().get_url(context)
        return url
    
    def build_prepared_request(self, *args, **kwargs):
        req = super().build_prepared_request(*args, **kwargs)
        return req

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("parent_asset_type_id", th.IntegerType),
        th.Property("visible", th.BooleanType),
        th.Property("description", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
    ).to_dict()