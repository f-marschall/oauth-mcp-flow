
from fastmcp import FastMCP
from fastmcp.server.auth.providers.azure import AzureProvider
import os
from dotenv import load_dotenv

from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet

load_dotenv()

# The AzureProvider handles Azure's token format and validation
auth_provider = AzureProvider(
    client_id=os.environ["AZURE_CLIENT_ID"],
    client_secret=os.environ["AZURE_CLIENT_SECRET"],
    tenant_id=os.environ["AZURE_TENANT_ID"],
    base_url=os.environ["AZURE_BASE_URL"],
    required_scopes=["read_user"],
    # identifier_uri defaults to api://{client_id}
    # identifier_uri="api://your-api-id",
    # Optional: request additional upstream scopes in the authorize request
    additional_authorize_scopes=[f"api://{os.environ['AZURE_CLIENT_ID']}/read_secrets"], #["User.Read", "offline_access", "openid", "email"],
    # redirect_path="/auth/callback"                  # Default value, customize if needed
    base_authority="login.microsoftonline.com"      # (default: login.microsoftonline.com)

    # Production token management
    # jwt_signing_key=os.environ["JWT_SIGNING_KEY"],
    # client_storage=FernetEncryptionWrapper(
    #     key_value=RedisStore(
    #         host=os.environ["REDIS_HOST"],
    #         port=int(os.environ["REDIS_PORT"])
    #     ),
    #     fernet=Fernet(os.environ["STORAGE_ENCRYPTION_KEY"])
    # )
)

mcp = FastMCP("API Management MCP Server", auth=auth_provider)

# Add a protected tool to test authentication
@mcp.tool
async def get_user_info() -> dict:
    """Returns information about the authenticated Azure user."""
    from fastmcp.server.dependencies import get_access_token
    
    token = get_access_token()
    # The AzureProvider stores user data in token claims
    print("Token:", token)
    return {
        "azure_id": token.claims.get("sub"),
        "email": token.claims.get("email"),
        "name": token.claims.get("name"),
        "job_title": token.claims.get("job_title"),
        "office_location": token.claims.get("office_location")
    }

@mcp.tool 
def request_fresh_user_info():
    """Requests fresh user info from Azure."""
    pass

@mcp.tool
def get_secret_data() -> str:
    """A protected tool that returns secret data."""
    from fastmcp.server.dependencies import get_access_token
    token = get_access_token()

    if not token:
        raise PermissionError("Authentication required to access this tool.")
    if not token.scopes or "read_secrets" not in token.scopes:
        raise PermissionError("Insufficient scopes to access this tool.")
    
    return "This is very secret data only for authenticated users!"

@mcp.tool("documentation:aws-waf")
def get_waf_logs(prefix: str):
    return f"Fetching AWS WAF logs with prefix: {prefix}"

@mcp.resource("documenation:azure-waf")
def azure_doc_waf():
    pass