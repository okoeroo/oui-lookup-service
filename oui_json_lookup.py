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


print(data)

app = FastAPI()


@app.get("/api/lookup")
async def lookup():
    return {"message": "Hello World"}
