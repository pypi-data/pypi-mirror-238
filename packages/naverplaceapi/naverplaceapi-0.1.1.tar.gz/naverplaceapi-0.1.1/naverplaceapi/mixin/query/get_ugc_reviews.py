def create(id: str, page_no: int, page_cnt: int):
    operation_name = 'getUgcReviewList'
    variables = _define_variables(id, page_no, page_cnt)
    query = {
        "operationName": operation_name,
        "variables": variables,
        "query": QUERY_STATEMENT
    }
    return query


def _define_variables(id: str, page_no: int, page_cnt: int):
    return {
        "businessId": id,
        "display": page_cnt,
        "start": page_no
    }


QUERY_STATEMENT = 'query getUgcReviewList($businessId: String) {\n  restaurant(id: $businessId, isNx: false, deviceType: "mobile") {\n    fsasReviews {\n      ...FsasReviews\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FsasReviews on FsasReviewsResult {\n  total\n  maxItemCount\n  items {\n    name\n    type\n    typeName\n    url\n    home\n    id\n    title\n    rank\n    contents\n    bySmartEditor3\n    hasNaverReservation\n    thumbnailUrl\n    thumbnailUrlList\n    thumbnailCount\n    date\n    isOfficial\n    isRepresentative\n    profileImageUrl\n    isVideoThumbnail\n    reviewId\n    authorName\n    createdString\n    __typename\n  }\n  __typename\n}\n'
