from src.zarinpal import ZarinPal
from src.utils.Config import Config

def get_transactions():
    try:
        config = Config(
            access_token= "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiYzIxOTY5MTNjNTk2MWNkMTE3NWM1NjZhZDBjOTRkMjhlN2ZjZjQ1NzEyY2UyYzJjYjkxZjM5MDEyNWNkZGFiOGRiZmZhMDgyZjU0MzFkZTUiLCJpYXQiOjE3MzYzNDc5MDguODUzMjMzLCJuYmYiOjE3MzYzNDc5MDguODUzMjQ2LCJleHAiOjE4OTQxMTQzMDguNzgxNTI2LCJzdWIiOiIxNDQxNDU3Iiwic2NvcGVzIjpbXX0.Xr3fiM3ZoYiFsITrw0w9mLzyYsAIYcdH02FKrHjPrSyt4oWM3AwOkgqZgl0X7K7AdFIjMt2jASKjWgm7qj5Cojz0MZgWY8Hrf_R78cQVMEdgV_MbCD5DZED61Pvan_obe897IKzMcdsURSuIbSobcmQ4-DdrjaAGyHlhftQljF7IupBjDZUhNq_HWS8Dh52UyJNTblMGVtFg2ukxmoJMvtGO6ph9NHXpiXbnpK1Cjo4YPpcuPkjrUHUZgh90fGGLYCCK6RkdwgNGsoDEI7MmyClhHC2zlIPNtKIRUfqwzJdtB0XJKmZ7Na7jzBbI1pEtg6HuLOL6pgbj1Sy3bF1Z1NjZ_3aJwS5fQ1xaL7IBMPNWwvJOXbwZCrV9VF7h33JgSUCtE1nXgw9tMU84D312VQbB5u_qRLU0GidmcZG5yPy89ZSZHvEnikhy2aXNqPyRGABI501TfqeSDv2Qs5CIkyl3PVWpuO0eG-MT3Jjc-J6Zvr2a1ZLXgw1D2X-11uK4UtxxPljrTclMEkKvfRm2EUNzClKyjvNqGpHlzTTPDAIhlGsLaMV9eN63hAZtanlpIL7bltrZnKhEFqqtuWYGP-JRMtU9wh1kUey12LaqyMkDreEImW90P41cJ1L3oRu0MYdDzujOheiKtFrNnWFmn8zNUjB1T8Gm2SUdm9s3I3w",
        )
        zarinpal = ZarinPal(config)

        transactions = zarinpal.transactions.list({
            "terminal_id": "387152",
            "filter": "PAID",  
            "limit": 10,  
            "offset": 0,
            
        })

        print("Transactions List:", transactions)
        
    except Exception as e:
        print("Error fetching transactions:", e)

if __name__ == "__main__":
    get_transactions()