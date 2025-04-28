import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from sb import get_client
from embed import embed_documents
from supabase import PostgrestAPIError
from dataclasses import dataclass

async def main():
    browser_config = BrowserConfig(verbose=True)
    run_config = CrawlerRunConfig(
        stream=True ,
        # Content filtering
        word_count_threshold=10,
        only_text=True,
        excluded_tags=['form', 'header'],
        exclude_external_links=True,
        # Crawl strategy
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2,
            include_external=False,
            max_pages=10
            ),
        
        # Content processing
        process_iframes=True,
        remove_overlay_elements=True,

        # Cache control
        cache_mode=CacheMode.ENABLED  # Use cache if available
    )
    async with AsyncWebCrawler() as crawler:
        # Returns an async iterator
        async for result in await crawler.arun(
            "https://nexergroup.com", 
            config=run_config
            ):
            # Process each result as it becomes available
            process_result(result)

def process_result(result):
    if result.success:
        # Print clean content
        print("Content:", result.markdown[:500])  # First 500 chars
        result_json = result_dict(result)
        sb_client = get_client()
        try:
            sb_client.table("crawled_data").insert(result_json).execute()
        except PostgrestAPIError as e:
            print(f"Error inserting into Supabase: {e}")
        

        embed_documents(result_json, sb_client)

        
    else:
        print(f"Crawl failed: {result.error_message}")

def result_dict(result)->dict:
    return {
        "url":result.url,
        "links":result.links,
        "metadata":result.metadata,
        "markdown":result.markdown
    }



if __name__ == "__main__":
    asyncio.run(main())


