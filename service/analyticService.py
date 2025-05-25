import pandas as pd

from service.transactionService import service as transaction_service

class AnalyticService:
    async def category_distribution(self, sender_id: int):
        transactions = await transaction_service.get_transactions_by_sender_id(sender_id)
        dataframe = pd.DataFrame(transactions)
        dataframe['category_name'] = dataframe['category'].apply(lambda x: x.get('name'))
        category_distribution = dataframe.groupby('category_name')['amount'].sum().sort_values(ascending=False).to_dict()

        return category_distribution

service = AnalyticService()