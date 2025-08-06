# ===================== Apresentação ========================================
"""
O objetivo desse código é criar um agente, assistente, de codificação.
Todo o processo de construção do agente estará contído nesse código
e ele será baseado no Artigo de Harrison Chase - CEO @LangChain que,
através de um compilado de informações extraídas do processo de construção
dos produtos da Claude Code, entre outros, elabora boas práticas na 
construção de Agentes.

Link: 
"""

## Boas Práticas:
"""
A estruturação das boas práticas na construção de agentes, chamadas no
arquivo de deep agents, é estruturada em cima de 4 pilares.

- Ferramentas de planejamento;
- Sub agents;
- File system;
- System Prompt.
"""
# ===================== Preparando o ambiente =============================

# Dependencias
from dotenv import load_dotenv
import os

# Carregando api keys
load_dotenv()

api_key = os.getenv("OPENAI_KEY")

#====================== Construção do Agente ======================================
# Estrutura básica do agente
from agno.agent import Agent, RunResponse # Classe do Agente
from agno.models.openai import OpenAIChat


# Tools:
from agno.tools.python import PythonTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.arxiv import ArxivTools
from MyTools.CLITools import *
from MyTools.WebTools import *
from MyTools.FileTools import *

# Structured Answer
from pydantic import BaseModel
from typing import Optional

# ----------- Resposta Estruturada ------------------
class StructureAnswer(BaseModel):
    answer: str
    links: Optional[list[str]]
    tools: Optional[list[str]]

# ----------------- Agent ---------------------------
agent = Agent(
    name="Generic Agent",
    model=OpenAIChat(id="gpt-4o", api_key=api_key),
    tools=[
        # CLI Tools - Ferramentas para interação com o Sistema
        find_directory, list_directory_contents, serch_for_full_path,

        # Web Tools - Ferramentas para buscas na internet 
        search_site_content, search_content_in_complex_site,
        GoogleSearchTools(), ArxivTools(), # Arxiv para buscas especializadas

        # FileTools - Ferramentas para manipulação de arquivos
        save_file,
        
        # Tools auxiliares - Ferramentas que preparam o modelo para tarefas diversas
        PythonTools()
        ],
    show_tool_calls=False,
    stream=False,
    response_model=StructureAnswer,
    structured_outputs=True,  # ativa modo estruturado
)

# Example: Send a template messagecon
msg = input("Prompt: ")
run_response:  RunResponse = agent.run(msg, markdown=True, stream=False)
resp: StructureAnswer = run_response.content
resp.tools = [ts.tool_name for ts  in run_response.tools] 
print(resp.answer)
print(resp.links)
print(resp.tools)

