# oui-lookup-service
OUI Lookup service and compatible with Graylog JSON

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
```docker build -t oui-lookup-service .```

### Run example
```docker run -dp 8001:8000 oui-lookup-service```
