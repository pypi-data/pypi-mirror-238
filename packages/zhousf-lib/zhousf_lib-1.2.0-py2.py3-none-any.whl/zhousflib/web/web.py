# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Date    : 2021/8/9 
# @Function: web服务配置与管理
import os
import time
import random
from flask import g
from app import FLASK_APP
from gevent import monkey
from zhousflib.web import log_util
from flask import request, Response
from gevent.pywsgi import WSGIServer
from zhousflib.web import response as res
from werkzeug.exceptions import HTTPException


class WebApp(object):
    def __init__(self, config_app):
        FLASK_APP.config.from_object(config_app)
        self.config_app = config_app
        self.app = FLASK_APP
        log_util.init_log(FLASK_APP, config_app.LOG_SERVICE_DIR)
        self.init_config()

    def save_pid(self):
        if not self.config_app.has_pid_file(self.config_app):
            return None
        pid = os.getpid()
        with open(file=self.config_app.PID_FILE, mode='a+') as f:
            f.write(pid.__str__() + "\n")
        return pid

    def start(self):
        server = WSGIServer((self.config_app.HOST, self.config_app.PORT), self.app)
        print("http://{0}:{1}".format(self.config_app.HOST, self.config_app.PORT))
        # pid = self.save_pid()
        # print("pid: {0}".format(pid))
        print("{0} app is starting...".format(self.config_app.ENVIRONMENT))
        try:
            server.serve_forever()
        except Exception as e:
            print(e)
            os.remove(self.config_app.PID_FILE)

    def init_config(self):
        print("create app...")
        if not self.config_app.DEBUG:
            monkey.patch_all()
        FLASK_APP.jinja_env.auto_reload = True
        FLASK_APP.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024
        FLASK_APP.json.ensure_ascii = self.config_app.JSON_AS_ASCII
        FLASK_APP.json.sort_keys = self.config_app.JSON_SORT_KEYS
        FLASK_APP.json.mimetype = self.config_app.JSONIFY_MIMETYPE

        @FLASK_APP.before_request
        def before_request():
            request_id = '{0}_{1}'.format(int(round(time.time() * 1000)), self.rand(digits=5))
            req_id = request.values.get("reqId", None)
            if req_id:
                request_id = req_id
            real_ip = request.headers.get('X-Real-Ip', request.remote_addr)
            g.request_id = request_id
            g.real_ip = real_ip
            g.request_time = time.time()
            g.static = False
            g.log = ""
            msg = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())) + '\n'
            msg += '[request:{0} | ip:{1} | url:{2} | method:{3}]\n'.format(request_id, real_ip, request.path, request.method)
            if request.view_args is not None and len(request.view_args) > 0:
                g.static = True
                delattr(g, "log")
                return
            params = request.data
            if params is None:
                g.static = True
                delattr(g, "log")
                return
            params = bytes.decode(params, encoding='utf-8')
            params = params.strip()
            if 0 < len(params) < 10240:
                msg += params + "\n"
            g.log = msg

        @FLASK_APP.after_request
        def after_request(response):
            """
            RuntimeError: Attempted implicit sequence conversion but
                        the response object is in direct passthrough mode.
            response.direct_passthrough = False
            """
            response.direct_passthrough = False
            msg_before = ""
            if hasattr(g, "log"):
                msg_before += g.log
            if hasattr(g, "logger"):
                g.logger.title_first("返回信息")
            cost = round(time.time() - g.request_time, 4)
            msg_after = '[response:{0} | cost_time:{1}s]\n'.format(g.request_id, cost)
            status_code = 200
            if isinstance(response, Response) and not g.static:
                if response.json is not None and response.content_length < 10240:
                    msg_after += "{0}\n".format(response.json)
                    status_code = response.json.get("code", status_code)
                if hasattr(g, "status_code"):
                    status_code = g.status_code
                if hasattr(g, "logger"):
                    if status_code in range(201, 500):
                        g.logger.log(msg_after)
                        log_util.warning(msg_before + msg_after)
                    elif status_code in range(500, 700):
                        g.logger.log(msg_after)
                        log_util.error(msg_before + msg_after)
                    elif status_code > 1000:
                        g.logger.log_txt = g.logger.log_txt.replace("\n\n", "\n")
                        g.logger.log(msg_after)
                        log_util.error(g.logger.log_txt)
                    else:
                        g.logger.log(msg_after)
                        log_util.info(msg_before + msg_after)
                    g.logger.save_log()
                else:
                    if hasattr(g, "log"):
                        log_util.error(msg_before + msg_after)
            return response

        @FLASK_APP.route('/')
        def index():
            ip, port = request.host.split(":")
            return res.success_tip(status=200, result="{0}:{1}".format(ip, port))

        @FLASK_APP.route('/favicon.ico')
        def get_fav():
            return FLASK_APP.send_static_file('images/favicon.ico')

        @FLASK_APP.errorhandler(HTTPException)
        def exception(e):
            log_util.warning(repr(e))
            g.status_code = e.code
            return res.failed_tip(status=e.code, result="{0}[{1}]".format(e.description, request.path))

    @staticmethod
    def rand(digits=3):
        """
        生成随机数
        :param digits: 随机数位数
        digits=3则生成范围[100,999]
        digits=4则生成范围[1000,9999]
        :return:
        """
        if digits < 1:
            return 0
        assert isinstance(digits, int)
        start = pow(10, digits - 1)
        end = pow(10, digits) - 1
        return random.randint(start, end)
