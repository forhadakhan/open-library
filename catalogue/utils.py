# Define menu options for dashboard as a list of dictionaries
dashboard_menu_options = [
    {"title": "All Books", "url_name": "all_books", "icon": "bi bi-book"},
    {"title": "Add Book", "url_name": "add_book", "icon": "bi bi-plus-square", "staff_only": True},
    {"title": "My Favorites", "url_name": "favorite_books", "icon": "bi bi-heart-half"},
    {"title": "Members", "url_name": "all_users", "icon": "bi bi-people", "staff_only": True}
]

def validate_rating(rating):
    """
    Validates if the rating is within the range of 1 to 5.

    Args:
        rating (int): The rating to be validated.

    Returns:
        int: The validated rating.

    Raises:
        ValueError: If the rating is not within the range of 1 to 5.
    """
    rating = int(rating)
    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5")
    return rating