# Introduction

This project provides easy to use wrapper around the Google Cloud Platform tracing library for REST API calls to track execution between services.

# Quick Start

```python
 

# request is an object which allows to check the request headers
# request.headers.get('X-Cloud-Trace-Context', None)
tracer = Tracer(request=request)

with tracer.start_span(name="Task A"):
    # Do something
    result = 1 + 1
    
```
