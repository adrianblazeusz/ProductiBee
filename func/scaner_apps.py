import winreg
import time

def foo(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]

    software_list = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]
            software['install_date'] = winreg.QueryValueEx(asubkey, "InstallDate")[0]
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            
            # Filter out applications with unwanted publishers, names, or keywords
            if 'Microsoft' in software['publisher'] or 'Microsoft Corporation' in software['publisher']:
                continue
            if 'Python' in software['name'] or 'Node.js' in software['name'] or 'Go Programming Language' in software['name']:
                continue
            
            software_list.append(software)
        except EnvironmentError:
            continue

    return software_list

def format_time(timestamp):
    if timestamp is None:
        return 'undefined'
    try:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp)))
    except ValueError:
        return 'undefined'

# Collect software list from all necessary registry locations
software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + foo(winreg.HKEY_CURRENT_USER, 0)

# Sort the software list based on the last run timestamp
sorted_software_list = sorted(software_list, key=lambda x: x.get('install_date', 0), reverse=True)

# Print the sorted list
for software in sorted_software_list:
    print('Name=%s, InstallDate=%s,' % (software['name'], format_time(software['install_date'])))

print('Number of installed apps: %s' % len(sorted_software_list))