import os, subprocess, json
from loguru import logger

class Render3D:
    def __init__(self):
        self.output_dir = "output/models"
        os.makedirs(self.output_dir, exist_ok=True)
        self.last_output = None

    def generate(self, name, description):
        """生成 3D 模型，返回 GLB 文件路径"""
        logger.info(f"  生成3D模型: {name}")
        try:
            from build123d import *
            import build123d as bd

            # 创建基础几何体
            box = bd.Box(30, 20, 60)
            cyl = bd.Cylinder(10, 70)
            result = box + bd.Pos(0, 0, 5) * cyl

            # 导出为 GLB
            path = os.path.join(self.output_dir, f"{name}.glb")
            bd.export_glb(result, path)
            logger.success(f"  3D模型已保存: {path}")
            self.last_output = path
            return path
        except ImportError as e:
            logger.warning(f"  build123d 未安装: {e}")
            logger.info("  运行 pip install build123d 安装")
            return None
        except Exception as e:
            logger.warning(f"  3D生成失败: {str(e)[:80]}")
            return None
