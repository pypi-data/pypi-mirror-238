# cognite-ai

A set of AI tools for working with CDF in Python. 

## Smart data frames
Chat with your data using LLMs. Built on top of [PandasAI](https://docs.pandas-ai.com/en/latest/) If you have loaded data into a Pandas dataframe, you can run

Install the package
```
%pip install cognite-ai
```

Chat with your data
```
from cognite.ai import load_pandasai
SmartDataframe, SmartDatalake = await load_pandasai()

workorders_df = client.raw.rows.retrieve_dataframe("tutorial_apm", "workorders", limit=-1).to_pandas()
workitems_df = client.raw.rows.retrieve_dataframe("tutorial_apm", "workitems", limit=-1).to_pandas()
workorder2items_df = client.raw.rows.retrieve_dataframe("tutorial_apm", "workorder2items", limit=-1).to_pandas()
workorder2assets_df = client.raw.rows.retrieve_dataframe("tutorial_apm", "workorder2assets", limit=-1).to_pandas()
assets_df = client.raw.rows.retrieve_dataframe("tutorial_apm", "assets", limit=-1).to_pandas()

from cognite.client import CogniteClient
client = CogniteClient()

smart_lake_df = SmartDatalake([workorders_df, workitems_df, assets_df, workorder2items_df, workorder2assets_df], cognite_client=client)
smart_lake_df.chat("Which workorders are the longest, and what work items do they have?")


s_workorders_df = SmartDataframe(workorders_df, cognite_client=client)
s_workorders_df.chat('Which 5 work orders are the longest?')
```
