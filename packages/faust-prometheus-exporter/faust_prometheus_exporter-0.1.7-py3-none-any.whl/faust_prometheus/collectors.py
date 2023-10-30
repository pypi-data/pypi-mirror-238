import asyncio
from typing import Dict, Iterable, Optional

import faust
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily
from prometheus_client.metrics_core import Metric
from prometheus_client.registry import Collector

#
# List of TODO metrics
#
# # Deque of run times used for averages
# events_runtime: Deque[float] = cast(Deque[float], None)
# # Deque of commit latency values
# commit_latency: Deque[float] = cast(Deque[float], None)
# # Deque of send latency values
# send_latency: Deque[float] = cast(Deque[float], None)
# # Deque of assignment latency values.
# assignment_latency: Deque[float] = cast(Deque[float], None)
# # Last committed offsets by TopicPartition
# tp_committed_offsets: TPOffsetMapping = cast(TPOffsetMapping, None)
# # Last read offsets by TopicPartition
# tp_read_offsets: TPOffsetMapping = cast(TPOffsetMapping, None)
# # Log end offsets by TopicPartition
# tp_end_offsets: TPOffsetMapping = cast(TPOffsetMapping, None)
# # Deque of previous n rebalance return latencies.
# rebalance_return_latency: Deque[float] = cast(Deque[float], None)
# # Deque of previous n rebalance end latencies.
# rebalance_end_latency: Deque[float] = cast(Deque[float], None)


class AsyncioCollector(Collector):
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        super().__init__()
        self.loop = loop

    def collect(self) -> Iterable[Metric]:
        if self.loop is None:
            try:
                self.loop = asyncio.get_running_loop()

            except RuntimeError:
                return

        yield GaugeMetricFamily(
            'python_asyncio_loops',
            'Count of active asyncio loops',
            1,
        )
        yield GaugeMetricFamily(
            'python_asyncio_tasks',
            'Count of active asyncio tasks',
            len(asyncio.all_tasks(self.loop)),
        )


