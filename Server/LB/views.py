from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models.project import Project
from .models.subnet import Subnet
from .models.vm import VM
import chardet

# Create your views here.
@csrf_exempt
def project(request):
    input = json.loads(request.body.decode(chardet.detect(request.body)["encoding"]))

    status = "failure"
    action = input["action"]
    type = input["type"]
    res = {
        "status": status,
        "action": action,
        "type": type,
        "info": {}
    }

    if(input["action"] == "create"):
        print("project create...")
        project = Project.create(input['user'], input['info']['name'])
        res["status"] = "successful"
        res["info"] = project.info()

    if(input["action"] == "info"):
        print("project info...")
        project = Project.getby(input['user'], input['info']['name'])
        if project is None:
            res["info"] = "can not fint project"
        else:
            res["status"] = "successful"
            res["info"] = project.info()

    if(input["action"] == "update"):
        print("project update...")
        status = "successful"

    if(input["action"] == "delete"):
        print("project delete...")
        project = Project.getby(input['user'], input['info']['name'])
        project.removeproj()
        status = "successful"


    if(input["action"] == "list"):
        res["info"] = Project.listall()
        status = "successful"
    
    return HttpResponse(json.dumps(res))

@csrf_exempt
def instance(request):
    input = json.loads(request.body.decode(chardet.detect(request.body)["encoding"]))

    status = "successful"
    action = input["action"]
    type = input["type"]
    res = {
        "status": status,
        "action": action,
        "type": type,
        "info": {}
    }

    if(input["action"] == "create"):
        print("instance create...")
        # user, proj_name, subnet_ip, backends, healthcheck
        instance = VM.create(input["user"], input["project"], input["info"]["subnet"], 
            input["info"]["backend"]["entities"], 
            input["info"]["backend"]["health-check"]["up"],
            input["info"]["backend"]["health-check"]["interval"],
            input["info"]["backend"]["health-check"]["timeout"],
            input["info"]["backend"]["health-check"]["threshold"]
            )
        res["info"] = instance.info()

    if (input["action"] == "info"):
        print("instance info...")
        try:
            ins = VM.objects.get(pk=input["id"])
            res["info"] = ins.info()
        except VM.DoesNotExist:
            res["type"] = "failure"
            res["info"] = "can not find instance"
    # if(input["action"] == "update"):
    #     print("instance update...")

    if(input["action"] == "delete"):
        print("instance delete...")
        try:
            ins = VM.objects.get(pk=input["id"])
            ins.removeins()
        except VM.DoesNotExist:
            res["type"]="failure"
            res["info"]= "can not find instance"
    
    return HttpResponse(json.dumps(res))

