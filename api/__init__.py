import azure.functions as func
from azure.functions._http_asgi import AsgiMiddleware

# Import the existing FastAPI app
from main_api import app as fastapi_app

asgi_middleware = AsgiMiddleware(fastapi_app)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return asgi_middleware.handle(req, context)
