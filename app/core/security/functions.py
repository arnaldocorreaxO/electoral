import socket

from core.pos.models import Company
from core.security.models import Dashboard
from datetime import datetime


def system_information(request):
    data = {
        'dshboard': get_dashboard(),
        'company': Company.objects.first(),
        'hostname': socket.gethostname(),
        'menu': get_layout(),
        'localhost': socket.gethostbyname(socket.gethostname()),
        'date_joined': datetime.now(),
    }
    return data


def get_dashboard():
    try:
        items = Dashboard.objects.all()
        if items.exists():
            return items[0]
    except:
        pass
    return None


def get_layout():
    objs = Dashboard.objects.filter()
    if objs.exists():
        objs = objs[0]
        if objs.layout == 1:
            return 'vtcbody.html'
        return 'hztbody.html'
    return 'hztbody.html'
