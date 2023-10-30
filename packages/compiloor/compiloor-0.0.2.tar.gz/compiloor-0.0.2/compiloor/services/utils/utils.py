from urllib.parse import urlparse


class Utils:
    """
        Miscellaneous utility functions.
    """
    
    @staticmethod
    def validate_url(url: str) -> bool:
        result = urlparse(url)
        return all([result.scheme, result.netloc])