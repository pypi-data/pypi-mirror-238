# coding: utf-8
#

import asyncio
import datetime
import hashlib
import io
import json
import os
import subprocess
import sys
import threading
import time
import traceback

import pytz
import tornado.websocket
from logzero import logger
from sqlalchemy import create_engine
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker
from tornado.escape import url_escape

from .models import PerfDataRecord, engine
from .page import BaseHandler
from .. import idbUtil, adbUtil
from .. import winUtil
from ..download_app import DownloadAPP
from ..monitor import MonitorThread

WDA_PORT_START = 7100
WDA_PID = None


Session = sessionmaker(bind=engine)


class DeviceListHandler(BaseHandler):
    def get(self):
        try:
            deviceinfo_list = []
            util_list = [adbUtil, idbUtil]
            for util in util_list:
                device_list = util.GetConnectedDevice()
                for device in device_list:
                    deviceinfo = util.GetDeviceInfo(device)
                    deviceinfo_list.append(deviceinfo)
            if sys.platform == "win32":
                deviceinfo_list.append(winUtil.get_pc_info())
            self.write({"data": deviceinfo_list})
        except Exception as e:
            logger.error("get device list error: %s", traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })


class PackageListHandler(BaseHandler):
    def get(self, deviceinfo):
        try:
            logger.info("select device is %s" % deviceinfo)
            deviceid = deviceinfo.split('|')[1]
            util = adbUtil
            if "iPhone" in deviceinfo or 'iOS' in deviceinfo:
                util = idbUtil
            elif "windows" in deviceinfo.lower():
                util = winUtil
            app_list = util.get_app_list(deviceid)
            self.write({"data": app_list})
        except Exception as e:
            logger.error("get package list error: %s", traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })


class DeviceAPPHandler(BaseHandler):
    def post(self):
        try:
            deviceinfo = self.get_argument("deviceinfo")
            package = self.get_argument("package").split('--')[-1]
            stop = False if self.get_argument("stop") == 'false' else True
            deviceid = deviceinfo.split('|')[1]
            util = adbUtil
            if "iPhone" in deviceinfo or 'iOS' in deviceinfo:
                util = idbUtil
            util.start_app(deviceid, package, stop=stop)
        except Exception as e:
            logger.error("start app error: %s", traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })


class DeviceAPPInstallHandler(BaseHandler):
    def post(self):
        try:
            deviceinfo = self.get_argument("deviceinfo")
            app_path = self.get_argument("app_path")
            all_install = False if self.get_argument("all_install") == 'false' else True
            deviceid = deviceinfo.split('|')[1]
            util = adbUtil
            subfix = ".apk"
            if "iPhone" in deviceinfo or 'iOS' in deviceinfo:
                util = idbUtil
                subfix = ".ipa"
            folder = os.path.join(os.environ['HOME'], "perftool")
            os.makedirs(folder, exist_ok=True)
            save_path = app_path
            if app_path.startswith("http"):
                save_path = os.path.join(folder, hashlib.md5(app_path.encode()).hexdigest() + subfix)
                if os.path.exists(save_path) is False:
                    DownloadAPP.download(app_path, save_path)
            util.install_app(deviceid, save_path, all_install)
            self.write({
                "success": True,
                "description": "安装成功",
            })
        except Exception as e:
            logger.error("start app error: %s", traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })


class PerfCaptrueHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def initialize(self):
        self.device_read_thread = {}
        self.device_monitor_thread = {}
        self.interval_time = 5

    def on_close(self):
        logger.warning("websocket closed, cleanup")
        for device in self.device_read_thread.keys():
            self.device_read_thread[device] = False
            monitor = self.device_monitor_thread[device]
            monitor.stop()
            del self.device_read_thread[device]
            del self.device_monitor_thread[device]
            time.sleep(2)

    async def prepare(self):
        pass

    def send_keyboard_interrupt(self):
        for device, monitor in self.device_monitor_thread:
            monitor.stop()

    async def open(self):
        logger.debug("websocket opened")

    def write2(self, data):
        self.write_message(json.dumps(data))

    async def on_message(self, message):
        logger.info("Receive:%s", message)
        data = json.loads(message)
        device, platform, package, action = data['device'], data['platform'], data['package'], data['action']
        file_name = data['filename']
        self.interval_time = data['intervaltime']
        capture_time = data.get("capture_time", 24)
        save_detail = data.get('save_detail', False)
        divided_core_nums = data.get('divided_core_nums', False)
        logger.info(f"自定义文件名：{file_name},是否保存详细数据：{save_detail}")
        device = device.split('|')[1]
        package = package.split('--')[-1]
        if action == 'start':
            monitor = MonitorThread(platform, device, package, capture_time, file_name, save_detail, divided_core_nums)
            monitor.setDaemon(True)
            monitor.start()
            self.device_monitor_thread[device] = monitor
            self.device_read_thread[device] = True
            th = threading.Thread(target=self.read_perf_data, args=(device,))
            th.setDaemon(True)
            th.start()
        elif action == 'stop':
            self.device_read_thread[device] = False
            monitor = self.device_monitor_thread[device]
            monitor.stop()
            filepath = monitor.get_perf_file_name()
            del self.device_read_thread[device]
            del self.device_monitor_thread[device]
            time.sleep(2)
            self.write2({"action": "stop", "filepath": filepath})
        elif action == 'change':
            logger.info(f'设置数据刷新时间间隔：{self.interval_time}s')
        elif action == 'dumphprof':
            self.device_monitor_thread[device].dump_hprof()
            self.write2({"dumphprof": True})
        else:
            logger.warning("Unknown received message: %s", data)

    def read_perf_data(self, device):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while True:
            if device not in self.device_read_thread or self.device_read_thread[device] is False:
                break
            data = self.device_monitor_thread[device].read_perf_data()
            if data:
                self.write2(data)
            time.sleep(int(self.interval_time))


class ExportDataHandler(BaseHandler):
    async def get(self, filepath, save_filename):
        logger.info(f'导出文件：{filepath},自定义文件名：{save_filename}')
        if os.path.exists(filepath) is False:
            logger.info('文件不存在：' + filepath)
            self.set_status(500)
            self.write({
                "success": False,
                "description": '文件不存在：' + filepath
            })
            return
        content = open(filepath, mode='r', encoding='utf-8').read()
        sio = io.BytesIO()
        sio.write(content.encode('utf-8'))
        if not save_filename:
            save_filename = os.path.basename(filepath)
        if not save_filename.endswith(".csv"):
            save_filename += ".csv"
        logger.info(f"导出后的文件名为：{save_filename}")
        self.set_header('Content-Type', 'text/csv')
        self.set_header('Content-Disposition',
                        'attachment; filename={}'.format(url_escape(save_filename)))
        self.write(sio.getvalue())


class StartWDAHandler(BaseHandler):
    def post(self):
        global WDA_PORT_START
        global WDA_PID
        try:
            serial = self.get_argument("serial")
            cmd = f"tidevice -u {serial} wdaproxy -p {WDA_PORT_START}"
            logger.info(f"启动WDA:{cmd}")
            folder = os.path.join(os.environ['HOME'], "perftool")
            os.makedirs(folder, exist_ok=True)
            wda_log_file = open(os.path.join(folder, serial + ".log"), mode='w+')
            pro = subprocess.Popen(cmd, shell=True, stdout=wda_log_file, stderr=wda_log_file)
            st = time.perf_counter()
            success = False
            data = ""
            read_log = open(os.path.join(folder, serial + ".log"), mode='r')
            while pro.poll() is None and time.perf_counter() - st < 120:
                data = read_log.read()
                if "WebDriverAgent start successfully" in data or "Test runner ready detected" in data:
                    WDA_PID = pro.pid
                    success = True
                    break
            read_log.close()
            if success is False:
                self.set_status(501)
            self.write({
                "devicePort": WDA_PORT_START,
                "description": data
            })
            WDA_PORT_START += 2
        except Exception as e:
            logger.error("start wda error: %s", traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })


