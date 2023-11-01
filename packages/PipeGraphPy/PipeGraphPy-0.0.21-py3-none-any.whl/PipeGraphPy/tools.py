#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import signal
import copy
import pandas as pd
from contextlib import  contextmanager
from PipeGraphPy.db.models import GraphsTB, PredictRecordTB
from datetime import datetime, timedelta
from PipeGraphPy.config import settings
from PipeGraphPy.db.utils import update_node_params
from PipeGraphPy.constants import MODULES
from PipeGraphPy.common import multi_graph
from PipeGraphPy.logger import rlog


def print_to_run_log(*args, graph_id=None, rlog_record_id=None):
    '''将内容输出到run_log里，前端来展示
    params:
        args: 要打印的内容
        graph_id: 运行图id
        rlog_record_id: 运行记录id
    '''
    assert graph_id, 'graph_id必传'
    msg = '\n'.join([str(i) for i in args])
    if settings.SDK_SHOW_LOG:
        print(msg)
    if isinstance(graph_id, int):
        GraphsTB.add_log(graph_id, msg)
    if rlog_record_id:
        rlog.info(msg)

def print_to_predict_log(*args, plog_record_id=None):
    '''将内容输出到预测日志里，前端来展示
    params:
        args: 要打印的内容
        plog_record_id: 预测记录id
    '''
    assert plog_record_id, 'plog_record_id必传'
    PredictRecordTB.add_log(plog_record_id, '\n'.join([str(i) for i in args]))

def update_params_value(key, value, node):
    """更新当前节点参数"""
    node.params[key] = value
    graph = multi_graph.get(node.graph_info["id"])
    if graph.use_db:
        update_node_params(node.id, key, value)
    return 1

def update_params_source(key, value, node):
    """更新当前节点参数source"""
    graph = multi_graph.get(node.graph_info["id"])
    if graph.use_db:
        update_node_params(node.id, key, value, value_key="source")
    return 1


def predict_to_csv(datas, filename="",
        graph_id='', node_id='',
        plog_record_id='', online_plog_record_id="",
        filepath=""):
    # 取出节点的数据导入节点
    assert isinstance(datas, pd.DataFrame), "预测保存的数据必须是DataFrame"
    assert graph_id, "未传graph_id"
    assert node_id, "未传node_id"
    if filepath:
        if not filepath.endswith(".csv"):
            raise Exception("预测数据只能保存csv文件")
        datas.to_csv(filepath, encoding="utf_8", index=False)
    else:
        if not plog_record_id and not online_plog_record_id:
            return 0
        predict_save_path = os.path.join(
                settings.PREDICT_RESULT_SAVE_PATH,
                str(graph_id))
        if not os.path.exists(predict_save_path):
            os.makedirs(predict_save_path)
        if filename:
            predict_filename = filename
        else:
            if online_plog_record_id:
                auto_file_name_prefix = "online_predict_%s" % online_plog_record_id
            else:
                auto_file_name_prefix = "predict_%s" % plog_record_id
            predict_filename = "%s_%s_%s.csv" % (
                    auto_file_name_prefix,
                    str(node_id),
                    (datetime.utcnow()+timedelta(hours=8)).strftime("%Y%m%d%H%M%S"))
        datas.to_csv(os.path.join(predict_save_path, predict_filename), encoding="utf_8", index=False)
    return 1


def read_predict_csv(graph_id, start_date=None, end_date=None):
    """读取模型历史的预测数据
    args:
        graph_id：预测模型的id
        start_date: 预测数据批次的开始日期 (包含), 不传的话只返回最近的一次数据, 格式：YYYYmmdd or YYYY-mm-dd
        end_date: 预测数据批次的结束日期（包含）, 不传的话只返回最近的一次数据, 格式：YYYYmmdd or YYYY-mm-dd
    """
    datas = pd.DataFrame()
    predict_save_path = os.path.join(settings.PREDICT_RESULT_SAVE_PATH, str(graph_id))
    if not os.path.exists(predict_save_path):
        return datas
    file_list = os.listdir(predict_save_path)
    file_time_dict = {(i.split("_")[-1]).replace(".csv", ""):i for i in file_list}
    time_list = list(file_time_dict.keys())
    if settings.RUN_ENV != "image":
        if start_date and end_date:
            start_date = str(start_date).replace('-', "")
            end_date = str(end_date).replace('-', "")
            daterange = pd.date_range(start_date, end_date, freq="D").to_list()
            for d in daterange:
                match_times = [i for i in time_list if i.startswith(d.strftime("%Y%m%d"))]
                match_time = None
                if len(match_times) > 1:
                    match_time = str(max(list(map(int, match_times))))
                elif len(match_times) == 1:
                    match_time = match_times[0]
                else:
                    continue
                df = pd.read_csv(os.path.join(predict_save_path, file_time_dict[match_time]))
                df["file_date"] = match_time[:8]
                datas = datas.append(df)
            return datas
        else:
            match_time = str(max(list(map(int, time_list))))
            datas = pd.read_csv(os.path.join(predict_save_path, file_time_dict[match_time]))
            datas["file_date"] = match_time[:8]
            return datas
    else:
        # 请求NPMOS的接口
        pass


