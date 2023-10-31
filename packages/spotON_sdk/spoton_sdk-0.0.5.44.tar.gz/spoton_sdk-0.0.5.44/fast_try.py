from spotON_sdk import all_Countries
from pprint import pprint

pprint (all_Countries.return_List)
pprint (all_Countries.get_country_by_name("Sweden"))

country_code = "AT"
if "_" in country_code:
    cleaned_code = country_code.split("_")[0]
else:
    cleaned_code = country_code
print(cleaned_code)
