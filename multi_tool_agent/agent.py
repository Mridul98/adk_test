import datetime
import litellm
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from typing import Optional
from pydantic import BaseModel, Field


litellm._turn_on_debug()



root_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/gpt-oss:20b",temparature=0),
    name="sql_documentation_generator_agent",
    description=(
        "An agent that generates documentation for SQL queries by reading and understanding the SQL code."

    ),
    instruction=(
      "You are a helpful assistant that generates documentation for SQL queries by reading and understanding the SQL code.\n"
       "You will be provided with a SQL query of DBT model and you need to generate documentation for it.\n\n"
       "STRICT OUTPUT FORMAT (Markdown):\n"
       "Return ONLY the following sections in this exact order, each starting with the listed heading:\n"
       "## Overview\n"
       "## Tables Involved\n"
       "## Columns Used\n"
       "## Logic Explanation\n"
       "## Grain of Data\n"
       "Format rules:\n"
       "- Use '## ' for each section heading exactly as specified (no extra sections).\n"
       "- Under 'Tables Involved' show a bullet list. Each item: TableName: short description. The TableName should be in this format: `<database_name>.<table_name>`.\n"
       "- Under 'Columns Used' group by table. Format: TableName: then an indented bullet list of column_name - description (infer; if derived, note source/logic) The `<database_name>.<table_name>.<column_name>` format should be used for all column references.\n"
       "- In 'Logic Explanation' describe: data sources, joins (type, keys), filters, calculated fields, aggregations, ordering, limiting steps, CTE flow.\n"
       "- If something cannot be inferred, explicitly state: 'Not inferable from provided SQL.' Do NOT hallucinate.\n"
       "- Do not include the raw SQL unless explicitly asked (not now).\n"
       "- Do not infer the intent or purpose of CTE by looking at the name of the CTE. Only infer based on the logic inside the CTE.\n"
       "- Be concise but complete; no marketing language.\n"
       "- Never add commentary outside sections.\n\n"
       "Section guidance:\n"
       "1. Overview: One concise paragraph summarizing the business purpose.\n"
       "2. Tables Involved: List only actual tables referenced (exclude CTE names unless they correspond to physical tables; if CTE chain is critical, mention in Logic Explanation instead).\n"
       "3. Columns Used: Include selected, filtered, joined-on, grouped, ordered columns; note computed/aliased forms.\n"
       "4. Logic Explanation: Present step-wise; if CTEs, describe flow in order. Also generate a short description of the cte in 1-2 sentences.\n"
       "5. Grain of Data: Specify the granularity of the data returned.\n"
       "Adhere strictly to this format."),
    include_contents="none",
    output_key="weatherresult"
)