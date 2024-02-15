import pytest
from pamps.config import settings

url_version = settings.version_api.VERSION_API_STR

@pytest.mark.order(1)
def test_post_create_user1(api_client_user1):
    """Cria 2 posts com um usuário"""
    for n in(1,2):
        response = api_client_user1.post(
            f"{url_version}/post/",
            json={
                "text": f"hello test {n}",
            },
        )
        assert response.status_code == 201
        result = response.json()
        assert result["text"] == f"hello test {n}"
        assert result["parent_id"] is None

@pytest.mark.order(2)
def test_reply_on_post_1(api_client, api_client_user1, api_client_user2):
    """ Cada usuário adicionará uma resposta à primeira postagem """
    posts = api_client.get(f"{url_version}/post/user/user1/").json()
    first_post = posts[0]
    for n, client in enumerate((api_client_user1, api_client_user2),1):
        response = client.post(
            f"{url_version}/post/",
            json={
                "text": f"resposta do user{n}",
                "parent_id": first_post["id"],
            }
        )

        assert response.status_code == 201
        result = response.json()
        assert result["text"] == f"resposta do user{n}"
        assert result["parent_id"] == first_post["id"]

@pytest.mark.order(3)
def test_post_list_without_replies(api_client):
    response = api_client.get(f"{url_version}/post/")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    for result in results:
        assert result["parent_id"] is None
        assert "hello test" in result["text"]

@pytest.mark.order(3)
def test_post1_detail(api_client):
    posts = api_client.get(f"{url_version}/post/user/user1").json()
    first_post = posts[0]
    first_post_id = first_post["id"]

    response = api_client.get(f"{url_version}/post/{first_post_id}/")
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == first_post_id
    assert result["user_id"] == first_post["user_id"]
    assert result["text"] == "hello test 1"
    assert result["parent_id"] is None
    replies = result["replies"]
    assert len(replies) == 2
    for reply in replies:
        assert reply["parent_id"] == first_post_id
        assert "resposta do user" in reply["text"]

@pytest.mark.order(3)
def test_all_posts_from_user1(api_client):
    response = api_client.get(f"{url_version}/post/user/user1")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    for result in results:
        assert result["parent_id"] is None
        assert "hello test" in result["text"]

@pytest.mark.order(3)
def test_all_posts_from_user1_with_replies(api_client):
    response = api_client.get(
        f"{url_version}/post/user/user1", params={"include_replies": True}
    )
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 3