from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from openai import OpenAI
from enum import Enum
import random
import os


class OpenAIModels(str, Enum):
    GPT_4O_MINI = "gpt-4o_mini"
    GPT_41_MINI = "gpt-4.1-mini"
    GPT_41_NANO = "gpt-4.1-nano"


MODEL = OpenAIModels.GPT_41_NANO

client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))


bible_books_catholic_en = [
    # Old Testament
    "genesis",
    "exodus",
    "leviticus",
    "numbers",
    "deuteronomy",
    "joshua",
    "judges",
    "ruth",
    "1-samuel",
    "2-samuel",
    "1-kings",
    "2-kings",
    "1-chronicles",
    "2-chronicles",
    "ezra",
    "nehemiah",
    "tobit",
    "judith",
    "esther",
    "job",
    "psalms",
    "proverbs",
    "ecclesiastes",
    "song-of-songs",
    "wisdom",
    "sirach",
    "isaiah",
    "jeremiah",
    "lamentations",
    "baruch",
    "ezekiel",
    "daniel",
    "hosea",
    "joel",
    "amos",
    "obadiah",
    "jonah",
    "micah",
    "nahum",
    "habakkuk",
    "zephaniah",
    "haggai",
    "zechariah",
    "malachi",
    "1-maccabees",
    "2-maccabees",
    # New Testament
    "matthew",
    "mark",
    "luke",
    "john",
    "acts",
    "romans",
    "1-corinthians",
    "2-corinthians",
    "galatians",
    "ephesians",
    "philippians",
    "colossians",
    "1-thessalonians",
    "2-thessalonians",
    "1-timothy",
    "2-timothy",
    "titus",
    "philemon",
    "hebrews",
    "james",
    "1-peter",
    "2-peter",
    "1-john",
    "2-john",
    "3-john",
    "jude",
    "revelation",
]

languages = {"en": "English", "es": "Español", "fr": "Français"}


def home(request):
    return HttpResponseRedirect(reverse("home-lang", args=["en"]))


