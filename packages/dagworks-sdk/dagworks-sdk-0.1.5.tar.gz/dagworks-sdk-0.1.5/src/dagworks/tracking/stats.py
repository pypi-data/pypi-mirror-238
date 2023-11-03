# Copyright (C) 2023-Present DAGWorks Inc.
#
# For full terms email support@dagworks.io.
#
# This software and associated documentation files (the "Software") may only be
# used in production, if you (and any entity that you represent) have agreed to,
# and are in compliance with, the DAGWorks Enterprise Terms of Service, available
# via email (support@dagworks.io) (the "Enterprise Terms"), or other
# agreement governing the use of the Software, as agreed by you and DAGWorks,
# and otherwise have a valid DAGWorks Enterprise license for the
# correct number of seats and usage volume.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from functools import singledispatch
import json
from typing import Dict, Any

import pandas as pd

from dagworks.tracking import sql_utils


@singledispatch
def compute_stats(result, node_name: str, node_tags: dict) -> Dict[str, Any]:
    """This is the default implementation for computing stats on a result.

    All other implementations should be registered with the `@compute_stats.register` decorator.

    :param result:
    :param node_name:
    :param node_tags:
    :return:
    """
    return {
        "observability_type": "unsupported",
        "observability_value": {
            "unsupported_type": str(type(result)),
            "action": "reach out to the DAGWorks team to add support for this type.",
        },
        "observability_schema_version": "0.0.1",
    }


@compute_stats.register(str)
@compute_stats.register(int)
@compute_stats.register(float)
@compute_stats.register(bool)
def compute_stats_primitives(result, node_name: str, node_tags: dict) -> Dict[str, Any]:
    return {
        "observability_type": "primitive",
        "observability_value": {
            "type": str(type(result)),
            "value": result,
        },
        "observability_schema_version": "0.0.1",
    }


@compute_stats.register(dict)
def compute_stats_dict(result: dict, node_name: str, node_tags: dict) -> Dict[str, Any]:
    try:
        # if it's JSON serializable, take it.
        d = json.dumps(result)
        result_values = json.loads(d)
    except Exception:
        # else just string it -- max 1000 chars.
        result_values = str(result)
        if len(result_values) > 1000:
            result_values = result_values[:1000] + "..."

    return {
        "observability_type": "dict",
        "observability_value": {
            "type": str(type(result)),
            "value": result_values,
        },
        "observability_schema_version": "0.0.2",
    }


@compute_stats.register(tuple)
def compute_stats_tuple(result: tuple, node_name: str, node_tags: dict) -> Dict[str, Any]:
    if "hamilton.data_loader" in node_tags and node_tags["hamilton.data_loader"] is True:
        # assumption it's a tuple
        if isinstance(result[1], dict):
            try:
                # double check that it's JSON serializable
                raw_data = json.dumps(result[1])
                _metadata = json.loads(raw_data)
            except Exception:
                _metadata = str(result[1])
                if len(_metadata) > 1000:
                    _metadata = _metadata[:1000] + "..."
            else:
                # enrich it
                if (
                    "SQL_QUERY" in _metadata
                ):  # we might need to think how to make this a constant...
                    _metadata["QUERIED_TABLES"] = sql_utils.parse_sql_query(_metadata["SQL_QUERY"])
                    if isinstance(result[0], pd.DataFrame):
                        # TODO: move this to dataframe stats collection
                        _memory = result[0].memory_usage(deep=True)
                        _metadata["DF_MEMORY_TOTAL"] = int(_memory.sum())
                        _metadata["DF_MEMORY_BREAKDOWN"] = _memory.to_dict()
            return {
                "observability_type": "dict",
                "observability_value": {
                    "type": str(type(result[1])),
                    "value": _metadata,
                },
                "observability_schema_version": "0.0.2",
            }
    return {
        "observability_type": "unsupported",
        "observability_value": {
            "unsupported_type": str(type(result)),
            "action": "reach out to the DAGWorks team to add support for this type.",
        },
        "observability_schema_version": "0.0.1",
    }
