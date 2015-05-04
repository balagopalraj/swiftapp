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
        try:
            self.conn.get_account()
        except swiftclient.ClientException:
            return False
        return True

    def get_all_containers(self):
        return self.conn.get_account()[1]

    def list_all_container_objects(self, container_name):
        return self.conn.get_container(container_name)[1]

    def download_object(self, container_name, object_name, dest_file=None):
        if not dest_file:
            dest_file = os.path.join(DEFAULT_LOCATION, container_name + '-' + object_name)

        if os.path.exists(dest_file):
            print "Error: Destination file '%(dest_file)s' already exists! \
                   So getting Object '%(object_name)s' from Container '%(container_name)s' failed." \
                   % {'dest_file': dest_file,
                      'object_name': object_name,
                      'container_name': container_name}
            return dest_file

        obj_tuple = self.conn.get_object(container_name, object_name)
        with open(dest_file, 'w') as f:
            f.write(obj_tuple[1])
        return dest_file

    def create_object(self, container_name, file_path, file_name):
        self.conn.put_container(container_name)
        with open(file_path, 'r') as f:
            self.conn.put_object(container_name, file_name,
                                 contents=f.read(),
                                 content_type='text/plain')
