from autoscraper import AutoScraper

# Initialize the scraper
scraper = AutoScraper()

# Amazon URL for the search page
amazon_url ='https://www.amazon.in/s?k=keyboard&crid=26W0I9TYMZZIG&sprefix=keyboard%2Caps%2C382&ref=nb_sb_noss_1'
wanted_list = ["Zebronics ZEB-KM2100 Multimedia USB Keyboard Comes with 114 Keys Including 12 Dedicated Multimedia Keys & with Rupee Key", "₹249"]

# Build the scraper with the wanted list
result = scraper.build(amazon_url, wanted_list)

# Debug: Print the initial result
print("Initial Build Result:")
print(result)

scraper_result = scraper.get_result_similar(amazon_url, grouped=True)

# Assuming the first 3 keys correspond to Title, Description, and Price respectively
scraper.set_rule_aliases({
    list(scraper_result.keys())[0]: 'Title',
    list(scraper_result.keys())[1]: 'Desc',
    list(scraper_result.keys())[2]: 'Price'
})

scraper.save('amazon-search')


# Function to load the scraper and use the saved aliases
def scrape_with_saved_alias(url):
    scraper.load('amazon-search')
    return scraper.get_result_similar(url, group_by_alias=True)


# Test with another URL to verify saved rules
try:
    result = scrape_with_saved_alias('https://www.amazon.in/s?k=iphones')
    print("Scraped Result with Saved Rules:")
    print(result)
except Exception as e:
    print(f"Error during scraping with saved rules: {e}")
