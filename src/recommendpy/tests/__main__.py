import unittest
import os

from recommendpy import RecommendAPI

from .contact.segment import suite as segment_suite
from .contact.list import suite as list_suite


# logging.basicConfig(level=logging.DEBUG)
api = RecommendAPI(
    os.environ.get('RECOMMEND_ACCOUNT_KEY'),
    credential_file_path=os.environ.get('RECOMMEND_CREDENTIAL_PATH')
)
print('*' * 70)
print('\ntesting contact segment')
unittest.TextTestRunner(verbosity=2).run(segment_suite(api))
print('*' * 70)
print('\ntesting contact list')
unittest.TextTestRunner(verbosity=2).run(list_suite(api))
