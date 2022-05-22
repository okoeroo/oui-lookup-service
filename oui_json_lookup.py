#!/usr/bin/env python3

from fastapi import FastAPI, Response, Request, Cookie, HTTPException, status, Depends
from starlette import status
import os
import sys
import urllib.parse
import requests
import configparser


def read_config_url(filepath="config.ini"):
    config = configparser.ConfigParser()
    config.read(filepath)
    return config


def load_oui_file(filepath):
    data = {}

    f = open(filepath, "r")
    source = f.read().splitlines()

    # Parse it
    for l in source:
        key, value = l.split("\t")
        data[key.upper()] = value
    return data

def lookup_oui_key(data, key):
    if key.upper() not in data.keys():
        return None

    return data[key.upper()]

def lookup_oui_mac(data, mac):
    n_mac = mac
    n_mac = n_mac.replace(':', '') # Unix, Linux, BSD, Apple
    n_mac = n_mac.replace('-', '') # Windows
    n_mac = n_mac.replace('.', '') # Cisco
    n_mac = n_mac[0:6] # To OUI
    return lookup_oui_key(data, n_mac)


# MAIN
data = {}

# Load config file
config = read_config_url("config.ini")
if config is None:
    print("Error: no configuration file load")
    sys.exit(1)

if 'settings' not in config:
    print("Error: section \'settings\' not found in config file")
    sys.exit(1)

if 'oui_url' not in config['settings']:
    print("Error: oui_url not found in config file")
    sys.exit(1)

if 'oui_file' not in config['settings']:
    print("Error: oui_file not found in config file")
    sys.exit(1)



# Load OUI file
data = load_oui_file(config['settings']['oui_file'])

# Tests
if data is None:
    print("Error: no OUI data loaded")
    sys.exit(1)


# Load FastAPI
app = FastAPI()


@app.get("/api/oui-lookup/oui")
async def lookup_oui(key: str):
    decode_key = urllib.parse.unquote(key)
    v = lookup_oui_key(data, decode_key)
    if v is None:
        raise HTTPException(status_code=404, detail="Item not found")

    r = {}
    r['value'] = v
    return r


@app.get("/api/oui-lookup/mac")
async def lookup_mac(key: str):
    decode_key = urllib.parse.unquote(key)
    v = lookup_oui_mac(data, decode_key)
    if v is None:
        raise HTTPException(status_code=404, detail="Item not found")

    r = {}
    r['value'] = v
    return r


@app.post("/api/oui-lookup/update")
async def update_oui_file():
    print("Using settings:")
    print(config['settings']['oui_url'])
    print(config['settings']['oui_file'])

    print("Downloading...")
    response = requests.get(config['settings']['oui_url'])
    if response.status_code < 200 or response.status_code > 299:
        raise HTTPException(status_code=500, detail="Error in OUI updating.")
        print("Error: downloading.")
        return

    print("Done downloading.")

    print("Writing...")
    open(config['settings']['oui_file'], "wb").write(response.content)
    print("Done writing to disk")

    print("Reloading OUI file from disk...")
    data = load_oui_file(config['settings']['oui_file'])
    print("Done reloading in memory.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


