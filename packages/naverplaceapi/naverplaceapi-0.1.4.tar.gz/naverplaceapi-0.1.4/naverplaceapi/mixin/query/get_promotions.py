def create(businessId:str, is_booking:bool = False):
# def create(channelId: str, isBooking: bool):
    operation_name = "getPromotions"
    variables = _define_variables(businessId, is_booking)
    query = {
        "operationName": operation_name,
        "variables": variables,
        "query": QUERY_STATEMENT
    }
    return query


# def _define_variables(channelId:str, isBooking: bool = False):
def _define_variables(businessId: str, is_booking: bool = False):

    return {
        "channelId": businessId,
        "input":{
            "channelId": businessId
        },
        "isBooking": is_booking
    }


QUERY_STATEMENT = """
    query getPromotions($channelId: String, $input: PromotionInput, $isBooking: Boolean!) {
      naverTalk @skip(if: $isBooking) {
        alarm(channelId: $channelId) {
          friendYn
          validation
          __typename
        }
        __typename
      }
      promotionCoupons(input: $input) {
        total
        naverId
        coupons {
          promotionSeq
          placeSeq
          couponSeq
          userCouponSeq
          promotionTitle
          conditionType
          couponUseType
          title
          description
          type
          expiredDateDescription
          status
          image {
            url
            width
            height
            desc
            __typename
          }
          downloadableCountInfo
          expiredPeriodInfo
          usedConditionInfos
          couponButtonText
          daysBeforeCouponStartDate
          usableLandingUrl {
            useSiteUrl
            useBookingUrl
            useOrderUrl
            __typename
          }
          couponUsableDetail {
            isImpPlace
            isImpBooking
            isImpOrder
            __typename
          }
          __typename
        }
        __typename
      }
    }
"""