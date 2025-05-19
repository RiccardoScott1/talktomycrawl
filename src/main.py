import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from sb import get_client
from embed import embed_documents
from supabase import PostgrestAPIError
import os

async def main():
    url= "https://nexergroup.com"
    
    browser_cfg = BrowserConfig(
        text_mode=True,
    )

    run_cfg = CrawlerRunConfig(
        excluded_tags=["script", "style", "form", "header", "footer", "nav"],
        excluded_selector="#nexer-navbar",
        only_text=True,
        remove_forms=True,
        exclude_social_media_links=True,
        exclude_external_links=True,
        remove_overlay_elements=True,
        magic=True,
        simulate_user=True,
        override_navigator=True,
        verbose=True,
        cache_mode=CacheMode.DISABLED,
        stream=True,
        # Crawl strategy
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2,
            include_external=False,
            #max_pages=10
            ),
        
    )
#nexer-navbar
    async with AsyncWebCrawler(
        config=browser_cfg,
        verbose=True,
        debug=True,
        use_playwright=True,
    ) as crawler:

        async for result in await crawler.arun(
            url=url,
            config=run_cfg,
            filter_main_content=True,
        ):
            process_result(result)

def process_result(result):
    if result.success:
        #print("Content:", result.markdown[:500])  # First 500 chars
        result_json = result_dict(result)
        sb_client = get_client()
        try:
            table_name = os.getenv("SUPABASE_TABLE_NAME_PAGES", "crawled_data")
            sb_client.table(table_name).insert(result_json).execute()
        except PostgrestAPIError as e:
            print(f"Error inserting into Supabase: {e}")
        
        try:
            embed_documents(result_json, sb_client)
        except Exception as e:
            print(f"Error embedding documents: {e}")
        print("Data inserted and embedded successfully.")

    else:
        print(f"Crawl failed: {result.error_message}")

def result_dict(result)->dict:
    return {
        "url":result.url,
        "links":result.links,
        "metadata":result.metadata,
        "markdown":result.markdown,
        "html":result.html,
        "cleaned_html":result.cleaned_html,
    }



if __name__ == "__main__":
    asyncio.run(main())


