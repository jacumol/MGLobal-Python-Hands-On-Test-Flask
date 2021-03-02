from flask import Blueprint

public_bp = Blueprint(
    "public",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/public",
)

from public import resources
