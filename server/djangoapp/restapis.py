import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
URL_DEALERSHIP_API = "https://62e7df6e.eu-gb.apigw.appdomain.cloud/api/dealership"
URL_REVIEW_API = "https://62e7df6e.eu-gb.apigw.appdomain.cloud/api/review"
URL_GET_REVIEW_API = "https://62e7df6e.eu-gb.apigw.appdomain.cloud/api/review/"
NATURAL_LANGUAGE_UNDERSTANDING_APIKEY="0Ph789ZofziUszw54ULkapu2c2juAaBVv8R5VpceqmnM"
NATURAL_LANGUAGE_UNDERSTANDING_URL="https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/9a44db7f-6240-4475-92cd-e1c65b99f260"


def get_request(url, **kwargs):
    print("GET from {} ".format(url))
    print(kwargs)
    api_key = kwargs.get('api_key')
    try:
        if api_key:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters, no authentication GET
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})

    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
    except:
        print("Network exception occurred")
    json_data = json.loads(response.text)
    return json_data


def add_dealer_review_to_db(review_post):
    """ Add Review """
    json_payload = {"review": review_post}
    return post_request(URL_REVIEW_API, json_payload=json_payload)


# get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(**kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(URL_DEALERSHIP_API)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            print(dealer)
            # Get its content in `doc` object
            dealer_obj = CarDealer(_id=dealer.get("id"), address=dealer.get("address"), city=dealer.get('city'),
                                   st=dealer.get("st"),
                                   full_name=dealer.get("full_name"),
                                   short_name=dealer.get("short_name"),
                                   lat=dealer.get("lat"),
                                   long=dealer.get("long"),
                                   zip=dealer.get("zip")
                                   )
            results.append(dealer_obj)
    return results


def get_dealers_by_state(st):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(URL_DEALERSHIP_API, st=st)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            print(dealer)
            # Get its content in `doc` object
            dealer_obj = CarDealer(_id=dealer.get("id"), address=dealer.get("address"), city=dealer.get('city'),
                                   st=dealer.get("st"),
                                   full_name=dealer.get("full_name"),
                                   short_name=dealer.get("short_name"),
                                   lat=dealer.get("lat"),
                                   long=dealer.get("long"),
                                   zip=dealer.get("zip")
                                   )
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(dealer_id):
    results = []
    json_result = get_request(URL_REVIEW_API, dealerId=dealer_id)
    if json_result:
        # Get the row list in JSON as reviews
        if json_result.get("error"):
            return []
        else:
            reviews = json_result.get("entries")
            for rev in reviews:
                review_obj = DealerReview(_id=rev.get("_id"),
                                          car_make=rev.get("car_make"),
                                          car_model=rev.get("car_model"),
                                          car_year=rev.get("car_year"),
                                          dealership=rev.get("dealership"),
                                          name=rev.get("name"),
                                          purchase=rev.get("purchase"),
                                          purchase_date=rev.get("purchase_date"),
                                          review=rev.get("review"),
                                          sentiment=analyze_review_sentiments(rev["review"]))
                results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    api_key = NATURAL_LANGUAGE_UNDERSTANDING_APIKEY
    json_result = get_request(NATURAL_LANGUAGE_UNDERSTANDING_URL, text=text, api_key=api_key)

    if json_result:
        sentiment_result = json_result.get('label', 'neutral')
    return sentiment_result
