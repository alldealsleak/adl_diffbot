from main.utils import unix_to_datetime


def display_product_row(product):
    """
    Returns product row to be displayed in datatable listings
    """
    title = u'{}'.format(product[1]).encode('utf-8')
    merchant = u'{}'.format(product[2]).encode('utf-8')
    created = unix_to_datetime(product[3])
    offer_price = product[4]
    regular_price = product[5]
    product_link = product[6]
    media_link = product[7]
    category = product[8]

    title_with_link = '<a href="{}">{}</a>'.format(product_link, title)
    if media_link:
        media_image = u'<img src="{}" width="50px" height="60px">'.format(media_link).encode('utf-8')
    else:
        media_image = ''
    product_data = [
        title_with_link,
        merchant,
        category,
        created.strftime('%Y-%m-%d'),
        offer_price,
        regular_price,
        media_image
    ]

    return product_data
