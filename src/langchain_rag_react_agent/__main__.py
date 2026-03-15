"""Entry point for CLI command and python -m execution."""

import asyncio

from langchain_rag_react_agent.agent import main as agent_main


def main():
    """Wrapper to run async main function."""
    asyncio.run(agent_main())


if __name__ == "__main__":
    main()
