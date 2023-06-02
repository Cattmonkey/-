# -*- coding:utf-8 -*-
# 3类实体，5种属性，2类事件


class HM:
    huashendunhao = {"hm1.type_id":"HM",
        "hm1.hm-chishuishendu": 12,
                     "hm1.hm-gouzaoshijian": 19980925,
                     "hm1.hm-xiashuishujian": 19990523,
                     "hm1.hm-paishuiliang": 6,
                     "hm1.hm-guojia": "中国",
                     "hm1.hm-ciji": "福特级航空母舰",
                     "hm1.hm-jiantingleixing": "核动力航空母母舰"}

    ligenhao = {"hm2.type_id":"HM",
        "hm2.hm-chishuishendu": 18,
        "hm2.hm-gouzaoshijian": 19980212,
        "hm2.hm-xiashuishujian": 20010304,
        "hm2.hm-paishuiliang": 9.7,
        "hm2.hm-guojia": "美国",
        "hm2.hm-ciji": "福特级航空母舰",
        "hm2.hm-jiantingleixing": "大型核动力航空母母舰"}

    qiyehao = {"hm3.type_id":"HM",
        "hm3.hm-chishuishendu": 10,
        "hm3.hm-gouzaoshijian": 19500102,
        "hm3.hm-xiashuishujian": 19600924,
        "hm3.hm-paishuiliang": 10,
        "hm3.hm-guojia": "美国",
        "hm3.hm-ciji": "尼米兹级航空母舰",
        "hm3.hm-jiantingleixing": None}


class JD:
    hengxuhe = {"jd1.type_id":"JD",
        "jd1.jd-local": "神奈川县横须贺市",
                "jd1.jd-jiancheng": "横须贺基地",
                "jd1.jd-goujianshijian": 19470521,
                "jd1.jd-guojia": "日本",
                }

    zuoshibao = {"jd2.type_id":"JD",
                 "jd2.jd-local": "佐世保",
                 "jd2.jd-jiancheng": "佐世保基地",
                 "jd2.jd-goujianshijian": 18830205,
                 "jd2.jd-guojia": "日本"}


class SJ:
    junshiyanxi = {"sj1.type_id":"SJ",
                   "sj1.sj-shijian": 20220707,
                   "sj1.sj-didian": "横须贺基地",
                   "sj1.sj-canyanguo": "美国",
                   }

    ziyouhangxing = {"sj2.type_id":"SJ",
                     "sj2.sj-shijian": 20100215,
                     "sj2.sj-didian": "台湾海峡",
                     "sj2.sj-guojia": "日本"}

    xxzhanzheng = {"sj3.type_id":"SJ",
                   "sj3.sj-shijian": 20010215,
                   "sj3.sj-didian": "日本",
                   "sj3.sj-guojia": "美国"}


class Relation:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes


class SPO:
    triples = [(HM.huashendunhao, Relation(name="驶入", attributes={"e-time": 20150625,"type_id":"驶入"}), JD.hengxuhe),
               (HM.ligenhao, Relation(name="驶出", attributes={"e-time": 20180625,"type_id":"驶出"}), JD.hengxuhe),
               (HM.qiyehao, Relation(name="驻扎", attributes={"e-time": 20130625,"type_id":"驻扎"}), JD.zuoshibao),
               (HM.qiyehao, Relation(name="驶入", attributes={"e-time": 20150625,"type_id":"驶入"}), JD.hengxuhe),
               (HM.qiyehao, Relation(name="同行", attributes={"e-time": 20120625,"type_id":"同行"}), HM.ligenhao),
               (SJ.junshiyanxi, Relation(name="参演航母", attributes={"e-time": 20170625,"type_id":"参演航母"}), HM.ligenhao),
               (SJ.ziyouhangxing, Relation(name="参加航母", attributes={"e-time": 20190625,"type_id":"参加航母"}), HM.huashendunhao),
               (SJ.junshiyanxi, Relation(name="演习基地", attributes={"e-time": 20210625,"type_id":"演习基地"}), JD.hengxuhe),
               (SJ.xxzhanzheng, Relation(name="参加航母", attributes={"e-time": 20010215,"type_id":"参加航母"}), HM.ligenhao),
               ]


