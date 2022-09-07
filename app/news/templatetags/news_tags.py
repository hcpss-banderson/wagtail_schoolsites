from django import template

register = template.Library()


@register.simple_tag()
def news_page_date_slug_url(news_page, news_listing):
    url = news_listing.full_url + news_listing.reverse_subpage(
        "news_by_slug",
        args=(
            news_page.first_published_at.year,
            "{0:02}".format(news_page.first_published_at.month),
            "{0:02}".format(news_page.first_published_at.day),
            news_page.slug,
        ),
    )

    return url
