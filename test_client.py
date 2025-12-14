from fastmcp import Client
import asyncio

async def main():
    # The client will automatically handle Azure OAuth
    async with Client("http://localhost:8000/mcp", auth="oauth") as client:
        # First-time connection will open Azure login in your browser
        print("✓ Authenticated with Azure!")
        
        # Test the protected tool
        result = await client.call_tool("get_user_info")
        print("✓ Retrieved user info from protected tool:")
        print("User Info:")
        print(result)
        data = result.data
        print(f"Azure user: {data.get('email')}")
        print(f"Name: {data.get('name')}")
        print("Call secret data tool:")
        secret_data = await client.call_tool("get_secret_data")
        print("Secret Data:")
        print(secret_data)
if __name__ == "__main__":
    asyncio.run(main())