def get_nodes():
    # return [HM.ligenhao, HM.huashendunhao, HM.qiyehao,
    #         JD.hengxuhe, JD.zuoshibao, SJ.junshiyanxi,
    #         SJ.ziyouhangxing, SJ.xxzhanzheng]
    nodes = {"errors": [{"code": 0}],
             "results": [{"data": [{"row": [HM.ligenhao]},
                                  {"row": [HM.qiyehao]},
                                  {"row": [HM.huashendunhao]},
                                  {"row": [JD.hengxuhe]},
                                  {"row": [JD.zuoshibao]},
                                  {"row": [SJ.junshiyanxi]},
                                  {"row": [SJ.xxzhanzheng]},
                                  {"row": [SJ.ziyouhangxing]},
                                  ]}]
             }
    return nodes


def get_triples():
    edges = {"errors": [{"code": 0}],
             "results": [{"data": [
                 {"row": [[HM.huashendunhao, rel(name="驶入", edgeId="e1", attributes={"e-time": 20150625,
                                                                                     "e-a": 1,
                                                                                     "e-b": 1,
                                                                                     "e-c": "abcd",
                                                                                     "type_id":"驶入"}), JD.hengxuhe]]},
                 {"row": [[HM.ligenhao, rel(name="驶出", edgeId="e2", attributes={"e-time": 20180625,
                                                                                "e-a": 2,
                                                                                "e-b": 1,
                                                                                "type_id":"驶出"}), JD.hengxuhe]]},
                 {"row": [[HM.qiyehao, rel(name="驻扎", edgeId="e3", attributes={"e-time": 20130625,
                                                                               "e-a": 8,
                                                                               "e-b": 8,
                                                                               "e-c": "abc",
                                                                               "type_id":"驻扎"}), JD.zuoshibao]]},
                 {"row":[ [HM.qiyehao, rel(name="驶入", edgeId="e4", attributes={"e-time": 20150625,
                                                                               "e-a": 5,
                                                                               "e-b": 15,
                                                                               "e-c": "d",
                                                                               "type_id":"驶入"}), JD.hengxuhe]]},
                 {"row":[ [HM.qiyehao, rel(name="同行", edgeId="e5", attributes={"e-time": 20120625,
                                                                               "e-a": 2,
                                                                               "e-b": 1,
                                                                               "e-c": "abc",
                                                                               "type_id":"同行"}), HM.ligenhao]]},
                 {"row": [[SJ.junshiyanxi, rel(name="参演航母", edgeId="e6", attributes={"e-time": 20170625,
                                                                                     "e-a": 4,
                                                                                     "e-b": 17,
                                                                                     "e-c": "abc",
                                                                                     "type_id":"参演航母"}), HM.ligenhao]]},
                 {"row": [[SJ.ziyouhangxing, rel(name="参加航母", edgeId="e7", attributes={"e-time": 20190625,
                                                                                       "e-a": 2,
                                                                                       "e-b": 14,
                                                                                       "e-c": "abc",
                                                                                       "type_id":"参加航母"}),
                          HM.huashendunhao]]},
                 {"row": [[SJ.junshiyanxi, rel(name="演习基地", edgeId="e8", attributes={"e-time": 20210625,
                                                                                     "e-b": 19,
                                                                                     "e-c": "abc",
                                                                                     "type_id":"演习基地"}), JD.hengxuhe]]},
                 {"row": [[SJ.xxzhanzheng, rel(name="参加航母", edgeId="e9", attributes={"e-time": 20010215,
                                                                                     "type_id":"参加航母"}), HM.ligenhao]]}

                 ]}]
             }

    return edges


def rel(name, edgeId, attributes):
    r = {"name": name, "edgeId": edgeId}
    r.update(attributes)
    return r


if __name__ == '__main__':
    print(SPO.triples)
    pass
