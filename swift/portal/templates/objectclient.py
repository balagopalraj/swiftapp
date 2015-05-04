import os
import swiftclient

DEFAULT_LOCATION = '/tmp/'

class ObjectClinet(object):
    def __init__(self, user=None, key=None, url=None,
                 tenant_name=None, auth_version='2.0'):
        self.user = user
        self.key = key
        self.url = url
        self.tenant_name = tenant_name
        self.auth_version = auth_version

    def isValidUser(self):
        self.conn = swiftclient.Connection(
                      user=self.user, key=self.key,
                      authurl=self.url,
                      tenant_name=self.tenant_name,
                      auth_version=self.auth_version,
        )
        self.conn.get_account()
        return True
