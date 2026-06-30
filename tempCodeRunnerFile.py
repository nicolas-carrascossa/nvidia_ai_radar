import firecrawl 
import os 
from dotenv import load_dotenv

load_dotenv()

app = firecrawl.FirecrawlApp(api_key = os.getenv("FIRECRAWL_API_KEY"))

resultado = app.scrape_url("https://nubank.com.br")

print(resultado)