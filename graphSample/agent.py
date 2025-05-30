from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.adk.tools.agent_tool import AgentTool

def graph_visualization_tool(
    request: str,
    tool_context: ToolContext,
) -> str:
    """Tool to return visualization."""
    try:
        # '이미지줘' 또는 유사한 요청이 있으면 고정 이미지 반환
        if '이미지' in request and ('줘' in request or '보여' in request):
            return "![이미지](https://shop-phinf.pstatic.net/20230720_195/1689860419804rbDFR_PNG/%B8%F4%B7%CE%B0%ED_400_Black.png?type=w640)"
        
        # 그 외에는 기본 이미지 반환
        return "![막대 차트](https://shop-phinf.pstatic.net/20230720_195/1689860419804rbDFR_PNG/%B8%F4%B7%CE%B0%ED_400_Black.png?type=w640)"
    except Exception as e:
        return f"오류 발생: {str(e)}"

# Create the graph visualization agent
root_agent = Agent(
    name="graph_visualization_agent",
    model="gemini-2.0-flash",
    instruction="""그래프 시각화 에이전트입니다.
    - '이미지줘'라고 하면 이미지 반환
    - 성공 시: 마크다운 이미지 문법으로 반환
    - 실패 시: 에러 메시지만 반환""",
    tools=[graph_visualization_tool],
)
