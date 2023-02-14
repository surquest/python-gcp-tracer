![GitHub](https://img.shields.io/github/license/surquest/python-gcp-tracer?style=flat-square)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/surquest/python-gcp-tracer/test.yml?branch=main&style=flat-square)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/surquest/6e25c317000917840152a5e702e71963/raw/python-gcp-tracer.json&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/surquest-GCP-tracer?style=flat-square)


# Introduction

This project is designed to simplify tracing for FastAPI based application running in Google Cloud Run. 

The Tracer class is a wrapper around `opentelemetry` libraries which allows to easily add tracing to your application. By design the Tracer uses Google Cloud Trace exporter to send the traces to the Google Cloud Platform. Moreover, the Tracer class accepts the `request` object as a parameter which allows to extract the `X-Cloud-Trace-Context` header and pass it to the exporter. This allows to trace the requests between the services.

# Quick Start

```python
# import the Tracer class
from surquest.GCP.tracer import Tracer

# request is an object which allows to check the request headers
# request.headers.get('X-Cloud-Trace-Context', None)
tracer = Tracer(request=request)

with tracer.start_span(name="Task A"):
    # Do something
    result = 1 + 1
```

## FastAPI integration

Following example shows how to integrate the Tracer class with FastAPI endpoints:

```python
from surquest.GCP.tracer import Tracer
import requests
from fastapi import FastAPI, Depends, Query, Path

app = FastAPI()

@app.get("/exchange/currencies/{base}/{quote}")
async def exchange(
        base: str = Path(..., description="Base currency"),
        quote: str = Path(..., description="Quote currency"),
        amount: float = Query(..., gt=0, description="Amount to exchange"),
        tracer: Tracer = Depends(Tracer),
):
    
    # get exchange rate from external API
    with tracer.start_span("Get exchange rate"):
        
        exchange_rate = requests.get(
            f"https://api.exchangeratesapi.io/v1/latest?base={base}&symbols={quote}",
            params={
                "base": base,
                "symbols": quote,
                "access_key": "<your_api_key>" # please set your own API key
            }
        ).json()["rates"][quote]
        
    with tracer.start_span("Calculate exchange"):
        result = amount * exchange_rate
        
    return {
        "currencies": {
            "base": base,
            "quote": quote
        },
        "amount": {
            "base": amount,
            "quote": result
        }
    }

```

# Local development

You are more than welcome to contribute to this project. To make your start easier we have prepared a docker image with all the necessary tools to run it as interpreter for Pycharm or to run tests.


## Build docker image
```
docker build `
     --tag surquest/gcp/tracer `
     --file package.base.dockerfile `
     --target test .
```

## Run tests
```
docker run --rm -it `
 -v "${pwd}:/opt/project" `
 -e "GOOGLE_APPLICATION_CREDENTIALS=/opt/project/credentials/keyfile.json" `
 -w "/opt/project/test" `
 surquest/gcp/tracer pytest
```