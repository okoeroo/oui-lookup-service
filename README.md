# oui-lookup-service
OUI Lookup service and compatible with Graylog JSON

## Configuration of for config.ini
config.ini
```dosini
[settings]
oui_url  = https://raw.githubusercontent.com/okoeroo/oui-lookup-service/main/ieee-oui-integerated-sort-u.txt
oui_file = ieee-oui-integerated-sort-u.txt
```

# Graylog integration
The REST API with JSON reply can be integrated in Graylog using two Data Adapters and Lookup Tables.

## Data Adapter for OUI based lookups
This adapter will accept six octets and will only search for these most significant 6 octets of the MAC address.

### Configuration  
Type: use HTTP JSONPath  
Lookup URL: `http://example.lan:8000/api/oui-lookup/oui?key=${key}`  
Single value JSONPath: `$.value`  
Multi value JSONPath: n/a  

### Example data:  
key: `14109f`  
response: `{"value":"Apple, Inc."}`  
key: `000001`  
response: `{"value":"XEROX CORPORATION"}`  

## Data Adapter for OUI based lookups
This adapter will accept a MAC address and extract the 6 most significant octets out of the MAC address to match against the OUI list. Supported formats include colon, dash and dot notations.

### Configuration
Type: use HTTP JSONPath  
Lookup URL: `http://example.lan:8000/api/oui-lookup/mac?key=${key}`  
Single value JSONPath: `$.value`  
Multi value JSONPath: n/a  

### Example data:  
Format: Unix, Linux, BSD, etc  
key: `14:10:9f:00:00:00`  
response: `{"value":"Apple, Inc."}`  

Format: Windows  
key: `14-10-9f-00-00-00`  
response: `{"value":"Apple, Inc."}`  

Format: Cisco  
key: `14109f.000000`  
response: `{"value":"Apple, Inc."}`  

## Docker
### Build with
```docker build -t okoeroo/oui-lookup-service:${TAG} .```

### Run example
```docker run -dp 8000:8000 okoeroo/oui-lookup-service:${TAG}```

### Tag new version
```
LOCAL_IMAGE="oui-lookup-service"
REPO_NAME="oui-lookup-service"
TAG=<version>

git commit -a -m "<text>"
git tag "${TAG}"
git push --tags

docker build -t okoeroo/oui-lookup-service:${TAG} .
```

## #Publish new version
Note 1: don't forget `docker login -u okoeroo`
Note 2: Use key per host

```
LOCAL_IMAGE="oui-lookup-service"
REPO_NAME="oui-lookup-service"
TAG=<version>

git tag "${TAG}"
git push --tags

docker build -t okoeroo/oui-lookup-service:${TAG} .
docker push okoeroo/${REPO_NAME}:${TAG}
```

## Benchmark
```bash
ab -c 50 -n 5000 "hacktic.koeroo.lan:8000/api/oui-lookup/mac?key=14109f.000000"
```

Works nicely, even when you update the service intermediately.
```
Server Software:        uvicorn
Server Hostname:        hacktic.koeroo.lan
Server Port:            8000

Document Path:          /api/oui-lookup/mac?key=14109f.000000
Document Length:        23 bytes

Concurrency Level:      50
Time taken for tests:   4.813 seconds
Complete requests:      5000
Failed requests:        0
Total transferred:      835000 bytes
HTML transferred:       115000 bytes
Requests per second:    1038.79 [#/sec] (mean)
Time per request:       48.133 [ms] (mean)
Time per request:       0.963 [ms] (mean, across all concurrent requests)
Transfer rate:          169.41 [Kbytes/sec] received
```


