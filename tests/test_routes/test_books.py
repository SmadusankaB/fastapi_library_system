from main import app
import json


#  Test cases
#  API: "/books/"
#  Function: create_book


def test_create_book(client, normal_user_token_headers, db_session):
    data = {
        "title": "Title",
        "author": "Author",
        "isbn": "978-0-9767736-6-5",
        "publication_date": "2023-08-10",
        "date_posted": "2023-08-10",
    }
    response = client.post(
        "/books/create-book/",
        data=json.dumps(data),
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["author"] == "Author"
    assert response.json()["isbn"] == "978-0-9767736-6-5"


def test_read_book(client, normal_user_token_headers, db_session):
    data = {
        "title": "Title",
        "author": "Author",
        "isbn": "0-9767736-6-X or 978-0-9767736-6-5",
        "publication_date": "2023-08-10",
        "date_posted": "2023-08-10",
    }
    response = client.post(
        "/books/create-book/",
        data=json.dumps(data),
        headers=normal_user_token_headers,
    )

    response = client.get("/books/get/1/")
    assert response.status_code == 200


# def test_read_books(client, normal_user_token_headers, db_session):
#     data = {
#         "title": "Title",
#         "author": "Authora",
#         "isbn": "0-9767736-6-X or 978-0-9767736-6-5",
#         "publication_date": "2023-08-10",
#         "date_posted": "2023-08-10",
#     }
#     client.post(
#         "/books/create-book/", data=json.dumps(data), headers=normal_user_token_headers
#     )
#     client.post(
#         "/books/create-book/", data=json.dumps(data), headers=normal_user_token_headers
#     )

#     response = client.get("/books/all/")
#     assert response.json() == 200


# def test_update_a_book(client, normal_user_token_headers):
#    data = {
#      "title": "Title",
#     "author": "Authora",
#     "isbn": "0-9767736-6-X or 978-0-9767736-6-5",
#     "publication_date": "2023-08-10",
#     "date_posted": "2023-08-10",
# }
#     client.post(
#         "/books/create-book/", data=json.dumps(data), headers=normal_user_token_headers
#     )
#     data["title"] = "test new title"
#     response = client.put("/books/update/1", json.dumps(data))
#     assert response.json()["msg"] == "Successfully updated data."


# def test_delete_a_book(client, normal_user_token_headers):
#     data = {
#         "title": "Title",
#         "author": "Author",
#         "isbn": "0-9767736-6-X or 978-0-9767736-6-5",
#         "publication_date": "2023-08-10",
#         "date_posted": "2023-08-10",
#     }
#     response = client.post(
#         "/books/create-book/", data=json.dumps(data), headers=normal_user_token_headers
#     )
#     # client.delete("/books/delete/1", headers=normal_user_token_headers)
#     # response = client.get("/books/get/1/")
#     assert response.status_code == status.HTTP_200_OK
