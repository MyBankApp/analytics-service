import asyncio
import httpx

class TransactionService:
    async def get_transactions_by_sender_id(self, sender_id: int):
        transaction_url = f"http://localhost:8080/api/transaction/user/{sender_id}"
        category_url = "http://localhost:8080/api/category"

        async with httpx.AsyncClient() as client:
            transactions, categories = await asyncio.gather(
                client.get(transaction_url),
                client.get(category_url)
            )

            transactions.raise_for_status()
            categories.raise_for_status()

        category_dict = {category["id"]: category for category in categories.json()}
        json_transactions = transactions.json()

        for transaction in json_transactions:
            transaction["category"] = category_dict.get(transaction["categoryId"])

        return json_transactions

service = TransactionService()