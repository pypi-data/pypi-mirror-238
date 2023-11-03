def create(keyword, page_no, page_cnt):
    operation_name = "getRestaurants"
    variables = _define_variables(keyword, page_no, page_cnt)
    query = {
        "operationName": operation_name,
        "variables": variables,
        "query": QUERY_STATEMENT
    }
    return query


def _define_variables(keyword: str, page_no: int, page_cnt: int):
    return {
        "input": {"query": keyword, "display": page_cnt, "start": page_no, "isNmap": False, "deviceType": "pcmap"},
        "isNmap": False,
        "isBounds": True
    }


QUERY_STATEMENT = """query getRestaurants(
                        $input: RestaurantsInput
                        $isNmap: Boolean!
                        $isBounds: Boolean!
                        ) {
                        restaurants(input: $input) {
                            total
                            items {
                            ...RestaurantItemFields
                            easyOrder {
                                easyOrderId
                                easyOrderCid
                                businessHours {
                                weekday {
                                    start
                                    end
                                    __typename
                                }
                                weekend {
                                    start
                                    end
                                    __typename
                                }
                                __typename
                                }
                                __typename
                            }
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
                            yogiyo {
                                businessHours {
                                actualDeliveryTime {
                                    start
                                    end
                                    __typename
                                }
                                bizHours {
                                    start
                                    end
                                    __typename
                                }
                                __typename
                                }
                                __typename
                            }
                            __typename
                            }
                            nlu {
                            ...NluFields
                            __typename
                            }
                            brand {
                            name
                            isBrand
                            type
                            menus {
                                order
                                id
                                images {
                                url
                                desc
                                __typename
                                }
                                name
                                desc
                                price
                                isRepresentative
                                detailUrl
                                orderType
                                catalogId
                                source
                                menuId
                                nutrients
                                allergies
                                __typename
                            }
                            __typename
                            }
                            optionsForMap @include(if: $isBounds) {
                            maxZoom
                            minZoom
                            includeMyLocation
                            maxIncludePoiCount
                            center
                            spotId
                            __typename
                            }
                            __typename
                        }
                        }
                        fragment RestaurantItemFields on RestaurantSummary {
                        id
                        dbType
                        name
                        businessCategory
                        category
                        description
                        hasBooking
                        hasNPay
                        x
                        y
                        distance
                        imageUrl
                        imageUrls
                        imageCount
                        phone
                        virtualPhone
                        routeUrl
                        streetPanorama {
                            id
                            pan
                            tilt
                            lat
                            lon
                            __typename
                        }
                        roadAddress
                        address
                        commonAddress
                        blogCafeReviewCount
                        bookingReviewCount
                        totalReviewCount
                        bookingReviewScore
                        bookingUrl
                        bookingHubUrl
                        bookingHubButtonName
                        bookingBusinessId
                        talktalkUrl
                        options
                        promotionTitle
                        agencyId
                        businessHours
                        microReview
                        tags
                        priceCategory
                        broadcastInfo {
                            program
                            date
                            menu
                            __typename
                        }
                        michelinGuide {
                            year
                            star
                            comment
                            url
                            hasGrade
                            isBib
                            alternateText
                            __typename
                        }
                        broadcasts {
                            program
                            menu
                            episode
                            broadcast_date
                            __typename
                        }
                        tvcastId
                        naverBookingCategory
                        saveCount
                        uniqueBroadcasts
                        isDelivery
                        isCvsDelivery
                        markerLabel @include(if: $isNmap) {
                            text
                            style
                            __typename
                        }
                        imageMarker @include(if: $isNmap) {
                            marker
                            markerSelected
                            __typename
                        }
                        isTableOrder
                        isPreOrder
                        isTakeOut
                        bookingDisplayName
                        bookingVisitId
                        bookingPickupId
                        popularMenuImages {
                            name
                            price
                            bookingCount
                            menuUrl
                            menuListUrl
                            imageUrl
                            isPopular
                            usePanoramaImage
                            __typename
                        }
                        visitorReviewCount
                        visitorReviewScore
                        detailCid {
                            c0
                            c1
                            c2
                            c3
                            __typename
                        }
                        streetPanorama {
                            id
                            pan
                            tilt
                            lat
                            lon
                            __typename
                        }
                        __typename
                        }
                        fragment NluFields on Nlu {
                        queryType
                        user {
                            gender
                            __typename
                        }
                        queryResult {
                            ptn0
                            ptn1
                            region
                            spot
                            tradeName
                            service
                            selectedRegion {
                            name
                            index
                            x
                            y
                            __typename
                            }
                            selectedRegionIndex
                            otherRegions {
                            name
                            index
                            __typename
                            }
                            property
                            keyword
                            queryType
                            nluQuery
                            businessType
                            cid
                            branch
                            franchise
                            titleKeyword
                            location {
                            x
                            y
                            default
                            longitude
                            latitude
                            dong
                            si
                            __typename
                            }
                            noRegionQuery
                            priority
                            showLocationBarFlag
                            themeId
                            filterBooking
                            repRegion
                            repSpot
                            dbQuery {
                            isDefault
                            name
                            type
                            getType
                            useFilter
                            hasComponents
                            __typename
                            }
                            type
                            category
                            menu
                            __typename
                        }
                        __typename
                        }
                        """
