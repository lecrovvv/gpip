from requests import get, post
import subprocess
import json
from bs4 import BeautifulSoup

def getInstalledPackages():
    output = subprocess.check_output(['pip', 'list']).decode('utf-8')
    installed_packages = []
    for line in output.split('\n')[2:-1]:
        package_name = line.split(' ')[0]
        installed_packages.append(package_name)
    return installed_packages
     
def uninstall_package(package_name):
    subprocess.check_call(['pip', 'uninstall', package_name, '-y'])

def install_package(package_name):
    subprocess.check_call(['pip', 'install', package_name])

def getInfo(search):
    r = get("https://pypi.org/pypi/%s/json" % search)

    return r.text

def searchPackage(query):
    url = 'https://pypi.org/search/?q=%s'
    response = get(url % query)

    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('span', class_='package-snippet__name')

    _results = []

    for result in results:
        package_name = result.get_text(strip=True)
        _results.append(package_name)

    return _results

r = json.loads(getInfo("pyqt5"))
print(json.dumps(r, indent=4, sort_keys=True))