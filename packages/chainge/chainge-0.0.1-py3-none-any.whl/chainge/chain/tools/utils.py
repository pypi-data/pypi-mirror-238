
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from pydantic import BaseModel, Field
from typing import Optional, Type

#Import our Stock Adapter
from chainge.api.api import stock_api
from typing import Union, Tuple, Dict

'''
Keyword --> Ticker Lookup tool
'''

class StockLookupInput(BaseModel):
    keyword: str = Field()

class StockLookupTool(BaseTool):
    name = "keyword_to_ticker"

    description = """Use this tool after the stock probe to find a list of related companies,
    and their ticker symbols.
    
    input: keywords like apple, google 
    """
    args_schema: Type[BaseModel] = StockLookupInput 

    def _run(
        self, keyword: str, run_manager = None
    ) -> str:
        """Use the tool."""

        attr = stock_api.lookup(keyword.strip())
        print("Looking for ", attr)

        return attr

    async def _arun(
        self, stock_ticker_name: str, run_manager = None
    ) -> str:
        """Use the tool asynchronously."""

        attr = stock_api.lookup(keyword.strip())

        return attr

'''
Find alternatives / competitors to companies
'''
class AlternativeInput(BaseModel):
    ticker: str = Field()

class AlternativesLookupTool(BaseTool):
    name = "alternative_tickers_from_ticker"

    description = """Use this tool after the stock probe to find the tickers of companies that are
    peers and competitors to the current company.
    
    input: stock ticker symbols like AAPL, GOOG
    """
    args_schema: Type[BaseModel] = StockLookupInput 

    def _run(
        self, keyword: str, run_manager = None
    ) -> str:
        """Use the tool."""

        attr = stock_api.alternatives(keyword.strip())
        return attr

    async def _arun(
        self, stock_ticker_name: str, run_manager = None
    ) -> str:
        """Use the tool asynchronously."""

        attr = stock_api.alternatives(keyword.strip())
        return attr