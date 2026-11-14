
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Arithmetic Server")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract the second number from the first number."""
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide the first number by the second number."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


@mcp.tool()
def modulus(a: int, b: int) -> int:
    """Return the remainder when a is divided by b."""
    if b == 0:
        raise ValueError("Modulus by zero is not allowed.")
    return a % b


if __name__ == "__main__":
    # Run using the standard input/output transport
    mcp.run(transport="stdio")
