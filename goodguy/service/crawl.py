import logging

import grpc
from cachetools.func import ttl_cache
from retrying import retry, RetryError

import goodguy.pb.crawl_service_pb2 as crawl_service_pb2
import goodguy.pb.crawl_service_pb2_grpc as crawl_service_pb2_grpc
from goodguy.util.config import GLOBAL_CONFIG


def get_recent_contest(platform: str) -> crawl_service_pb2.RecentContest:
    @ttl_cache(ttl=3600)
    @retry(stop_max_attempt_number=5, wait_fixed=20, wrap_exception=True)
    def inner() -> crawl_service_pb2.RecentContest:
        host = GLOBAL_CONFIG.get("crawl_service.host", "")
        port = GLOBAL_CONFIG.get("crawl_service.port", 50051)
        with grpc.insecure_channel(f'{host}:{port}') as channel:
            stub = crawl_service_pb2_grpc.CrawlServiceStub(channel)
            return stub.GetRecentContest(crawl_service_pb2.GetRecentContestRequest(
                platform=platform,
            ))

    try:
        return inner()
    except RetryError as e:
        logging.exception(e)
    return crawl_service_pb2.RecentContest()
