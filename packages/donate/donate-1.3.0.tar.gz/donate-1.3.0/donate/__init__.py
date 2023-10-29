import requests
from .data import Data

package_name = "donate"
response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
data = response.json()
check_version = data['info']['version']

current_version = "1.3.0"

if check_version == current_version:
	pass
else:
	print(f"you use old version it library! your version {current_version}:new version {check_version}")