from autoscraper import AutoScraper
from flask import Flask, request, jsonify
from pathlib import Path


# Initialize the scraper
amazon_scraper = AutoScraper()


# Define the path to the scraper model file
file_path = Path(r'E:/ZZ Development/Problems/python/Amazon_scraping/amazon-search')


# Check if the file exists
if not file_path.is_file():
    raise FileNotFoundError(f"File not found: {file_path}")

# Load the scraper configuration
amazon_scraper.load(str(file_path))

# Initialize Flask app
app = Flask(__name__)



def get_amazon_result(search_query):
    """
    Perform a search on Amazon and return aggregated results.
    """
    url = f'https://www.amazon.in/s?k={search_query.replace(" ", "+")}&crid=26W0I9TYMZZIG&sprefix={search_query.replace(" ", "+")}%2Caps%2C382&ref=nb_sb_noss_1'
    
    # Debug: Print the search URL
    print(f"Search URL: {url}")
    
    # Perform the scraping
    result = amazon_scraper.get_result_similar(url, group_by_alias=True)
    
    # Aggregate the results
    aggregated_result = _aggregate_result(result)
    
    return aggregated_result



def _aggregate_result(result):
    """
    Aggregate the result from the scraper into a final structured format.
    """
    if not result:
        print("No results found.")
        return []

    # Find the minimum length of the lists
    min_length = min(len(values) for values in result.values())
    print(f"Minimum length of lists: {min_length}")

    # Debug: Print the result dictionary for tracing
    print(f"Result Dictionary: {result}")

    final_result = []
    for i in range(min_length):
        try:
            item = {alias: result[alias][i] for alias in result}
            # Remove the unnamed field if it exists
            item.pop('', None)
            final_result.append(item)
        except IndexError:
            pass

    # Handle any remaining items that were not part of the smallest list
    for alias, values in result.items():
        for i in range(len(final_result), len(values)):
            try:
                # Add missing keys with empty strings if not already present
                item = {key: '' for key in result.keys()}
                item[alias] = values[i]
                # Remove the unnamed field if it exists
                item.pop('', None)
                final_result.append(item)
            except IndexError:
                pass

    return final_result



@app.route('/', methods=['GET'])
def search_api():
    """
    API endpoint to handle search queries.
    """
    query = request.args.get('q')
    
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    print(f"Search query: {query}")
    
    results = get_amazon_result(query)
    
    return jsonify({'result': results})



if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
