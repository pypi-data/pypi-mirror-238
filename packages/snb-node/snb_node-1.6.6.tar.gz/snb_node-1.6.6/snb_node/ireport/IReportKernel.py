import json
import sys
import time
from typing import Union, Optional, Awaitable, Dict, Any

import requests
import tornado.websocket
from tornado import gen, web
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from jupyter_client.jsonutil import json_default
import snb_plugin.utils.snb_RSA as snb_rsa
from snb_plugin.utils.snb_kernel_client import SnbKernelClient,snb_kernel_pool
from snb_plugin.graph.ToGraph import parsePara, toGraph
from snb_node.config.Config import SNB_SERVER_URL, config, pem, workspace_uid, envir_uid
import threading

# 系统缓存
client_cache = {}

idle_timeout = 1000  # 设置空闲超时时间为 3600 秒
def check_idle_timeout():
    while True:
        try:
            for kernel_id in list(client_cache.keys()):
                try:
                    client=client_cache[kernel_id]
                    if time.time() - client.last_time > idle_timeout:
                        print("Kernel idle timeout reached. release kernel.",kernel_id,file=sys.stderr)
                        client_cache[kernel_id].reset_Release()
                        del client_cache[kernel_id]
                except Exception as e:
                    print(e,file=sys.stderr)
        except Exception as e:
            print(e,file=sys.stderr)
        print(len(client_cache),snb_kernel_pool.get_idle_count(),'.',file=sys.stderr)
        time.sleep(30)  # 每分钟检查一次

# 启动检查函数的线程
thread = threading.Thread(target=check_idle_timeout)
thread.start()

class CellRunError(Exception):
    pass

