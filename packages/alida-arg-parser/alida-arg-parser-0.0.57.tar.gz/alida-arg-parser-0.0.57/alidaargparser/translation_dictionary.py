from .type_utils import str2bool, str2json

translation = {"type":{str:"STRING", int: "INT", float:"DOUBLE", str2bool:"BOOLEAN", str2json:"JSON", None:"ANY"},
                "column_types": {str:"STRING", None:"ANY", int:"NUMBER", float: "NUMBER"}
                }