class CloseWDAHandler(BaseHandler):
    def post(self):
        global WDA_PID
        try:
            if sys.platform != "win32":
                serial = self.get_argument("serial")
                cmd = "kill -9 " + str(WDA_PID)
                logger.info(f"关闭WDA:{cmd}")
                os.system(cmd)
                for item in os.popen("ps -ef | grep tidevice |grep '{}' | grep -v grep".format(serial)).readlines():
                    info = item.split(" ")
                    os.system("kill -9 " + info[3])
        except Exception as e:
            logger.error("start wda error: %s", traceback.format_exc())
            self.set_status(500)
            self.write({
                "success": False,
                "description": traceback.format_exc(),
            })


# 创建Tornado应用
class AddOrGetDataHandler(BaseHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            with Session() as session:
                new_data = PerfDataRecord(**data)
                session.add(new_data)
                session.commit()
                self.write({"message": "Data added successfully", "id": new_data.id})
        except Exception as e:
            self.set_status(400)
            self.write({"error": str(e)})

    def get(self):
        try:
            page = int(self.get_argument("page", 1))
            per_page = int(self.get_argument("page_size", 20))
            search_query = self.get_argument("search", None)  # 获取搜索关键字
            with Session() as session:
                query = session.query(PerfDataRecord)

                if search_query:
                    # 构建模糊搜索查询条件
                    search_term = f"%{search_query}%"  # 添加 '%' 用于模糊匹配
                    search_filter = or_(
                        PerfDataRecord.start_time.ilike(search_term),
                        PerfDataRecord.devices.ilike(search_term),
                        PerfDataRecord.app_name.ilike(search_term),
                        PerfDataRecord.app_version.ilike(search_term),
                        PerfDataRecord.app_package.ilike(search_term)
                    )
                    query = query.filter(search_filter)

                total_records = query.count()

                # 倒序排列数据
                query = query.order_by(PerfDataRecord.id.desc())

                # 分页查询
                data = query.limit(per_page).offset((page - 1) * per_page).all()

                # 格式化时间为 "yyyy-MM-dd HH:mm:ss" 格式，并设置时区
                formatted_data = []
                local_timezone = pytz.timezone("Asia/Shanghai")  # 例如，设置为东八区时区

                for d in data:
                    start_time_local = d.start_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
                    end_time_local = d.end_time.replace(tzinfo=pytz.utc).astimezone(
                        local_timezone) if d.end_time else None

                    formatted_d = {
                        "id": d.id,
                        "start_time": start_time_local.strftime("%Y-%m-%d %H:%M:%S"),
                        "end_time": end_time_local.strftime("%Y-%m-%d %H:%M:%S") if end_time_local else None,
                        "devices": d.devices,
                        "app_name": d.app_name,
                        "filepath": d.filepath,
                        "app_version": d.app_version,
                        "app_package": d.app_package
                    }
                    if d.end_time:
                        formatted_d["duration"] = round(float(((d.end_time - d.start_time).total_seconds()) / 60), 1)
                    else:
                        formatted_d["duration"] = None
                    formatted_data.append(formatted_d)

                # 构建 JSON 响应
                response = {
                    "total_records": total_records,
                    "page": page,
                    "per_page": per_page,
                    "data": formatted_data
                }
                self.write(response)
        except Exception as e:
            self.set_status(400)
            self.write({"error": str(e)})


class DeleteOrUpdateDataHandler(BaseHandler):
    def delete(self, data_id):
        try:
            with Session() as session:
                data = session.query(PerfDataRecord).filter_by(id=data_id).first()
                if data:
                    session.delete(data)
                    session.commit()
                    self.write({"message": "Data deleted successfully"})
                else:
                    self.set_status(404)
                    self.write({"message": "Data not found"})
        except Exception as e:
            self.set_status(400)
            self.write({"error": str(e)})

    def patch(self, data_id):
        try:
            data_updates = json.loads(self.request.body)
            with Session() as session:
                data = session.query(PerfDataRecord).filter_by(id=data_id).first()
                if data:
                    # 更新数据字段
                    for key, value in data_updates.items():
                        setattr(data, key, value)
                    data.end_time = datetime.datetime.utcnow()
                    session.commit()
                    self.write({"message": "Data updated successfully"})
                else:
                    self.set_status(404)
                    self.write({"message": "Data not found"})
        except Exception as e:
            self.set_status(400)
            self.write({"error": str(e)})
