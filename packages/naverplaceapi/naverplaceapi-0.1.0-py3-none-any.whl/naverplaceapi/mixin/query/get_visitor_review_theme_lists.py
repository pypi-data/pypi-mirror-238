def create(id: str, page_no:int, page_size:int):
    query = {
        "operationName": "getVisitorReviewThemeLists",
        "variables": _define_variables(id, page_no, page_size),
        "query": QUERY_STATEMENT
    }
    return query


def _define_variables(id: str, page_no:int, page_size:int):
    return {
        "input":{
            "businessId": id,
            "display":page_size,
            "page": page_no
        }
    }


QUERY_STATEMENT = """
query getVisitorReviewThemeLists($input: ThemeListsInput) {
  themeLists(input: $input) {
    themeLists {
      id
      title
      viewCount
      itemCount
      reviews {
        businessName
        reviewBody
        imageUrl
        __typename
      }
      authorNickname
      authorImageUrl
      isFollowing
      themeListUrl
      authorUrl
      __typename
    }
    total
    __typename
  }
}

"""
