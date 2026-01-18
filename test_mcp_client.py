import asyncio
import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Get the absolute path to the python executable and the server script
PYTHON_EXE = sys.executable
SERVER_SCRIPT = os.path.abspath(os.path.join("src", "data_governance", "server.py"))
TEST_DATA_CSV = os.path.abspath("test_data.csv")

async def run_client():
    # Define server parameters
    # We are launching the server script we just wrote
    server_params = StdioServerParameters(
        command=PYTHON_EXE,
        args=[SERVER_SCRIPT],
        env=None
    )

    print(f"🔌 Connecting to MCP Server at: {SERVER_SCRIPT}...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Initialize
            await session.initialize()
            print("✅ Connected and Initialized!")

            # 2. List Available Tools
            print("\n📋 Listing Available Tools:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            # 3. Call 'check_data_quality' Tool
            print(f"\n🛠️  Calling Tool: check_data_quality on {TEST_DATA_CSV}")
            try:
                result = await session.call_tool(
                    name="check_data_quality",
                    arguments={"csv_path": TEST_DATA_CSV}
                )
                print("  Result:")
                # MCP results are a list of content blocks
                for content in result.content:
                    print(f"    {content.text}")
            except Exception as e:
                print(f"  ❌ Error calling tool: {e}")

            # 4. Call 'scan_privacy' Tool
            print(f"\n🛠️  Calling Tool: scan_privacy on {TEST_DATA_CSV}")
            try:
                result = await session.call_tool(
                    name="scan_privacy",
                    arguments={"csv_path": TEST_DATA_CSV}
                )
                print("  Result:")
                for content in result.content:
                    print(f"    {content.text}")
            except Exception as e:
                print(f"  ❌ Error calling tool: {e}")

            # 5. Call 'analyze_bias' Tool
            print(f"\n🛠️  Calling Tool: analyze_bias on {TEST_DATA_CSV}")
            try:
                result = await session.call_tool(
                    name="analyze_bias",
                    arguments={
                        "csv_path": TEST_DATA_CSV, 
                        "sensitive_column": "gender",
                        "target_column": "loan_approved"
                    }
                )
                print("  Result:")
                for content in result.content:
                    print(f"    {content.text}")
            except Exception as e:
                print(f"  ❌ Error calling tool: {e}")

if __name__ == "__main__":
    # Ensure test data exists (from previous demo.py run)
    if not os.path.exists(TEST_DATA_CSV):
        print("⚠️  test_data.csv not found. Please run demo.py first.")
    else:
        asyncio.run(run_client())
