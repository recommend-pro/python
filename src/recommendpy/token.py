from datetime import datetime, timezone

# from ...models.settings import SystemSettings
from .exceptions import RecommendTokenError

import logging
log = logging.getLogger('recommendpy')


REFRESH_LIFETIME_PERCENT = 50


def get_current_timestamp():
    return datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()


class RecommendAPIToken(object):
    """RecommendAPIToken object."""

    def __init__(self, token=None, expire_at=None, created_at=None):
        self.token = token
        self.expire_at = expire_at

        self.created_at = created_at or get_current_timestamp()

    @property
    def is_expired(self):
        return get_current_timestamp() >= self.expire_at

    @property
    def life_time(self):
        return self.expire_at - self.created_at

    @property
    def refresh_life_time(self):
        return self.life_time * REFRESH_LIFETIME_PERCENT / 100

    @property
    def need_refresh(self):
        return get_current_timestamp() >= (
            self.created_at + self.refresh_life_time
        )

    def set_from_dict(self, data, from_db=False):
        try:
            self.token = data['token']
            expire_at_key = 'expire_at' if from_db else 'expire_date'
            self.expire_at = data[expire_at_key]
            if from_db and data.get('created_at'):
                self.created_at = data['created_at']
        except KeyError as e:
            log.exception(e)
            raise RecommendTokenError('Invalid data')

    def to_dict(self):
        return {
            'token': self.token,
            'expire_at': self.expire_at,
            'created_at': self.created_at,
        }
