import paramiko

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from NB_CMDB.views import loginValid, getConnection
from User.forms import RegisterForm
from Equipment.models import Equipment

# Create your views here
eq_list = [{'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'macOS Sierra', 'mac': '00:0c:29:cd:9b:e4', 'cpu_count': 4, 'memory': 'SAMSUNG DDR4 2400T DDR3 32G', 'ip': '192.168.1.2', 'hostname': 'local_2', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'OS X Yosemite', 'mac': '00:0c:29:cd:4b:e6', 'cpu_count': 4, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.3', 'hostname': 'local_3', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'OS X Yosemite', 'mac': '00:0c:29:cd:4b:e2', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 8G', 'ip': '192.168.1.4', 'hostname': 'local_4', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 600GB SAS 10K 2.5', 'sys_version': 'win8', 'mac': '00:0c:24:cd:7b:e5', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.5', 'hostname': 'local_5', 'sys_type': 'Windows'}, {'disk': 'SEAGATE 600GB SAS 10K 2.5', 'sys_version': 'CentOS ', 'mac': '00:0c:23:cd:6b:e6', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.6', 'hostname': 'local_6', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'win8', 'mac': '00:0c:25:cd:3b:e1', 'cpu_count': 3, 'memory': 'SAMSUNG DDR4 2400T DDR3 16G', 'ip': '192.168.1.7', 'hostname': 'local_7', 'sys_type': 'Windows'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'win2000', 'mac': '00:0c:23:cd:9b:e6', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.8', 'hostname': 'local_8', 'sys_type': 'Windows'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'Fedora', 'mac': '00:0c:25:cd:9b:e8', 'cpu_count': 4, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.9', 'hostname': 'local_9', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 600GB SAS 10K 2.5', 'sys_version': 'OS X Yosemite', 'mac': '00:0c:22:cd:5b:e8', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 16G', 'ip': '192.168.1.10', 'hostname': 'local_10', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'win2000', 'mac': '00:0c:22:cd:1b:e9', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 16G', 'ip': '192.168.1.11', 'hostname': 'local_11', 'sys_type': 'Windows'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'CentOS ', 'mac': '00:0c:27:cd:8b:e3', 'cpu_count': 4, 'memory': 'SAMSUNG DDR4 2400T DDR3 32G', 'ip': '192.168.1.12', 'hostname': 'local_12', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'win95', 'mac': '00:0c:25:cd:5b:e9', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.13', 'hostname': 'local_13', 'sys_type': 'Windows'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'OpenSUSE', 'mac': '00:0c:24:cd:6b:e1', 'cpu_count': 2, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.14', 'hostname': 'local_14', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 600GB SAS 10K 2.5', 'sys_version': 'macOS Sierra', 'mac': '00:0c:28:cd:2b:e8', 'cpu_count': 2, 'memory': 'SAMSUNG DDR4 2400T DDR3 8G', 'ip': '192.168.1.15', 'hostname': 'local_15', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'Ubuntu', 'mac': '00:0c:23:cd:6b:e2', 'cpu_count': 2, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.16', 'hostname': 'local_16', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'CentOS ', 'mac': '00:0c:28:cd:9b:e5', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.17', 'hostname': 'local_17', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'Fedora', 'mac': '00:0c:29:cd:7b:e5', 'cpu_count': 3, 'memory': 'SAMSUNG DDR4 2400T DDR3 8G', 'ip': '192.168.1.18', 'hostname': 'local_18', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 600GB SAS 10K 2.5', 'sys_version': 'Ubuntu', 'mac': '00:0c:22:cd:9b:e8', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 8G', 'ip': '192.168.1.19', 'hostname': 'local_19', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'Linux ', 'mac': '00:0c:24:cd:9b:e8', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 16G', 'ip': '192.168.1.20', 'hostname': 'local_20', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'RHEL', 'mac': '00:0c:27:cd:2b:e9', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 32G', 'ip': '192.168.1.21', 'hostname': 'local_21', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 600GB SAS 10K 2.5', 'sys_version': 'win10', 'mac': '00:0c:21:cd:8b:e5', 'cpu_count': 2, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.22', 'hostname': 'local_22', 'sys_type': 'Windows'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'OS X Yosemite', 'mac': '00:0c:28:cd:7b:e2', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 32G', 'ip': '192.168.1.23', 'hostname': 'local_23', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'win8', 'mac': '00:0c:23:cd:7b:e8', 'cpu_count': 2, 'memory': 'SAMSUNG DDR4 2400T DDR3 16G', 'ip': '192.168.1.24', 'hostname': 'local_24', 'sys_type': 'Windows'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'RHEL', 'mac': '00:0c:25:cd:8b:e2', 'cpu_count': 4, 'memory': 'SAMSUNG DDR4 2400T DDR3 8G', 'ip': '192.168.1.25', 'hostname': 'local_25', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'OS X Yosemite', 'mac': '00:0c:24:cd:6b:e5', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 32G', 'ip': '192.168.1.26', 'hostname': 'local_26', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 600GB SAS 10K 2.5', 'sys_version': 'OS X Mountain Lion', 'mac': '00:0c:29:cd:4b:e3', 'cpu_count': 4, 'memory': 'SAMSUNG DDR4 2400T DDR3 32G', 'ip': '192.168.1.27', 'hostname': 'local_27', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'OS X Mavericks', 'mac': '00:0c:27:cd:1b:e8', 'cpu_count': 4, 'memory': 'SAMSUNG DDR4 2400T DDR3 8G', 'ip': '192.168.1.28', 'hostname': 'local_28', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 600GB SAS 10K 2.5', 'sys_version': 'win7', 'mac': '00:0c:24:cd:3b:e1', 'cpu_count': 2, 'memory': 'SAMSUNG DDR4 2400T DDR3 8G', 'ip': '192.168.1.29', 'hostname': 'local_29', 'sys_type': 'Windows'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'macOS Sierra', 'mac': '00:0c:23:cd:3b:e5', 'cpu_count': 3, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.30', 'hostname': 'local_30', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 600GB SAS 10K 2.5', 'sys_version': 'Linux ', 'mac': '00:0c:21:cd:1b:e5', 'cpu_count': 3, 'memory': 'SAMSUNG DDR4 2400T DDR3 8G', 'ip': '192.168.1.31', 'hostname': 'local_31', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'OS X Yosemite', 'mac': '00:0c:22:cd:3b:e8', 'cpu_count': 2, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.32', 'hostname': 'local_32', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'macOS Sierra', 'mac': '00:0c:23:cd:3b:e9', 'cpu_count': 2, 'memory': 'SAMSUNG DDR4 2400T DDR3 32G', 'ip': '192.168.1.33', 'hostname': 'local_33', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'Linux ', 'mac': '00:0c:26:cd:8b:e7', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.34', 'hostname': 'local_34', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'win xp', 'mac': '00:0c:25:cd:2b:e5', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 16G', 'ip': '192.168.1.35', 'hostname': 'local_35', 'sys_type': 'Windows'}, {'disk': 'SEAGATE 600GB SAS 10K 2.5', 'sys_version': 'win95', 'mac': '00:0c:24:cd:3b:e7', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 8G', 'ip': '192.168.1.36', 'hostname': 'local_36', 'sys_type': 'Windows'}, {'disk': 'SEAGATE 600GB SAS 10K 2.5', 'sys_version': 'OS X Mountain Lion', 'mac': '00:0c:22:cd:6b:e4', 'cpu_count': 3, 'memory': 'SAMSUNG DDR4 2400T DDR3 8G', 'ip': '192.168.1.37', 'hostname': 'local_37', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'RHEL', 'mac': '00:0c:23:cd:7b:e2', 'cpu_count': 4, 'memory': 'SAMSUNG DDR4 2400T DDR3 16G', 'ip': '192.168.1.38', 'hostname': 'local_38', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'OpenSUSE', 'mac': '00:0c:21:cd:9b:e8', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 16G', 'ip': '192.168.1.39', 'hostname': 'local_39', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'win98', 'mac': '00:0c:29:cd:4b:e4', 'cpu_count': 2, 'memory': 'SAMSUNG DDR4 2400T DDR3 8G', 'ip': '192.168.1.40', 'hostname': 'local_40', 'sys_type': 'Windows'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'Ubuntu', 'mac': '00:0c:27:cd:5b:e3', 'cpu_count': 1, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.41', 'hostname': 'local_41', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'RHEL', 'mac': '00:0c:28:cd:4b:e9', 'cpu_count': 4, 'memory': 'SAMSUNG DDR4 2400T DDR3 4G', 'ip': '192.168.1.42', 'hostname': 'local_42', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'win95', 'mac': '00:0c:23:cd:6b:e5', 'cpu_count': 4, 'memory': 'SAMSUNG DDR4 2400T DDR3 32G', 'ip': '192.168.1.43', 'hostname': 'local_43', 'sys_type': 'Windows'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'macOS Sierra', 'mac': '00:0c:23:cd:7b:e4', 'cpu_count': 3, 'memory': 'SAMSUNG DDR4 2400T DDR3 32G', 'ip': '192.168.1.44', 'hostname': 'local_44', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'Ubuntu', 'mac': '00:0c:22:cd:1b:e7', 'cpu_count': 3, 'memory': 'SAMSUNG DDR4 2400T DDR3 32G', 'ip': '192.168.1.45', 'hostname': 'local_45', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'win98', 'mac': '00:0c:22:cd:5b:e3', 'cpu_count': 4, 'memory': 'SAMSUNG DDR4 2400T DDR3 32G', 'ip': '192.168.1.46', 'hostname': 'local_46', 'sys_type': 'Windows'}, {'disk': 'SEAGATE 200GB SAS 10K 2.5', 'sys_version': 'Ubuntu', 'mac': '00:0c:28:cd:3b:e8', 'cpu_count': 4, 'memory': 'SAMSUNG DDR4 2400T DDR3 8G', 'ip': '192.168.1.47', 'hostname': 'local_47', 'sys_type': 'Linux'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'OS X Yosemite', 'mac': '00:0c:21:cd:5b:e7', 'cpu_count': 2, 'memory': 'SAMSUNG DDR4 2400T DDR3 8G', 'ip': '192.168.1.48', 'hostname': 'local_48', 'sys_type': 'Mac'}, {'disk': 'SEAGATE 400GB SAS 10K 2.5', 'sys_version': 'Linux ', 'mac': '00:0c:29:cd:5b:e8', 'cpu_count': 2, 'memory': 'SAMSUNG DDR4 2400T DDR3 16G', 'ip': '192.168.1.49', 'hostname': 'local_49', 'sys_type': 'Linux'}]
eq_count = len(eq_list)


