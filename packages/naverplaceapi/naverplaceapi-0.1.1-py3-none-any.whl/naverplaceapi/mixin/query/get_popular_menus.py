def create(businessId: str, cid: str = "231053", type: str = 'PICKUP'):
    operation_name = "getPopularMenus"
    variables = _define_variables(businessId, cid, type)
    query = {
        "operationName": operation_name,
        "variables": variables,
        "query": QUERY_STATEMENT
    }
    return query


def _define_variables(businessId: str, cid: str = '231053', type='PICKUP'):
    return {
        "bookingBusinessId": businessId,
        "cid":cid,
        "itemType": type,
        "timeout": 3000
    }


QUERY_STATEMENT = """
     query getPopularMenus($input: PopularMenusInput) {
      popularMenus(input: $input) {
        hasPopular
        items {
          id
          name
          bookingCount
          price
          normalPrice
          imageUrl
          menuListUrl
          menuUrl
          isPopular
          images
          score
          __typename
        }
        __typename
      }
    }
"""
