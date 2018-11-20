from django.db import models
from .util import _create_ns, _get_ns_name
import logging

logger = logging.getLogger(__name__)
MAX_NAME_LENGTH = 50
class Project(models.Model):
    user = models.CharField(max_length=MAX_NAME_LENGTH)
    # project name
    name = models.CharField(max_length=MAX_NAME_LENGTH)

    @classmethod
    def create(cls, user, name):
        try:
            project = Project.objects.get(user=user, name=name)
        except Project.DoesNotExist:
            project = Project(user=user, name=name)

            # save to db
            project.save()

            # create project ns
            project.create_ns()

        return project

    def delete(self):
        for subnet in self.subnet_set.all():
            for vm in subnet.vm_set.all():
                vm.delete()
        self.delete_ns()

    def info(self):
        res = {
                "user": self.user,
                "name": self.name,
                "vms": []
        }
        for subnet in self.subnet_set.all():
            for vm in subnet.vm_set.all():
                vm_info = vm.info()
                res["vms"].append(vm_info)
        return res

    def __str__(self):
        return "id: " + str(self.pk) + ", user: " + self.user + ", name: " + self.name 

    def create_ns(self):
        ns_name = self.get_ns_name()
        _create_ns(ns_name)

    def delete_ns(self):
        ns_name = self.get_ns_name()
        _remove_ns(ns_name)

    def get_ns_name(self):
        return _get_ns_name(self.user, self.name, self.pk)

    @classmethod
    def listall(cls): 
        res =[str(item) for item in Project.objects.all()]
        # logger.info(res)
        return res

    def get_id(self):
        return self.pk