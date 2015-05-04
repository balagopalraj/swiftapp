from django.template.loader import get_template
from django.template import Context
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, render_to_response
from django.core.servers.basehttp import FileWrapper
from django.views.static import serve


import config
import objectclient
import os

# Create your views here.

PORTAL_TEMPLATE_DIR = "portal/templates"

obj_cli = None
user = None

@csrf_protect
def portal_page(request, page):
    template_page = PORTAL_TEMPLATE_DIR + "/" + page.lower() + ".html"
    data = {}
    data["page"] = page

    if page == "Login":
        data["projects"] = config.PROJECTS
    if page == "Logout":
        template_page = PORTAL_TEMPLATE_DIR + "/home.html"

    return render(request, template_page, data)

@csrf_protect
def log_me_in(request):
    global obj_cli
    global user
    user = request.POST['user']
    password = request.POST['password']
    tenant = request.POST['project']

    obj_cli = objectclient.ObjectClinet(user, password,
                                        config.SERVER_URL,
                                        tenant)
    if not obj_cli.isValidUser():
        template_page = PORTAL_TEMPLATE_DIR + "/login.html"
        t = get_template(template_page)
        data = {}
        data["page"] = "Login"
        data["projects"] = config.PROJECTS
        data["isInValidUser"] = True

        return render(request, template_page, data)

    containers = obj_cli.get_all_containers()

    containers_page = PORTAL_TEMPLATE_DIR + "/containers.html"
    return render(request, containers_page, {'folders': containers, 'user': user})

def show_files(request, container_name):
    global obj_cli
    files = obj_cli.list_all_container_objects(container_name)
    files_page = PORTAL_TEMPLATE_DIR + "/files.html"
    return render(request, files_page, {'files': files, 'folder': container_name})

def download_file(request, container, object_name):
    global obj_cli

    file_path = obj_cli.download_object(container, object_name)
    f = open(file_path, 'r')

    response = HttpResponse(f.read())
    response["Content-Disposition"]= "attachment; filename=%s" % (object_name)
    return response 

def upload_file(request):
    global obj_cli

    #if (not obj_cli) or (obj_cli and not obj_cli.isValidUser()):
    #    template_page = PORTAL_TEMPLATE_DIR + "/login.html"
    #    t = get_template(template_page)
    #    data = {}
    #    data["page"] = "Login"
    #    data["projects"] = config.PROJECTS
    #    data["isInValidUser"] = False

    #    return render(request, template_page, data)

    upload_page = PORTAL_TEMPLATE_DIR + "/upload.html"

    return render(request, upload_page)
    return HttpResponse("Upload")

def do_upload(request):
    global obj_cli

    global user
    file_name = request.POST['file_name']
    container = request.POST['folder_name']
    file_path = request.POST['file_path']
    obj_cli.create_object(container, file_path, file_name)
    
    containers = obj_cli.get_all_containers()

    containers_page = PORTAL_TEMPLATE_DIR + "/containers.html"
    return render(request, containers_page, {'folders': containers, 'user': user})
