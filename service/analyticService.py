import pandas as pd

from service.transactionService import service as transaction_service

class AnalyticService:
    async def category_distribution(self, sender_id: int):
        transactions = await transaction_service.get_transactions_by_sender_id(sender_id)

        dataframe = pd.DataFrame(transactions)
        dataframe['category_id'] = dataframe['category'].apply(lambda x: x.get('id'))
        dataframe['category_name'] = dataframe['category'].apply(lambda x: x.get('name'))
        
        grouped = dataframe.groupby(['category_id', 'category_name'])['amount'].sum()

        category_distribution = [
            {
                "id": (idx[0] if idx[0] is not None else 0),
                "label": (idx[1] if idx[1] is not None else "No Category"),
                "value": amount
            }
            for idx, amount in grouped.sort_values(ascending=False).items()
        ]

        return category_distribution

service = AnalyticService()