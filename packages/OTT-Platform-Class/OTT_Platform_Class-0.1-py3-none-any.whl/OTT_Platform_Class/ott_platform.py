# %%
import json

# %%
with open(r'C:\Users\minautee.m\Downloads\ea94cbce-f829-4405-8758-378610adcd15_83d04ac6-cb74-4a96-a06a-e0d5442aa126_ott_nested_small.json', 'r') as file:
    ott_data = json.load(file)

# %%
ott_data

# %%
def count_subscription_type(ott_data, ott_platform='HBO Max'):
    total_revenue = 0.0

    for customer in ott_data:
        for subscription in customer['Subscriptions']:
            if subscription['OTTPlatform'] == ott_platform:
                total_revenue += subscription['AmountPaid']

    return total_revenue

# %%
# Calculate total revenue for HBO Max
total_revenue_hbo = count_subscription_type(ott_data)
print(f"Total revenue for HBO Max: {total_revenue_hbo}")

# Calculate total revenue for Disney+
total_revenue_disney = count_subscription_type(ott_data, ott_platform='Disney+')
print(f"Total revenue for Disney+: {total_revenue_disney}")

# %%
import pandas as pd

# %%
import pprint

pp = pprint.PrettyPrinter(indent=2)

# %%
def json_to_df(data_dict: dict) -> pd.DataFrame:
    data_list=[]

    for customer in ott_data:
        for subscription_info in customer['Subscriptions']:
            for watch_history in subscription_info['WatchHistory']:
                subscription_data = {
                    'Customer_ID': customer['CustomerID'],
                    'Name':customer['CustomerName'],
                    'OTT_Platform': subscription_info['OTTPlatform'],
                    'Subscription_Date': subscription_info['SubscriptionDate'],
                    'Subscription_Type': subscription_info['SubscriptionType'],
                    'Duration': subscription_info['Duration'],
                    'Amount_Paid': subscription_info['AmountPaid'],
                    'Title': watch_history['Title'],
                    'Date_Watched': watch_history['DateWatched'],
                    'Duration_Watched': watch_history['DurationWatched']                 
                }
                data_list.append(subscription_data)
    
    df = pd.DataFrame(data_list)
    return df
        


# %%
ott_df = json_to_df(ott_data)
ott_df

# %%
class AlreadySubscribedError(Exception):
    def __init__(self, plan_name):
        self.plan_name = plan_name
        super().__init__(f'Already subscribed to {plan_name}')

# %%
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.subscription_plan = None
        self.watched_content = []

    def subscribe(self, plan_name):
        if self.subscription_plan is not None and plan_name in self.subscription_plan:
            raise AlreadySubscribedError(plan_name)
        if self.subscription_plan is None:
            self.subscription_plan = [plan_name]
        else:
            self.subscription_plan.append(plan_name)
        return f"Subscribed to {plan_name}"

    def watch(self, content_name):
        if self.subscription_plan is None:
            return "You don't have access to this content"
        else:
            return f"Watching {content_name}"

    def get_watch_history(self):
        return self.watched_content

# %%
User1 = User(user_id=2000, name="Alice Smith")

# %%
User1.subscribe("Premium")

# %%
User1.watch("Big Bang Theory")

# %%
User1.get_watch_history()

# %%



