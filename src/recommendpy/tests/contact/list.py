from ..base import BaseTestCase, get_identifier, get_suite

# from recommendpy.exceptions import RecommendAPIError


class ContactListTestCase(BaseTestCase):
    def setUp(self):
        self._id = get_identifier()
        self.data = self.api_namespace._test_data
        self.api_namespace.create(self._id, self.data)

    def runTest(self):  # NOQA
        """attach, detach by email and search."""
        test_emails = ['test@recommend.pro']
        # attach
        self.assertEqual(
            self.api_namespace.attach(
                identifier=self._id, emails=test_emails
            ),
            True
        )
        # response = self.api_namespace.search(
        #     self._id, field='email', identifiers=test_emails
        # )
        # self.assertEqual(response.get('data'), test_emails)

        # detach
        self.assertEqual(
            self.api_namespace.detach(
                identifier=self._id, emails=test_emails
            ),
            True
        )
        # response = self.api_namespace.search(
        #     self._id, field='email', identifiers=test_emails
        # )
        # self.assertEqual(response.get('data'), [])

    def tearDown(self):
        self.api_namespace.delete(self._id)


def suite(api):
    namespace = api.contact.list
    suite = get_suite(namespace)
    suite.addTest(ContactListTestCase(namespace))
    return suite
