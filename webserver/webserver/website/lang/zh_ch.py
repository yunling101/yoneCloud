#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webserver.website.common import load_index_config

zh_lang = {
    "none":                     "无",
    "hide":                     "隐藏",
    "true":                     "正常",
    "normal":                   "正常",
    "false":                    "禁止",
    "refresh":                  "刷新",
    "add":                      "添加",
    "edit":                     "编辑",
    "del":                      "删除",
    "delete":                   "删除",
    "condition":                "条件",
    "sign in":                  "登 录",
    "first":                    "首 页",
    "previous":                 "上一页",
    "next":                     "下一页",
    "last":                     "末 页",
    "drag to sort":             "拖动进行排序",
    "alarm group":              "报警分组",
    "alarm name":               "报警名称",
    "for":                      "间隔时间",
    "expr":                     "规则",
    "description":              "描述",
    "analysis":                 "解析",
    "value":                    "值",
    "line":                     "线路",
    "position":                 "位置",
    "model":                    "型号",
    "command":                  "命令",
    "playback":                 "回放",
    "business":                 "业务",
    "hosts":                    "主机",
    "results":                  "返回结果",
    "result":                   "执行结果",
    "frequency":                "次数",
    "priority":                 "优先级",
    "other":                    "其他",
    "dashboard":                "仪表盘",
    "not executed":             "未执行",
    "executed":                 "已执行",
    "confirm":                  "确认",
    "expand":                   "展开",
    "format":                   "格式",
    "minute":                   "分钟",
    "hour":                     "小时",
    "day":                      "日",
    "month":                    "月",
    "week":                     "周",
    "clear":                    "清除",
    "run":                      "运行",
    "note":                     "注意",
    "disable":                  "禁用",
    "enable":                   "启用",
    "restore":                  "还原",
    "destroy":                  "销毁",
    "all":                      "全部",
    "password":                 "密码",
    "certificate":              "凭证",
    "export":                   "导出",
    "group":                    "分组",
    "level":                    "级别",
    "info":                     "提示",
    "warning":                  "警告",
    "critical":                 "严重",
    "rule":                     "规则",
    "global":                   "全局",
    "config":                   "配置",
    "route":                    "路由",
    "close":                    "关闭",
    "open":                     "开启",
    "save":                     "保存",
    "link":                     "链接",
    "key":                      "秘钥",
    "search":                   "搜索",
    "parent":                   "父级",
    "default":                  "默认",
    "old":                      "旧",
    "new":                      "新",
    "permission":               "权限",
    "history":                  "历史",
    "online":                   "在线",
    "offline":                  "离线",
    "server":                   "服务器",
    "filter":                   "过滤",
    "abnormal":                 "异常",
    "unknown":                  "未知",
    "sort":                     "排序",
    "login":                    "登录",
    "community":                "开源版",

    "serial number":            "序列号",
    "resource pool":            "资源池",
    "security group":           "安全组",
    "batch delete":             "批量删除",
    "batch import":             "批量导入",

    "event":                    "事件",
    "event id":                 "事件ID",
    "event type":               "事件类型",
    "event title":              "事件标题",
    "event content":            "事件内容",
    "recent event":             "近期事件",

    "today":                    "今天",
    "yesterday":                "昨天",
    "last 7 days":              "最近7天",
    "last 30 days":             "最近30天",
    "this month":               "本月",
    "last month":               "上月",
    "custom range":             "自定义",

    "sunday":                   "星期日",
    "monday":                   "星期一",
    "tuesday":                  "星期二",
    "wednesday":                "星期三",
    "thursday":                 "星期四",
    "friday":                   "星期五",
    "saturday":                 "星期六",

    "sid":                      "序列ID",
    "address":                  "地址",
    "hostname":                 "主机名",
    "port":                     "端口",
    "type":                     "类型",
    "source":                   "来源",
    "object":                   "对象",
    "role":                     "角色",
    "comment":                  "备注",
    "name":                     "名称",
    "title":                    "标题",
    "icon":                     "图标",
    "weigh":                    "权重",
    "ismenu":                   "菜单",
    "menu":                     "菜单",
    "view":                     "视图",
    "content":                  "内容",
    "username":                 "用户名",
    "user":                     "用户",
    "instance id":              "实例ID",
    "alias":                    "别名",
    "domain":                   "域名",
    "intranet":                 "内网",
    "version":                  "版本",
    "current":                  "当前",
    "monitor":                  "监控",
    "account":                  "账户",
    "project":                  "项目",
    "platform":                 "平台",
    "interval":                 "间隔",
    "nickname":                 "姓名",
    "start":                    "开始",
    "stop":                     "停止",
    "create time":              "创建时间",
    "deadline time":            "到期时间",
    "update time":              "更新时间",
    "start time":               "开始时间",
    "end time":                 "结束时间",
    "common search":            "过滤",
    "repeat":                   "重复",
    "wait":                     "等待",
    "time":                     "时间",
    "submit":                   "提交",
    "hints":                    "提示",
    "reset":                    "重置",
    "choose":                   "选择",
    "operate":                  "操作",
    "detail":                   "详情",
    "email":                    "邮箱",
    "last login":               "最后登录时间",
    "is active":                "状态",
    "status":                   "状态",
    "once":                     "一次",
    "period":                   "周期",
    "region":                   "区域",
    "labels":                   "标签",
    "provider":                 "提供商",
    "osname":                   "系统名",
    "cpu":                      "CPU(核)",
    "memory":                   "内存(G)",
    "disk":                     "磁盘(G)",
    "public":                   "公网",
    "check update":             "检查更新",
    "instance name":            "实例名",
    "instance status":          "实例状态",
    "timer type":               "定时类型",
    "execution time":           "执行时间",
    "execution status":         "执行状态",
    "timer time":               "定时时间",
    "timeline":                 "时间线",
    "last updated":             "最近更新时间",
    "click to search %s":       "点击搜索 %s",
    "click to toggle":          "点击切换",
    "operation completed":      "操作成功!",
    "operation failed":         "操作失败!",
    "unknown data format":      "未知的数据格式!",
    "unknown exception error":  "未知的异常错误",
    "email_configs":            "接收邮箱",
    "wechat_configs":           "企业微信",
    "webhook_configs":          "WebHook",
    "cannot be empty":          "不能为空",
    "risk warning":             "风险提示",
    "kind tips":                "温馨提示",
    "template file":            "模板文件",
    "testers":                  "测试人员",
    "maintainer":               "维护人员",
    "life cycle":               "生命周期",
    "mark read":                "标记已读",
    "empty list":               "空列表",
    "total {0} available":      "共{0}个可选",
    "host selected":            "已选择主机",
    "host can be selected":     "可选择主机",
    "previous page":            "上一页",
    "next page":                "下一页",
    "home page":                "首页",
    "last page":                "尾页",
    "code":                     "验证码",
    "get":                      "获取",
    "forgot password":          "忘记密码",
    "remember password":        "记住密码",

    "Already latest":             "已是最新版本",
    "MENU":                       "导航",
    "EXTRA":                      "扩展",
    "Monitor Dashboard":          "监控可视化",
    "View All":                   "查看全部",
    "Log out":                    "退出",
    "Change Password":            "修改密码",
    "Welcome {0}":                "欢迎 {0} 登录",
    "You have {0} messages":      "您有{0}条消息未查看",
    "empty the recycle bin":      "清空回收站",
    "error in getting role":      "角色获取出错",

    "resource growth in the past 7 days": "近7日资源增长",
    "total number of hosts in 7 days":    "主机7日总数",
    "total business volume in 7 days":    "业务7日总数",
    "recent login records":               "最近登录记录",
    "recent operation records":           "最近操作记录",
    "welcome back to the console":        "欢迎您回到控制台",
    "yyyy-mm-dd":                         "YYYY年MM月DD日",
    "please select at least 1 host":      "请至少选择1台主机",
    "you must select a host":             "必须选择主机",

    "permission selection cannot be empty": "权限选择不能为空",
    "fill in the template format and import": "按照模板格式填写在导入",
    "importing requires a specific file format, please download": "主机池导入需要特定的文件格式，请下载",
    "before enabling monitoring," +
    " you need to install node_exporter on the monitored host and specify the default port as 17000.":
        "开启监控前需要在被监控主机上安装 node_exporter 并指定默认端口为 17000。",
    "currently only supports binding one certificate to one host": "暂仅支持一个主机绑定一个凭证",
    "after selection, the tree must be in expanded state, otherwise the selected items cannot be obtained.": "选择后树形必须是展开状态，否则无法获取选择项。",
    "scheduled tasks depend on the controller manager service. please ensure that this service is available.":
        "定时任务依赖于 ControllerManager 服务，请确保此服务是可用状态。",
    "the batch command will execute the command and record the execution log as the credential user bound to the host. " +
    "please use the command with caution!": "批量命令将以主机绑定的凭证用户执行命令并记录执行日志，请谨慎使用命令！",
    "please enter the command to be executed in batches": "请输入要批量执行的命令",
    "only one sh command is supported (not shell script)": "仅支持一条sh命令（非shell脚本）",
    "are you sure you want to delete this item?":         "确定删除此项?",
    "are you sure you want to truncate?": "确定要清空吗?",
    "are you sure you want to delete the %s selected item?": "确定要删除选中的 %s 条项目吗?",
    "are you sure you want all the markers read?": "确定要全部标为已读吗?"
}


def get_lang(message):
    basic_config = load_index_config()
    if basic_config["code"] and basic_config["msg"].get("language") == "english":
        return message

    if zh_lang.get(message) is None:
        return message
    return zh_lang[message]


def get_language():
    basic_config = load_index_config()
    if basic_config["code"] and basic_config["msg"].get("language") == "english":
        return {}
    return zh_lang


class Lang:
    @staticmethod
    def get(message):
        return get_lang(message)
