from __future__ import annotations
import sys
import argparse
from pathlib import Path
from typing import Iterable
import os
from textwrap import shorten


#!/usr/bin/env python3
"""
Iterate through all .sql files under the compiled dbt models directory and process their contents.


Default root:
   /Users/mahmud.nabi/data-services-dbt/ds_dbt/target/compiled/ds_dbt/models


You can override the root via CLI argument:
   python sql_doc_gen.py /custom/path


Currently it just prints the relative path and first N characters.
Extend the process_sql_file() function to add documentation generation logic.
"""




DEFAULT_ROOT = Path("/home/granite/adk_test/sql")




def parse_args(argv: list[str]) -> argparse.Namespace:
       """Parse CLI arguments."""
       parser = argparse.ArgumentParser(
               description="Generate markdown documentation for compiled dbt SQL models."
       )
       parser.add_argument(
               "root",
               nargs="?",
               type=Path,
               default=DEFAULT_ROOT,
               help=f"Root directory to search (default: {DEFAULT_ROOT})",
       )
       parser.add_argument(
               "--limit",
               type=int,
               default=None,
               help="Process only the first N files (after sorting).",
       )
       parser.add_argument(
               "--preview-len",
               type=int,
               default=200,
               dest="preview_len",
               help="Preview length when LLM generation fails (default: 200).",
       )
       return parser.parse_args(argv)




def iter_sql_files(root: Path) -> Iterable[Path]:
       """Yield all .sql files under root (recursively)."""
       if not root.exists():
               raise FileNotFoundError(f"Root path does not exist: {root}")
       for p in root.rglob("*.sql"):
               if p.is_file():
                       yield p




def read_file(path: Path) -> str:
       """Read file content safely."""
       try:
               return path.read_text(encoding="utf-8", errors="replace")
       except Exception as e:
               raise RuntimeError(f"Failed to read {path}: {e}") from e




def process_sql_file(path: Path, project_root: Path, preview_len: int = 200) -> None:
       """
       Generate markdown documentation for a SQL file using litellm.
       Adds optional streaming mode (env: SQL_DOC_STREAM=1) for token-by-token output.
       Skips processing if:
         - a markdown file with the same base name already exists under ./data/generated_sql_docs
         - the SQL file resides under any folder named 'schema.yaml' or 'schema.yml'
       Falls back to a simple preview if generation fails.
       """
       rel = path.relative_to(project_root)


       if any(part in {"schema.yaml", "schema.yml"} for part in rel.parts):
               print("=" * 80)
               print(f"FILE: {rel}")
               print("[SKIP] Located under a schema.yaml/schema.yml subfolder")
               print()
               return


       output_root = Path("./data/generated_sql_docs")
       target_md_name = path.with_suffix(".md").name
       if output_root.exists():
               found_existing = next(
                       (p for p in output_root.rglob(target_md_name) if p.is_file()),
                       None,
               )
               if found_existing:
                       print("=" * 80)
                       print(f"FILE: {rel}")
                       print(f"[SKIP] Documentation already exists (matched existing file: {found_existing})")
                       print()
                       return


       content = read_file(path)
       sql_text = content.strip()


       base_prompt = (
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
               "Adhere strictly to this format."
       )


       print("=" * 80)
       print(f"FILE: {rel}")
       print(f"SIZE: {len(content)} chars")


       model = os.getenv("SQL_DOC_MODEL", "ollama/gpt-oss:20b")
       temperature = float(os.getenv("SQL_DOC_TEMPERATURE", "0"))
       use_stream = os.getenv("SQL_DOC_STREAM", "0") in {"1", "true", "yes", "on"}


       try:
           from litellm import completion  # type: ignore


           messages = [
               {"role": "system", "content": base_prompt},
               {
                   "role": "user",
                   "content": f"SQL QUERY:\n{sql_text}\n\nGenerate the required documentation strictly following the format.",
               },
           ]


           doc: str
           if use_stream:
               print("[INFO] Streaming model output...\n")
               chunks: list[str] = []
               try:
                   stream_resp = completion(
                       base_url="http://localhost:11434",
                       model=model,
                       messages=messages,
                       reasoning_effort='medium',
                       temperature=temperature,
                       stream=True,
                   )
                   # litellm stream yields objects with .choices[0].delta/content or similar
                   for chunk in stream_resp:
                       try:
                           choice = chunk.choices[0]
                           piece = ""
                           # Support both delta/content patterns
                           if hasattr(choice, "delta") and getattr(choice.delta, "content", None):
                               piece = choice.delta.content
                           elif getattr(choice, "message", None) and getattr(choice.message, "content", None):
                               piece = choice.message.content
                           elif getattr(choice, "content", None):
                               piece = choice.content
                           if piece:
                               chunks.append(piece)
                               print(piece, end="", flush=True)
                       except Exception:
                           continue
                   print()  # newline after stream
                   doc = "".join(chunks).strip()
               except Exception as stream_err:
                   print(f"[WARN] Streaming failed ({stream_err}); retrying without streaming.")
                   resp = completion(
                       base_url="http://localhost:11434",
                       model=model,
                       messages=messages,
                       reasoning_effort='medium',
                       temperature=temperature,
                   )
                   doc = resp.choices[0].message.content.strip()
           else:
               resp = completion(
                   base_url="http://localhost:11434",
                   model=model,
                   messages=messages,
                   reasoning_effort='medium',
                   temperature=temperature,
               )
               doc = resp.choices[0].message.content.strip()
               print(doc)


           required = [
               "## Overview",
               "## Tables Involved",
               "## Columns Used",
               "## Logic Explanation",
               "## Grain of Data",
           ]
           if not all(h in doc for h in required):
               raise ValueError("Model response missing required sections")


           output_path = output_root / rel.with_suffix(".md")
           output_path.parent.mkdir(parents=True, exist_ok=True)
           try:
               output_path.write_text(doc + "\n", encoding="utf-8")
               print(f"[OK] Documentation saved to {output_path}")
           except Exception as file_err:
               print(f"[WARN] Failed to write documentation file {output_path}: {file_err}")
       except Exception as e:
           print(f"[WARN] Documentation generation failed ({e}). Showing preview instead.\n")
           preview = shorten(sql_text.replace("\n", " ")[: preview_len], width=preview_len, placeholder=" ...")
           print("--- PREVIEW (FALLBACK) ---")
           print(preview)
       print()




def main(argv: list[str]) -> int:
       args = parse_args(argv)
       root: Path = args.root


       try:
               files = list(iter_sql_files(root))
       except Exception as e:
               print(f"Error: {e}", file=sys.stderr)
               return 1


       if not files:
               print(f"No .sql files found under {root}")
               return 0


       files.sort()
       if args.limit is not None:
               files = files[: args.limit]


       print(f"Discovered {len(files)} .sql file(s) under {root}\n")


       for f in files:
               process_sql_file(path=f, project_root=root, preview_len=args.preview_len)


       return 0




if __name__ == "__main__":
       raise SystemExit(main(sys.argv[1:]))
