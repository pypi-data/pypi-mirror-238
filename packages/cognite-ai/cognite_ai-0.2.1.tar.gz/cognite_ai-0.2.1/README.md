# cognite-ai

A set of AI tools for working with CDF in Python. 

## MemoryVectorStore
Store and query vector embeddings created from CDF. This can enable a bunch of use cases where the number of vectors aren't that big.

Install the package
```
%pip install cognite-ai
```

Then you can create vectors from text (both multiple lines or a list of strings) like this

```
from cognite.ai import MemoryVectorStore
vector_store = MemoryVectorStore(client)

vector_store.store_text("Hi, I am a software engineer working for Cognite.")
vector_store.store_text("The moon is orbiting the earth, which is orbiting the sun.")
vector_store.store_text("Coffee can be a great way to stay awake.")

vector_store.query_text("I am tired, what can I do?")
```

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