def addEquipment(request):
    result = {"statue": "error", "data": ""}
    if request.method == "POST":
        requestData = request.POST
        ip = requestData.get("ipaddress", '')
        username = requestData.get("username", '')
        password = requestData.get("password", "")
        port = requestData.get("port", "22")

        if ip and username and password:
            connect = getConnection(ip, username, password, port)
            if connect["statue"] == "success":
                transport = connect["data"]
                sftp = paramiko.SFTPClient.from_transport(transport)
                sftp.put("", "")
                sftp.put("", "")
                sftp.put("", "")
                transport.close()
            else:
                result["data"] = connect["data"]
        else:
            result["data"] = "ip or username or password not be null"
    else:
        result["data"] = "your request must be post"

    return JsonResponse(result)


@loginValid
def eqList(request):
    register = RegisterForm()

    return render(request, "eqList.html", locals())

@loginValid
def eqDatas(request, pagenum):
    pagenum = int(pagenum)
    start = (pagenum - 1)*10
    end = pagenum*10
    if eq_count%10:
        Prange = range(1, eq_count/10 + 2)
    else:
        Prange = range(1, eq_count/10 + 1)

    Prange.reverse()
    result = {"result": eq_list[start:end], "Prange": Prange}

    return JsonResponse(result)

@csrf_exempt
def equip_api(request):
    result = {"statue": "error", "data": ""}
    if request.method == 'POST':
        requestDatas = request.POST
        hostname = requestDatas.get("hostname")
        mac = requestDatas.get("mac")
        ip = request.META["REMOTE_ADDR"]
        system_type = requestDatas.get("system")
        memory = requestDatas.get("memory")
        disk = requestDatas.get("disk")
        cpu_count = requestDatas.get("cpu_count")
        sys_ver = requestDatas.get("version")
        try:
            eq = Equipment()
            eq.hostname = hostname
            eq.mac = mac
            eq.ip = ip
            eq.sys_type = system_type
            eq.memory = memory
            eq.disk = disk
            eq.cpu_count = cpu_count
            eq.sys_version = sys_ver
            eq.save()
        except Exception as e:
            result ["data"] = str(e)
        else:
            result["statue"] = "success"
            result['data'] = "your data is saved"
    else:
        result['data'] = "request must be post"

    return JsonResponse(result)


def gateone(request):

    return render(request, "cmdb_terminal.html")

