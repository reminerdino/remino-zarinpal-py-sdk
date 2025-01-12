from zarinpal import ZarinPal
from utils.Config import Config


def generate_payment_url(base_url, authority):
    start_pay_url = "/pg/StartPay/"
    return f"{base_url}{start_pay_url}{authority}"

def initiate_payment():
    try:
        config = Config(
            merchant_id="Your Merchent Id",  
            sandbox=True,  
        )
        zarinpal = ZarinPal(config)
        response = zarinpal.payments.create({
            "amount": 10000, 
            "callback_url": "https://zarinpal.com/", 
            "description": "Payment creat", 
            "mobile": "09123456789",  
            "email": "customer@example.com",  
            "cardPan": ["6219861034529007", "5022291073776543"], 
            "referrer_id": "affiliate123", 
        })

        print("Payment created successfully:", response)
        
        if "data" in response and "authority" in response["data"]:
            authority = response["data"]["authority"]
            payment_url = generate_payment_url(zarinpal.base_url, authority)
            print("Payment URL:", payment_url)
        else:
            print("Authority not found in response.")


    except Exception as e:
        print("Error during payment creation:", e)

if __name__ == "__main__":
    initiate_payment()