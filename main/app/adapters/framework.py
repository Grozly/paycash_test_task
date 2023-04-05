from fastapi import HTTPException, status


class FastapiAdapter:
    """
    FastApi adapter class.
    """

    def http_exception_400(self, detail: str) -> HTTPException:
        """
        Get http exception.

        Args:
            detail (str): detail description
        Returns:
            HTTPException: code 400 exception
        """
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
