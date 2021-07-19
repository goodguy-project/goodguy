import logging

import grpc
from cachetools.func import ttl_cache
from retrying import retry

import goodguy.pb.crawl_service_pb2 as crawl_service_pb2
import goodguy.pb.crawl_service_pb2_grpc as crawl_service_pb2_grpc
from goodguy.util.catch_exception import catch_exception
from goodguy.util.config import GLOBAL_CONFIG


@catch_exception(ret=crawl_service_pb2.RecentContest())
@ttl_cache(ttl=3600)
@retry(stop_max_attempt_number=5, wait_fixed=20, wrap_exception=True)
def get_recent_contest(platform: str) -> crawl_service_pb2.RecentContest:
    host = GLOBAL_CONFIG.get("crawl_service.host", "localhost")
    port = GLOBAL_CONFIG.get("crawl_service.port", 50051)
    with grpc.insecure_channel(f'{host}:{port}') as channel:
        stub = crawl_service_pb2_grpc.CrawlServiceStub(channel)
        return stub.GetRecentContest(crawl_service_pb2.GetRecentContestRequest(
            platform=platform,
        ))


if __name__ == '__main__':
    print(str(get_recent_contest('codeforces')))
