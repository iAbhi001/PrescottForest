from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from config.settings import settings
from src.agent.prompts import get_growth_prompt, NICHE_DICTIONARY
from src.ingestion.twitter_client import TwitterScraperClient

class PrescottForestEngine:
    def __init__(self):
        # Bind the brain model with an optimal operational temperature (0.7 for creative copywriting)
        self.llm = ChatOpenAI(
            model="gpt-4o", 
            temperature=0.7, 
            api_key=settings.OPENAI_API_KEY
        )
        self.scraper = TwitterScraperClient()
        self.prompt_template = get_growth_prompt()

    def generate_viral_content(self, raw_input: str, niche_key: str = "solopreneurship") -> str:
        """Coordinates retrieval, text injection, and LLM compilation into a single workflow execution."""
        
        # 1. Fetch dynamic real-time context from the X timeline
        top_tweets = self.scraper.fetch_top_niche_posts(query=niche_key, max_results=3)
        context_string = "\n---\n".join(top_tweets)
        
        # 2. Extract corresponding domain words from dictionary
        niche_words = NICHE_DICTIONARY.get(niche_key, "execution, leverage, scale")

        # 3. Assemble the LangChain Runnable Pipeline (LCEL)
        chain = (
            {
                "viral_context": lambda x: context_string,
                "niche_words": lambda x: niche_words,
                "input_text": RunnablePassthrough()
            }
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )

        # Execute processing loop
        return chain.invoke(raw_input)