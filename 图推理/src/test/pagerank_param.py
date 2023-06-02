# -*- coding:utf-8 -*-
"""
1、------------图谱信息------------
1）节点与边的结构
2）节点的属性
3）边的属性

2、------------图信息------------
1）节点与边的结构（有向与无向图）
2）边的属性的权重
3）节点的属性权重


3、------------信息转换------------
基于知识图谱数据信息，通过图计算手段，对知识图谱进行算法分析，将知识图谱中的可利用信息转化成图算法可利用的信息，主要有三个个方面：
   ---> 图普（或子图普）的结构转化为图的结构
   ---> 图谱中关系的属性转化为图中边的权重
   ---> 图普中实体的属性转化为图中节点的权重

3、------------图计算-----------
   --->pagerank
   --->lpa
   --->...
"""

params = {
    # entities 暂时保留
    "entities": [
        {
            "type": "ENTITY",
            "type_id": "12334621",  # 如航空母舰
            "weight_subject_to": [0.8]  # 实体的权重属性赋值，必须 0-1之间
        }
    ],

    # 关系重要性配置
    "relations": [
        {
            "type": "ENTITY",
            "relation_id": "232132321",  # 如：航空母舰与地区之间的部署关系的id
            "start_type_id": "6111123131",  # 如：航空母舰
            "end_type_id": "13485411231",  # 如：地区
            "weight_subject_to": [0.6]  # #关系的权重属性赋值，必须 0-1之间
        },
        {
            "type": "EVENT",
            "relation_id": "232132321",  # 如：演习事件与参演航母的关系id
            "start_type_id": "13463445213",  # 如xxx军事演习事件id
            "end_type_id": "146213155453",  # 如参演航母id，
            "weight_subject_to": [0.6]  # #关系的权重属性赋值，必须 0-1之间
        }
    ],
    # 属性重要性配置，包含实体属性，关系的属性，事件的属性
    "attributes": [
        {
            "type": "ENTITY",
            "type_id": "232132321",  # 如：航空母舰的id
            "attribute_id": "121223235",  # 如航空母舰的排水量id
            "value_type": "NUMERICAL",  # 如 数值型
            "rule": "ASCENDING",  # 大写
            "rule_subject_to": [],  # 约束区间
            "weight_subject_to": [0, 1]  # 约束区间，必须 0-1之间
        },
        {
            "type": "RELATION",
            "type_id": "232132321",
            "attribute_id": "121223235",
            "value_type": "NUMERICAL",  # 如 数值型
            "rule": "DESCENDING",
            "rule_subject_to": [],  # 约束区间
            "weight_subject_to": [0, 1]  # 约束区间
        },
        {
            "type": "EVENT",
            "type_id": "12132312",  # 如，xxx军事演习事件id
            "attribute_id": "445121",  # 如：演习时间id
            "value_type": "NUMERICAL",  # 如 数值型
            "rule": "DESCENDING",
            "rule_subject_to": [],  # 约束区间
            "weight_subject_to": [0.5, 1.0]  # 约束区间
        },
        {
            "type": "ENTITY",
            "type_id": "232132321",  # 如：航空母舰的id
            "attribute_id": "121223235",  # 如航空母舰的键长id
            "value_type": "NUMERICAL",  # 如 数值型
            "rule": "BETWEEN",
            "rule_subject_to": [250, 300],  # 约束区间
            "weight_subject_to": [0.8]  # 属性权重约束区间
        },
        {
            "type": "ENTITY",
            "type_id": "232132321",  # 如：航空母舰的id
            "attribute_id": "121223235",  # 如航空母舰的键长id
            "value_type": "NUMERICAL",  # 如 数值型
            "rule": "GT",  # EQ，LT，GT，LEQ，GEQ 同理
            "rule_subject_to": [100],  # 约束区间
            "weight_subject_to": [0.9]
        },
        # 以下是字符型
        {
            "type": "ENTITY",
            "type_id": "232132321",  # 如：航空母舰的id
            "attribute_id": "121223235",  # 如航空母舰的级别id
            "value_type": "CHARACTER",  # 如 字符型
            "rule": "ASCENDING",  # 升序
            "rule_subject_to": ["A", "B", "C", "D"],  # 值约束区间
            "weight_subject_to": [0.8, 1.0]
        },
        {
            "type": "ENTITY",
            "type_id": "232132321",  # 如：航空母舰的id
            "attribute_id": "121223235",  # 如航空母舰的级别id
            "value_type": "CHARACTER",  # 如 字符型
            "rule": "EQ",  # 等于
            "rule_subject_to": ["尼米兹级"],  # 值约束区间
            "weight_subject_to": [0.8]
        },
        {
            "type": "ENTITY",
            "type_id": "232132321",  # 如：航空母舰的id
            "attribute_id": "121223235",  # 如航空母舰的级别id
            "value_type": "CHARACTER",  # 如 字符型
            "rule": "CONTAINS",  # 包含
            "rule_subject_to": ["尼米兹"],  # 值约束区间
            "weight_subject_to": [0.8]
        },
        {
            "type": "ENTITY",
            "type_id": "232132321",  # 如：航空母舰的id
            "attribute_id": "121223235",  # 如航空母舰的级别id
            "value_type": "CHARACTER",  # 如 字符型
            "rule": "IN",  # 被包含
            "rule_subject_to": ["尼米兹级", "企业级", "金刚级"],  # 值约束区间
            "weight_subject_to": [0.9]
        },
    ]
}
