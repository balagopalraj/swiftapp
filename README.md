Cloud Point (Data Management Portal)

This application is based on OpenStack Swift storage backend. Developed in Django.

Below are the steps to use it:

Admin Tasks (OpenStack Side):
> source openrc

> keystone tenant-create --name Project-1 --description "This is first project."
> keystone tenant-create --name Project-2 --description "This is second project."

> keystone user-create --name emp1 --pass password1 --email emp1@1-cloud.net
> keystone user-create --name emp2 --pass password2 --email emp2@1-cloud.net

> keystone user-create --name emp3 --pass password3 --email emp3@1-cloud.net
> keystone user-create --name emp4 --pass password4 --email emp4@1-cloud.net

> keystone user-role-add --user emp1 --tenant Project-1 --role admin
> keystone user-role-add --user emp2 --tenant Project-1 --role admin

> keystone user-role-add --user emp3 --tenant Project-2 --role admin
> keystone user-role-add --user emp4 --tenant Project-2 --role admin

User side:

> sudo apt-get install python-django python-swiftclient
> git clone https://github.com/RBalaGopal/cloudpoint.git
> cd clouppoint
> OpenStack "cloudpoint/portal/config.py" file and set the SERVER_URL to your OpenStack Environment.
> python manage.py runserver 0.0.0.0:1234
> Go to URL: "http://<your ip>:1234"
> Log with any of below creds:
  emp1, password1, Project-1
  emp2, password2, Project-1
  emp3, password3, Project-2
  emp4, password4, Project-2
  
> Let me know if you face any issues. Thanks.
