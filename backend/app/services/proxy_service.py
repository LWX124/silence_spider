"""
代理服务器服务
用于微信爬虫的代理功能
"""
import asyncio
import logging
from typing import Optional
from mitmproxy import ctx
from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster

logger = logging.getLogger(__name__)


class ProxyService:
    """代理服务器服务类"""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.master: Optional[DumpMaster] = None
        self.is_running = False
    
    async def start_proxy(self):
        """启动代理服务器"""
        try:
            opts = Options(listen_host='0.0.0.0', listen_port=self.port)
            config = ProxyConfig(opts)
            
            self.master = DumpMaster(opts)
            self.master.server = ProxyServer(config)
            
            # 添加事件监听器
            self.master.addons.add(WeChatAddon())
            
            logger.info(f"代理服务器启动在端口 {self.port}")
            self.is_running = True
            
            # 启动代理服务器
            await self.master.run()
            
        except Exception as e:
            logger.error(f"代理服务器启动失败: {e}")
            self.is_running = False
    
    def stop_proxy(self):
        """停止代理服务器"""
        if self.master:
            self.master.shutdown()
            self.is_running = False
            logger.info("代理服务器已停止")
    
    def is_proxy_running(self) -> bool:
        """检查代理服务器是否运行"""
        return self.is_running


class WeChatAddon:
    """微信爬虫代理插件"""
    
    def __init__(self):
        self.request_data = []
    
    def request(self, flow):
        """处理请求"""
        # 过滤微信相关请求
        if 'mp.weixin.qq.com' in flow.request.pretty_host:
            ctx.log.info(f"捕获微信请求: {flow.request.url}")
            # 这里可以添加请求拦截和修改逻辑
    
    def response(self, flow):
        """处理响应"""
        # 过滤微信相关响应
        if 'mp.weixin.qq.com' in flow.request.pretty_host:
            ctx.log.info(f"捕获微信响应: {flow.request.url}")
            # 这里可以添加响应拦截和修改逻辑


# 全局代理服务实例
proxy_service = ProxyService()


async def start_proxy_server():
    """启动代理服务器的异步函数"""
    await proxy_service.start_proxy()


def stop_proxy_server():
    """停止代理服务器"""
    proxy_service.stop_proxy() 