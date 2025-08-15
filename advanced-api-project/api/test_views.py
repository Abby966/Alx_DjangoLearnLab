# api/test_views.py
from datetime import date
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Author, Book

class BookAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author1 = Author.objects.create(name="Chinua Achebe")
        cls.author2 = Author.objects.create(name="Ngũgĩ wa Thiong'o")
        cls.book1 = Book.objects.create(title="Things Fall Apart", publication_year=1958, author=cls.author1)
        cls.book2 = Book.objects.create(title="No Longer at Ease", publication_year=1960, author=cls.author1)
        cls.book3 = Book.objects.create(title="Petals of Blood", publication_year=1977, author=cls.author2)

        User = get_user_model()
        cls.user = User.objects.create_user(username="tester", password="pass12345")

        cls.url_list    = reverse("book-list")
        cls.url_detail1 = reverse("book-detail", kwargs={"pk": cls.book1.pk})
        cls.url_create  = reverse("book-create")
        cls.url_update1 = reverse("book-update", kwargs={"pk": cls.book1.pk})
        cls.url_delete1 = reverse("book-delete", kwargs={"pk": cls.book1.pk})

    def setUp(self):
        self.client = APIClient()

    # -------- Read (public) --------
    def test_book_list_public(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure response.data is a list-like and contains our titles
        titles = {item["title"] for item in response.data}
        self.assertIn("Things Fall Apart", titles)
        self.assertIn("No Longer at Ease", titles)

    def test_book_detail_public(self):
        response = self.client.get(self.url_detail1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Things Fall Apart")

    # -------- Write (auth required) --------
    def test_book_create_requires_auth(self):
        payload = {"title": "Arrow of God", "publication_year": 1964, "author": self.author1.id}
        response = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # unauth must be 401

        self.client.login(username="tester", password="pass12345")
        response = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Arrow of God")

    def test_book_update_requires_auth(self):
        payload = {"title": "Things Fall Apart (Updated)"}
        response = self.client.patch(self.url_update1, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.login(username="tester", password="pass12345")
        response = self.client.patch(self.url_update1, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Things Fall Apart (Updated)")

    def test_book_delete_requires_auth(self):
        response = self.client.delete(self.url_delete1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.login(username="tester", password="pass12345")
        response = self.client.delete(self.url_delete1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    # -------- Filtering / Searching / Ordering --------
    def test_filter_by_author_id(self):
        response = self.client.get(self.url_list, {"author": self.author1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure only author1 books are present using response.data
        author_ids = {item["author"] for item in response.data}
        self.assertTrue(self.author2.id not in author_ids)

    def test_search_title(self):
        response = self.client.get(self.url_list, {"search": "Things"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data]
        self.assertIn("Things Fall Apart", titles)

    def test_ordering_by_year_desc(self):
        response = self.client.get(self.url_list, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [item["publication_year"] for item in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    # -------- Validation --------
    def test_future_publication_year_rejected(self):
        future_year = date.today().year + 1
        payload = {"title": "Future Book", "publication_year": future_year, "author": self.author1.id}
        self.client.login(username="tester", password="pass12345")
        response = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("future" in " ".join(map(str, response.data.get("publication_year", []))).lower())
