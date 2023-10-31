from django.conf import settings
import hypercurrent_metering
from hypercurrent_metering.rest import ApiException
import time
import logging


class HyperCurrentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        HC_API_KEY = getattr(settings, 'HYPERCURRENT_API_KEY', None)
        HC_API_URL = getattr(settings, 'HYPERCURRENT_API_URL', "https://api.hypercurrent.io/meter/v1/api")

        self.hypercurrent = hypercurrent_metering.MeteringControllerApi(hypercurrent_metering.ApiClient())
        self.hypercurrent.api_client.default_headers["x-api-key"] = HC_API_KEY
        self.hypercurrent.api_client.configuration.host = HC_API_URL

    def __call__(self, request):

        logger = logging.getLogger('hypercurrent_middleware')

        HC_METADATA_HEADER = getattr(settings, 'HYPERCURRENT_METADATA_HEADER', "NO_METADATA")
        HC_APPLICATION_HEADER = getattr(settings, 'HYPERCURRENT_APPLICATION_HEADER', "clientId")

        start_time = time.time() 
        response = self.get_response(request)
        end_time = time.time()

        latency = int((end_time - start_time) * 1000)

        application_value = request.headers.get(HC_APPLICATION_HEADER)
        if not application_value:
            application_value = request.user.id 

        metering_data = {
            "application": application_value,
            "method": request.method,
            "url": request.path.rstrip('/'),
            "response_code": response.status_code,
            "request_headers": list(request.headers.keys()),
            "response_headers": list(response.headers.keys()),
            "content_type": response.headers.get('Content-Type',None),
            "remote_host": request.headers.get('x-forwarded-for',None),
            "request_message_size": request.headers.get('content-length',None),
            "response_message_size": response.headers.get('content-length',None),
            "user_agent": request.headers.get('user-agent',None),
            "backend_latency": latency,
            "metadata": response.headers.get(HC_METADATA_HEADER, None),
        }

        filtered_data = {k: v for k, v in metering_data.items() if v is not None}

        body = hypercurrent_metering.MeteringRequestDTO(**filtered_data)

        try:
            self.hypercurrent.meter(body)
        except Exception as e:
            logger.error(f"Exception when metering API request: {e}")

        return response
