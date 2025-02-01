from flask import Blueprint, make_response
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta

bp_sitemap = Blueprint("sitemap", __name__)
CORS(bp_sitemap)



@bp_sitemap.route("/sitemap2.xml")
@cross_origin(methods=["GET"])
def sitemap_2():
    # Generate your sitemap content (e.g., read from a file or dynamically create it)
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset
            xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
                    http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">

        <url>
            <loc>https://www.d-tuning.com/</loc>
            <lastmod>2023-12-19T14:34:26+00:00</lastmod>
            <changefreq>monthly</changefreq>
        </url>

        <url>
            <loc>https://www.d-tuning.com/projects.html</loc>
            <lastmod>2023-12-19T14:34:26+00:00</lastmod>
            <changefreq>monthly</changefreq>
        </url>

        <url>
            <loc>https://www.d-tuning.com/profile/laurindo-c-benjamim.html</loc>
            <lastmod>2023-12-19T14:34:26+00:00</lastmod>
            <changefreq>monthly</changefreq>
        </url>

        <url>
            <loc>https://www.d-tuning.com/ws/api/countries.html</loc>
            <lastmod>2023-12-19T14:34:26+00:00</lastmod>
            <changefreq>monthly</changefreq>
        </url>

        <url>
            <loc>https://www.d-tuning.com/ai/convert-audio-speech-into-text.html</loc>
            <lastmod>2023-12-19T14:34:26+00:00</lastmod>
            <changefreq>monthly</changefreq>
        </url>

        <url>
            <loc>https://www.d-tuning.com/blog/article/articles.html</loc>
            <lastmod>2023-12-19T14:34:26+00:00</lastmod>
            <changefreq>monthly</changefreq>
        </url>

        <url>
            <loc>https://www.d-tuning.com/blog/article/azure-data-lake-storage-gen2.html</loc>
            <lastmod>2023-12-19T14:34:26+00:00</lastmod>
            <changefreq>monthly</changefreq>
        </url>




        </urlset>
    """

    response = make_response(sitemap_content)
    response.headers["Content-Type"] = "application/xml"
    #return f'{response}'
    return response


