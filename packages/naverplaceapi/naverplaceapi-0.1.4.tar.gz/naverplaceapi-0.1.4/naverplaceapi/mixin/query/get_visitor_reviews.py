
def create(id:str, page_no:int, page_cnt:int):
    operation_name = "getVisitorReviews"
    variables = _define_variables(id, page_no, page_cnt)
    query = {
        "operationName": operation_name,
        "variables": variables,
        "query": QUERY_STATEMENT
    }
    return query


def _define_variables(id:str, page_no: int, page_cnt:int):
    return {
        "input": {
            "businessId": id,
            "bookingBusinessId": "null",
            "display": page_cnt,
            "page": page_no,
            "includeContent": True,
        },
        "id": id,
    }

QUERY_STATEMENT = """query getVisitorReviews($input: VisitorReviewsInput) {
                                visitorReviews(input: $input) {
                                    items {
                                    id
                                    rating
                                    author {
                                        id
                                        nickname
                                        from
                                        imageUrl
                                        objectId
                                        url
                                        review {
                                        totalCount
                                        imageCount
                                        avgRating
                                        __typename
                                        }
                                        theme {
                                        totalCount
                                        __typename
                                        }
                                        __typename
                                    }
                                    body
                                    thumbnail
                                    media {
                                        type
                                        thumbnail
                                        class
                                        __typename
                                    }
                                    tags
                                    status
                                    visitCount
                                    viewCount
                                    visited
                                    created
                                    reply {
                                        editUrl
                                        body
                                        editedBy
                                        created
                                        replyTitle
                                        __typename
                                    }
                                    originType
                                    item {
                                        name
                                        code
                                        options
                                        __typename
                                    }
                                    language
                                    highlightOffsets
                                    apolloCacheId
                                    translatedText
                                    businessName
                                    showBookingItemName
                                    showBookingItemOptions
                                    bookingItemName
                                    bookingItemOptions
                                    votedKeywords {
                                        code
                                        iconUrl
                                        iconCode
                                        displayName
                                        __typename
                                    }
                                    userIdno
                                    isFollowing
                                    followerCount
                                    followRequested
                                    loginIdno
                                    receiptInfoUrl
                                    __typename
                                    }
                                    starDistribution {
                                    score
                                    count
                                    __typename
                                    }
                                    hideProductSelectBox
                                    total
                                    showRecommendationSort
                                    __typename
                                }
                                }"""