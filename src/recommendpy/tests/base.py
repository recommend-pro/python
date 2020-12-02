from datetime import datetime

import unittest

from recommendpy.exceptions import RecommendNotFoundError, RecommendAPIError


def get_identifier():
    return 'test-{}'.format(datetime.utcnow().timestamp())


class BaseTestCase(unittest.TestCase):
    def __init__(self, namespace, *args, **kwargs):
        self.api_namespace = namespace
        super().__init__(*args, **kwargs)


class BaseListReadTestCase(BaseTestCase):
    def runTest(self):  # NOQA
        """Get list of items."""
        self.assertIsInstance(self.api_namespace(), list)


class BaseReadTestCase(BaseTestCase):
    def runTest(self):  # NOQA
        """Get item that doesn't exist."""
        with self.assertRaises(RecommendNotFoundError):
            self.api_namespace(get_identifier())


class BaseCreateTestCase(BaseTestCase):
    def setUp(self):
        self._id = get_identifier()
        self.data = self.api_namespace._test_data

    def runTest(self):  # NOQA
        """Create item."""
        self.assertEqual(self.api_namespace.create(self._id, self.data), True)

    def tearDown(self):
        self.api_namespace.delete(self._id)


class BaseEntityItemTestCase(BaseTestCase):
    def setUp(self):
        self._id = get_identifier()
        self.data = self.api_namespace._test_data
        self.api_namespace.create(self._id, self.data)

    def test_get_item(self):
        """Get item."""
        self.assertIsInstance(self.api_namespace(self._id), dict)

    def test_create_diplicated_item(self):
        """Create item with identifier that already exists."""
        with self.assertRaises(RecommendAPIError):
            self.api_namespace.create(self._id, self.data)

    def test_update_item(self):
        """Update item."""
        data = self.data
        if hasattr(self.api_namespace, '_test_update_data'):
            data = self.api_namespace._test_update_data
        self.api_namespace.update(self._id, data)

    def tearDown(self):
        self.api_namespace.delete(self._id)


def get_suite(namespace):
    suite = unittest.TestSuite()

    if getattr(namespace, 'list'):
        suite.addTest(BaseListReadTestCase(namespace))

    if getattr(namespace, 'get'):
        suite.addTest(BaseReadTestCase(namespace))
        suite.addTest(BaseEntityItemTestCase(namespace, 'test_get_item'))

    if getattr(namespace, 'create'):
        suite.addTest(BaseCreateTestCase(namespace))

        suite.addTest(
            BaseEntityItemTestCase(namespace, 'test_create_diplicated_item')
        )
    if getattr(namespace, 'update'):
        suite.addTest(BaseEntityItemTestCase(namespace, 'test_update_item'))

    return suite
