from goodguy.pb import crawl_service_pb2


def user_contest_record_parser(handle: str, platform: str,
                               user_contest_record: crawl_service_pb2.UserContestRecord) -> str:
    return "\n".join([f"{key}: {value}" for key, value in (
        ('handle', handle),
        ('platform', platform),
        ('rating', user_contest_record.rating),
        ('contest length', user_contest_record.length),
    )])
