import os
import uvicorn
from fastapi import FastAPI, Request, Response, APIRouter, Depends
from starlette.middleware.sessions import SessionMiddleware

from .config import Auth0Config
import json

from .auth.auth_client import AuthClient
from .server.routes import router, register_auth_routes
from .errors import register_exception_handlers


# Create FastAPI app instance
app = FastAPI(title="Auth0 FastAPI SDK Example")



# Add SessionMiddleware; use your secret for session encryption
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("APP_SECRET", "3bd450f7eba16a28301f68878344cdd2a069582b840c045c2cf56c746f68ab4"))

# Load configuration (you could also load from a config file)
config = Auth0Config(
    domain="demo.iam-federatedat-2.auth0c.com",
    clientId="a9HWNuoK0dqzV4KIE4ckzXkB8s017oHb",
    clientSecret="PYAXoadeJvORIX3DmW_ZoZvKnrcLoBmSEC_dLsAYIQn0U5rzl25NsqGL45QYzOIP",
    appBaseUrl="http://localhost:8000",
    secret=os.environ.get("APP_SECRET", "3bd450f7eba16a28301f68878344cdd2a069582b840c045c2cf56c746f68ab4"),
    audience=os.environ.get("AUTH0_AUDIENCE", None),
    pushed_authorization_requests=False,
    mount_routes=True,
    cookie_name="auth0_session",
    authorization_params={"scope":"openid profile email offline_access", "response_type":"code", "access_type":"offline", "grant_type":"authorization_code", "prompt": "consent"},
    session_expiration=259200,  # 3 days in seconds
)

# Store the configuration in app state for access in routes, if needed
app.state.config = config

# Instantiate the AuthClient with the configuration
auth_client = AuthClient(config)
app.state.auth_client = auth_client

register_auth_routes(router, config)

# Include the authentication routes
app.include_router(router)

# Register custom exception handlers for Auth0 errors
register_exception_handlers(app)

@app.get("/")
def index():
    return {"message": "Hello from test_script.py!"}

#############Back Channel Testing Code #########################

# app = FastAPI(title="Auth0 FastAPI SDK Example")
# router = APIRouter()

# auth0 = ServerClient(
#     domain="dev-skishore.us.auth0.com",
#     client_id="U5aSExzav1So8dGzJi54R0mmMAFWt4OO",
#     client_secret="x20VTYIF7XoCBr9pVbO82KRzowmsB2KnSR7UmzqT2pSCakjpbEo0qD5KIZnizvCe",
#     secret="3bd450f7eba16a28301f68878344cdd2a069582b840c045c2cf56c746f68ab48"
# )



# def get_response():
#     return Response()

# @router.route("/auth/back-channel", methods=["GET", "POST"])
# async def backchannel_auth(request: Request):
#     options = LoginBackchannelOptions(
#         login_hint={"sub": "auth0|678f493689fb30e67dedefea"},
#         binding_message="Login to Example App",
#         authorization_params={
#             "scope": "openid profile email payments",
#             "audience" : "https://api.example.com",
#             "authorization_details": json.dumps([{
#                 "type": "payment_initiation",
#                 "locations": ["https://example.com/payments"],
#                 "instructedAmount": {
#                     "currency": "EUR",
#                     "amount": "123.50"
#                 },
#                 "creditorName": "Merchant A",
#                 "creditorAccount": {
#                     "bic": "ABCIDEFFXXX",
#                     "iban": "DE021001001093071118603"
#                 },
#                 "remittanceInformationUnstructured": "Ref Number Merchant"
#             }])
#         }
#     )

#     try:
#         # Don't pass a response object in the store_options
#         result = await auth0.login_backchannel(options)
#         print(result)
#         return {
#             "status": "success",
#             "message": "User authenticated via backchannel"
#         }
#     except Exception as e:
#         return {
#             "status": "error",
#             "message": str(e)
#         }
    

# app.include_router(router)

if __name__ == "__main__":
    # Run the application using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




# from dotenv import find_dotenv, load_dotenv

# import sys
# import os
# from fastapi import FastAPI
# from starlette.middleware.sessions import SessionMiddleware
# import uvicorn
# import asyncio
# import secrets

# from auth.auth_client import Auth
# # from ai_auth import AIAuth

# ENV_FILE = find_dotenv()
# if ENV_FILE:
#     load_dotenv(ENV_FILE)

# # Create user's FastAPI app
# app = FastAPI()

# app.add_middleware(SessionMiddleware, secret_key="3bd450f7eba16a28301f68878344cdd2a069582b840c045c2cf56c746f68ab48")


# # Create auth client with the user's app
# auth_client = Auth(app=app, store="CookieStore")

# # 5. Optionally, define any additional routes or logic in this file
# @app.get("/")
# def index():
#     return {"message": "Hello from test_script.py!"}

# # Start server as the user wants
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)



# from fastapi import FastAPI, Request, Depends
# from fastapi.responses import HTMLResponse
# from auth.auth_client import Auth0, get_user
# import uvicorn

# app = FastAPI()

# # Initialize Auth0
# auth0 = Auth0(
#     app=app,  # Pass the FastAPI app for automatic route setup
#     domain="demo.iam-federatedat-2.auth0c.com",
#     client_id="a9HWNuoK0dqzV4KIE4ckzXkB8s017oHb",
#     client_secret="PYAXoadeJvORIX3DmW_ZoZvKnrcLoBmSEC_dLsAYIQn0U5rzl25NsqGL45QYzOIP",
#     app_base_url="http://localhost:8000",
#     secret="3bd450f7eba16a28301f68878344cdd2a069582b840c045c2cf56c746f68ab48",
# )

# # Public route
# @app.get("/", response_class=HTMLResponse)
# async def home():
#     return """
#         <h1>Welcome to our app!</h1>
#         <p><a href="/profile">Go to Profile</a> | <a href="/auth/login">Login</a></p>
#     """

# # Protected route using decorator
# @app.get("/profile", response_class=HTMLResponse)
# @auth0.requires_auth
# async def profile(request: Request):
#     user = await auth0.get_user(request)
#     return f"""
#         <h1>Profile</h1>
#         <p>Welcome, {user.name}!</p>
#         <img src="{user.picture}" alt="Profile picture" width="100">
#         <p>Email: {user.email}</p>
#         <p><a href="/auth/logout">Logout</a></p>
#     """

# # Protected route using dependency
# @app.get("/api/user-info")
# async def user_info(user=Depends(get_user)):
#     return user

# # # Protected API route with access token
# # @app.get("/api/data")
# # async def protected_data(request: Request, access_token=Depends(get_access_token)):
# #     if not access_token:
# #         return {"error": "Unauthorized"}
    
# #     # Use the access token to call external APIs
# #     return {"message": "Protected data", "token_available": True}


# # Start server as the user wants
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
