"""Functions to help tracing the application, i.e. via logging.
"""
import logging
import multiprocessing

import humanize

logger = logging.getLogger(__name__)


class DownloadTracer:
    """Log meta-info about any long-running download task.

    Note: This is Thread-safe -- can be used with "`multiprocessing.dummy`" package.
        Downloads are I/O bound anyhow, so multithreading works well. 

    WARNING: This is _not_ concurrency-safe. Do not use this with "`multiprocessing.Pool`" directly.
    """
    def __init__(self, service_name: str, log_every_count_bytes:int = 10000):
        self._name = service_name
        self._threshold = log_every_count_bytes
        self._total_bytes_downloaded = 0
        self._prior_logged_total_bytes_downloaded = 0
        self._lock = multiprocessing.Lock()

    @property
    def total_bytes(self):
        return self._total_bytes_downloaded

    def trace(self, data_len: int):
        """Add data_len to the running total.
        """
        self._lock.acquire()
        try:
            self._total_bytes_downloaded += data_len
            if self._total_bytes_downloaded > self._threshold + self._prior_logged_total_bytes_downloaded:
                logger.info(f'Total downloaded from {self._name}: {humanize.naturalsize(self._total_bytes_downloaded)}')
                self._prior_logged_total_bytes_downloaded = self._total_bytes_downloaded
        finally:
            self._lock.release()


one_kilobyte = 1000
one_megabyte = 1000 * one_kilobyte

netdot_download_tracer = DownloadTracer('Netdot', one_megabyte)
# alias to enable trace.downloads(response)
netdot_downloads = netdot_download_tracer.trace
