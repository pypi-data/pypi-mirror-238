from datetime import datetime, timezone, timedelta
import os
import queue
import threading
import time
import json
import signal
import sys
import traceback
import argparse
import csv
import pathlib
import shutil
import pandas as pd

from pymongo import MongoClient, ASCENDING, DESCENDING

from ..mongo_client_gateway import MongoClientTradeGateway

from .constants import (GATEWAY_NAME, FILES)
from .utils import (decode_emc_status, side_to_target_type, decode_exchange_id, encode_emc_side,
                    decode_ordtype, encode_emc_market, get_today_date, get_time_from_str, decode_emc_market)


try:
    import thread
except ImportError:
    import _thread as thread

LL9 = 1000000000


class EmcServer(MongoClientTradeGateway):
    def __init__(self, config_filename, endtime, gateway_name):
        MongoClientTradeGateway.__init__(
            self, config_filename, endtime, gateway_name)

        self.load_tg_setting(config_filename)

        self.insert_orders = {}
        self.oid_to_ref = {}
        self.sids = []
        self.oid_to_traded = {}
        self.oid_to_traded_money = {}

        self.sid_to_req = {}
        self.oid_to_req = {}
        self.oid_to_sid = {}
        self.oid_to_acc = {}
        self.db_id_to_oid = {}
        self.ref_to_oid = {}
        # dbf文件当前index
        self.trade_count = {}
        for acc in self.accounts_run:
            self.trade_count[acc] = 0
        self.oid_to_local_ids = {}
        self.oid_to_instr_ids = {}

    def monitor(self):
        self.thread_pool.submit(self.monitor_algo_order_insert)
        self.thread_pool.submit(self.monitor_algo_task_update)
        # self.thread_pool.submit(self.monitor_cancel_order_insert)
        # self.thread_pool.submit(self.monitor_order_update)
        self.thread_pool.submit(self.monitor_trade_update)
        self.thread_pool.submit(self.update_asset)
        self.thread_pool.submit(self.update_equity_position)
        self.thread_pool.submit(self.date_change)

    def load_tg_setting(self, config_filename):
        try:
            #config_filename = os.path.join(config_path, 'atx_server_config.json')
            f = open(config_filename, encoding='gbk')
            setting = json.load(f)
            #self.insert_order_path = setting['insert_order_path'].replace('/', '\\')
            self.recv_msg_dir = setting['recv_msg_path'].replace('/', '\\')
            self.insert_order_msg_dir = setting['insert_order_msg_path'].replace(
                '/', '\\')
            self.pos_interval = setting['pos_interval']
            self.acc_interval = setting['acc_interval']
            self.algo_task_scan_interval = setting['algo_task_scan_interval']

        except Exception as e:
            err = traceback.format_exc()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(
                exc_type, exc_value, exc_traceback, limit=None, file=sys.stdout)
            print(f"load config failed! (exception){err}")
            exit(0)

    @MongoClientTradeGateway.error_handler
    def req_buy_order_insert(self, obj):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y%m%d%H%M%S%f")[:-3]
        temp_filename = self.insert_order_msg_dir + \
            '_temp\\' + FILES.ORDERS + '1_buy.' + formatted_time + '.csv'

        header = ['fundID', 'algoType', 'stkCode', 'Market', 'Direction', 'orderQty',
                  'orderPrice', 'beginTime', 'endTime', 'customerOrderRef', 'algoParam1', 'algoParam2']

        with open(temp_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)

            target_account_name = obj['accountName']
            acc = self.target_account_names_to_acc[target_account_name]
            account_id = self.account_id[acc]

            oid = str(self.gen_order_id())
            sid = str(obj['sid'])

            local_report_no = oid
            fund_id = int(account_id)
            stkcode = obj['ticker']
            market = encode_emc_market(stkcode)
            Direction = 1

            qty = int(obj["volume"])
            algo_type = decode_ordtype(obj['executionPlan']["order_type"])
            start_time = str(obj['executionPlan']["start_time"])
            end_time = str(obj['executionPlan']["end_time"])
            algo_price = 0
            limit_action = 1
            if not obj.get('LimAction') is None:
                if not limit_action:
                    limit_action = 0
            after_action = 0
            algo = f"limit_action={limit_action}:after_action={after_action}"
            row = [fund_id, algo_type, stkcode, market, Direction,
                   qty, '', start_time, end_time, oid, algo, 1]

            writer.writerow(row)

        # Save the workbook
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y%m%d%H%M%S%f")[:-3]
        final_filename = f"{self.insert_order_msg_dir}\\{FILES.ORDERS}1_buy.{formatted_time}.csv"
        shutil.move(temp_filename, final_filename)

        self.logger.info(
            f"[req_buy_order] insert_success (oid){oid} (sid){sid} (param){row}")
        db_id = obj['_id']
        order_dict = {
            'oid': oid,
            'sid': sid,
            "db_id": db_id,
            "ticker": obj['ticker'],
            "volume": qty,
            "accountName": target_account_name,
            "order_type": str(obj['executionPlan']["order_type"]),
            "start_time": str(obj['executionPlan']["start_time"]),
            "end_time": str(obj['executionPlan']["end_time"]),
            "order_time": datetime.utcnow(),
            'side': 1
        }

        target_collection = self.order_info_db[acc]['target']
        delete_query = {
            '_id': db_id
        }
        delete_res = target_collection.delete_one(delete_query)
        self.logger.info(f"[on_req_buy_order] delete (target){obj}")

        atx_order_collection = self.order_info_db[acc]['atx_order']
        local_id_list = []
        instr_id_list = []
        db_msg = {
            "oid": oid,
            "sid": sid,
            "traded_vol": 0,
            "traded_amt": 0,
            "local_ids": local_id_list,
            "instr_ids": instr_id_list,
            "order_msg": order_dict,
        }
        query = {"oid": oid}
        res = atx_order_collection.replace_one(query, db_msg, True)
        self.logger.info(
            f"[on_req_order_insert] insert_gf_order_info (res){res} (msg){db_msg}")

        self.sids.append(sid)

        self.sid_to_req[sid] = order_dict
        self.oid_to_req[oid] = order_dict
        self.oid_to_sid[oid] = sid
        self.db_id_to_oid[db_id] = oid
        self.oid_to_acc[oid] = acc
        self.oid_to_traded[oid] = 0
        self.oid_to_traded_money[oid] = 0
        self.oid_to_local_ids[oid] = local_id_list
        self.oid_to_instr_ids[oid] = instr_id_list

    @MongoClientTradeGateway.error_handler
    def req_sell_order_insert(self, obj):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y%m%d%H%M%S%f")[:-3]
        temp_filename = self.insert_order_msg_dir + \
            '_temp\\' + FILES.ORDERS + '1_sell.' + formatted_time + '.csv'

        header = ['fundID', 'algoType', 'stkCode', 'Market', 'Direction', 'orderQty',
                  'orderPrice', 'beginTime', 'endTime', 'customerOrderRef', 'algoParam1', 'algoParam2']

        with open(temp_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)

            target_account_name = obj['accountName']
            acc = self.target_account_names_to_acc[target_account_name]
            account_id = self.account_id[acc]

            oid = str(self.gen_order_id())
            sid = str(obj['sid'])

            fund_id = int(account_id)
            stkcode = obj['ticker']
            market = encode_emc_market(stkcode)
            Direction = 2

            qty = int(obj["volume"])
            algo_type = decode_ordtype(obj['executionPlan']["order_type"])
            start_time = str(obj['executionPlan']["start_time"])
            end_time = str(obj['executionPlan']["end_time"])
            limit_action = 1
            if not obj.get('LimAction') is None:
                if not limit_action:
                    limit_action = 0

            after_action = 0
            algo = f"limit_action={limit_action}:after_action={after_action}"
            row = [fund_id, algo_type, stkcode, market, Direction,
                   qty, '', start_time, end_time, oid, algo, 2]

            writer.writerow(row)

        # Save the workbook
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y%m%d%H%M%S%f")[:-3]
        final_filename = f"{self.insert_order_msg_dir}\\{FILES.ORDERS}1_buy.{formatted_time}.csv"
        shutil.move(temp_filename, final_filename)

        self.logger.info(
            f"[req_sell_order] insert_success (oid){oid} (sid){sid} (param){row}")
        db_id = obj['_id']
        order_dict = {
            'oid': oid,
            'sid': sid,
            "db_id": db_id,
            "ticker": obj['ticker'],
            "volume": qty,
            "accountName": target_account_name,
            "order_type": str(obj['executionPlan']["order_type"]),
            "start_time": str(obj['executionPlan']["start_time"]),
            "end_time": str(obj['executionPlan']["end_time"]),
            "order_time": datetime.utcnow(),
            'side': 2
        }

        target_collection = self.order_info_db[acc]['target']
        delete_query = {
            '_id': db_id
        }
        delete_res = target_collection.delete_one(delete_query)
        self.logger.info(f"[on_req_buy_order] delete (target){obj}")

        atx_order_collection = self.order_info_db[acc]['atx_order']
        local_id_list = []
        instr_id_list = []
        db_msg = {
            "oid": oid,
            "sid": sid,
            "traded_vol": 0,
            "traded_amt": 0,
            "local_ids": local_id_list,
            "instr_ids": instr_id_list,
            "order_msg": order_dict,
        }
        query = {"oid": oid}
        res = atx_order_collection.replace_one(query, db_msg, True)
        self.logger.info(
            f"[on_req_order_insert] insert_gf_order_info (res){res} (msg){db_msg}")

        self.sids.append(sid)

        self.sid_to_req[sid] = order_dict
        self.oid_to_req[oid] = order_dict
        self.oid_to_sid[oid] = sid
        self.db_id_to_oid[db_id] = oid
        self.oid_to_acc[oid] = acc
        self.oid_to_traded[oid] = 0
        self.oid_to_traded_money[oid] = 0
        self.oid_to_local_ids[oid] = local_id_list
        self.oid_to_instr_ids[oid] = instr_id_list

    @MongoClientTradeGateway.error_handler
    def monitor_algo_task_update(self):
        while not self.is_stopped:
            header = ['算法单号', '自定义编号', '资金账号', '证券代码', '证券名称', '市场', '委托方向', '算法类型', '状态',
                      '状态值', '目标数量', '执行进度', '成交数量', '成交金额', '成交均价', '开始时间', '结束时间', '备注', '算法风格']
            for acc in self.accounts_run:
                trade_acc = self.account_id[acc]
                algo_task_filename = self.recv_msg_dir + \
                    '\\' + str(trade_acc) + FILES.ALGO_TASKS + \
                    get_today_date() + '.csv'
                data_list = []
                algo_types = {
                    '算法单号': str,
                    '自定义编号': str
                }
                df = pd.DataFrame()
                try:
                    df = pd.read_csv(algo_task_filename,
                                     dtype=algo_types, encoding='gbk')
                except:
                    self.logger.warning(
                        "[monitor_algo_task_update] file not exist")
                for _, row in df.iterrows():
                    row_dict = {}
                    for col in header:
                        row_dict[col] = row[col]
                    data_list.append(row_dict)

                for record in data_list:
                    if len(record['算法单号']) != 0 and len(record['自定义编号']) != 0:
                        oid = record['自定义编号']
                        ref = record['算法单号']
                        self.oid_to_ref[oid] = ref
                        self.ref_to_oid[ref] = oid
                        self.update_algo_status(record, acc)
            time.sleep(self.algo_task_scan_interval)

    def update_algo_status(self, record, acc):

        if record['成交数量'] == 0 or len(record['算法单号']) == 0:
            self.logger.warning(
                f"[update_order] nothing_traded (record){record}")
            return

        mudan_id = record['算法单号']
        if not mudan_id in self.ref_to_oid:
            return
        oid = self.ref_to_oid[mudan_id]
        if len(oid) == 0:
            self.logger.warning(
                f"[update_order] not use file to order record:{record}")
            return

        sid = ""
        order_dict = {}
        if not oid in self.oid_to_acc:  # shut_down or other problem

            order_info_collection = self.order_info_db[acc]['atx_order']
            query = {'oid': oid}
            order_info_target = order_info_collection.find_one(query)
            if not order_info_target is None:
                order_dict = order_info_target['order_msg']
                sid = order_info_target['sid']
                try:
                    self.oid_to_instr_ids[oid] = order_info_target['instr_ids']
                except:
                    self.oid_to_instr_ids[oid] = []
                self.oid_to_traded_money[oid] = 0
                self.oid_to_traded[oid] = 0
                self.oid_to_sid[oid] = sid
                self.oid_to_req[oid] = order_dict
                self.oid_to_ref[oid] = mudan_id
            else:
                self.logger.error(f"[update_order] can't_find_oid (oid){oid}")
                return
        else:
            order_dict = self.oid_to_req[oid]
            sid = self.oid_to_sid[oid]

        traded_vol = record['成交数量']

        int_stock_code = int(record['证券代码'])
        ticker = f'{int_stock_code:06d}'
        exchange = decode_exchange_id(ticker)
        volume = record['成交数量']

        price = 0
        if (traded_vol != 0):
            price = float(record['成交均价'])

        tg_name = order_dict['accountName'].split('@')[0]
        accountName = order_dict['accountName'].split('@')[1]
        order_type = order_dict['order_type']
        start_time = order_dict['start_time']
        end_time = order_dict['end_time']
        order_time = order_dict['order_time']

        target_type = side_to_target_type(order_dict['side'])
        status = decode_emc_status(record['状态'])
        utc_start_time = get_time_from_str(str(start_time))

        replace_collection = self.tradelog_db[acc]['order']
        query = {'sid': sid, '_id': int(oid)}
        replace_target = replace_collection.find_one(query)
        dbtime = order_time if order_time > utc_start_time else utc_start_time

        order_msg = {
            "_id": int(oid),
            "tg_name": tg_name,  # 对应 account_info._id
            "exchange": exchange,  # 对应 tlclient.trader.constant 包 ExchangeID
            "target_type": target_type,    # 'buy' | 'sell'
            "volume": volume,  # 成交volume
            "price": price,  # 实际成交均价
            "order_type": order_type,
            "ticker": ticker,
            "sid": sid,  # target中对应的 母单sid
            "accountName": accountName,  # 对应 account_info.account_name
            "algo_args": {  # 具体的算法参数
                "order_type": order_type,
                "start_time": start_time,
                "end_time": end_time
            },
            "status": status,  # 'active' | 'filled' | 'canceled'
            "filled_vol": traded_vol,  # 实际成交的 volume
            "dbTime": dbtime,
        }

        res = replace_collection.replace_one(query, order_msg, True)
        self.logger.info(f"[rtn_order] (res){res} (order_msg){order_msg}")

        atx_order_collection = self.order_info_db[acc]['atx_order']
        atx_order_msg = {
            "instr_ids": self.oid_to_instr_ids[oid],
        }
        update_atx_order_msg = {"$set": atx_order_msg}
        query = {"oid": oid}
        res = atx_order_collection.update_one(query, update_atx_order_msg)
        self.logger.info(
            f"[update_order] update_atx_order_info (res){res} (msg){update_atx_order_msg}")

    @MongoClientTradeGateway.error_handler
    def monitor_order_update(self):
        while not self.is_stopped:
            header = ['算法单号', '资金账号', '证券代码', '委托日期', '委托时间', '委托价格', '委托编号', '合同序号',
                      '委托数量', '成交数量', '成交均价', '撤单数量', '委托状态', '委托状态值', '业务类型', '信用交易类型', '来源']
            algo_order_types = {
                '算法单号': str,
                '自定义编号': str
            }
            for acc in self.accounts_run:
                trade_acc = self.account_id[acc]
                order_filename = self.recv_msg_dir + \
                    '\\' + str(trade_acc) + FILES.ORDERS + \
                    get_today_date() + '.csv'

                data_list = []

                df = pd.DataFrame()
                try:
                    df = pd.read_csv(
                        order_filename, dtype=algo_order_types, encoding='gbk')
                except:
                    self.logger.warning(
                        "[monitor_order_update] file not exist")

                data_list = []
                current_len = df.shape[0]
                #order_count = self.order_count[acc]

                for _, row in df.iterrows():
                    row_dict = {}
                    for col in header:
                        row_dict[col] = row[col]
                    data_list.append(row_dict)

                for record in data_list:
                    if record['委托状态'] in ['已成', '部撤', '已撤']:
                        self.update_order(record, acc)
                    elif record['委托状态'] in ['废单']:
                        self.logger.info(
                            f"[monitor_order_update] order_rejected msg{record}")

            time.sleep(self.order_scan_interval)

    @MongoClientTradeGateway.error_handler
    def update_asset(self):
        while not self.is_stopped:
            for acc in self.accounts_run:
                trade_acc = self.account_id[acc]
                asset_filename = self.recv_msg_dir + \
                    '\\' + str(trade_acc) + FILES.ACCOUNTS + \
                    get_today_date() + '.csv'
                df = pd.DataFrame()
                try:
                    df = pd.read_csv(asset_filename,  encoding='gbk')
                except:
                    self.logger.warning("[update_asset] file not exist")
                for _, row in df.iterrows():
                    avail_amt = row["可用资金"]
                    stkasset = row["总市值"]
                    all_asset = row["资金资产"]
                    ftmargin = row["资金余额"]  # 持仓占用保证金
                    creditmargin = row["可用资金"]  # 保证金可用
                    assurebalance = row["冻结资金"]  # 担保品可用

                    tg_name = self.tgnames[acc]
                    accountname = self.log_account_names[acc]
                    db_msg = {
                        "_id": tg_name,  # 对应之前的 TG 名称
                        "accountName": accountname,  # 产品名称
                        "avail_amt": avail_amt,  # 可用资金（可现金买入的资金）
                        # 净资产.  最好是由券商那边提供，通常普通账户是 可用资金(包含预扣费用) + 市值；信用账户是总资金 - 总负债
                        "balance": all_asset,
                        "holding": stkasset,  # 市值,
                        "updated_at": datetime.utcnow()
                    }

                    update_msg = {"$set": db_msg}
                    asset_collection = self.order_info_db[acc]['TestEquityAccount']
                    query = {'_id': tg_name, 'accountName': accountname}
                    res = asset_collection.update_one(query, update_msg)
                    self.logger.info(
                        f"[rtn_asset] (res){res} (asset_msg){db_msg}")

            time.sleep(self.acc_interval)

    @MongoClientTradeGateway.error_handler
    def update_equity_position(self):
        while not self.is_stopped:
            for acc in self.accounts_run:
                trade_acc = self.account_id[acc]
                pos_filename = self.recv_msg_dir + \
                    '\\' + str(trade_acc) + FILES.POSITIONS + \
                    get_today_date() + '.csv'
                dtypes = {
                    '证券代码': str,
                    '市场': str,
                }
                df = pd.DataFrame()
                try:
                    df = pd.read_csv(
                        pos_filename, dtype=dtypes, encoding='gbk')
                except:
                    self.logger.warning(
                        "[update_equity_position] file not exist")
                for acc in self.accounts_run:
                    tg_position_collection = self.order_info_db[acc]['tg_equity_position']
                    remove = tg_position_collection.delete_many(
                        {'account_name': self.log_account_names[acc], 'tg_name': self.target_account_names[acc]})
                    self.logger.info(
                        f"[update_equity_position] delete_old_position_info (remove){remove} ")
                for _, row in df.iterrows():
                    market = row["市场"]
                    exchange = decode_emc_market(market)
                    stkcode = int(row["证券代码"])
                    ticker = f'{stkcode:06d}'
                    # direction = row["direction"] # 'B' 多 ‘S’ 空
                    out_direction = "long"

                    stkholdqty = row["持仓数量"]
                    stkavl = row["可用数量"]
                    costprice = row["成本价"]
                    #ftmargin = row["ftmargin"]

                    tg_name = self.target_account_names[acc]
                    accountname = self.log_account_names[acc]
                    pos_collection = self.order_info_db[acc]['tg_equity_position']
                    query = {'tg_name': tg_name,
                             'accountName': accountname, "ticker": ticker}
                    pos_msg = {
                        "account_name": accountname,
                        "tg_name": tg_name,
                        "ticker": ticker,
                        "exchange": exchange,
                        "direction": out_direction,  # long/short，没有short部分就只存long部分
                        "avail_pos": stkavl,  # 可用仓位
                        # 今仓，TODO 需要统计下不同券商盘中，对于卖出的position 是直接从 yd_pos 上减，还是在 td_pos 增加一个负的值。
                        "total_pos": stkholdqty,
                        "cost": costprice,  # 没有
                        "type": "stock",
                        "updated_at": datetime.utcnow()
                    }
                    res = pos_collection.replace_one(pos_msg, pos_msg, True)
                    self.logger.info(
                        f"[update_equity_position] (res){res.modified_count} (order_msg){pos_msg}")
            time.sleep(self.pos_interval)

    @MongoClientTradeGateway.error_handler
    def update_order(self, record, acc):
        if record['成交数量'] == 0 or len(record['算法单号']) == 0:
            self.logger.warning(
                f"[update_order] nothing_traded (record){record}")
            return
        mudan_id = record['算法单号']
        if not mudan_id in self.ref_to_oid:
            return
        oid = self.ref_to_oid[mudan_id]
        if len(oid) == 0:
            self.logger.warning(
                f"[update_order] not use file to order record:{record}")
            return

        sid = ""
        order_dict = {}
        if not oid in self.oid_to_acc:  # shut_down or other problem

            order_info_collection = self.order_info_db[acc]['atx_order']
            query = {'oid': oid}
            order_info_target = order_info_collection.find_one(query)
            if not order_info_target is None:
                order_dict = order_info_target['order_msg']
                sid = order_info_target['sid']
                try:
                    self.oid_to_instr_ids[oid] = order_info_target['instr_ids']
                except:
                    self.oid_to_instr_ids[oid] = []
                self.oid_to_traded_money[oid] = 0
                self.oid_to_traded[oid] = 0
                self.oid_to_sid[oid] = sid
                self.oid_to_req[oid] = order_dict
                self.oid_to_ref[oid] = mudan_id
            else:
                self.logger.error(f"[update_order] can't_find_oid (oid){oid}")
                return
        else:
            order_dict = self.oid_to_req[oid]
            sid = self.oid_to_sid[oid]

        traded_vol = record['成交数量']

        int_stock_code = int(record['证券代码'])
        ticker = f'{int_stock_code:06d}'
        exchange = decode_exchange_id(ticker)
        volume = record['成交数量']

        price = 0
        if (traded_vol != 0):
            price = float(record['成交价格'])

        tg_name = order_dict['accountName'].split('@')[0]
        accountName = order_dict['accountName'].split('@')[1]
        order_type = order_dict['order_type']
        start_time = order_dict['start_time']
        end_time = order_dict['end_time']
        order_time = order_dict['order_time']

        target_type = side_to_target_type(order_dict['side'])
        status = decode_emc_status(record['委托状态'])
        utc_start_time = get_time_from_str(str(start_time))

        replace_collection = self.tradelog_db[acc]['order']
        query = {'sid': sid, '_id': int(oid)}
        replace_target = replace_collection.find_one(query)
        dbtime = order_time if order_time > utc_start_time else utc_start_time

        order_msg = {
            "_id": int(oid),
            "tg_name": tg_name,  # 对应 account_info._id
            "exchange": exchange,  # 对应 tlclient.trader.constant 包 ExchangeID
            "target_type": target_type,    # 'buy' | 'sell'
            "volume": volume,  # 成交volume
            "price": price,  # 实际成交均价
            "order_type": order_type,
            "ticker": ticker,
            "sid": sid,  # target中对应的 母单sid
            "accountName": accountName,  # 对应 account_info.account_name
            "algo_args": {  # 具体的算法参数
                "order_type": order_type,
                "start_time": start_time,
                "end_time": end_time
            },
            "status": status,  # 'active' | 'filled' | 'canceled'
            "filled_vol": traded_vol,  # 实际成交的 volume
            "dbTime": dbtime,
        }

        res = replace_collection.replace_one(query, order_msg, True)
        self.logger.info(f"[rtn_order] (res){res} (order_msg){order_msg}")

        atx_order_collection = self.order_info_db[acc]['atx_order']
        atx_order_msg = {
            "instr_ids": self.oid_to_instr_ids[oid],
        }
        update_atx_order_msg = {"$set": atx_order_msg}
        query = {"oid": oid}
        res = atx_order_collection.update_one(query, update_atx_order_msg)
        self.logger.info(
            f"[update_order] update_atx_order_info (res){res} (msg){update_atx_order_msg}")

    @MongoClientTradeGateway.error_handler
    def monitor_algo_order_insert(self):
        while not self.is_stopped:
            print("[monitor_algo_order_insert]")
            for acc in self.accounts_run:
                target_accountname = self.target_account_names[acc]
                buy_query = {"accountName": target_accountname}
                buy_targets = self.order_info_db[acc]["target"].find(buy_query)
                if buy_targets.count() == 0:
                    self.logger.warning(
                        f"[monitor_buy_order] no_buy_target (acc){acc}")
                    continue
                for target in buy_targets:
                    if target['_id'] not in self.order_dbids:
                        self.order_dbids.append(target['_id'])
                        self.req_buy_order_insert(target)
                    else:
                        self.logger.warning(
                            f"[monitor_algo_order_insert] _id_existed (_id){target['_id']}")
            for acc in self.accounts_run:
                target_accountname = self.target_account_names[acc]
                sell_query = {"accountName": target_accountname}
                sell_targets = self.order_info_db[acc]["sell_target"].find(
                    sell_query)
                if sell_targets.count() == 0:
                    self.logger.warning(
                        f"[monitor_sell_order] no_sell_target (acc){acc}")
                    continue
                for sell_target in sell_targets:
                    if sell_target['_id'] not in self.sell_order_dbids:
                        self.sell_order_dbids.append(sell_target['_id'])
                        self.req_sell_order_insert(sell_target)
                    else:
                        self.logger.warning(
                            f"[monitor_algo_order_insert] _id_existed (_id){sell_target['_id']}")
            time.sleep(self.scan_interval)

    @MongoClientTradeGateway.error_handler
    def monitor_cancel_order_insert(self):
        while not self.is_stopped:
            for acc in self.accounts_run:
                print("[monitor_cancel_order_insert]")
                target_accountname = self.target_account_names[acc]
                query = {"accountName": target_accountname}
                with self.cancel_orderlock:
                    cancel_targets = self.order_info_db[acc]["cancel_target"].find(
                        query)
                    if cancel_targets.count() == 0:
                        self.logger.warning(
                            "[monitor_cancel_order] no_cancel_info")
                        continue
                    for cancel_target in cancel_targets:
                        if cancel_target['_id'] not in self.cancel_order_ids:
                            self.cancel_order_ids.append(cancel_target['_id'])
                            self.req_cancel_order(cancel_target, acc)
            time.sleep(self.scan_interval)

    @MongoClientTradeGateway.error_handler
    def monitor_trade_update(self):
        header = ['算法单号', '资金账号', '证券代码', '成交日期', '成交时间', '成交数量',
                  '委托编号', '成交编号', '成交价格', '回报类型', '业务类型', '信用交易类型', '来源']
        algo_trade_types = {
            '算法单号': str
        }
        while not self.is_stopped:
            print("[monitor_trade_update]")

            for acc in self.accounts_run:
                trade_acc = self.account_id[acc]
                trade_filename = self.recv_msg_dir + \
                    '\\' + str(trade_acc) + FILES.TRADES + \
                    get_today_date() + '.csv'
                data_list = []

                df = pd.DataFrame()
                try:
                    df = pd.read_csv(
                        trade_filename, dtype=algo_trade_types, encoding='gbk')
                except:
                    self.logger.warning(
                        "[monitor_trade_update] file not exist")

                data_list = []

                for _, row in df.iterrows():
                    row_dict = {}
                    for col in header:
                        row_dict[col] = row[col]
                    data_list.append(row_dict)

                for record in data_list:
                    self.on_trade_msg(record, acc)

            time.sleep(self.trade_scan_interval)

    @MongoClientTradeGateway.error_handler
    def on_trade_msg(self, record, acc):
        if record['成交数量'] == 0:
            self.logger.warning(
                f"[on_trade_msg] nothing_traded (record){record}")
            return

        mudan_id = record['算法单号']

        if not mudan_id in self.ref_to_oid:
            self.logger.warning(
                f"[on_trade_msg] not use file to  trade record:{record}")
            return

        oid = self.ref_to_oid[mudan_id]

        sid = ""
        order_dict = {}
        if not oid in self.oid_to_acc:  # shut_down or other problem
            trade_acc = record['资金账号']
            acc = self.account_id_to_acc[trade_acc]
            order_info_collection = self.order_info_db[acc]['atx_order']
            query = {'oid': oid}
            order_info_target = order_info_collection.find_one(query)

            if not order_info_target is None:
                order_dict = order_info_target['order_msg']
                sid = order_info_target['sid']
                self.oid_to_local_ids[oid] = order_info_target['local_ids']
                self.oid_to_traded[oid] = 0
                self.oid_to_traded_money[oid] = 0
                self.oid_to_sid[oid] = sid
                self.oid_to_req[oid] = order_dict
                self.oid_to_ref[oid] = mudan_id
            else:
                self.logger.error(f"[on_trade_msg] can't_find_oid (oid){oid}")
                return
        else:
            acc = self.oid_to_acc[oid]
            order_dict = self.oid_to_req[oid]
            sid = self.oid_to_sid[oid]
        _id = str(int(record['成交编号']))
        if _id in self.oid_to_local_ids[oid]:
            #self.logger.warning(f"[on_trade_msg] duplicate_trade_msg (record){record}")
            return
        else:
            self.oid_to_local_ids[oid].append(_id)

        int_stock_code = int(record['证券代码'])
        ticker = f'{int_stock_code:06d}'
        exchange = decode_exchange_id(ticker)
        traded_vol = int(record['成交数量'])
        traded_price = float(record['成交价格'])
        trade_amt = float(traded_vol * traded_price)

        target_type = encode_emc_side(record['业务类型'])
        if target_type == 1:
            self.oid_to_traded_money[oid] += trade_amt
            self.oid_to_traded[oid] += traded_vol
        elif target_type == 2:
            self.oid_to_traded_money[oid] -= trade_amt
            self.oid_to_traded[oid] -= traded_vol
        entrust_vol = record['成交数量']
        #entrust_price = record.Price
        entrust_price = float(record['成交价格'])
        match_time = str(record['成交时间'])
        dbTime = get_time_from_str(match_time)

        commission = 0
        order_type = order_dict['order_type']
        target_account_name = order_dict['accountName']
        acc = self.target_account_names_to_acc[target_account_name]
        log_accountname = order_dict['accountName'].split('@')[1]
        tg_name = order_dict['accountName'].split('@')[0]

        side = encode_emc_side(record['业务类型'])

        db_msg = {
            "trade_ref": _id,
            "oid": int(oid),
            "tg_name": tg_name,
            "exchange": exchange,
            "ticker": ticker,
            "traded_vol": traded_vol,
            "traded_price": traded_price,
            "order_type": order_type,
            "side": side,  # 对应 tlclient.trader.constant 包 Side
            "entrust_vol": entrust_vol,
            "entrust_price": entrust_price,  # 没有下单价格，只有成交价
            "dbTime": dbTime,
            "sid": sid,  # 对应订单中的 sid
            "commission": commission,  # 没有
            "trade_time": dbTime,  # 具体交易时间

            "accountName":  log_accountname,  # 对应 account_info.account_name
        }
        trade_collection = self.tradelog_db[acc]['trade']
        replace_trade_query = {"trade_ref": _id, "oid": oid,
                               "sid": sid, "accountName": log_accountname}
        db_res = trade_collection.replace_one(
            replace_trade_query, db_msg, True)
        self.logger.info(
            f"[rtn_trade] (db_res){db_res} (db_msg){db_msg} (traded_vol){traded_vol} (traded_price){traded_price}")
        self.update_position(traded_vol, order_dict, sid,
                             oid, side, trade_amt, exchange)

        atx_order_collection = self.order_info_db[acc]['atx_order']
        atx_order_msg = {
            "local_ids": self.oid_to_local_ids[oid],
        }
        update_atx_order_msg = {"$set": atx_order_msg}
        query = {"oid": oid}
        res = atx_order_collection.update_one(query, update_atx_order_msg)
        self.logger.info(
            f"[on_trade_msg] update_atx_order_info (res){res} (msg){update_atx_order_msg}")

    @MongoClientTradeGateway.error_handler
    def update_position(self, traded_vol, order, sid, oid, side, trade_amt, exchange):
        target_accountname = order['accountName']
        acc = self.target_account_names_to_acc[target_accountname]

        query = {'sid': sid, 'accountName': target_accountname}
        position_collection = self.order_info_db[acc]['EquityPosition']
        position = position_collection.find_one(query)
        if position is None and traded_vol > 0:
            if oid not in self.oid_to_req:
                self.logger.warning(
                    f"[update_position] can't_find_req (sid){sid} (oid){oid}")
                return
            if oid not in self.oid_to_traded:
                self.logger.error(f"[update_position]no trade_vol (sid){sid}")
                return
            td_trade_vol = self.oid_to_traded[oid]

            amt = self.oid_to_traded_money[oid]

            ticker = order['ticker']
            yd_pos = 0
            mkt_value = amt
            cost = 0
            if not td_trade_vol == 0:
                cost = amt / td_trade_vol
            update_time = datetime.now(timezone.utc)

            position_msg = {
                "ticker": ticker,
                "cost": cost,  # 成本价
                "td_pos_long": td_trade_vol,  # 今仓
                "yd_pos_long": yd_pos,  # 昨仓（可卖），挂止盈单后为0
                "td_pos_short": 0,
                "yd_pos_short": 0,
                "actual_td_pos_long": td_trade_vol,  # 实际的今仓
                "actual_yd_pos_long": yd_pos,  # 实际的昨仓
                "enter_date": update_time,
                "holding_days": 0,  # 持仓时间（交易日累计）
                "mkt_value": mkt_value,  # 市值
                "exchange": exchange,  # 对应 tlclient.trader.constant 包 ExchangeID
                "sid": sid,  # 我们策略生成的id，需要根据实际下单情况维护各sid的持仓。
                # 格式: {account_info.tg_name}@{account_info.account_name}
                "accountName": target_accountname,
                "update_date": update_time,
            }
            query2 = {'sid': sid,
                      'accountName': target_accountname}
            res = position_collection.replace_one(query2, position_msg, True)
            self.logger.info(
                f"[update_position] (res){res} (msg){position_msg}")
        else:
            if oid not in self.oid_to_req:
                self.logger.warning(
                    f"[update_position] can't_find_req (sid){sid}")
                return
            if oid not in self.oid_to_traded:
                self.logger.error(f"[update_position]no trade_vol (sid){sid}")
                return
            actual_yd_pos = position['actual_yd_pos_long']
            amt = trade_amt
            yd_pos = position['yd_pos_long']
            if side == 1 or side == 3:
                td_trade_vol = position['actual_td_pos_long'] + traded_vol
                mkt_value = position['mkt_value'] + amt
            elif side == 2:
                td_trade_vol = position['actual_td_pos_long'] - traded_vol
                mkt_value = position['mkt_value'] - amt
                yd_pos = yd_pos - traded_vol

            ticker = order['ticker']

            cost = 0
            total_vol = td_trade_vol + yd_pos
            if not total_vol == 0:
                cost = mkt_value / total_vol
            update_time = datetime.now(timezone.utc)
            accountName = order['accountName']
            enter_time = position['enter_date']
            holding_days = position['holding_days']
            position_msg = {
                "ticker": ticker,
                "cost": cost,  # 成本价
                "td_pos_long": td_trade_vol,  # 今仓
                "yd_pos_long": yd_pos,  # 昨仓（可卖），挂止盈单后为0
                "td_pos_short": 0,
                "yd_pos_short": 0,
                "actual_td_pos_long": td_trade_vol,  # 实际的今仓
                "actual_yd_pos_long": actual_yd_pos,  # 实际的昨仓
                "enter_date": enter_time,
                "holding_days": holding_days,  # 持仓时间（交易日累计）
                "mkt_value": mkt_value,  # 市值
                "exchange": exchange,  # 对应 tlclient.trader.constant 包 ExchangeID
                "sid": sid,  # 我们策略生成的id，需要根据实际下单情况维护各sid的持仓。
                # 格式: {account_info.tg_name}@{account_info.account_name}
                "accountName": accountName,
                "update_date": update_time,
            }
            query = {'sid': sid,
                     'accountName': accountName}
            res = position_collection.replace_one(query, position_msg, True)
            self.logger.info(
                f"[update_position] (res){res} (msg){position_msg}")

    def start(self):
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        _msg = f"[login] gf_server_start (time){datetime.now()}"
        self.send_to_user(logger=self.logger, url_list=self.url_list, msg=_msg)
        self.monitor()

    def close(self):
        return super().close()

    def join(self):
        while self.is_stopped == False:
            time.sleep(0.01)
            if self.is_stopped:
                self.logger.info(
                    "[close] main thread is stopped,active_orders message will lose")
                self.close()


if __name__ == "__main__":

    sys.stdout.reconfigure(encoding='utf-8')
    description = "emc_server,get target from mongodb and serve gf"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-e', '--end_time', dest='end_time', default='15:30')
    _config_filename = "C:/Users/Administrator/Desktop/emc_batandconfig/emc_server_config.json"
    parser.add_argument('-p', '--config_filepath',
                        dest='config_filepath', default=_config_filename)

    args = parser.parse_args()
    print(f"(args){args}")

    td = EmcServer(args.config_filepath, args.end_time, GATEWAY_NAME)
    td.start()

    td.join()
