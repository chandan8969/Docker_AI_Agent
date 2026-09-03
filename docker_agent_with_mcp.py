from langchain_mcp_adapters.client import MultiServerMCPClient 
import asyncio
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

async def main():
        client = MultiServerMCPClient(
            {
                "docker-mcp" : {
                "command": "python",
                "args" : ["mcp_server.py"],
                "transport": "stdio"
            
                }
            }
        )

        tools = await client.get_tools()

        model = ChatOllama(model = "gemma4",  temperature = 0.8)
        agent = create_agent(model,tools)
        print("Agent created, invoking...")

    
        #response = await agent.ainvoke({"messages": [{"role": "user", "content": "how many containers running on local system"}]})
        #print("Got response!")
        #print(response["messages"][-1].content)
        try:
            response = await asyncio.wait_for(
                agent.ainvoke(
                    {"messages": [{"role": "user", "content": "how many containers running on local system"}]}
                ),
                timeout=300,
            )
            print("Got response!")
            print(response["messages"][-1].content)
        except asyncio.TimeoutError:
            print("Still hanging after 5 minutes — not just slow, likely a parsing/format issue.")

if __name__ == "__main__":
    asyncio.run(main())