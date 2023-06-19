import asyncio
import os
from json import load

import pytest
from catleg.query import (
    _article_from_legifrance_reply,
    _get_legifrance_credentials,
    get_backend,
)


@pytest.mark.skipif(
    _get_legifrance_credentials(raise_if_missing=False)[0] is None,
    reason="this test requires legifrance credentials",
)
def test_query_article():
    back = get_backend("legifrance")
    article = asyncio.run(back.article("LEGIARTI000038814944"))
    assert "logement" in article.text


@pytest.mark.skipif(
    _get_legifrance_credentials(raise_if_missing=False)[0] is None,
    reason="this test requires legifrance credentials",
)
def test_query_articles():
    back = get_backend("legifrance")
    art1, art2 = asyncio.run(
        back.articles(["LEGIARTI000038814944", "LEGIARTI000038814948"])
    )
    assert "logement" in art1.text
    assert "pacte" in art2.text


def test_no_extraneous_nota():
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.dirname(path_to_current_file)
    article_path = os.path.join(current_directory, "LEGIARTI000038814944.json")
    with open(article_path, "r") as f:
        article = load(f)
    res = _article_from_legifrance_reply(article)
    assert "NOTA" not in res.text
