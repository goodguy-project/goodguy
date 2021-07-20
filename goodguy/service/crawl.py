import asyncio

import grpc
from cachetools.func import ttl_cache
from retrying import retry

from goodguy.pb import crawl_service_pb2
from goodguy.pb import crawl_service_pb2_grpc
from goodguy.util.catch_exception import catch_exception
from goodguy.util.config import GLOBAL_CONFIG


@catch_exception(ret=crawl_service_pb2.RecentContest())
@ttl_cache(ttl=3600)
@retry(stop_max_attempt_number=5, wait_fixed=20, wrap_exception=True)
async def get_recent_contest(platform: str) -> crawl_service_pb2.RecentContest:
    host = GLOBAL_CONFIG.get("crawl_service.host", "localhost")
    port = GLOBAL_CONFIG.get("crawl_service.port", 50051)
    with grpc.insecure_channel(f'{host}:{port}') as channel:
        stub = crawl_service_pb2_grpc.CrawlServiceStub(channel)
        return stub.GetRecentContest(crawl_service_pb2.GetRecentContestRequest(
            platform=platform,
        ))


@catch_exception(ret=crawl_service_pb2.UserContestRecord())
@ttl_cache(ttl=3600)
@retry(stop_max_attempt_number=5, wait_fixed=20, wrap_exception=True)
async def get_user_contest_record(platform: str, handle: str) -> crawl_service_pb2.UserContestRecord:
    host = GLOBAL_CONFIG.get("crawl_service.host", "localhost")
    port = GLOBAL_CONFIG.get("crawl_service.port", 50051)
    with grpc.insecure_channel(f'{host}:{port}') as channel:
        stub = crawl_service_pb2_grpc.CrawlServiceStub(channel)
        return stub.GetUserContestRecord(crawl_service_pb2.GetUserContestRecordRequest(
            platform=platform,
            handle=handle,
        ))


if __name__ == '__main__':
    print(str(asyncio.run(get_recent_contest('codeforces'))))
