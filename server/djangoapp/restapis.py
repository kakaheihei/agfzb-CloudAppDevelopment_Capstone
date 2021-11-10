import requests
import json
import numpy as np
# import related models here
from .models import CarDealer, CarMake, CarModel, DealerReview
from requests.auth import HTTPBasicAuth

# import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    
    try:
         response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)

    except Exception as error:
        print('api test error', error)
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_request_auth(url, params, api_key, **kwargs):
    """
    Function to get json data using an api key
    """

    print(kwargs)
    print("GET from {} ".format(url))

    try:
        response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                            auth=HTTPBasicAuth('apikey', api_key))

    except Exception as error:
        print('api test errror:', error)


    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data



# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    """
    Function to post reviews
    """

    try:
        print('json_payload:', json_payload)
        # response = requests.get(url, params=kwargs, json=json_payload)
        headers = {"Content-Type": "application/json", "X-Debug-Mode":"true"}
        response = requests.request("POST", url, data=json_payload, headers=headers)

        print('response:', response)

    except Exception as error:
        print("post error:", error)

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data






# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    """
    Function to return dealers info.
    """
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # TEST
        # print('json_result:', json_result['dealerships'][0])
        
        # Get the row list in JSON as dealers
        dealers = json_result['dealerships']
        #TEST
        # print('dealers', dealers)

        # For each dealer object


        # for dealer in dealers:
        #     # Get its content in `doc` object
        #     dealer_doc = dealer["doc"]
        #     # Create a CarDealer object with values in `doc` object
        #     dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
        #                            id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
        #                            short_name=dealer_doc["short_name"],
        #                            st=dealer_doc["st"], zip=dealer_doc["zip"])
        #     results.append(dealer_obj)

        try:
            for dealer in dealers:
                dealer_obj = CarDealer(address=dealer["address"],
                                        city=dealer["city"],
                                        full_name=dealer["full_name"],
                                        id=dealer["id"],
                                        lat=dealer["lat"],
                                        long=dealer["long"],
                                        short_name=dealer["short_name"],
                                        st=dealer["st"],
                                        zip=dealer["zip"])
                
                # print('dealer_obj', dealer_obj)
                results.append(dealer_obj)

        except Exception as error:
            print("Append dealer results error:", error)

    return results



def get_dealer_by_st(url, st):
    """
    Function to return dealers info.
    """
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, st)
    if json_result:
        # TEST
        # print('json_result:', json_result['dealerships'][0])
        
        # Get the row list in JSON as dealers
        dealers = json_result['dealerships']
        #TEST
        # print('dealers', dealers)

        try:
            for dealer in dealers:
                dealer_obj = CarDealer(address=dealer["address"],
                                        city=dealer["city"],
                                        full_name=dealer["full_name"],
                                        id=dealer["id"],
                                        lat=dealer["lat"],
                                        long=dealer["long"],
                                        short_name=dealer["short_name"],
                                        st=dealer["st"],
                                        zip=dealer["zip"])
                
                # print('dealer_obj', dealer_obj)
                results.append(dealer_obj)

        except Exception as error:
            print("Append dealer results error:", error)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, dealerId):
    """
    Function to get reviews for a specific dealer
    """
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealerId)

    print('Get_dealer_reviews_from_cf has kicked off.')
    # test if exists
    if json_result:
        # TEST
        print('json_result:', json_result)
        
        # # Get the row list in JSON as dealers
        reviews = json_result['results']

        try:
            for review in reviews:
                review_obj = DealerReview(dealership=review['dealership'],
                    name=review['name'],
                    purchase=review['purchase'],
                    review=review['review'],
                    purchase_date=review['purchase_date'],
                    car_make=review['car_make'],
                    car_model=review['car_model'],
                    car_year=review['car_year'],
                    sentiment=analyze_review_sentiments(review['review']),
                    id=review['id'])

                results.append(review_obj)

        except Exception as error:
            print("Append dealer results error:", error)


    print('returned details:', results)
    return results    



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    """
    Function to get the sentiment of a review
    """

    api_key = "s_TkKnbbGIAZ9n74bm47iQ3xij3xrtoDquIoRLUWhWfa"

    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/5a78596d-caca-44ca-a7e2-514384bae147"

    version = "2020-08-01" 

    feature = "sentiment"

    return_analyzed_text = True 

    headers = {'Content-Type': 'application/json'}

    params = dict()

    # params["text"] = kwargs["text"]
    # params["version"] = kwargs["version"]
    # params["features"] = kwargs["features"]
    # params["return_analyzed_text"] = kwargs["return_analyzed_text"]

    params["text"] = dealerreview
    params["version"] = version
    params["features"] = feature
    params["return_analyzed_text"] = True

    try:
        # sentiment = get_request_auth(url, params, api_key)
        print("---------------------------------------------")
        print("This is the text to be analyzed for sentiment:", dealerreview)
        print("---------------------------------------------")

        apikey = "s_TkKnbbGIAZ9n74bm47iQ3xij3xrtoDquIoRLUWhWfa"

        authenticator = IAMAuthenticator(apikey)
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2021-08-01',
            authenticator=authenticator
        )

        url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/5a78596d-caca-44ca-a7e2-514384bae147"

        natural_language_understanding.set_service_url(url)


        response = natural_language_understanding.analyze(text=dealerreview, language="en",
        features=Features(sentiment=SentimentOptions(document=True))).get_result()

        sentiment = response["sentiment"]['document']['label']

        print('sentiment:', sentiment)

        return sentiment

    except Exception as error:
        print('Sentiment error:', error)
