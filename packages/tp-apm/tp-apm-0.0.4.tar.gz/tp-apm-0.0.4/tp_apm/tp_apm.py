import inspect, socket, requests, functools, calendar, time
from pkg_resources import get_distribution

def _get_caller_info():
    stack = inspect.stack()
    for frame_info in stack:
        module = inspect.getmodule(frame_info[0])
        package = module.__package__ if module else None
        if package != "tp_apm":
            return module.__name__, package
    return "",""

def _event(application, func_name, duration):
    try:
        s = requests.session()
        # s.keep_alive = False
        # s.post("http://172.104.91.248:5000/api/apm",data={
        #     'a': application,
        #     'h': socket.gethostname(),
        #     's': f"{func_name}"
        # },timeout=3)
        s.close()
    finally:
        return

def detector(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = calendar.timegm(time.gmtime())
        caller_module, caller_package = _get_caller_info()
        result = func(*args, **kwargs)
        _event(caller_package, func.__name__, (calendar.timegm(time.gmtime())-start_time))        
        return result
    return wrapper