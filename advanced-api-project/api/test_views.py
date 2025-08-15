# api/test_views.py
"""
Unit tests for Django REST Framework endpoints for the Book model.
Covers:
- CRUD endpoints (list, detail, create, update, delete)
- Permissions (read: public; write: authenticated)
- Filtering (?title=, ?author=, ?publication_year=)
- Searching (?search= on title and author name)
- Ordering (?ordering=title / -publication_year)
- Validation (publication_year cannot be in the future)
"""

from datetime import date
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.models import Author, Book


class BookAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Authors
        cls.author1 = Author.objects.create(name="Chinua Achebe")
        cls.author2 = Author.objects.create(name="Ngũgĩ wa Thiong'o")

        # Books
        cls.book1 = Book.objects.create(
            title="Things Fall Apart", publication_year=1958, author=cls.author1
        )
        cls.book2 = Book.objects.create(
            title="No Longer at Ease", publication_year=1960, author=cls.author1
        )
        cls.book3 = Book.objects.create(
            title="Petals of Blood", publication_year=1977, author=cls.author2
        )

        # Auth user for write ops
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="tester", password="pass12345"
        )

        # Common URLs (names must match api/urls.py)
        cls.url_list = reverse("book-list")               # /api/books/
        cls.url_detail_1 = reverse("book-detail", kwargs={"pk": cls.book1.pk})
        cls.url_create = reverse("book-create")           # /api/books/create/
        cls.url_update_1 = reverse("book-update", kwargs={"pk": cls.book1.pk})
        cls.url_delete_1 = reverse("book-delete", kwargs={"pk": cls.book1.pk})

    def setUp(self):
        self.client = APIClient()

    # -------- Read (public) --------
    def test_book_list_public(self):
        resp = self.client.get(self.url_list)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data), 3)

    def test_book_detail_public(self):
        resp = self.client.get(self.url_detail_1)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["title"], "Things Fall Apart")

    # -------- Write (auth required) --------
    def test_book_create_requires_auth(self):
        payload = {
            "title": "Arrow of God",
            "publication_year": 1964,
            "author": self.author1.id,
        }
        # unauthenticated should be 401/403 depending on auth classes
        resp = self.client.post(self.url_create, payload, format="json")
        self.assertIn(resp.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # login then create
        self.client.login(username="tester", password="pass12345")
        resp2 = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp2.data["title"], "Arrow of God")

    def test_book_update_requires_auth(self):
        payload = {"title": "Things Fall Apart (Updated)"}

        resp = self.client.patch(self.url_update_1, payload, format="json")
        self.assertIn(resp.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        self.client.login(username="tester", password="pass12345")
        resp2 = self.client.patch(self.url_update_1, payload, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertEqual(resp2.data["title"], "Things Fall Apart (Updated)")

    def test_book_delete_requires_auth(self):
        resp = self.client.delete(self.url_delete_1)
        self.assertIn(resp.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        self.client.login(username="tester", password="pass12345")
        resp2 = self.client.delete(self.url_delete_1)
        self.assertEqual(resp2.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    # -------- Filtering --------
    def test_filter_by_title(self):
        resp = self.client.get(self.url_list, {"title": "Things Fall Apart"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(all(b["title"] == "Things Fall Apart" for b in resp.data))

    def test_filter_by_author_id(self):
        resp = self.client.get(self.url_list, {"author": self.author1.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Only books from author1
        titles = {b["title"] for b in resp.data}
        self.assertTrue("Petals of Blood" not in titles)

    def test_filter_by_publication_year(self):
        resp = self.client.get(self.url_list, {"publication_year": 1960})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(all(b["publication_year"] == 1960 for b in resp.data))

    # -------- Searching --------
    def test_search_by_title(self):
        resp = self.client.get(self.url_list, {"search": "Things"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = {b["title"] for b in resp.data}
        self.assertIn("Things Fall Apart", titles)

    def test_search_by_author_name(self):
        resp = self.client.get(self.url_list, {"search": "Achebe"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # all results should be by Achebe
        self.assertTrue(all("Achebe" in Author.objects.get(pk=b["author"]).name for b in resp.data))

    # -------- Ordering --------
    def test_ordering_by_title_asc(self):
        resp = self.client.get(self.url_list, {"ordering": "title"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.data]
        self.assertEqual(titles, sorted(titles))

    def test_ordering_by_year_desc(self):
        resp = self.client.get(self.url_list, {"ordering": "-publication_year"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in resp.data]
        self.assertEqual(years, sorted(years, reverse=True))

    # -------- Validation --------
    def test_future_publication_year_rejected(self):
        future_year = date.today().year + 1
        payload = {"title": "Future Book", "publication_year": future_year, "author": self.author1.id}
        self.client.login(username="tester", password="pass12345")
        resp = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        # Error message should mention "future"
        joined = " ".join(str(v) for v in resp.data.get("publication_year", []))
        self.assertIn("future", joined.lower())
