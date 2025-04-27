#/app/db/基础数据库操作.py

import asyncio
from  loguru import logger
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

# 配置日志


class 数据库操作:
    def __init__(self, 数据库名称: str, 数据库连接url: str):
        """
        初始化数据库操作类。

        Args:
            数据库名称: 要连接的数据库的名称。
            数据库连接url: MongoDB 连接 URL。
        """
        self.数据库名称 = 数据库名称
        self.数据库连接url = 数据库连接url
        self.数据库: Optional[AsyncIOMotorClient] = None  # 数据库对象

    async def 连接数据库(self):
        """
        连接到 MongoDB 数据库并返回数据库对象。

        Returns:
            数据库对象，如果连接失败则返回 None。
        """
        try:
            self.客户端 = AsyncIOMotorClient(self.数据库连接url)
            self.数据库 = self.客户端[self.数据库名称]
            logger.info(f"成功连接到数据库: {self.数据库名称}")
            return {"状态": "成功", "数据库对象": self.数据库}
        except ConnectionFailure as e:
            logger.error(f"连接数据库失败: {e}")
            return None
        except Exception as e:
            logger.error(f"连接数据库失败: {e}")
            return None

    async def 关闭连接(self):
        """
        关闭数据库连接。
        """
        try:
            if self.数据库 is not None:  # 检查数据库对象是否存在
                if self.数据库.client is not None: # 检查客户端是否存在
                    self.数据库.client.close()
                    logger.info("数据库连接已关闭")
                else:
                    logger.info("客户端未建立，无需关闭")
            else:
                logger.info("数据库连接未建立，无需关闭")
        except Exception as e:
            logger.error(f"关闭数据库连接失败: {e}")
        finally:
            self.数据库 = None

