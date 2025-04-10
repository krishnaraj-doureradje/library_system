from starlette import status


class HTTPResponseCode:
    """App HTTPResponseCode Model."""

    OK = status.HTTP_200_OK
    CREATED = status.HTTP_201_CREATED
    NO_CONTENT = status.HTTP_204_NO_CONTENT
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED
    FORBIDDEN = status.HTTP_403_FORBIDDEN
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR

    # We can add more custom status codes here
