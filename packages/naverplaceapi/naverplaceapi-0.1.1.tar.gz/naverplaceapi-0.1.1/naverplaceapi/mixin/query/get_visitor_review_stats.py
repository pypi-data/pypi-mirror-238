def create(id: str):
    query = {
        "operationName": "getVisitorReviewStats",
        "variables": {
            "businessType": "restaurant",
            "id": id
        },
        "query": QUERY_STATEMENT
    }
    return query


def _define_variables(id: str):
    return {
        "id": id,
        "businessType": "restaurant",
    }


QUERY_STATEMENT = """query getVisitorReviewStats($id: String, $itemId: String, $businessType: String = "place") {
                                visitorReviewStats(input: {businessId: $id, itemId: $itemId, businessType: $businessType}) {
                                    id
                                    name
                                    review {
                                        avgRating
                                        totalCount
                                        starDistribution {
                                            count
                                            score
                                        }
                                        imageReviewCount
                                        authorCount
                                    }
                                    analysis {
                                        themes {
                                            code
                                            label
                                            count
                                        }
                                        menus {
                                            label
                                            count
                                        }
                                        votedKeyword {
                                            totalCount
                                            reviewCount
                                            userCount
                                            details {
                                                category
                                                code
                                                iconUrl
                                                iconCode
                                                displayName
                                                count
                                                previousRank
                                            }
                                        }
                                    }
                                    visitorReviewsTotal
                                    ratingReviewsTotal
                                }
                            }"""
