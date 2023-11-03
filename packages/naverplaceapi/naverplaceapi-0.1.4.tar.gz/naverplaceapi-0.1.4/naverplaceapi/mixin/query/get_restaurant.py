def create(businessId: str):
    operation_name = "restaurant"
    variables = _define_variables(businessId)
    query = {
        "operationName": operation_name,
        "variables": variables,
        "query": QUERY_STATEMENT
    }
    return query


def _define_variables(businessId: str):
    return {
        "deviceType": "pcmap",
        "businessId": businessId,
        "isNx": False
    }


QUERY_STATEMENT = """
query restaurant($businessId: String) {
  restaurant(id: $businessId, isNx: false, deviceType: "pcmap") {
    base {
      address
      baemin {
        businessHours {
          deliveryTime {
            start
            end
            __typename
          }
          closeDate {
            start
            end
            __typename
          }
          temporaryCloseDate {
            start
            end
            __typename
          }
          __typename
        }
        __typename
      }
      # bookingAwards
      bookingBusinessId
      bookingButtonName
      bookingDisplayName
      bookingHubButtonName
      broadcastInfos {
        program
        date
        menu
        __typename
      }
      businessHours {
        day
        description
        endTime
        hourString
        index
        isDayOff
        startTime
        __typename
      }
      category
      categoryCode
      categoryCodeList
      categoryCount
      cescoCheck
      # cescoLink
      cescofsCheck
      # cescofsLink
      chatBotUrl
      conveniences
      coordinate {
        x
        y
        mapZoomLevel
        __typename
      }
      dbType
      defaultCategoryCodeList
      description
      detailPath
      # driveThru
      # easyOrder
      # foodSafetyInfo
      giftCards
      gifticonId
      gifticonMoreUrl
      hasAiCall
      hasOfficialImages
      hasSmartOrder
      hideBusinessHours
      hidePrice
      homepages {
        # etc
        repr {
          isDeadUrl
          isRep
          landingUrl
          order
          type
          url
          __typename
        }
        __typename
      }
      id
      images {
        desc
        height
        infoTitle
        number
        origin
        source
        url
        width
      }
      imagesLastModified
      imagesLastModifiedDate
      is100YearCertified
      isEasyOrder
      isForcedTakeOut
      isKtis
      isRelaxRestaurant
      isStarbucks
      keywords
      mapUrl
      menuImages {
        imageUrl
      }
      # menuSource
      menus {
        change
        description
        id
        images
        index
        name
        price
        priceType
        priority
        recommend
      }
      # mfds
      # michelinGuide
      microReviews
      missingInfo {
        isBizHourMissing
        isMenuImageMissing
        isAccessorMissing
        isBoss
        isConveniencesMissing
        isDescriptionMissing
        needLargeSuggestionBanner
        __typename
      }
      moreBookingReviewsPath
      moreFsasReviewsPath
      morePhotosPath
      moreUGCReviewsPath
      nPayPromotion
      name
      # naverBlog
      naverBookingHubUrl
      # naverBookingPromotion
      naverBookingUrl
      newOpening
      # openingHours
      paymentInfo
      phone
      poiInfo {
        # polyline
        # polygon
        __typename
      }
      # preOrder
      promotionTitle
      rcode
      relatedLinks {
        clickCode
        iconName
        name
        url
        __typename
      }
      reportWrongInfoType
      reviewSettings {
        blog
        cafe
        keyword
        showVisitorReviewScore
        __typename
      }
      road
      roadAddress
      routeUrl
      siteId
      staticMapUrl
      streetPanorama {
        id
        lat
        lon
        pan
        tilt
        __typename
      }
      # tableOrder
      # takeOut
      talktalkUrl
      themes
      virtualPhone
      visitorReviewsScore
      visitorReviewsTextReviewTotal
      visitorReviewsTotal
      zoomLevel
      __typename
    }
    bookingItems {
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
    brandPromotion {
      brandDirNum
      brandLogoImage
      brandMobileUrl
      brandPcUrl
      brandPhone
      brandTitle
      eDate
      promotionDetail
      promotionEdate
      promotionEdayOfWeek
      promotionImage
      promotionMobileUrl
      promotionPcUrl
      promotionPlaceImage
      promotionSdate
      promotionSdayOfWeek
      promotionType
      sDate
      status
      __typename
    }
    busStations {
      displayCode
      id
      innerRoutes {
        routeType {
          innerRoute {
            id
            name
            __typename
          }
          type
          typeName
          __typename
        }
        __typename
      }
    }
    businessStats {
      age {
        ageKey
        rank
        value
        __typename
      }
      # alsoSearched
      # contexts
      daily {
        dayKey
        hourly {
          hourKey
          value
          __typename
        }
        __typename
      }
      gender {
        f
        m
        __typename
      }
      lastUpdated
      __typename
    }
    businessTools {
      tools {
        countInString
        description
        link
        title
        type
        using
        __typename
      }
      __typename
    }
    datalabPhotos {
      clusterId
      clusterName
      imageUrl
      items {
        orgPath
        __typename
      }
      __typename
    }
    excludeTargets {
      image
      imageSection
      review
      __typename
    }
    fsasReviews {
      items {
        authorName
        bySmartEditor3
        bypassToken
        contents
        createdString
        date
        hasNaverReservation
        home
        id
        isOfficial
        isRepresentative
        isVideoThumbnail
        name
        profileImageUrl
        rank
        reviewId
        thumbnailCount
        thumbnailUrl
        thumbnailUrlList
        title
        type
        typeName
        url
        __typename
      }
      maxItemCount
      total
      __typename
    }
    hasFeed {
      blogExist
      feedExist
      __typename
    }
    # kinQna
    # navercasts
    ncr {
      festivalSectionHeadInfo
      # festivals
      headInfo
      # performances
      __typename
    }
    newBusinessHours {
      businessHours {
        breakHours {
          start
          end
          __typename
        }
        businessHours {
          end
          start
          __typename
        }
        day
        description
        lastOrderTimes {
          time
          type
          __typename
        }
        __typename
      }
      businessStatusDescription {
        blindDescription
        description
        status
        __typename
      }
      # comingIrregularClosedDays
      comingRegularClosedDays
      freeText
      name
      __typename
    }
    shopWindow {
      # branchNews
      # itemsFromChannelNo
      # itemsFromInterlockId
      typeName
      url
      __typename
    }
    subwayStations {
      color
      name
      no
      priority
      station {
        id
        lat
        lng
        name
        nearestExit
        nearestExitType
        walkTime
        walkingDistance
        __typename
      }
      # transfers
      type
      typeDesc
      __typename
    }
    tabs {
      tabId
      __typename
    }
    # tvcasts
    visitorReviewStats {
      analysis {
        menus {
          count
          label
          __typename
        }
        themes {
          code
          count
          label
          __typename
        }
        votedKeyword {
          details {
            category
            code
            count
            displayName
            iconCode
            iconUrl
            previousRank
            __typename
          }

          reviewCount
          totalCount
          userCount
          __typename
        }
      }
      apolloCacheId
      id
      name
      ratingReviewsTotal
      review {
        authorCount
        avgRating
        imageReviewCount
        maxScoreWithMaxCount
        maxSingleReviewScoreCount
        scores {
          count
          score
          __typename
        }
        starDistribution {
          count
          score
          __typename
        }
        totalCount
        __typename
      }
      visitorReviewsTotal
      __typename
    }
  }

  sasImages(
    input: {
      businessId: $businessId
      businessType: "restaurant"
      display: 30
      excludeAuthorIds: []
      excludeSection: []
    }
  ) {
    items {
      authorThumbnail
      authorname
      date
      height
      imgUrl
      link
      originalUrl
      rank
      section
      subsection
      text
      title
      width
      __typename
    }
    relation
    total
    __typename
  }
  user {
    myplace {
      profile {
        borderImageUrl
        imageUrl
        __typename
      }
      __typename
    }
    partnerHashedIdNo
    __typename
  }
  visitorReviewMediasTotal {
    total
  }
  visitorReviewStats {
    analysis {
      menus {
        count
        label
        __typename
      }
      themes {
        code
        count
        label
        __typename
      }
      votedKeyword {
        details {
          category
          code
          count
          displayName
          iconCode
          iconUrl
          previousRank
          __typename
        }
        reviewCount
        totalCount
        userCount
        __typename
      }
    }
    # apolloCacheId
    id
    name
    ratingReviewsTotal
    review {
      authorCount
      avgRating
      imageReviewCount
      maxScoreWithMaxCount
      maxSingleReviewScoreCount
      scores {
        count
        score
        __typename
      }
      starDistribution {
        count
        score
        __typename
      }
      totalCount
      __typename
    }
    visitorReviewsTotal
    __typename
  }
  visitorReviews {
    hideProductSelectBox
    items {
      author {
        borderImageUrl
        from
        id
        imageUrl
        isFollowing
        nickname
        objectId
        # review
        # theme
        url
        __typename
      }
      body
      businessName
      created
      highlightOffsets
      id
      # item
      language
      media {
        thumbnail
        type
        videoId
        videoOriginSource
        __typename
      }
      originType
      rating
      receiptInfoUrl
      reply {
        body
        created
        editUrl
        editedBy
        isReported
        isSuspended
        replyTitle
        __typename
      }
      status
      tags
      thumbnail
      translatedText
      viewCount
      visitCount
      visited
      __typename
    }
    # starDistribution
    total
    __typename
  }
}

"""
