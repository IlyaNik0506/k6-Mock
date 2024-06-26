# from fastapi import FastAPI, HTTPException, Body, Request
from read_configs_endpoints import load_endpoints
import asyncio


async def mig_2():
    delay = await load_endpoints("MIG_2")
    
    await asyncio.sleep(delay / 1000)
    
    response_data = {"MT": "MIG_2"}

    return response_data