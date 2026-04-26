def save_to_markdown(content: str, filename: str = "response.md") -> str:
    """Saves the provided content to a markdown file.
    
    Args:
        content (str): The text content to save.
        filename (str): The name of the file (default: response.md).
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully saved to {filename}"
    except Exception as e:
        return f"Error saving file: {str(e)}"