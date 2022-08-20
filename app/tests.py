from tokenize import PlainToken
from django.test import TestCase
import unittest
from .models import Plan
from django.urls import reverse_lazy

class TestTopPage(TestCase):

    def test_top_page(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

    def test_project_page(self):
        res = self.client.get("/project/")
        self.assertEqual(res.status_code, 200)

    def test_course_page(self):
        res = self.client.get("/course/")
        self.assertEqual(res.status_code, 200)