class IReportKernelHandler(web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    def output_dep_search(self,output_cell_uid, output_edge_dict):
        res_list = []
        for output_uid in output_cell_uid:
            if output_uid in output_edge_dict:
                res_list.extend(output_edge_dict[output_uid])
                res_list.extend(self.output_dep_search(output_edge_dict[output_uid], output_edge_dict))
        return list(set(res_list))

    def input_dep_search(self,inout_cell_uid, input_edge_dict):
        res_list = []
        for input_uid in inout_cell_uid:
            if input_uid in input_edge_dict:
                res_list.extend(input_edge_dict[input_uid])
                res_list.extend(self.input_dep_search(input_edge_dict[input_uid], input_edge_dict))
        return list(set(res_list))

    def dep_process(self,graph_data, init_cell_uid, input_cell_uid, input_para, output_cell_uid):
        output_edge_dict = graph_data['output_edge_dict']
        input_edge_dict = graph_data['input_edge_dict']
        node_dict = graph_data['node_dict']

        output_dep_cell_uid = self.output_dep_search(output_cell_uid, output_edge_dict)
        input_dep_cell_uid = self.input_dep_search(input_cell_uid, input_edge_dict)

        for node in graph_data["node"]:
            if 'is_exec' in node and node['is_exec'] != 'init':
                del node['is_exec']
            if 'is_out' in node:
                del node['is_out']
            if 'input_cell_code' in node:
                del node['input_cell_code']

        try:
            for cell_uid in output_dep_cell_uid:
                if node_dict[cell_uid]["is_run"] == 0:
                    node_dict[cell_uid]["is_exec"] = "dep"

            for cell_uid in input_dep_cell_uid:
                node_dict[cell_uid]["is_exec"] = "dep"

            for cell_uid in init_cell_uid:
                if cell_uid:
                    node_dict[cell_uid]["is_exec"] = "init"

            for cell_uid_index, cell_uid in enumerate(input_cell_uid):
                node_dict[cell_uid]["is_exec"] = "input"
                node_dict[cell_uid]["input_cell_code"] = input_para[cell_uid_index]

            for cell_uid in output_cell_uid:
                node_dict[cell_uid]["is_exec"] = "output"
                node_dict[cell_uid]["is_out"] = "output"
        except KeyError as e:
            raise CellRunError(f"运行失败，单元格不存在{str(e)}")

        return graph_data

    def get_notebook_graph_data(self,snb_uid, preview=""):

        url = "".join([SNB_SERVER_URL, "/api/snb_native/nbver_last/" + snb_uid, "?preview="+preview])
        sign_str = snb_rsa.sign("/api/snb_native/nbver_last/" + snb_uid+"?preview="+preview, pem)
        header = {"Cookie": "cookie", "sign": sign_str, "workspaceUid": workspace_uid}
        conn_info = requests.get(url, headers=header)
        resp = conn_info.json()
        if resp["code"] == 200:
            snb = json.loads(resp["data"])

            """if True:
            snb = json.loads(open("/home/excute_test_01.snb", 'rb').read())"""

            cell_data = parsePara(snb)
            graph_data = toGraph(cell_data)

            node_dict = {}
            output_edge_dict = {}
            input_edge_dict = {}

            for node in graph_data["node"]:
                node['is_run'] = 0
                node_dict[node["cell_uid"]] = node

            for edge in graph_data["edge"]:
                if edge["dst_uid"] in output_edge_dict:
                    output_edge_dict[edge["dst_uid"]].append(edge["src_uid"])
                else:
                    output_edge_dict[edge["dst_uid"]] = [edge["src_uid"]]

            for edge in graph_data["edge"]:
                if edge["src_uid"] in input_edge_dict:
                    input_edge_dict[edge["src_uid"]].append(edge["dst_uid"])
                else:
                    input_edge_dict[edge["src_uid"]] = [edge["dst_uid"]]

            graph_data['node_dict'] = node_dict
            graph_data['output_edge_dict'] = output_edge_dict
            graph_data['input_edge_dict'] = input_edge_dict

            return graph_data
        else:
            raise Exception("Notebook版本不存在")

    @gen.coroutine
    #@interceptor
    def post(self, ws_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        try:
            body = json.loads(self.request.body.strip().decode("utf-8"))
            snb_uid = body.get("snb_uid")
            kernel_id = body.get("kernel_id", "")
            init_cell_uid = body.get("init_cell_uid", [])
            input_cell_uid = body.get("input_cell_uid", [])
            input_para = body.get("input_para", [])
            output_cell_uid = body.get("output_cell_uid", [])
            preview = body.get("preview", "")
            #yield
            output_res,error_res,kernel_id =  yield self.Excute_Graph(kernel_id=kernel_id, snb_uid=snb_uid,preview=preview,
                                                           init_cell_uid=init_cell_uid, input_cell_uid=input_cell_uid,
                                                           input_para=input_para, output_cell_uid=output_cell_uid)

            res = {"code": 200, "msg": "成功", "data": {"result": output_res, "kernel_id": kernel_id,"error_res":error_res}}
            self.finish(json.dumps(res, default=json_default))
        except CellRunError as e:
            print(e,file=sys.stderr)
            res = {"code": 400, "msg": "失败:" + str(e), "data": []}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e:
            print(e,file=sys.stderr)
            res = {"code": 400, "msg": "失败:" + str(e), "data": []}
            self.finish(json.dumps(res, default=json_default))

    def get_output(self, client, dep_res):
        """执行关联代码的output"""
        output_res = {}
        error_res=[]
        excute_count=0
        for node in dep_res["node"]:
            is_exec=node.get("is_exec", "")
            if is_exec == "input" or is_exec == "dep" or is_exec == "output":
                if node["cell_type"] == "sql":
                    res = client.execute(node["py_code"])
                    node['is_run'] = 1
                    excute_count=excute_count+1
                else:
                    if node['snb_cell_type'].startswith("interact"):
                        if node["cell_code"]:
                            res = client.execute(node["cell_code"])
                            excute_count = excute_count + 1
                            node['is_run'] = 1
                        else:
                            res = []
                        if 'input_cell_code' in node :
                            res = client.execute(node["input_cell_code"])
                            excute_count = excute_count + 1
                    else:
                        res = client.execute(node["cell_code"])
                        node['is_run'] = 1
                        excute_count = excute_count + 1

                for r in res:
                    if 'output_type' in r and r['output_type'] == 'error':
                        error_res.append({"node":node,"error":r})

                if node.get("is_out", "") == 'output':
                    output_res[node["cell_uid"]] = res
        print('*'*2,excute_count,'*'*2,file=sys.stderr)
        return output_res,error_res

    @run_on_executor
    def Excute_Graph(self, kernel_id, snb_uid,preview,init_cell_uid, input_cell_uid, input_para, output_cell_uid):
        """连接kernel"""
        key = snb_uid + "_" + kernel_id
        #print(key, file=sys.stderr)

        if kernel_id and key in client_cache and client_cache[key].is_alive():
            client = client_cache[key]
            kernel_id = client.get_kernel_id()
            graph_data=getattr(client,'graph_data')
            graph_data = self.dep_process(graph_data, init_cell_uid, input_cell_uid, input_para, output_cell_uid)
            client.__setattr__('graph_data', graph_data)
            #print('is_exist',key, file=sys.stderr)
        else:
            if kernel_id and key in client_cache:
                del client_cache[key]

            client = SnbKernelClient()
            #print('not_exist', key, file=sys.stderr)

            kernel_id = client.startKernel()

            graph_data = self.get_notebook_graph_data(snb_uid, preview)
            graph_data = self.dep_process(graph_data, init_cell_uid, input_cell_uid, input_para, output_cell_uid)
            client.__setattr__('graph_data',graph_data)

            for node in graph_data["node"]:
                if node.get("is_exec", "") == "init":
                    if node["cell_type"] == "sql":
                        client.execute(node["py_code"])
                    else:
                        client.execute(node["cell_code"])
            key = snb_uid + "_" + kernel_id
            client_cache[key] = client

        output_res,error_res =self.get_output(client=client, dep_res=graph_data)
        client.last_time=time.time()
        #print(kernel_id)
        return output_res,error_res,kernel_id

_conn_uid_regex = r"(?P<conn_uid>.*)"
_ws_uid = r"(?P<ws_uid>[^/]+)"
default_handlers = [
    (rf"/api/snb/node/ireportKernel/{_ws_uid}", IReportKernelHandler),
]
