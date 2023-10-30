# Faust Prometheus Exporter

Module for exporting monitoring values for Prometheus

[![PyPI](https://img.shields.io/pypi/v/faust-prometheus-exporter)](https://pypi.org/project/faust-prometheus-exporter/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/faust-prometheus-exporter)](https://pypi.org/project/faust-prometheus-exporter/)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/faust-prometheus)](https://gitlab.com/rocshers/python/faust-prometheus)

[![Test coverage](https://codecov.io/gitlab/rocshers:python/faust-prometheus/graph/badge.svg?token=3C6SLDPHUC)](https://codecov.io/gitlab/rocshers:python/faust-prometheus)
[![Downloads](https://static.pepy.tech/badge/faust-prometheus-exporter)](https://pepy.tech/project/faust-prometheus-exporter)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/faust-prometheus)](https://gitlab.com/rocshers/python/faust-prometheus)

## Functionality

- Adds `/metrics` endpoint
- Gives basic `Prometheus-client` metrics
- Gives custom user`s metrics
- Adds internal `faust` metrics

## Installation

`pip install faust-prometheus-exporter`

## Quick start


```python
import faust
from faust_prometheus import FaustPrometheusExporter

app = faust.App('app', broker='localhost:9092')

# Adding the Prometheus Exporter
exporter = FaustPrometheusExporter(app)
```

```bash
# see default metrics
curl localhost:8000/metrics
```

## Playground

```python
import logging
from random import randint

import faust
from prometheus_client import Counter, Histogram

from faust_prometheus import FaustPrometheusExporter

logger = logging.getLogger('app')

# Prometheus custom metrics
prometheus_counter_topic_1_messages = Counter('topic_1_messages', 'Count of messages successfully processed from topic_1')
prometheus_histogram_size_messages = Histogram('size_messages', 'Histogram about messages size')

app = faust.App(
    'faust_prometheus',
    broker='localhost:9092',
)

# Adding the Prometheus Exporter
exporter = FaustPrometheusExporter(app)

topic_1 = app.topic('topic_1')

@app.agent(topic_1)
async def agent_topic_1(messages: faust.Stream[str]):
    async for message in messages:
        logger.info(f'Received topic_1 message: {message}')
        prometheus_counter_topic_1_messages.inc()
        prometheus_histogram_size_messages.observe(len(message))

@app.timer(interval=1.0)
async def example_sender(app):
    await topic_1.send(value='Nisi lorem ullamco veniam elit' * randint(1, 10))

if __name__ == '__main__':
    app.main()

```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/faust-prometheus/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/faust-prometheus>

Before adding changes:

```bash
make install-dev
```

After changes:

```bash
make format test
```
