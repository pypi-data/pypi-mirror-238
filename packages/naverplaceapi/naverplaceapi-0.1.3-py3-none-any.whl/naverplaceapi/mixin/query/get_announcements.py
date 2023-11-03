def create(businessId: str, businessType: str = "restaurant", deviceType: str = "pcmap"):
    operation_name = "getAnnouncements"
    variables = _define_variables(businessId, businessType, deviceType)
    query = {
        "operationName": operation_name,
        "variables": variables,
        "query": QUERY_STATEMENT
    }
    return query


def _define_variables(businessId: str, businessType: str, deviceType: str):
    return {
        "businessId": businessId,
        "businessType": businessType,
        "deviceType": deviceType
    }


QUERY_STATEMENT = """
    query getAnnouncements($businessId: String!, $businessType: String!, $deviceType: String!) {
      announcements: announcementsViaCP0(
        businessId: $businessId
        businessType: $businessType
        deviceType: $deviceType
      ) {
        ...AnnouncementFields
        __typename
      }
    }

    fragment AnnouncementFields on Feed {
      feedId
      category
      title
      relativeCreated
      period
      thumbnail {
        url
        count
        isVideo
        __typename
      }
      __typename
    }
    """
