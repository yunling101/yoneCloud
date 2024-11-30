#!/usr/bin/env python
# -*- coding:utf-8 -*-

from webserver.common import api
from webserver.common.views import LoginValidate, BaseView
from django.core.serializers import serialize
from webserver.website.lang.zh_ch import Lang
from webserver.ResourceManage.models import Hosts, Certificate, Network, Group
from webserver.common.permissions import PermissionViewMixin
from webserver.ResourceManage.consuld import CC
from webserver.BusinessManage.models import Business
from webserver.AuthManage.models import Authorize
from webserver.common.utils import SystemConfig, ResourceOption
from webserver.SystemManage.models import Recycle
from webserver.settings import WORKDIR
from webserver.common.files import FileImport
from webserver.ResourceManage.resources import provider
from webserver.ResourceManage.network import network_type


class ResourcesPool(BaseView):
    """
        主机池
    """
    permission_view = "view_hosts"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', Hosts.objects.all().order_by('-id'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            info["content"] = str(e)
        return info


class ResourcesPoolAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑主机
    """
    permission_view = "add_hosts"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            if request_data is not None:
                data = api.Api.json_load(request_data)
                certificate_lists = []
                if data.get("certificate"):
                    for cert in data.get("certificate"):
                        certificate = Certificate.objects.filter(id=int(cert))
                        certificate_lists.extend(certificate)
                if data.get("status") == "0":
                    status = api.Api.json_dump({"time": api.Api.sftime(), "status": "unknown"})
                else:
                    status = api.Api.json_dump({"time": api.Api.sftime(), "status": "success"})
                if data.get("id") == "":
                    hosts = Hosts.objects.filter(ip=data.get("ip"))
                    if len(hosts) == 0:
                        hosts_save = Hosts()
                        hosts_save.sid = int(api.Api.get_sid(8))
                        hosts_save.ip = data.get("ip")
                        hosts_save.hostname = data.get("hostname")
                        hosts_save.instance_id = data.get("hostname")
                        hosts_save.provider = data.get("provider")
                        hosts_save.proxy = True if data.get("proxy") == "1" else False
                        hosts_save.alias = data.get("alias")
                        hosts_save.domain = data.get("domain")
                        hosts_save.status = status
                        hosts_save.comment = data.get("comment")
                        hosts_save.save()
                        try:
                            if data.get("business"):
                                business = Business.objects.filter(id=int(data.get("business")))
                            else:
                                business = Business.objects.filter(id=1)
                        except Exception as e:
                            api.logger.error(str(e))
                            info["msg"] = "业务查找出错，请稍后再试！"
                            return info

                        for cert in certificate_lists:
                            hosts_save.certificate.add(cert)
                        hosts_save.business.add(business[0])
                        hosts_save.save()
                        info["code"] = True
                    else:
                        info["msg"] = "此{0}IP地址已存在！".format(data.get("ip"))
                else:
                    modify_hosts = Hosts.objects.filter(id=int(data.get("id")))
                    modify_hosts.update(
                        ip=data.get("ip"),
                        hostname=data.get("hostname"),
                        provider=data.get("provider"),
                        proxy=True if data.get("proxy") == "1" else False,
                        alias=data.get("alias"),
                        status=status,
                        domain=data.get("domain"),
                        comment=data.get("comment")
                    )
                    business = Business.objects.filter(id=int(data.get("business")))
                    if len(business) == 1 and len(modify_hosts) == 1:
                        modify_hosts[0].business.clear()
                        modify_hosts[0].certificate.clear()

                        for cert in certificate_lists:
                            modify_hosts[0].certificate.add(cert)
                        modify_hosts[0].business.add(business[0])
                        modify_hosts[0].save()
                        info["code"] = True
                    else:
                        info["content"] = "业务查找出错，请稍后再试！"
            else:
                info["msg"] = "参数错误！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class ResourcesPoolMonitor(LoginValidate, PermissionViewMixin, BaseView):
    """
        开启/关闭主机监控
    """
    permission_view = "change_hosts_monitor"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            hosts = Hosts.objects.filter(id=int(request_id))
            if len(hosts) == 1:
                if hosts[0].monitor:
                    try:
                        CC().deregister(str(hosts[0].sid))
                        hosts.update(monitor=False)
                        info["code"] = True
                    except Exception as e:
                        api.logger.error(str(e))
                        info["msg"] = str(e)
                else:
                    business = "default"
                    if hosts[0].business is not None:
                        business = hosts[0].business.get().name
                    try:
                        CC().register(
                            business,
                            str(hosts[0].sid),
                            hosts[0].ip,
                            17000,
                            hosts[0].hostname,
                            business
                        )
                        hosts.update(monitor=True)
                        info["code"] = True
                    except Exception as e:
                        api.logger.error(str(e))
                        info["msg"] = str(e)
            else:
                info["msg"] = "主机查询错误！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class ResourcesPoolDetail(BaseView):
    """
        主机详情
    """
    def get(self, *args, **kwargs):
        info = {"code": False, "msg": ""}
        request_id = int(self.args[0])
        data = serialize('json', Hosts.objects.filter(id=request_id))
        for line in api.Api.json_load(data):
            sd = line["fields"]
            sd["id"] = line["pk"]
            info["msg"] = sd
        info["code"] = True
        return info


class ResourcesPoolDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        删除主机
    """
    permission_view = "delete_hosts"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            hosts_lists = Hosts.objects.none()
            for h in request_id.split(","):
                hosts_lists |= Hosts.objects.filter(id=int(h))

            if SystemConfig.is_recycle():
                data = serialize('json', hosts_lists)
                for hosts in api.Api.json_load(data):
                    sd = hosts["fields"]
                    sd["id"] = hosts["pk"]

                    lists = Recycle.objects.filter(name=sd.get("hostname"))
                    if len(lists) == 0:
                        recycle = Recycle()
                        recycle.name = sd.get("hostname")
                        recycle.ip = sd.get("ip")
                        recycle.type = "hosts"
                        recycle.username = request.user.username
                        recycle.data = api.Api.json_dump(sd)
                        recycle.save()
                    else:
                        info["msg"] = "{0}资源回收站中已存在!".format(sd.get("hostname"))
                        return info
            hosts_lists.delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class ResourcesPoolBatch(LoginValidate, PermissionViewMixin, BaseView):
    """
        批量命令主机列表
    """
    permission_view = "batch_hosts"
    operation_record = False

    def get(self, request, *args, **kwargs):
        info = {"code": False, "msg": "", "results": {}}
        request_super = request.user.is_superuser
        try:
            if request_super:
                hosts = Hosts.objects.all()
                for h in hosts:
                    if h.business.count() != 0:
                        business = h.business.get().name
                    else:
                        business = "默认业务"
                    if info["results"].get(business):
                        info["results"][business]["hosts"].append({
                            "id": h.id,
                            "hostname": h.hostname,
                            "sid": h.sid,
                            "ip": h.ip,
                            "proxy": True if h.proxy else False
                        })
                    else:
                        info["results"][business] = {"hosts": [{
                            "id": h.id,
                            "hostname": h.hostname,
                            "sid": h.sid,
                            "ip": h.ip,
                            "proxy": True if h.proxy else False
                        }]}
                info["code"] = True
            else:
                auth = Authorize.objects.filter(user=request.user.id)
                if len(auth) == 1:
                    for b in auth[0].business.all():
                        if not info["results"].get(b.name):
                            info["results"][b.name] = {"hosts": []}
                        hosts = Hosts.objects.filter(business=b.id)
                        for h in hosts:
                            info["results"][b.name]["hosts"].append({
                                "id": h.id,
                                "hostname": h.hostname,
                                "sid": h.sid,
                                "ip": h.ip,
                                "proxy": True if h.proxy else False
                            })

                    for h in auth[0].hosts.all():
                        if h.business.count() == 1:
                            business = h.business.get().name
                        else:
                            business = "默认业务"
                        if info["results"].get(business):
                            info["results"][business]["hosts"].append({
                                "id": h.id,
                                "hostname": h.hostname,
                                "sid": h.sid,
                                "ip": h.ip,
                                "proxy": True if h.proxy else False
                            })
                        else:
                            info["results"][business] = {"hosts": [{
                                "id": h.id,
                                "hostname": h.hostname,
                                "sid": h.sid,
                                "ip": h.ip,
                                "proxy": True if h.proxy else False
                            }]}
                    info["code"] = True
                else:
                    info["msg"] = "权限拒绝，请联系管理员！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class ResourcesHostsGroupAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        资产分组添加
    """
    permission_view = "add_asset_group"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            if request_data is not None:
                data = api.Api.json_load(request_data)
                hosts = []
                if data.get("select_hosts"):
                    if isinstance(data.get("select_hosts"), str):
                        asset = Hosts.objects.filter(id=int(data.get("select_hosts")))
                        for h in asset:
                            hosts.append(h)
                    elif isinstance(data.get("select_hosts"), list):
                        for ids in data.get("select_hosts"):
                            asset = Hosts.objects.filter(id=int(ids))
                            for h in asset:
                                if h not in hosts:
                                    hosts.append(h)
                if data.get("id") == "":
                    asset_group = Group.objects.filter(name=data.get("name"))
                    if len(asset_group) == 0:
                        asset_group = Group()
                        asset_group.name = data.get("name")
                        asset_group.comment = data.get("comment")
                        asset_group.save()

                        for h in hosts:
                            asset_group.hosts.add(h)
                        asset_group.save()
                        info["code"] = True
                    else:
                        info["msg"] = data.get("name") + " 分组名称已存在！"
                else:
                    asset_group = Group.objects.filter(id=int(data.get("id")))
                    asset_group.update(
                        name=data.get("name"),
                        comment=data.get("comment")
                    )
                    if len(asset_group) == 1:
                        asset_group[0].hosts.clear()
                        for h in hosts:
                            asset_group[0].hosts.add(h)
                        asset_group[0].save()
                        info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class ResourcesHostsGroupDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        资产分组删除
    """
    permission_view = "delete_asset_group"

    def post(self, request, *args, **kwargs):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            if request_id is not None:
                Group.objects.filter(id=int(request_id)).delete()
                info["code"] = True
            else:
                info["msg"] = "未知的错误！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class ResourcesCertificateLists(LoginValidate, PermissionViewMixin, BaseView):
    """
        主机凭证列表
    """
    permission_view = "view_certificate"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', Certificate.objects.all().order_by('-id'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            info["msg"] = str(e)
        return info


class ResourcesCertificateAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑主机凭证
    """
    permission_view = "add_hosts_certificate"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            if request_data is not None:
                data = api.Api.json_load(request_data)
                if data.get("id") == "":
                    hosts = Certificate.objects.filter(name=data.get("name"))
                    if len(hosts) == 0:
                        certificate = Certificate()
                        certificate.name = data.get("name")
                        certificate.ssh_type = data.get("ssh_type")
                        certificate.ssh_port = int(data.get("ssh_port"))
                        certificate.ssh_user = data.get("ssh_user")
                        if data.get("ssh_type") == "KEY":
                            if data.get("ssh_key"):
                                certificate.ssh_key = data.get("ssh_key")
                            else:
                                info["msg"] = "SSH KEY不能为空！"
                                return info
                        else:
                            certificate.ssh_password = data.get("ssh_password")
                        certificate.save()
                        info["code"] = True
                    else:
                        info["msg"] = "此{0}凭证名称已存在！".format(data.get("name"))
                else:
                    ssh_password, ssh_key = "", ""
                    if data.get("ssh_type") == "KEY":
                        if data.get("ssh_key"):
                            ssh_key = data.get("ssh_key")
                        else:
                            info["msg"] = "SSH KEY不能为空！"
                            return info
                    else:
                        ssh_password = data.get("ssh_password")
                    Certificate.objects.filter(id=int(data.get("id"))).update(
                        name=data.get("name"),
                        ssh_type=data.get("ssh_type"),
                        ssh_port=int(data.get("ssh_port")),
                        ssh_user=data.get("ssh_user"),
                        ssh_key=ssh_key,
                        ssh_password=ssh_password
                    )
                    info["code"] = True
            else:
                info["msg"] = "参数错误！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class ResourcesCertificateDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        删除主机凭证
    """
    permission_view = "delete_hosts_certificate"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            Certificate.objects.filter(id=int(request_id)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class ResourcesNetworkAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑网络设备
    """
    permission_view = "add_network"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            if request_data is not None:
                data = api.Api.json_load(request_data)
                if data.get("id") == "":
                    name = Network.objects.filter(name=data.get("name"))
                    if len(name) == 0:
                        network = Network()
                        network.name = data.get("name")
                        network.address = data.get("address")
                        network.network_model = data.get("network_model")
                        network.equipment = data.get("equipment")
                        network.region = data.get("region")
                        network.network_type = data.get("network_type")
                        network.monitoring_status = True if data.get("monitoring_status") == "1" else False
                        network.other_info = data.get("comment")
                        network.save()
                        info["code"] = True
                    else:
                        info["msg"] = "此{0}设备名称已存在！".format(data.get("name"))
                else:
                    Network.objects.filter(id=int(data.get("id"))).update(
                        name=data.get("name"),
                        address=data.get("address"),
                        network_model=data.get("network_model"),
                        equipment=data.get("equipment"),
                        network_type=data.get("network_type"),
                        monitoring_status=True if data.get("monitoring_status") == "1" else False,
                        region=data.get("region"),
                        other_info=data.get("comment")
                    )
                    info["code"] = True
            else:
                info["msg"] = "参数错误！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class ResourcesNetworkDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        删除网络设备
    """
    permission_view = "delete_network"

    def post(self, request, *args, **kwargs):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            if request_id is not None:
                Network.objects.filter(id=int(request_id)).delete()
            else:
                info["msg"] = "未知的参数错误！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class ResourcesNetworkMonitor(LoginValidate, PermissionViewMixin, BaseView):
    """
        开启/关闭网络设备监控
    """
    permission_view = "change_network_monitor"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            network = Network.objects.filter(id=int(request_id))
            if len(network) == 1:
                if network[0].monitoring_status:
                    CC().deregister(str(network[0].id))
                    network.update(monitoring_status=False)
                else:
                    if network[0].address is None or network[0].address == "":
                        info["msg"] = "管理地址不能为空!"
                        return info
                    CC().network(
                        "network",
                        str(network[0].id),
                        network[0].address
                    )
                    network.update(monitoring_status=True)
                info["code"] = True
            else:
                info["msg"] = "网络设备查询错误！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class ResourcesPoolUpload(BaseView):
    """
        主机池资源导入
    """
    # permission_view = "upload_hosts"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_files = request.FILES.get("data", None)
        try:
            if request_files is not None:
                storage_path = "public/storage/"
                storage_dir = "{0}/{1}".format(WORKDIR, storage_path)

                if not api.Api.path_exists(storage_dir):
                    api.Api.mkdir_p(storage_dir)

                filename = "{0}hosts_import_{1}.xlsx".format(storage_dir, api.Api.sftime(format="%Y%m%d%H%M%S"))
                with open(filename, "wb+") as f:
                    for chunk in request_files.chunks():
                        f.write(chunk)
                    f.close()

                success, fail = 0, 0
                for line in FileImport(filename).read_file():
                    if line.get("code"):
                        add = ResourceOption.add_hosts(line.get("data"))
                        if add.get("code"):
                            success += 1
                        else:
                            fail += 1
                    else:
                        fail += 1

                info["code"] = True
                info["msg"] = "成功: {0} 失败: {1} 共计: {2}".format(success, fail, success + fail)
            else:
                info["msg"] = "读取文件错误, 请稍后再试！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class ResourcesProvider(BaseView):
    """
        资源提供商
    """
    def get(self, request):
        info = {"code": False, "msg": ""}
        request_item = request.GET.get("item", None)
        try:
            if request_item is not None:
                if provider.get(request_item):
                    info["data"] = provider.get(request_item)
                else:
                    info["data"] = provider
            else:
                info["data"] = provider
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class ResourcesNetworkType(BaseView):
    """
        网络设备类型
    """
    def get(self, request):
        info = {"code": False, "msg": ""}
        try:
            info["data"] = network_type
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info
