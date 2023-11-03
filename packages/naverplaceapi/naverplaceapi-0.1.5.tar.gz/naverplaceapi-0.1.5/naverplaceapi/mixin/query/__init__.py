from . import get_visitor_reviews
from . import get_visitor_review_stats
from . import get_ugc_reviews
from . import get_restaurants
from . import get_visitor_review_theme_lists
from . import get_visitor_review_photos_in_visitor_review_tab
from . import get_promotions
from . import get_booking_items
from . import get_announcements
from . import get_popular_menus
from . import get_restaurant


Query = {
    "get_announcement": get_announcements,
    "get_restaurants": get_restaurants,
    "get_popular_menus": get_popular_menus,
    "get_visitor_reviews": get_visitor_reviews,
    "get_ugc_reviews": get_ugc_reviews,
    "get_visitor_review_stats": get_visitor_review_stats,
    "get_visitor_review_photos_in_visitor_review_tab": get_visitor_review_photos_in_visitor_review_tab,
    "get_visitor_review_theme_lists": get_visitor_review_theme_lists,
    "get_promotions": get_promotions,
    "get_booking_items":get_booking_items,
    "get_restaurant": get_restaurant
}

__all__ = [get_restaurants]