def home_lang(request, lang):
    if lang not in languages:
        return HttpResponseNotFound(f"Language '{lang}' is not available")
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Styled Link Div</title>
        <style>
            /* 0. Centers the H1 heading */
            h1 {
                text-align: center;
                margin-top: 40px;
                font-family: sans-serif;
                color: #222;
            }
            /* 1. Remove the link styling from the anchor tag */
            .wrapper-link {
                text-decoration: none;
                color: inherit; /* Keeps text color black/natural instead of blue */
                display: block; /* Makes the entire area clickable */
            }

            /* 2. Style the div container */
            .custom-box {
                text-align: center;      /* Centers the text inside */
                border: 2px solid #333;  /* The border */
                padding: 30px;           /* Space inside the border */
                margin: 20px;            /* Space outside the border */
                border-radius: 8px;      /* Optional: rounds the corners slightly */
                transition: background 0.3s; /* Smooth transition for hover */
            }

            /* 3. Optional: Add a hover effect so users know it's a link */
            .custom-box:hover {
                background-color: #f0f0f0;
                border-color: #007bff;
            }

            /* 4. The Container for the buttons */
            .button-row {
                display: flex;         /* Turns on Flexbox */
                text-align: center;         
                gap: 10px;             /* Adds a small space between buttons */
                margin: 20px;
                padding: 30px;  
                border: 2px solid #333;  /* The border */
                border-radius: 8px;
            }

            /* 5. The Anchor tags acting as buttons */
            .lang-button {
                flex: 1;               /* Forces all buttons to be the exact same size */
                text-align: center;    /* Centers text inside */
                text-decoration: none; /* Removes underline */
                color: white;          /* Text color */
                background-color: #333;/* Button color */
                padding: 15px 0;       /* Vertical padding */
                border-radius: 5px;    /* Slightly rounded corners */
                font-family: sans-serif;
                font-weight: bold;
                transition: background 0.3s;
            }

            /* 6. Hover effect */
            .lang-button:hover {
                background-color: #555;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
    """
    match lang:
        case "es":
            html += "<h1>Versos de la Biblia</h1>"
        case "fr":
            html += "<h1>Versets Bibliques</h1>"
        case _:
            html += "<h1>Bible Verses</h1>"

    url_en = reverse("home-lang", args=["en"])
    url_es = reverse("home-lang", args=["es"])
    url_fr = reverse("home-lang", args=["fr"])

    html += f"""
    <div class="button-row">
        <a href="{url_en}" class="lang-button">English</a>
        <a href="{url_es}" class="lang-button">Español</a>
        <a href="{url_fr}" class="lang-button">Français</a>
    </div>
    """
    messages = [
        {
            "role": "system",
            "content": (
                """You give the answers exactly how the user asks you. Without greeting or asking extra questions.
                For example: If the user asks you to give him a list of 5 names of cities in Peru, one per line 
                without bullet points or extra stuff:
                Lima
                Trujillo
                Tarapoto
                Chiclayo
                Arequipa
                """
            ),
        },
        {
            "role": "user",
            "content": f"""I need you to return exactly 5 lines. Each line is going to contain exactly the following:
         bible-book/chapter-number/verse-number/bible-book-text/verse-text

         Such that:
         '/': This is just the separator used to parse the answer you give me and process each part. Only used this between parts.
         bible-book: select one of these books '{random.sample(bible_books_catholic_en, 5)}', it should have the exact same name, and a different book should be selected per line.
         chapter-number: a random chapter number from the selected book. it should be a single integer number, not a range
         verse-number: a random verse number from the selected book and chapter. it should be a single integer number, not a range
         bible-book-text: The complete name of the book I selected in {languages[lang].lower()}.
         verse-text: The whole text of the selected verse in {languages[lang].lower()}.

         Make sure that each line has 5 parts. Separted by '/' (so there will be 4 '/' in total)
         Also make sure the output has exactly 5 lines. One per verse, each one containing the parts I mentioned.
         """,
        },
    ]
    openai_response = (
        client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.3,
        )
        .choices[0]
        .message.content
    )
    print(openai_response)
    for response in openai_response.split("\n"):
        response = response.split("/")
        bible_book = response[0]
        chapter_number = response[1]
        verse_number = response[2]
        bible_book_text = response[3]
        verse_text = response[4]
        url = reverse(
            "verse-lang", args=[bible_book, chapter_number, verse_number, lang]
        )
        html += f"""
        <a href='{url}' class='wrapper-link'>
          <div class='custom-box'>
            <h2>{bible_book_text.title()} {chapter_number} : {verse_number}</h2>
            <p>{verse_text}</p>
          </div>
        </a>
        """
    html += """
    </body>
    </html>
    """
    return HttpResponse(html)


def verse(request, book, chapter, verse):
    return HttpResponseRedirect(
        reverse("verse-lang", args=[book, chapter, verse, "en"])
    )


def verse_lang(request, book, chapter, verse, lang):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Styled Link Div</title>
        <style>
            /* 0. Centers the H1 heading */
            h1 {
                text-align: center;
                margin-top: 40px;
                font-family: sans-serif;
                color: #222;
            }
            /* 1. Remove the link styling from the anchor tag */
            .wrapper-link {
                text-decoration: none;
                color: inherit; /* Keeps text color black/natural instead of blue */
                display: block; /* Makes the entire area clickable */
            }

            /* 2. Style the div container */
            .custom-box {
                text-align: center;      /* Centers the text inside */
                border: 2px solid #333;  /* The border */
                padding: 30px;           /* Space inside the border */
                margin: 20px;            /* Space outside the border */
                border-radius: 8px;      /* Optional: rounds the corners slightly */
                transition: background 0.3s; /* Smooth transition for hover */
            }

            /* 3. Optional: Add a hover effect so users know it's a link */
            .custom-box:hover {
                background-color: #f0f0f0;
                border-color: #007bff;
            }

            /* 4. The Container for the buttons */
            .button-row {
                display: flex;         /* Turns on Flexbox */
                width: 100%;           /* Full width of the parent */
                gap: 10px;             /* Adds a small space between buttons */
                margin: 20px 0;
            }

            /* 5. The Anchor tags acting as buttons */
            .lang-button {
                flex: 1;               /* Forces all buttons to be the exact same size */
                text-align: center;    /* Centers text inside */
                text-decoration: none; /* Removes underline */
                color: white;          /* Text color */
                background-color: #333;/* Button color */
                padding: 15px 0;       /* Vertical padding */
                border-radius: 5px;    /* Slightly rounded corners */
                font-family: sans-serif;
                font-weight: bold;
                transition: background 0.3s;
            }

            /* 6. Hover effect */
            .lang-button:hover {
                background-color: #555;
                cursor: pointer;
            }

            img {
                width: 100%;
            }
        </style>
    </head>
    <body>
    """

    messages = [
        {
            "role": "system",
            "content": (
                """You give the answers exactly how the user asks you. Without greeting or asking extra questions.
                For example: If the user asks you to give him a list of 5 names of cities in Peru, one per line 
                without bullet points or extra stuff:
                Lima
                Trujillo
                Tarapoto
                Chiclayo
                Arequipa
                """
            ),
        },
        {
            "role": "user",
            "content": f"""I am giving you these inputs:
            book: {book}
            chapter: {chapter}
            verse: {verse}

            From the bible book name, chapter and verse, I need you to give the following exact result (1 line):

            `bible-book*chapter-number*verse-number*bible-book-text*verse-text*image-url`

            Such that:
            '*': This is just the separator used to parse the answer you give me and process each part. Only use this between parts.
            bible-book: normalized name of the input book in english. It should be exactly one of these bible book names '{bible_books_catholic_en}'.
            chapter-number: the same number as chapter. this should be a single integer number, not a range, to be considered correct and not an error
            verse-number: the same number as verse. it should be a single integer number, not a range, to be considered correct and not an error
            bible-book-text: The complete real name of the input book in {languages[lang].lower()}.
            verse-text: The whole text of the selected verse in {languages[lang].lower()}.
            image-url: The url of an image related to the verse.

            I can give you the input book, not necesarilly well written, and it could be maybe in another language different than {languages[lang].lower()}. 
            Your job will be to determine if the book refers to one of the books in the list {bible_books_catholic_en}.
            If the book is not part of the list or is just any string without sense, or if the chapter and verse combination does not exist for this bible book
            just return a single line explaining the error, sth like: `book` is not a valid bible book for example, etc.
            
            So there are two possible answers (both single line answers): The error message (in {languages[lang].lower()}) or `bible-book*chapter-number*verse-number*bible-book-text*verse-text*image-url`
         """,
        },
    ]
    openai_response = (
        client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.3,
        )
        .choices[0]
        .message.content
    )

    print(openai_response)

    if len(openai_response.split("*")) != 6:
        html += f"""
        <h1>{openai_response}</h1>
        """
    else:
        response = openai_response.split("*")
        bible_book = response[0]
        chapter_number = int(response[1])
        verse_number = int(response[2])
        bible_book_text = response[3]
        verse_text = response[4]
        image_url = response[5]
        url_en = reverse(
            "verse-lang", args=[bible_book, chapter_number, verse_number, "en"]
        )
        url_es = reverse(
            "verse-lang", args=[bible_book, chapter_number, verse_number, "es"]
        )
        url_fr = reverse(
            "verse-lang", args=[bible_book, chapter_number, verse_number, "fr"]
        )
        html += f"""
        <h1>{bible_book_text.title()} {chapter_number} : {verse_number}</h1>
        <div class="button-row">
            <a href="{url_en}" class="lang-button">English</a>
            <a href="{url_es}" class="lang-button">Español</a>
            <a href="{url_fr}" class="lang-button">Français</a>
        </div>
        <div class='custom-box'>
            <p>{verse_text}</p>
            <img src="{image_url}">
        </div>
        """

    html += """
    </body>
    </html>
    """
    return HttpResponse(html)
