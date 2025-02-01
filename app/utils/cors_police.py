

from app.dependencies import CORS



    
TRUESTED_DOMAINS=[
    "http://localhost:52330",
    "http://localhost:5000",
    "https:www.d-tuning.com",
    "https://laurindocbenjamim.github.io"
]
#
def allowed_domains_to_api_route():
    """
    
    """
    return [TRUESTED_DOMAINS[0],TRUESTED_DOMAINS[1],TRUESTED_DOMAINS[2],TRUESTED_DOMAINS[3]]

#
def allowed_domains_to_upload_route():
    """
    
    """
    return [TRUESTED_DOMAINS[0],TRUESTED_DOMAINS[1],TRUESTED_DOMAINS[2],TRUESTED_DOMAINS[3]]

#
def allowed_domains_to_files_route():
    """
    
    """
    return [TRUESTED_DOMAINS[0],TRUESTED_DOMAINS[1],TRUESTED_DOMAINS[2],TRUESTED_DOMAINS[3]]



cors = CORS(resources={
        r"/videos/post": {"origins": allowed_domains_to_upload_route()},
        r"/upload": {"origins": allowed_domains_to_upload_route()},
        r"/api/csrf-token/get": {"origins": allowed_domains_to_upload_route()},
        r"/api/upload": {"origins": allowed_domains_to_upload_route()},
        r"/api/files-storage": {"origins": allowed_domains_to_files_route()},
        r"/api/*": {"origins": allowed_domains_to_api_route()},
    })