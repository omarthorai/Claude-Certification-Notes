from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(
    name="read_document",
    description="Read the content of a given document"
)
def read_document(doc_id: str = Field(description = "Id of the document to read")):
    if doc_id not in docs:
        raise ValueError(f"Doc id {doc_id} is not present")
    return docs[doc_id]

# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_document",
    description="Edit the document by replacing the old string in the documents content with the new string"
)
def edit_document(
    doc_id: str = Field(description = "Id of the document to read"),
    old_str: str = Field(description = "Old string in the documents content which should be replaced. Must be present in the documents content."),
    new_str: str = Field(description = "New string that should replace the old string in the documents content")
    ):
    if doc_id not in docs:
        raise ValueError(f"Doc id {doc_id} is not present")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
# TODO: Write a resource to return all doc id's
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def get_docs() -> list[str]:
    return list(docs.keys())
# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc_content(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc id {doc_id} is not present")
    return docs[doc_id]


# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
