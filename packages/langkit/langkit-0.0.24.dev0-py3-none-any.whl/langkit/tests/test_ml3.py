import langkit.llm_metrics as llmm
from langkit import LangKitConfig

no_response_config = LangKitConfig(
    prompt_languages={"", "en"},
    response_languages=set(),
    response_pattern_file_path=None,  # regexes are semi-international, could leave this as default
    response_sentiment_lexicon=None,
    response_theme_file_path=None,
    response_topic_model_path=None,
    response_toxicity_model_path=None,
    response_transformer_name=None,
)
schema = llmm.init(config=no_response_config)

import whylogs as why
from langkit.whylogs.samples import load_chats, show_first_chat

chats = load_chats()
results = why.log(chats, schema=schema)

for column in results.view().get_columns().keys():
  print(column)

