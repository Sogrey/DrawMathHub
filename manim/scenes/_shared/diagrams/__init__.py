"""
按题型（非讲次）拆分的图解 Mixin。

同一题型的不同讲次共用同一模块，在各自 problem_N.py 里传入不同数据即可。

目录：
  common.py   — 公共图元（人圈、省略号）
  between.py  — 之间问题
  queue.py    — 排队问题
  transfer.py — 移多补少
  period.py   — 周期问题
"""

from diagrams.between import BetweenDiagramMixin
from diagrams.common import DiagramCommonMixin
from diagrams.period import PeriodDiagramMixin
from diagrams.queue import QueueDiagramMixin
from diagrams.transfer import TransferDiagramMixin
from diagrams.substitution import SubstitutionDiagramMixin
from diagrams.time_vertical import TimeVerticalDiagramMixin

__all__ = [
    "DiagramCommonMixin",
    "BetweenDiagramMixin",
    "QueueDiagramMixin",
    "TransferDiagramMixin",
    "PeriodDiagramMixin",
    "SubstitutionDiagramMixin",
    "TimeVerticalDiagramMixin",
]
