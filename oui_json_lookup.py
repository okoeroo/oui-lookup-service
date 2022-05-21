#!/usr/bin/env python3

from fastapi import FastAPI
import os
import sys


f = open("ieee-oui-integerated-sort-u.txt", "r")
source = f.read().splitlines()


data = {}

for l in source:
    key, value = l.split("\t")
    data[key] = value


app = FastAPI()


@app.get("/api/lookup/oui")
async def lookup_oui(key: str):
    return {"message": "Hello World"}

@app.get("/api/lookup/mac")
async def lookup_mac(key: str):
    return {"message": "Hello World"}
