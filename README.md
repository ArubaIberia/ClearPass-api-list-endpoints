# ClearPass-api-list-endpoints
Get a CSV with whole list of endpoints including all attributes of them (including custom attributes).
Script to get a CSV file with the list of Endpoints in ClearPass. You have to configure the followings parameters before run the script:
* Create a Bearer Token in ClearPass
* Configure this token in the Script file
* Configure IP Address of ClearPass

ClearPass has a limit of 1000 endpoint returned in each query. The script will try to get more data with several queries. In the case you want to reducice each iteration, you can change it from 1000 to the limit wanted.

How to run this script:
```
python3 get_endpoints.py 
```
