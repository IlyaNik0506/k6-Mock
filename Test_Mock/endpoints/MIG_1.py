# from fastapi import FastAPI, HTTPException, Body, Request
from read_configs_endpoints import load_endpoints
import asyncio
from pydantic import BaseModel
import json

# class RequestModel_RReq(BaseModel):
#     MV: str

    
async def mig_1():
    # mv_value = request.MV
    
    delay = await load_endpoints("MIG_1")
    
    await asyncio.sleep(delay / 1000)
    
    response_data = {"MT": "MIG_1",
                     "MV": "123"}

    return json.dumps(response_data)