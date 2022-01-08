import requests
from api.parentchecker import ParentChecker
import json



URL1 = "https://payments.braintree-api.com/graphql"

HEADERS1 = """Host: payments.braintree-api.com
Connection: keep-alive
Content-Length: 733
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2NDE3MDA3MTMsImp0aSI6ImZlMGU5NDFlLTk1NWItNGViYy05MzRmLTM5ZmNhNWIwNDE1OSIsInN1YiI6IjRtM21oNzI1NWQ3eHJzN2oiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6IjRtM21oNzI1NWQ3eHJzN2oiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0Il0sIm9wdGlvbnMiOnsibWVyY2hhbnRfYWNjb3VudF9pZCI6ImRlcm1hY2FyZWRpcmVjdEdCUCJ9fQ.ecnQr3XK0rNeQwcb81d-HLw0FiNghSlDDbIGZlX7cX7NX0IwtK3sqzWxG-E1YdQthvq2uVcFcAf9IVO6ok-bhQ
Content-Type: application/json
sec-ch-ua-mobile: ?1
User-Agent: Mozilla/5.0 (Linux; Android 12; Phone 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36
Braintree-Version: 2018-05-10
sec-ch-ua-platform: "Android"
Accept: */*
Origin: https://assets.braintreegateway.com
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://assets.braintreegateway.com/
Accept-Encoding: gzip, deflate, br
Accept-Language: es-US,es;q=0.9
"""

# format: ccn, month year, cvc
POSTDATA1 = """{{"clientSdkMetadata":{{"source":"client","integration":"custom","sessionId":"a789396e-0013-4ef4-ad97-267c2143ff9e"}},"query":"mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {{   tokenizeCreditCard(input: $input) {{     token     creditCard {{       bin       brandCode       last4       expirationMonth      expirationYear      binData {{         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }}     }}   }} }}","variables":{{"input":{{"creditCard":{{"number":"{ccn}","expirationMonth":"{month}","expirationYear":"{year}","cvv":"{cvc}"}},"options":{{"validate":false}}}}}},"operationName":"TokenizeCreditCard"}}"""



class check(parentchecker):
    """arg: Only the card details separated by |"""
    def __init__(self, card):
        super().__init__(card):

    def requests_1(self):
        url = URL1
        headers = super().format_headers(HEADERS1)
        postdata = 
