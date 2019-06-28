神秘博士 模拟对话生成器

让你能够和神秘博士对话！

基于GTP-2构建！

# 初步计划

基于huggingface的[transfer-learning-conv-ai](https://github.com/huggingface/transfer-learning-conv-ai)，针对剧本的特点，需要对input进行一些变化。

剧本要素：
- 场景描述：剧本中会有需要场景描述的词语，在这里可以作为input输入
- 角色基本信息：这部分信息在剧本没有直接体现，需要通过其他的渠道获取，例如BBC的演员性别、年龄、人物介绍之类的
- doctor的第几任的信息：每一任博士其实还是有一丢丢区别的，所以也可以把这种区别稍微理清一下。