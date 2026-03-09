import logging
import os

import dlt
from dlt.sources.rest_api import rest_api_resources
from typing import Tuple

from database import DSN

MOCK_SERVER_URL = os.getenv('MOCK_SERVER_URL', 'http://127.0.0.1:5000')

logger = logging.getLogger('pipeline_service')


def run_customer_ingestion() -> Tuple[str, int]:
    pipeline = dlt.pipeline(
        pipeline_name='customer_pipeline',
        dataset_name='customer_dataset',
        destination=dlt.destinations.postgres(credentials=DSN),
    )
    data = rest_api_resources(
        {
            "client": {
                "base_url": f'{MOCK_SERVER_URL}/api',
            },
            "resource_defaults": {
                "write_disposition": "merge",
                "endpoint": {
                    "params": {
                        "page": 1,
                        "limit": 10,
                    },
                },
            },
            "resources": [
                {
                    "name": "customers",
                    "primary_key": "customer_id",
                    "endpoint": {
                        "path": "customers",
                        "data_selector": "data",
                        "paginator": {
                            "type": "page_number",
                            "base_page": 1,
                        }
                    },
                }
            ],
        }
    )
    try:
        pipeline.run(data)
        return "success", pipeline.last_trace.last_normalize_info.row_counts['customers']
    except Exception as e:
        logger.error(f'An error has been occured: {e}')
        return "error", 0
