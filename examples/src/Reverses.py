from src.Zarinpal import ZarinPal
from src.utils.Config import Config

def reverse_transaction():
    try:
        config = Config(
            merchant_id= "Your Merchent Id",
            sandbox=True, 
        )
        zarinpal = ZarinPal(config)

        response = zarinpal.reversals.reverse({
            #Enter authority:
            "authority": " ",  
        })

        print("Transaction Reversed Successfully:", response)
    except Exception as e:
        print("Error during transaction reversal:", e)

if __name__ == "__main__":
    reverse_transaction()