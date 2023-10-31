# Weni Profilers

The `weni-profilers` library allows you to add a simple profiler to a Django project to analyze the performance of views.  

## Setup in project

### 1. Install weni-profilers

```
pip install weni-profilers
```

### 2. Configure the middleware
```py
MIDDLEWARE = [
    # ...
    'weni.profilers.CProfilerMiddleware',
]
```


## Variables

```py
USE_PROFILER = True
PROFILER_AUTH_TOKEN = "your-secret-key"
```

| Name | Description |
|------|-------------|
| USE_PROFILER | This variable enables the profiler if it is `True` |
| PROFILER_AUTH_TOKEN | Based on this variable, the middleware will authenticate the request |

> It is recommended that both are configured by environment variables, mainly `PROFILER_AUTH_TOKEN`

## Using

To profile a view, add `?prof` to the URL of the view you want to analyze:

```
http://localhost:8000/your-view/?prof
```

You can pass the following parameters in the URL to customize the output:

- `?sort`: Sorts the output by a specific metric. The default is "team". See the official documentation for all ordering options.
- `?count`: Defines the number of lines to be displayed. The default is 100.
- `?download`: Downloads the profile file for viewing in tools such as SnakeViz or RunSnakeRun.

Example URL with parameters:
```
http://localhost:8000/your-view/?prof&sort=cumulative&count=50&download
```

---

This repository is a fork of https://github.com/omarish/django-cprofile-middleware