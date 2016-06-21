types = {
    'most_viewed': 'Most Viewed',
    'new': 'New',
    'best': 'Best',
    'categories': 'Categories',
    'tags': 'Tags'
}


def add_types(request):
    return {
        'types': types,
    }
