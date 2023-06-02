# -*- coding:utf-8 -*-
import json
import os


class TrainInfoWriter:

    def __init__(self,file=None, model_root_path=None, algo_name=None, model_name=None, model_version=None):
        if file:
            self.info_path = file
        else:
            self.info_path = model_root_path + "/" + model_name + "_" + model_version
        if not os.path.exists(self.info_path):
            os.makedirs(self.info_path)

        self.train_info_file_path = self.info_path + "/train_info.json"
        train_info = {
            "algo_name": algo_name,
            "model_name": model_name,
            "model_version": model_version,
            "model_status": "not_start",
            "model_size": None,
            "data_process_status": "not_start",
            "train_info": {}
        }
        if not os.path.exists(self.train_info_file_path):
            with open(self.train_info_file_path, 'w', encoding="utf-8") as file_obj:
                json.dump(train_info, file_obj)

    def update_model_status(self, model_status):
        with open(self.train_info_file_path, 'r', encoding='utf-8') as file_obj:
            train_info = json.load(file_obj)

        train_info["model_status"] = model_status

        with open(self.train_info_file_path, 'w', encoding="utf-8") as file_obj:
            json.dump(train_info, file_obj)

    def update_model_size(self, model_size):
        with open(self.train_info_file_path, 'r', encoding='utf-8') as file_obj:
            train_info = json.load(file_obj)

        train_info["model_size"] = model_size

        with open(self.train_info_file_path, 'w', encoding="utf-8") as file_obj:
            json.dump(train_info, file_obj)

    def update_train_time(self, train_time):
        with open(self.train_info_file_path, 'r', encoding='utf-8') as file_obj:
            train_info = json.load(file_obj)

        train_info["train_info"]["train_time"] = train_time

        with open(self.train_info_file_path, 'w', encoding="utf-8") as file_obj:
            json.dump(train_info, file_obj)

    def update_data_process_status(self, data_process_status):
        with open(self.train_info_file_path, 'r', encoding='utf-8') as file_obj:
            train_info = json.load(file_obj)

        train_info["data_process_status"] = data_process_status

        with open(self.train_info_file_path, 'w', encoding="utf-8") as file_obj:
            json.dump(train_info, file_obj)

    def update_train_progress(self, epochs=None, train_data_size=None, dev_data_size=None, loss=None, precession=None
                              , recall=None, f1=None):
        if epochs:
            with open(self.train_info_file_path, 'r', encoding='utf-8') as file_obj:
                train_info = json.load(file_obj)
                train_info["train_info"]["epochs"] = epochs
            with open(self.train_info_file_path, 'w', encoding="utf-8") as file_obj:
                json.dump(train_info, file_obj)

        if train_data_size:
            with open(self.train_info_file_path, 'r', encoding='utf-8') as file_obj:
                train_info = json.load(file_obj)
                train_info["train_info"]["train_data_size"] = train_data_size
            with open(self.train_info_file_path, 'w', encoding="utf-8") as file_obj:
                json.dump(train_info, file_obj)
        if dev_data_size:
            with open(self.train_info_file_path, 'r', encoding='utf-8') as file_obj:
                train_info = json.load(file_obj)
                train_info["train_info"]["dev_data_size"] = dev_data_size
            with open(self.train_info_file_path, 'w', encoding="utf-8") as file_obj:
                json.dump(train_info, file_obj)

        if loss:
            with open(self.train_info_file_path, 'r', encoding='utf-8') as file_obj:
                train_info = json.load(file_obj)
                train_info["train_info"]["loss"] = loss
            with open(self.train_info_file_path, 'w', encoding="utf-8") as file_obj:
                json.dump(train_info, file_obj)

        if precession:
            with open(self.train_info_file_path, 'r', encoding='utf-8') as file_obj:
                train_info = json.load(file_obj)
                train_info["train_info"]["precession"] = precession
            with open(self.train_info_file_path, 'w', encoding="utf-8") as file_obj:
                json.dump(train_info, file_obj)

        if recall:
            with open(self.train_info_file_path, 'r', encoding='utf-8') as file_obj:
                train_info = json.load(file_obj)
                train_info["train_info"]["recall"] = recall
            with open(self.train_info_file_path, 'w', encoding="utf-8") as file_obj:
                json.dump(train_info, file_obj)
        if f1:
            with open(self.train_info_file_path, 'r', encoding='utf-8') as file_obj:
                train_info = json.load(file_obj)
                train_info["train_info"]["f1"] = f1
            with open(self.train_info_file_path, 'w', encoding="utf-8") as file_obj:
                json.dump(train_info, file_obj)


class PredictInfoWriter:

    def __init__(self, file=None,prediction_output_path=None, algo_name=None, prediction_output_name=None):
        if file:
            self.info_path = file
        else:
            self.info_path = prediction_output_path + "/" + prediction_output_name
        if not os.path.exists(self.info_path):
            os.makedirs(self.info_path)

        self.predict_info_file_path = self.info_path + "/predict_info.json"
        predict_info = {
            "algo_name": algo_name,
            "corpus_name": prediction_output_name,
            "predict_status": "not_start",
            "predict_info": {}
        }
        if not os.path.exists(self.predict_info_file_path):
            with open(self.predict_info_file_path, 'w', encoding="utf-8") as file_obj:
                json.dump(predict_info, file_obj)

    def update_predict_status(self, predict_status):
        with open(self.predict_info_file_path, 'r', encoding='utf-8') as file_obj:
            predict_info = json.load(file_obj)

        predict_info["predict_status"] = predict_status

        with open(self.predict_info_file_path, 'w', encoding="utf-8") as file_obj:
            json.dump(predict_info, file_obj)

    def update_predict_progress(self, corpus_file_name, corpus_file_name_status):

        with open(self.predict_info_file_path, 'r', encoding='utf-8') as file_obj:
            train_info = json.load(file_obj)
            train_info["predict_info"][corpus_file_name] = corpus_file_name_status
            with open(self.predict_info_file_path, 'w', encoding="utf-8") as file_obj:
                json.dump(train_info, file_obj)


def get_file_size(dir):
    def getFileFolderSize(fileOrFolderPath):
        """get size for file or folder"""
        totalSize = 0

        if not os.path.exists(fileOrFolderPath):
            return totalSize

        if os.path.isfile(fileOrFolderPath):
            totalSize = os.path.getsize(fileOrFolderPath)  # 5041481
            return totalSize

        if os.path.isdir(fileOrFolderPath):
            with os.scandir(fileOrFolderPath) as dirEntryList:
                for curSubEntry in dirEntryList:
                    curSubEntryFullPath = os.path.join(fileOrFolderPath, curSubEntry.name)
                    if curSubEntry.is_dir():
                        curSubFolderSize = getFileFolderSize(curSubEntryFullPath)  # 5800007
                        totalSize += curSubFolderSize
                    elif curSubEntry.is_file():
                        curSubFileSize = os.path.getsize(curSubEntryFullPath)  # 1891
                        totalSize += curSubFileSize
                return totalSize

    return int(getFileFolderSize(dir) / 1024)


if __name__ == '__main__':
    print(get_file_size("F:\\project\\AI\\NER-spacy\data\model\\0628_v1\model"))
