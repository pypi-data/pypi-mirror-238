def create(id: str, page_no, page_size):
    query = {
        "operationName": "getVisitorReviewPhotosInVisitorReviewTab",
        "variables": _define_variables(id, page_no, page_size),
        "query": QUERY_STATEMENT
    }
    return query


def _define_variables(id: str, page_no: int, page_size: int):
    return {
        "businessId": id,
        "businessType": 'restaurant',
        "display": page_size,
        "page": page_no
    }


QUERY_STATEMENT = """
query getVisitorReviewPhotosInVisitorReviewTab($businessId: String!, $businessType: String, $page: Int, $display: Int, $theme: String, $item: String) {
  visitorReviews(
    input: {businessId: $businessId, businessType: $businessType, page: $page, display: $display, theme: $theme, item: $item, isPhotoUsed: true}
  ) {
    items {
      id
      rating
      author {
        id
        nickname
        from
        imageUrl
        borderImageUrl
        objectId
        url
        __typename
      }
      body
      thumbnail
      media {
        type
        thumbnail
        videoId
        videoOriginSource
        __typename
      }
      tags
      status
      visited
      originType
      item {
        name
        code
        options
        __typename
      }
      businessName
      isFollowing
      visitCount
      votedKeywords {
        code
        iconUrl
        iconCode
        displayName
        __typename
      }
      __typename
    }
    starDistribution {
      score
      count
      __typename
    }
    hideProductSelectBox
    total
    __typename
  }
}
"""
