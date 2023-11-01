import os
import json
from tests.utils import fixtures_path
from hestia_earth.validation.validators.product import validate_product_yield

fixtures_folder = os.path.join(fixtures_path, 'integration', 'distribution')


def test_validate_product_yield():
    with open(os.path.join(fixtures_folder, 'product-yield-invalid.json')) as f:
        cycle = json.load(f)

    assert validate_product_yield(cycle, cycle.get('site')) == {
        'level': 'warning',
        'dataPath': '.products[0].value',
        'message': 'is outside confidence interval',
        'params': {
            'country': {'@id': 'GADM-GBR', '@type': 'Term'},
            'max': 11862.277598759105,
            'min': 4048.5487693054897,
            'outliers': [1000],
            'term': {'@id': 'wheatGrain', '@type': 'Term', 'termType': 'crop'},
            'threshold': 0.95
        }
    }