class FaustCollector(Collector):
    def __init__(self, faust_app: faust.App, prefix: Optional[str] = 'faust_') -> None:
        self.faust_app = faust_app
        self.prefix = prefix

    def get_faust_app_info(self) -> Dict[str, str]:
        info = {
            'is_leader': 'is_not_leader',
            'id': self.faust_app.conf.id,
            'name': self.faust_app.conf.name,
            'consumer_generation_id': str(self.faust_app.consumer_generation_id),
        }

        try:
            if self.faust_app.is_leader():
                info['is_leader'] = 'is_leader'

        except BaseException:
            pass

        return info

    def collect(self) -> Iterable[Metric]:
        m = self.faust_app.monitor

        yield InfoMetricFamily('faust', 'Faust app info', self.get_faust_app_info())

        yield GaugeMetricFamily(
            f'{self.prefix}max_avg_history',
            'Max number of total run time values to keep to build average',
            m.max_avg_history,
        )
        yield GaugeMetricFamily(
            f'{self.prefix}max_commit_latency_history',
            'Max number of commit latency numbers to keep',
            m.max_commit_latency_history,
        )
        yield GaugeMetricFamily(
            f'{self.prefix}max_send_latency_history',
            'Max number of send latency numbers to keep',
            m.max_send_latency_history,
        )
        yield GaugeMetricFamily(
            f'{self.prefix}max_assignment_latency_history',
            'Max number of assignment latency numbers to keep',
            m.max_assignment_latency_history,
        )

        yield GaugeMetricFamily(
            f'{self.prefix}messages_active',
            'Number of messages currently being processed',
            m.messages_active,
        )

        yield GaugeMetricFamily(
            f'{self.prefix}messages_received',
            'Number of messages processed in total',
            m.messages_received_total,
        )

        yield GaugeMetricFamily(
            f'{self.prefix}messages_s',
            'Number of messages being processed this second',
            m.messages_s,
        )

        yield GaugeMetricFamily(
            f'{self.prefix}messages_sent',
            'Number of messages sent in total',
            m.messages_sent,
        )

        c = GaugeMetricFamily(
            f'{self.prefix}messages_sent_by_topic',
            'Number of messages sent in total by topic',
            labels=['topic'],
        )

        for topic, value in m.messages_sent_by_topic.items():
            c.add_metric([topic], value)

        yield c

        c = GaugeMetricFamily(
            f'{self.prefix}messages_received_by_topic',
            'Number of messages processed in total',
            labels=['topic'],
        )

        for topic, value in m.messages_received_by_topic.items():
            c.add_metric([topic], value)

        yield c

        yield GaugeMetricFamily(
            f'{self.prefix}events_active',
            'Number of events currently being processed',
            m.events_active,
        )

        yield GaugeMetricFamily(
            f'{self.prefix}events_total',
            'Number of events processed in total',
            m.events_total,
        )

        yield GaugeMetricFamily(
            f'{self.prefix}events_s',
            'Number of events processed in total',
            m.events_s,
        )

        yield GaugeMetricFamily(
            f'{self.prefix}events_runtime_avg',
            'Average event runtime over the last second',
            m.events_runtime_avg,
        )

        yield GaugeMetricFamily(
            f'{self.prefix}events_runtime_avg',
            'Average event runtime over the last second',
            m.events_runtime_avg,
        )

        # c = GaugeMetricFamily(f'{self.prefix}events_runtime', 'Count of events processed by task', labels=['task'])

        # for topic, value in m.events_runtime.items():
        #     c.add_metric([topic], value)

        # yield c

        c = GaugeMetricFamily(
            f'{self.prefix}topic_buffer_full',
            'Counter of times a topics buffer was full',
            labels=['topic', 'partition'],
        )

        for topic, value in m.topic_buffer_full.items():
            c.add_metric(
                [
                    getattr(topic, 'topic', 'None'),
                    str(getattr(topic, 'partition', 'None')),
                ],
                value,
            )

        yield c

        c = GaugeMetricFamily(
            f'{self.prefix}metric_counts',
            'Arbitrary counts added by apps',
            labels=['app'],
        )

        for key, value in m.metric_counts.items():
            c.add_metric([key], value)

        yield c

        yield GaugeMetricFamily(
            f'{self.prefix}send_errors',
            'Number of produce operations that ended in error',
            m.send_errors,
        )

        yield GaugeMetricFamily(
            f'{self.prefix}assignments_completed',
            'Number of partition assignments completed',
            m.assignments_completed,
        )

        yield GaugeMetricFamily(
            f'{self.prefix}assignments_failed',
            'Number of partitions assignments that failed',
            m.assignments_failed,
        )

        yield GaugeMetricFamily(
            f'{self.prefix}rebalances',
            'Number of rebalances seen by this worker',
            m.rebalances,
        )

        yield GaugeMetricFamily(
            f'{self.prefix}rebalance_return_avg',
            'Average rebalance return latency',
            m.rebalance_return_avg,
        )

        yield GaugeMetricFamily(
            f'{self.prefix}rebalance_end_avg',
            'Average rebalance end latency',
            m.rebalance_end_avg,
        )

        c = GaugeMetricFamily(
            f'{self.prefix}http_response_codes',
            'Counter of returned HTTP status codes',
            labels=['core'],
        )

        for key, value in m.http_response_codes.items():
            c.add_metric([str(key._value_)], value)

        yield c

        # c = GaugeMetricFamily(
        #     'http_response_latency',
        #     'Deque of previous n HTTP request->response latencies',
        #     labels=['core'],
        # )

        # for key, value in m.http_response_latency.items():
        #     c.add_metric([str(key)], value)

        # yield c

        yield GaugeMetricFamily(
            f'{self.prefix}http_response_latency_avg',
            'Average request->response latency',
            m.http_response_latency_avg,
        )

        c = GaugeMetricFamily(
            f'{self.prefix}stream_inbound_time',
            'nothing',
            labels=['topic', 'partition'],
        )

        for key, value in m.stream_inbound_time.items():
            c.add_metric([key.topic, str(key.partition)], value)

        yield c

        c = GaugeMetricFamily(
            f'{self.prefix}tables_action',
            'Mapping of tables actions',
            labels=['name', 'action'],
        )

        for key, value in m.tables.items():
            c.add_metric([value.table.name, 'retrieved'], value.keys_retrieved)
            c.add_metric([value.table.name, 'updated'], value.keys_updated)
            c.add_metric([value.table.name, 'deleted'], value.keys_deleted)

        yield c

        #
        # TODO: Add metrics about stream and
        #

        # c = GaugeMetricFamily(
        #     f'{self.prefix}events_by_task',
        #     'Count of events processed by task',
        #     labels=['task'],
        # )

        # for topic, value in m.events_by_task.items():
        #     c.add_metric([topic], value)

        # yield c

        # c = GaugeMetricFamily(
        #     'asyncio_tasks',
        #     'Lookup for names to tasks to reduce __repr__ overhead',
        #     labels=['topic', 'partition'],
        # )

        # for key, value in m.task_lookup.items():
        #     c.add_metric([key], value)

        # yield c

        for mf in self.get_steams_metrics():
            yield mf

        for mf in self.get_tasks_metrics():
            yield mf

    def get_steams_metrics(self):
        m = self.faust_app.monitor

        streams: Dict[str, faust.Stream] = {}

        for stream, value in m.stream_lookup.items():
            streams[value] = stream

        yield GaugeMetricFamily(
            f'{self.prefix}streams',
            'Count of streams',
            value=len(streams),
        )

        c = GaugeMetricFamily(
            f'{self.prefix}events_by_stream',
            'Count of events processed by stream',
            labels=['stream'],
        )

        for stream_name, value in m.events_by_stream.items():
            stream = streams[stream_name]
            c.add_metric([str(id(stream))], value)

        yield c

    def get_tasks_metrics(self):
        m = self.faust_app.monitor

        tasks: Dict[str, asyncio.Task] = {}

        for task, task_name in m.task_lookup.items():
            tasks[task_name] = task

        yield GaugeMetricFamily(
            f'{self.prefix}tasks',
            'Count of tasks',
            value=len(tasks),
        )

        c = GaugeMetricFamily(
            f'{self.prefix}events_by_task',
            'Count of events processed by task',
            labels=['task'],
        )

        for task_name, value in m.events_by_task.items():
            task = tasks[task_name]
            c.add_metric([str(id(task))], value)

        yield c
