from app.services.markdown_parser import parse_markdown


def test_duplicate_headings():

    nodes = parse_markdown(
        "data/ct200_manual.md"
    )

    titles = [node.title for node in nodes]

    assert len(titles) > 0

    duplicate_titles = [
        title
        for title in titles
        if titles.count(title) > 1
    ]

    assert duplicate_titles is not None