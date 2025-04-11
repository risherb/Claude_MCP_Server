import os
import re
import json
import requests
from typing import Dict, List, Any, Optional, Literal
from dataclasses import dataclass, asdict
import openai
import anthropic
import httpx

DUCKDUCKGO_ENDPOINT = "https://api.duckduckgo.com"
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "")

LLMProvider = Literal["claude"]

@dataclass
class DDGRequest:
    q: str
    format: str = "json"
    no_html: int = 1
    skip_disambig: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
@dataclass
class WebResult:
    title: str
    url: str
    description: str

class MCPClient:
    def __init__(self, endpoint: str = DUCKDUCKGO_ENDPOINT):
        self.endpoint = endpoint

    def search(self, query: str, count: int = 10) -> List[WebResult]:
        request = DDGRequest(q=query)

        try:
            response = requests.get(
                self.endpoint,
                params=request.to_dict()
            )

            response.raise_for_status()

            data = response.json()
            results = []

            if data.get("Abstract"):
                results.append(WebResult(
                    title=data.get("Heading", ""),
                    url = data.get("AbstractURL", ""),
                    description=data.get("Abstract", "")
                ))
            return results
        except Exception as e:
            print(e)
            return []
    
class ClaudeMCPBridge:

    def __init__(self, llm_provider: LLMProvider = "claude"):
        self.mcp_client = MCPClient()
        self.llm_provider = llm_provider

        if llm_provider == "claude":
            # Create a custom httpx client without proxies
            http_client = httpx.Client()
            self.claude_client = anthropic.Anthropic(
                api_key=CLAUDE_API_KEY,
                http_client=http_client
            )

    def extract_website_queries_with_llm(self, user_message: str) -> List[str]:
        if self.llm_provider == "claude":
            return self._extract_with_claude(user_message)
        else:
            return ["error"]
        
    def _extract_with_claude(self, user_message: str) -> List[str]:

        try:
            response = self.claude_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0.1,
                system="You are a helpful assistant that identifies web search queries in user message. Extract any specific website or topic queries the user wants information about. Return results as a JSON object with a 'queries' field containing an array of strings. If no queries are found, return an empty array.",
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            content = response.content[0].text
            json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', content, re.DOTALL)
            if json_match:
                result= json.loads(json_match.group(1))
            else:
                try:
                    result = json.loads(content)

                except:
                    return "error"
            queries = result.get("queries", [])
            return queries
        
        except Exception as e:
            print(e)
            return []
        
def handle_claude_tool_call(tool_params: Dict[str, Any]) -> Dict[str, Any]:
    query = tool_params.get("query", "")
    if not query:
        return {"error": "no query"}
    
    bridge = ClaudeMCPBridge()
    results = bridge.mcp_client.search(query)

    return {
        "results": [asdict(result) for result in results]
    }
    

        
    