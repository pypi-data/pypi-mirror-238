import logging

import faust
from faust.web import Request
from prometheus_client import REGISTRY, CollectorRegistry
from prometheus_client.exposition import choose_encoder

from faust_prometheus.collectors import AsyncioCollector, FaustCollector

logger = logging.getLogger('faust_prometheus')


class FaustPrometheusExporter(object):
    faust_app: faust.App
    registry: CollectorRegistry

    def __init__(
        self,
        faust_app: faust.App,
        url: str = '/metrics',
        registry: CollectorRegistry = REGISTRY,
        prefix: str = 'faust_',
    ) -> None:
        self.faust_app = faust_app
        self.registry = registry
        self.url = url

        self.registry.register(AsyncioCollector())
        self.registry.register(FaustCollector(faust_app, prefix))

        self.faust_app.page(self.url)(self._url_metrics_handler)

    async def _url_metrics_handler(self, request: Request):
        logger.debug(f'Handled {request.url} request. Make response with faust & python metrics')

        accept_header = request.headers.get('Accept')
        request.headers.get('Accept-Encoding')
        encoder, content_type = choose_encoder(accept_header)
        response = self.faust_app.web.bytes(encoder(self.registry))
        response.content_type = content_type
        return response
