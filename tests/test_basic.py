from pydiff import resolve_diff


def test_abc():
    snippet_a = (
        "# Router definition",
        "api_router = APIRouter()"
    )
    snippet_b = (
        "# Make sure endpoint are immune to missing trailing slashes",
        "api_router = APIRouter(redirect_slashes=True)"
    )
    snippet_c = (
        "# Router definition",
        "\napi_router = APIRouter(",
        "\n\tredirect_slashes=True",
        "\n)"
    )

    res_ab = "- api_router = APIRouter()\n+ api_router = APIRouter(redirect_slashes=True)"
    res_bc = ""

    assert res_ab == resolve_diff(snippet_a, snippet_b)
    assert res_bc == resolve_diff(snippet_b, snippet_c)


if __name__ == '__main__':
    test_abc()
