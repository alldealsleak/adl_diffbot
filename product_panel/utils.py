from main.utils import unix_to_datetime, CURRENCY_CODES


def display_product_row(product, country_code):
    """
    Returns product row to be displayed in datatable listings
    """
    title = u'{}'.format(product[1]).encode('utf-8')
    company = u'{}'.format(product[2]).encode('utf-8')
    merchant = u'{}'.format(product[3]).encode('utf-8')
    created = unix_to_datetime(product[4])
    offer_price = product[5]
    regular_price = product[6]
    product_link = product[7]
    media_link = product[8]
    category = product[9]

    title_with_link = '<a href="{}">{}</a>'.format(product_link, title)
    if media_link:
        media_image = u'<img src="{}" width="50px" height="60px">'.format(media_link).encode('utf-8')
    else:
        media_image = ''

    offer_price = '{} {:,.2f}'.format(CURRENCY_CODES[country_code], offer_price)
    regular_price = '{} {:,.2f}'.format(CURRENCY_CODES[country_code], regular_price)
    product_data = [
        title_with_link,
        company.title(),
        merchant.title(),
        category.capitalize(),
        created.strftime('%Y-%m-%d'),
        offer_price,
        regular_price,
        media_image
    ]

    return product_data
