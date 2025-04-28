import pandas as pd
from sqlalchemy import create_engine
import json

engine = create_engine('postgresql+psycopg2://ue4cqkav5o8jfl:p9dda30e2c723dd7e46e474c00a4b57fb1fb991ebbab59cceb39fb1bbb2e9d47f@postgres-prod.wartnerpro.io:5432/d66k62itvf3kmq')

step_labels_client = {
    3: 'shipped',
    1011: 'recu_client',
    21: 'Stocked client',
    964: 'chute',
    965: 'chute',
    4: 'received'
}

query = """
SELECT 
    audits.auditable_id,
    audits.created_at,
    audits.new_step_id,
    salesforce.product2.name AS product_name
FROM public.audits
INNER JOIN followups ON audits.auditable_id = followups.id
INNER JOIN salesforce.quotelineitem ON followups.quoteline_sfid = salesforce.quotelineitem.sfid
INNER JOIN salesforce.quote ON salesforce.quotelineitem.quoteid = salesforce.quote.sfid
INNER JOIN salesforce.account ON salesforce.quote.accountid = salesforce.account.sfid
INNER JOIN salesforce.product2 ON salesforce.quotelineitem.product2__code__c = salesforce.product2.sfid
WHERE audits.new_step_id IN (3, 4, 21, 1011, 964, 965)
  AND salesforce.account.name = 'HOTEL GEORGE  V HSK  (GV)'
ORDER BY audits.auditable_id, audits.created_at
"""

df = pd.read_sql_query(query, engine)
df.columns = df.columns.str.strip().str.lower()
df['step_label'] = df['new_step_id'].replace(step_labels_client)

df_latest = df.sort_values('created_at').groupby('auditable_id').tail(1)

pivot_df = df_latest.pivot_table(index='product_name', columns='step_label', values='auditable_id', aggfunc='count', fill_value=0).reset_index()
pivot_data = pivot_df.to_dict(orient='records')

steps = {}
for step in ['shipped', 'recu_client', 'Stocked client', 'chute', 'received']:
    articles = df_latest[df_latest['step_label'] == step][['product_name', 'auditable_id']].to_dict(orient='records')
    steps[step] = articles

result = {
    "pivot": pivot_data,
    "steps": steps
}

with open("data_articles.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
