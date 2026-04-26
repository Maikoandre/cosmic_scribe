from docling.document_converter import DocumentConverter

source = ""
converter = DocumentConverter()
result = converter.convert(source)
with open("output.md", "w") as f:
    f.write(result.document.export_to_markdown())
# print(result.document.export_to_markdown())  # output: "## Docling Technical Report[...]"