def create(businessId: str, businessType: str = "restaurant", type: str = 'STANDARD'):
    operation_name = "getBookingItems"
    variables = _define_variables(businessId, businessType, type)
    query = {
        "operationName": operation_name,
        "variables": variables,
        "query": QUERY_STATEMENT
    }
    return query


def _define_variables(businessId: str, businessType: str = 'restaurant', type: str = 'STANDARD'):
    return {
        "bizItemTypes": [type],
        "businessId": businessId,
        "businessType": businessType,
        "timeout": 3000
    }


QUERY_STATEMENT = """
    query getBookingItems($id: String, $businessType: String, $bizItemTypes: [String], $timeout: Int) {
      bookingItems(
        input: {bookingBusinessId: $id, businessType: $businessType, bizItemTypes: $bizItemTypes, timeout: $timeout}
      ) {
        items {
          id
          businessId
          name
          isNPayUsed
          desc
          bookingUrl
          imageUrls
          bizItemType
          reviewStat {
            score
            count
            __typename
          }
          originalBookingUrl
          __typename
        }
        __typename
      }
      visitorReviewStatsByBookingBusinessId(input: {bookingBusinessId: $id}) {
        items {
          id
          itemId
          score
          count
          __typename
        }
        __typename
      }
    }
"""
