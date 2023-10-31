from .base import SynchronousMicrosoftApiClient


class SynchronousGraphClient(SynchronousMicrosoftApiClient):
    def __init__(
            self,
            tenant_id,
            client_id=None,
            client_secret=None,
            creds=None,
            scope='https://graph.microsoft.com/.default'):
        super().__init__(
            tenant_id,
            client_id,
            client_secret,
            creds,
            scope=scope,
            base_url='https://graph.microsoft.com/v1.0')

    def get(self, url, params=None, headers=None, token_retry=False, **kwargs):
        """
        Send a GET request to the specified URL.

        Available OData query parameters for Microsoft Graph API:

        - $filter: Filters the results based on a condition (e.g., "startswith(displayName, 'A')")
        - $select: Narrows the properties returned (e.g., "id,displayName")
        - $orderby: Orders the results based on properties (e.g., "displayName asc")
        - $skip: Skips a specified number of results
        - $top: Limits the number of results returned (up to 999)
        - $search: Performs a full-text search (e.g., "$search="displayName: 'John'")
        - $count: Returns the count of results (true or false)
        - $expand: Expands related entities inline

        Note: Not all parameters are available for all endpoints. Always
        consult Microsoft Graph API documentation for endpoint-specific details.

        :param url: URL for the GET request
        :param headers: Optional headers dictionary
        :param params: Optional dictionary of query parameters
        :param token_retry: Internal flag to ensure we don't enter an infinite
                            loop if there's a token issue
        :return: JSON response from the server
        """
        headers = self.adjust_headers_for_odata(params, headers)
        return super().get(
            url, params, headers=headers,
            token_retry=token_retry, **kwargs)

    def get_users(self, params=None):
        """
        fetch a list of users from the microsoft graph api.

        available odata query parameters for the /users endpoint:

        - $filter: filters the results based on a condition (e.g., "accountEnabled eq true")
        - $select: narrows the properties returned (e.g., "id,displayName,mail")
        - $orderby: orders the results based on properties (e.g., "displayName asc")
        - $skip: skips a specified number of results
        - $top: limits the number of results returned (up to 999)
        - $count: returns the count of results (true or false)
        - $expand: expands related entities inline (e.g., "manager,memberOf")
        - $search: performs a full-text search on specific properties
                   (requires 'ConsistencyLevel' header to be set to 'eventual')

        for detailed information and additional query options, consult the
        official microsoft graph api documentation for the /users endpoint:
        https://docs.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0

        :param params: optional dictionary of query parameters
        :return: list of users
        """
        endpoint = f'{self.base_url}/users'
        return list(self.yield_result(endpoint, params))

    def subscribed_skus(self, **kwargs):
        url = f'{self.base_url}/subscribedSkus'
        return list(self.yield_result(url, **kwargs))

    def subscribed_skus_map(self, **kwargs):
        return {
            x['skuId']: x['skuPartNumber']
            for x in self.subscribed_skus(params={
                '$select': 'skuId,skuPartNumber',
            })
        }
