#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
import os
import sys


def load_oui_file(filepath = "ieee-oui-integerated-sort-u.txt"):
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
    n_mac = n_mac.replace(':', '')
    n_mac = n_mac.replace('-', '')
    n_mac = n_mac[0:6]
    print(mac, "->", n_mac)
    return lookup_oui_key(data, n_mac)


# MAIN
data = {}

# Load OUI file
data = load_oui_file("ieee-oui-integerated-sort-u.txt")


app = FastAPI()


@app.get("/api/lookup/oui")
async def lookup_oui(key: str):
    v = lookup_oui_key(data, key)
    if v is None:
        raise HTTPException(status_code=404, detail="Item not found")

    r = {}
    r['value'] = v
    return r

@app.get("/api/lookup/mac")
async def lookup_mac(key: str):
    v = lookup_oui_mac(data, key)
    if v is None:
        raise HTTPException(status_code=404, detail="Item not found")

    r = {}
    r['value'] = v
    return r

