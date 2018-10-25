import base64
import json
import requests
import urllib


class OAuthToken:
    """Generates bearer token that must be sent with every search request to
    the Twitter Standard Search API. See API documentation below
    https://developer.twitter.com/en/docs/basics/authentication/overview/application-only

    Attributes:
        API_OAUTH_ENDPOINT: URL for OAuth requests to Twitter API.
        API_CONSUMER_KEY: API key obtained after making Twitter dev 
            account.
        API_SECRET_KEY: See above.
    """
    API_OAUTH_ENDPOINT = 'https://api.twitter.com/oauth2/token'
    API_CONSUMER_KEY = 'bym5ha8MQewR5fEqy2dZwRdBI'
    API_SECRET_KEY = 'VafZzWm4mRvwhZ4v9wKrgAtqneMhfVrHywjcdCR9auoUJ2JcMa'

    def __init__(self):
        """Initializes OAuthToken."""
        self.bearer_token = self._request_bearer_token()

    def _request_bearer_token(self):
        """Sends HTTP POST to Twitter API endpoint to generate a 'bearer token' 
        that must be included in the header when sending search queries to
        Search API.

        Returns:
            A string containing the bearer token.
        """

        # Format and encode key, see Twitter API documentation.
        key_secret = '{}:{}'.format(
            OAuthToken.API_CONSUMER_KEY,
            OAuthToken.API_SECRET_KEY)
        b64_encoded_key = base64.b64encode(key_secret.encode('ascii'))
        b64_encoded_key = b64_encoded_key.decode('ascii')

        # Create header with encoded API key and send POST using requests
        # library.
        headers = {
            'User-Agent':'TemperatureOfTheRoom',
            'Authorization':'Basic ' + b64_encoded_key,
            'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
            'Accept-Encoding':'gzip'} 
        body = {'grant_type':'client_credentials'}
        request = requests.post(
            OAuthToken.API_OAUTH_ENDPOINT,
            data = body,
            headers = headers)

        bearer_token = request.json()['access_token']
        return bearer_token

class TwitterSearch:
    """UTF-8 and URL encodes query to Twitter Search API and stores the 
    resulting text from the Tweets in a list.

    Attributes:
        API_SEARCH_ENDPOINT: Search API URL endpoint.
    """
    API_SEARCH_ENDPOINT = 'https://api.twitter.com/1.1/search/tweets.json?q='

    def __init__(self, query, bearer_token):
        """ Initializes TwitterSearch object.

        Args:
            query: A string containing search terms.
            bearer_token: A string containg a bearer token generated by OAuthToken()
            object.

        For clarity:
            count: An integer representing the number of Tweets that will be 
            returned from search.
            lang: A string corresponding to the language of the tweets to be 
            searched.
            tweet_mode: A string, 'extended' means the Search API will return 
            full text of tweets with more than 280 characters. A blank string 
            will cause only the first 140 characters to be returned.
            url_suffix: A string to be added to search query URL. This string 
            contains parameters (lang, tweet_mode, count from above) that affect
            search results.
            search_results: A dictionary converted from search APIs JSON 
            response.
            tweet_text: A list of strings containing the text from Tweets.
            """
        self.query = self._modify_query(query)
        self.bearer_token = bearer_token
        self.count = 10
        self.lang = 'en'
        self.tweet_mode = 'extended'
        self.url_suffix = self._build_suffix()
        self.search_results = self.send_search(bearer_token)
        self.tweet_text = self._find_text()        

    def _modify_query(self,query):
        """Modifies query to exclude retweets and replies."""
        modified_query = "{} -filter:retweets -filter:replies".format(query)
        return modified_query

    def send_search(self,bearer_token):
        """Sends HTTP GET to send search to Twitter Search API.
        
        Args:
            bearer_token: A string containing bearer token.
        Returns:
            results: A dictionary created from Search API's JSON response for a
            given search.
        """
        encoded_query = urllib.parse.quote(self.query.encode('utf-8'))
        url = self.API_SEARCH_ENDPOINT + encoded_query + self.url_suffix
        headers = {
            'User-Agent':'TemperatureOfTheRoom',
            'Authorization':'Bearer ' + self.bearer_token,
            'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'}
        response = requests.get(url, headers = headers)
        results = json.loads(response.content)
        return results

    def _build_suffix(self):
        """Builds a 'suffix' for the URL containing a search. There are many
        parameters built in to the Search API that could go here.
        """
        suffix = '&count={}&lang={}&tweet_mode={}'.format(
            self.count,
            self.lang,
            self.tweet_mode)
        return suffix

    def _find_text(self):
        """Stores the full text of the Tweets returned from the search in a
        list.

        Returns:
            A list of strings containing the full text for all Tweets returned 
            from sendSearch().
        """
        tweet_text = []
        for item in self.search_results['statuses']:
            tweet_text.append(item['full_text'])
        return tweet_text

class SentimentAnalysis:
    """Sends Tweet text to http://text-processing.com/api/sentiment/ and stores
    the response.

    Attributes:
        SENTIMENT_API_ENDPOINT: Sentiment Processing API endpoint.
    """
    SENTIMENT_API_ENDPOINT = 'http://text-processing.com/api/sentiment/'

    def __init__(self, tweet_text):
        """Initializes Sentiment Analysis object
        
        Args:
            tweet_text = a list of strings containing the text to be sent to 
            Sentiment Analysis API.
        """
        self.tweet_text = tweet_text
        self.sentiment_results = self._total_results()

    
    def get_sentiment(self, text):
        """Sends HTTP POST request to Text-Sentiment Sentiment-Analysis API
        
        Args:
            text: A string to be analyzed for sentiment.
        
        Returns:
            A string containing either 'Positive', 'Negative', or 'Neutral',
            depending on the 'label' in API response.
        """
        headers = {
            'X-Mashape-Key':'Zx3Hnd9BrvmshEBx4i5UfCZlJqHKp1ddegSjsnmdXY62V9Ndsh',
			'Content-Type':'application/x-www-form-urlencoded',
			'Accept':'application/json'}
        body = {'language':'english', "text":text}
        response = requests.post(
            SentimentAnalysis.SENTIMENT_API_ENDPOINT,
            data = body,
            headers = headers)
        sentiment_result = json.loads(response.content)
        sentiment_result = sentiment_result['label']

        # Change sentiment labels to full words.
        # TODO Move this to view or template, since this is only for display 
        # purposes.
        if (sentiment_result == 'pos'):
            sentiment_result = 'Positive'
        if (sentiment_result == 'neg'):
            sentiment_result = 'Negative'
        if (sentiment_result == 'neutral'):
            sentiment_result = 'Neutral'
        return sentiment_result

    def _total_results(self):
        """ Creates a list of sentiment results by sending each string in 
        tweet_text to Sentiment-Analysis API individually.

        Returns:
            A list containing sentiment analysis results corresponding to each
            string in tweet_text.
        """
        sentiment_results = []
        for item in self.tweet_text:
            sentiment_results.append(self.get_sentiment(item))
        return sentiment_results






