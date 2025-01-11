from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom error handler to provide more meaningful error messages.
    Logs the error and returns a consistent error response format.
    """
    # Call DRF's default exception handler first to get the standard error response
    response = exception_handler(exc, context)

    if response is not None:
        # Check if the error is a validation error
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            return Response({
                'error': 'Validation Error',
                'details': response.data,
                'message': 'Your request data is invalid.'
            }, status=response.status_code)

        # Check if the error is an authentication error
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response({
                'error': 'Authentication Error',
                'message': 'You are not authorized to perform this action. Please log in.'
            }, status=response.status_code)

        # Check if the error is a permission error
        if response.status_code == status.HTTP_403_FORBIDDEN:
            return Response({
                'error': 'Permission Denied',
                'message': 'You do not have permission to perform this action.'
            }, status=response.status_code)

        # Handle other standard errors
        return Response({
            'error': 'Request Error',
            'details': response.data,
            'message': 'An error occurred while processing your request.'
        }, status=response.status_code)

    # Log the unexpected error for debugging purposes
    logger.error(f"Unexpected error: {exc}", exc_info=True)

    # Return a generic 500 error response for unhandled exceptions
    return Response({
        'error': 'Unexpected Error',
        'message': 'An internal server error occurred. Please try again later.'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
