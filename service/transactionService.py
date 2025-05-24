import httpx

class TransactionService:
    async def get_transactions_by_sender_id(self, sender_id: int):
        spring_boot_url = f"http://localhost:8080/api/transaction/user/{sender_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(spring_boot_url)
            response.raise_for_status()

        return response.json()

service = TransactionService()