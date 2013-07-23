__author__ = 'Brian'
import json
from django.utils.text import slugify
"""
Idea is to generate json code from some very seldomly changing data
"""
data = []

# A user
data.append({
    "pk": 1,
    "model": "auth.user",
    "fields": {
        "email": "hardbyte@gmail.com"
    }
})

