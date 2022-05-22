#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
import os
import sys
import urllib.parse


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
    n_mac = n_mac.replace(':', '') # Unix, Linux, BSD, Apple
    n_mac = n_mac.replace('-', '') # Windows
    n_mac = n_mac.replace('.', '') # Cisco
    n_mac = n_mac[0:6] # To OUI
    return lookup_oui_key(data, n_mac)


# MAIN
data = {}

# Load OUI file
data = load_oui_file("ieee-oui-integerated-sort-u.txt")


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

