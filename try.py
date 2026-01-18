
import os
import sys
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Force unbuffered stdout/stderr
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

async def test_report_debug():
    print("🚀 Starting Debug Script...", flush=True)
    
    # 模拟数据
    mock_data = {
        "quality_status": "HIGH",
        "privacy_status": "LOW",
        "bias_status": "MEDIUM",
        "quality_summary": "Data integrity checks failed (75% success).",
        "privacy_summary": "No PII detected.",
        "bias_summary": "Gender bias detected.",
        "carbon_footprint": "0.45",
        "bias_details": "Female: 60%, Male: 40%"
    }

    # 启动 Server
    server_script = os.path.join("src", "data_governance", "server.py")
    print(f"🔧 Server Script: {server_script}", flush=True)
    
    server_params = StdioServerParameters(command=sys.executable, args=[server_script], env=None)
    
    print("🔌 Connecting to server...", flush=True)
    try:
        async with stdio_client(server_params) as (read, write):
            print("✅ Transport Established.", flush=True)
            async with ClientSession(read, write) as session:
                print("🔄 Initializing Session...", flush=True)
                await session.initialize()
                print("✅ Session Initialized.", flush=True)
                
                # 调用工具
                print("🛠️ Calling generate_conformity_report...", flush=True)
                # 设置超时，防止无限等待
                try:
                    result = await asyncio.wait_for(
                        session.call_tool("generate_conformity_report", arguments={"data_json": json.dumps(mock_data)}),
                        timeout=30.0
                    )
                    
                    print("📝 Tool Result:", flush=True)
                    for content in result.content:
                        print(f"  {content.text}", flush=True)
                except asyncio.TimeoutError:
                    print("❌ Error: Tool call timed out after 30s.", flush=True)
                        
    except Exception as e:
        print(f"❌ Connection Error: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_report_debug())