def train_to_csv(datas, graph_id='', node_id=''):
    # 取出节点的数据导入节点
    assert isinstance(datas, pd.DataFrame), "预测保存的数据必须是DataFrame"
    assert graph_id, "未传graph_id"
    assert node_id, "未传node_id"
    run_save_path = os.path.join(
            settings.RUN_RESULT_SAVE_PATH,
            str(graph_id))
    if not os.path.exists(run_save_path):
        os.makedirs(run_save_path)
    run_filename = "run_%s.csv" % str(node_id)
    datas.to_csv(os.path.join(run_save_path, run_filename), encoding="utf_8", index=False)
    return 1


def read_train_csv(graph_id, node_id):
    """读取模型历史的预测数据
    args:
        graph_id：预测模型的id
        node_id: 节点
    """
    run_save_path = os.path.join(settings.RUN_RESULT_SAVE_PATH, str(graph_id))
    file_list = os.listdir(run_save_path)
    datas = pd.DataFrame()
    if node_id:
        file_list = [f for f in file_list if int(str(str(f).split("-")[-1]).replace(".csv", "")) == int(node_id)]
    for f in file_list:
        df = pd.read_csv(os.path.join(run_save_path, f))
        df["node_id"] = str(str(f).split("-")[-1]).replace(".csv", "")
        datas = datas.append(df)
    return datas


def get_model_save_path(graph_id, node_id):
    """获取模型的自定义模型的保存路径
    args:
        graph_id：预测模型的id
        node_id: 节点id
    """
    if settings.RUN_ENV == 'sdk':
        model_save_path = settings.SDK_MODEL_SAVE_PATH
        custom_model_save_path = os.path.join(model_save_path, str(graph_id), str(node_id))
    else:
        model_save_path = settings.RUN_MODEL_SAVE_PATH
        custom_model_save_path = os.path.join(model_save_path, str(graph_id), 'custom/%s/' % node_id)
    return custom_model_save_path


def update_nwp_config(nwp_config, node):
    # 取出节点的数据导入节点
    import_nodes = []
    graph = multi_graph.get(node.graph_info["id"])
    if graph is None:
        raise Exception("全局未找到graph")

    for n in graph.a._iter_fathers(node):
        if n.module.parent.info["cls_name"] == MODULES.IMPORT and n not in import_nodes:
            import_nodes.append(n)
    if len(import_nodes) > 1:
        raise Exception("导入数据节点有多个，只能更新一个导入数据节点的nwp_config")
    if len(import_nodes) == 0:
        raise Exception("未找到Algodata或StrategyAlgodata数据导入节点")
    import_node = import_nodes[0]
    if import_node.params.get("nwp_config") is None:
        raise Exception("数据导入节点%s没有nwp_config参数" % import_node.info["cls_name"])

    # 验证nwp_config的格式是否正确
    if not isinstance(nwp_config, dict):
        raise Exception("nwp_config格式不正确")
    if not nwp_config:
        raise Exception("nwp_config传值为空")
    # 更新节点里面的参数
    import_node.params["nwp_config"] = nwp_config
    if graph.use_db:
        # 更新数据库里面的参数
        update_node_params(import_node.id, "nwp_config", str(nwp_config))
    print_to_run_log("更新nwp_config为:%s" % str(nwp_config), graph_id=node.graph_info["id"])
    return 1

def get_nwp_config(node):
    # 取出节点的数据导入节点
    import_nodes = []
    graph = multi_graph.get(node.graph_info["id"])
    if graph is None:
        raise Exception("全局未找到graph")

    for n in graph.a._iter_fathers(node):
        if n.module.parent.info["cls_name"] == MODULES.IMPORT and n not in import_nodes:
            import_nodes.append(n)
    if len(import_nodes) == 0:
        raise Exception("未找到Algodata或StrategyAlgodata数据导入节点")
    nwp_configs = []
    for n in import_nodes:
        if n.params.get("nwp_config") is not None:
            nwp_configs.append(n.params["nwp_config"])

    if len(nwp_configs) > 1:
        raise Exception("数据导入节点存在多个nwp_config")

    if len(nwp_configs) == 0:
        raise Exception("数据导入节点不存在nwp_config参数")

    return nwp_configs[0]


@contextmanager
def timeout(duration):
    def timeout_handler(signum, frame):
        raise TimeoutError(f'block timedout after {duration} seconds')
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(duration)
    yield
    signal.alarm(0)
