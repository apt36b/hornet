# informations.py
import platform
import psutil
import socket
import os
from datetime import datetime
import json

def get_os_info():
    try:
        os_info = {
            'system': platform.system(),
            'node_name': platform.node(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
        }
        return os_info
    except Exception as e:
        return {'error': str(e)}

def get_cpu_info():
    try:
        cpu_freq = psutil.cpu_freq()
        cpu_info = {
            'physical_cores': psutil.cpu_count(logical=False),
            'total_cores': psutil.cpu_count(logical=True),
            'max_frequency_mhz': cpu_freq.max if cpu_freq else None,
            'min_frequency_mhz': cpu_freq.min if cpu_freq else None,
            'current_frequency_mhz': cpu_freq.current if cpu_freq else None,
            'cpu_usage_per_core': psutil.cpu_percent(percpu=True, interval=1),
            'total_cpu_usage_percent': psutil.cpu_percent(),
        }
        return cpu_info
    except Exception as e:
        return {'error': str(e)}

def get_memory_info():
    try:
        vm = psutil.virtual_memory()
        memory_info = {
            'total_bytes': vm.total,
            'available_bytes': vm.available,
            'percent_used': vm.percent,
            'used_bytes': vm.used,
            'free_bytes': vm.free,
        }
        return memory_info
    except Exception as e:
        return {'error': str(e)}

def get_disk_info():
    try:
        partitions = psutil.disk_partitions(all=False)
        disk_info = {}
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.device] = {
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total_bytes': usage.total,
                    'used_bytes': usage.used,
                    'free_bytes': usage.free,
                    'percent_used': usage.percent,
                }
            except PermissionError:
                # This can happen on some systems where certain partitions require elevated privileges
                disk_info[partition.device] = {'error': 'Permission Denied'}
        return disk_info
    except Exception as e:
        return {'error': str(e)}

def get_network_info():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        # Getting MAC address in a cross-platform way
        mac_address = None
        addrs = psutil.net_if_addrs()
        for interface, addr_list in addrs.items():
            for addr in addr_list:
                if addr.family == psutil.AF_LINK:
                    mac_address = addr.address
                    break
            if mac_address:
                break
        network_info = {
            'hostname': hostname,
            'ip_address': ip_address,
            'mac_address': mac_address,
            'interfaces': list(psutil.net_if_addrs().keys()),
        }
        return network_info
    except Exception as e:
        return {'error': str(e)}

def get_boot_time():
    try:
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        boot_time = bt.strftime("%Y-%m-%d %H:%M:%S")
        return boot_time
    except Exception as e:
        return {'error': str(e)}

def get_battery_info():
    try:
        battery = psutil.sensors_battery()
        if battery:
            battery_info = {
                'percent': battery.percent,
                'secs_left': battery.secsleft,
                'power_plugged': battery.power_plugged,
            }
            return battery_info
        else:
            return {'info': 'No battery information available (possibly a desktop system)'}
    except Exception as e:
        return {'error': str(e)}

def get_environment_variables():
    try:
        env_vars = dict(os.environ)
        return env_vars
    except Exception as e:
        return {'error': str(e)}

def collect_system_info():
    system_info = {
        'os_info': get_os_info(),
        'cpu_info': get_cpu_info(),
        'memory_info': get_memory_info(),
        'disk_info': get_disk_info(),
        'network_info': get_network_info(),
        'boot_time': get_boot_time(),
        'battery_info': get_battery_info(),
        'environment_variables': get_environment_variables(),
    }
    return system_info

if __name__ == "__main__":
    system_info = collect_system_info()
    # Pretty-print the JSON data
    print(json.dumps(system_info, indent=4))

