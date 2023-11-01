# govdata
Client-library to fetch data from GovData/OpenData-sources via DKAN-REST-API. 
Take a look at [https://www.govdata.de/](https://www.govdata.de/) to determine if your city of interest provides some data.

## install 
```bash
python -m pip install govdata
```

## usage
```py
from govdata.interface import DKANPortalClient 
import requests
# get opendata-city-client
cityclient = DKANPortalClient(city="braunschweig", apiversion=3)

# get all available packages (topics)
packagelist = cityclient.get_packages()

# request data for package from packagelist
first_package_id_from_list = packagelist[0]
package_meta = cityclient.get_package_metadata(package_id=first_package_id_from_list)
resources_for_package = package_meta["resources"]

# fetch informations from choosen resource by id
index_of_choosen_resource = 1
resource_id = resources_for_package[index_of_choosen_resource]["id"]
resource = cityclient.get_resource_by_id(resource_id=resource_id)

# now send get-request to resource-url to download file as <resourcename>.csv
response = requests.get(resource["url"])
if response.ok:
    with open(f"{resource['name']}.csv", mode="wb") as file:
        file.write(response.content)
```

## run tests
```bash
pytest --cov=interface tests
```

## testcoverage
```
============================= test session starts ==============================
platform linux -- Python 3.8.10, pytest-7.4.3, pluggy-1.3.0
plugins: requests-mock-1.11.0, cov-4.1.0
collected 8 items

tests/test_interface.py ........                                         [100%]

---------- coverage: platform linux, python 3.8.10-final-0 -----------
Name           Stmts   Miss  Cover
----------------------------------
interface.py      93     45    52%
----------------------------------
TOTAL             93     45    52%


============================== 8 passed in 0.16s ===============================
```

