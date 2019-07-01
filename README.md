神秘博士 模拟对话生成器

让你能够和神秘博士对话！

基于GTP-2构建！

# 初步计划

基于huggingface的[transfer-learning-conv-ai](https://github.com/huggingface/transfer-learning-conv-ai)，针对剧本的特点，需要对input进行一些变化。

剧本要素：
- 场景描述：剧本中会有需要场景描述的词语，在这里可以作为input输入
- 角色基本信息：这部分信息在剧本没有直接体现，需要通过其他的渠道获取，例如BBC的演员性别、年龄、人物介绍之类的
- doctor的第几任的信息：每一任博士其实还是有一丢丢区别的，所以也可以把这种区别稍微理清一下。

## 剧本文本格式化

- **[Area 29]** 表示地点信息 需要保留
- (The Doctor leaves. Korwin's hands twitch.) 表示动作信息，忽略
- FRANCINE [OC] 在可视画面范围外发生的动作或对白，当成普通的训练语料，忽略掉[OC]
- 人物基本信息：来源于Doctor Who 官网[BBC DOCTOR WHO](https://www.bbc.co.uk/programmes/b006q2x0),这里暂时只考虑用第一段文本的介绍数据（爬虫的时候会把所有的介绍数据都爬下来），其实wiki上也有，不过感觉wiki上写的太详细了，没有必要

在使用爬虫将人物数据抓取下来之后，需要和剧本中的人物一一对应上。所以需要建立一个剧本任务数据库，记录每一集剧本的基本信息

#### 剧本数据库表设计



#### 格式化之后的数据样例

考虑到使用GPT-2，small的pretrain模型的输入维度是768，也就是在经过BPE之后整个的input长度不超过768，这里在划分训练集的时候需要注意的问题。
考虑按照剧本中的地点进行划分，只要输入长度不到768，就可以归在一个训练集中；如果长度超过768，则需要进行分割，分割的时候，尽量把Doctor的对话平均分在不同的sample中。
```json
{
    "place":"China",
    "profile":
        {"Doctor":"balabalabala","ROSE":"balebabalel"},
    "dialog":
        [
            {"Doctor":["sdfdsfdsf","sdfdsfdsfsd"]},
            {"ROSE":["balbalababaa"]}
        ]
}
```

## input设计

借鉴huggingface的“transfer-learning-conv-ai”，分为三个部分，persona，history，reply
这里需要在最开始添加一个place部分，同时需要将人物所有属性对应起来

### 详细设计

- embedding: 与“transfer-learning-conv-ai”相同，设计为三个，word/position/segment
- segment embedding: 分为

### 当前进度

- 已经从BBC上将能够找到的人物角色介绍抓取下来
- 剧本中的人物进行一一对应
- 剔除不含有doctor的场景

- 下一步需要开始进行分句和分词，同时对于场景进行分割，这里借鉴“transfer-learning-conv-ai”中构建数据集的部分