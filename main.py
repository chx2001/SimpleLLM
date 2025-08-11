from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool
from prompt import prompt_template

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used:list[str]
 

#chatopenai
#llm = ChatOpenAI(model='gpt-4o-mini')
#chat anthropic
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = prompt_template(parser)

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=[], verbose=True)
#query = input("What can i help you research?")
#raw_response = agent_executor.invoke({"query":query})
raw_response = agent_executor.invoke({"query":"What is the capital of France?"})
print(raw_response)

#structered_response = parser.parse(raw_response.get("output")[0]["text"])
#print(structered_response)

try:
    structered_response = parser.parse(raw_response.get("output")[0]["text"])
    print(structered_response)
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)

#response = llm.invoke("What is the meaning of life?")
#print(response)