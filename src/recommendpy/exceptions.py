import json


class RecommendAPIError(Exception):

    def __init__(self, message=None, response=None):
        Exception.__init__(self, response.status_code if response else 0)
        self.response = response
        self.message = message
        self.error_code = None

        if self.response:
            try:
                data = response.json()
            except json.JSONDecodeError:
                data = None

            if data:
                if not self.message and data.get('error_message'):
                    self.message = data['error_message']
                if data.get('error_code'):
                    self.error_code = data['error_code']

    def __str__(self):
        if self.response:
            return '{} {}'.format(
                self.error_code or self.response.status_code,
                self.message or ''
            )
        return self.message or ''

    # python2
    def __unicode__(self):
        if self.response:
            return u'{} {}'.format(
                self.self.error_code or self.response.status_code,
                self.message or ''
            )
        return self.message or ''


class RecommendTokenError(RecommendAPIError):
    pass


class RecommendAuthenticationError(RecommendAPIError):
    pass


class RecommendUnauthorizedError(RecommendAPIError):
    pass


class RecommendNotFoundError(RecommendAPIError):
    pass


class RecommendBatchError(object):
    def __init__(self, error_type=None, identifier=None, message=None, code=None):
        self.type = error_type
        self.identifier = identifier
        self.message = message
        self.code = code


class RecommendBatchErrorList(RecommendAPIError):
    def errors(self):
        data = self.response.json()
        errors = []
        for error_data in data['batch_error_list']:
            errors.append(RecommendBatchError(error_data))
        return errors
