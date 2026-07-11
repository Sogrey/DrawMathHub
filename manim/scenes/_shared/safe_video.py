"""
safe_video.py — Manim 视频安全区域公共模块
集成片头/片尾/字幕 + 安全区域自动约束，确保所有文字和图形不超出视频范围。

用法：
    from safe_video import SafeScene

    class MyVideo(SafeScene):
        def construct(self):
            title = self.show_title("主题", subtitle="副标题")
            # 内容区域通过 self.safe_* 方法或 self.content_center 等定位
            circle = Circle().move_to(self.content_center)
            self.safe_add(circle)  # 自动裁剪到安全区域
            self.play(Create(circle))
            self.show_credits("THE END")

运行测试:
    manim safe_video.py SafeVideoTest -pqm
"""

from __future__ import annotations

from manim import *
import numpy as np


# ═══════════════════════════════════════════════════════════════
#  安全区域 Scene 基类
# ═══════════════════════════════════════════════════════════════

class SafeScene(Scene):
    """
    带安全区域约束的 Scene 基类。

    安全区域定义（默认值适用于 16:9 画面）：
        - 顶部留白：标题常驻区（标题缩移后占据左上角）
        - 四边 margin：确保文字/图形不超出画面

    子类只需关注内容本身，布局安全由基类保障。
    """

    # ── 可在子类中覆盖的类变量 ──
    BG_COLOR         = "#111122"
    FRAME_W          = 16
    FRAME_H          = 9
    MARGIN           = 0.6      # 四边最小留白（Manim 单位）
    TITLE_ZONE_H     = 1.2      # 顶部标题常驻区高度（show_title 前预估值）
    SECTION_TITLE_GAP       = 0.5   # 左上角标题底边 → 段内小标题中心的间距
    SUBTITLE_BOTTOM_OFFSET  = 0.35  # 底部字幕距安全区下沿（越小越靠下，正文空间越大）
    DEFAULT_FONT     = "Microsoft YaHei"

    def setup(self):
        """Manim 生命周期：在 construct 之前执行。"""
        self.camera.background_color = self.BG_COLOR
        self.camera.frame_width = self.FRAME_W
        self.camera.frame_height = self.FRAME_H

        # 半宽 / 半高
        hw = self.FRAME_W / 2
        hh = self.FRAME_H / 2
        m  = self.MARGIN
        tz = self.TITLE_ZONE_H

        # ── 安全区域边界 ──
        self.safe_left   = -hw + m
        self.safe_right  =  hw - m
        self.safe_top    =  hh - m
        self.safe_bottom = -hh + m

        # ── 内容区域（扣除标题常驻区后的可用区域）──
        self.content_top    =  hh - tz
        self.content_bottom = -hh + m
        self.content_center = np.array([
            (self.safe_left + self.safe_right) / 2,
            (self.content_top + self.content_bottom) / 2,
            0,
        ])

        # 标题组占位（show_title 后赋值）
        self._title_group = None

    def section_title_y(self, gap: float | None = None) -> float:
        """段内小标题纵坐标：紧贴左上角常驻标题下方，不影响 content_center。"""
        if gap is None:
            gap = self.SECTION_TITLE_GAP
        if self._title_group is not None:
            return self._title_group.get_bottom()[1] - gap
        return self.content_top - 0.4

    def place_section_title(
        self, text: str, *, font_size: int = 38, color=YELLOW, gap: float | None = None,
    ):
        """段内小标题：居中，与左上角常驻标题保持间距。"""
        t = self.safe_text(text, font_size=font_size, color=color)
        t.move_to(np.array([0, self.section_title_y(gap), 0]))
        return self.clamp_content(t)

    def place_below_section_title(
        self, mob, section_title, *, buff: float = 0.55,
    ):
        """将内容放在段内小标题正下方并水平居中。"""
        mob.next_to(section_title, DOWN, buff=buff)
        mob.move_to(np.array([0, mob.get_center()[1], 0]))
        return self.clamp_content(mob)

    # ── 边界约束工具 ───────────────────────────────────────────

    def clamp(self, mob, bounds=None):
        """
        将 Mobject 的 bounding box 约束到指定范围内。
        默认约束到安全区域。

        参数:
            mob    — Mobject 实例
            bounds — (left, right, top, bottom) 四元组，默认安全区域

        返回:
            mob 本身（链式调用）
        """
        if bounds is None:
            bounds = (self.safe_left, self.safe_right, self.safe_top, self.safe_bottom)
        left, right, top, bottom = bounds

        mob_left   = mob.get_left()[0]
        mob_right  = mob.get_right()[0]
        mob_top    = mob.get_top()[1]
        mob_bottom = mob.get_bottom()[1]

        dx = dy = 0
        if mob_left < left:
            dx = left - mob_left
        elif mob_right > right:
            dx = right - mob_right
        if mob_bottom < bottom:
            dy = bottom - mob_bottom
        elif mob_top > top:
            dy = top - mob_top

        if dx != 0 or dy != 0:
            mob.shift(np.array([dx, dy, 0]))
        return mob

    def clamp_content(self, mob):
        """约束到内容区域（扣除标题常驻区）。"""
        return self.clamp(mob, bounds=(
            self.safe_left, self.safe_right,
            self.content_top, self.safe_bottom,
        ))

    def fit_to_width(self, mob, max_width):
        """如果宽度超限则等比缩放。"""
        if mob.width > max_width:
            mob.scale(max_width / mob.width)
        return mob

    def fit_to_height(self, mob, max_height):
        """如果高度超限则等比缩放。"""
        if mob.height > max_height:
            mob.scale(max_height / mob.height)
        return mob

    def fit_safe(self, mob, bounds=None):
        """
        先缩放再约束：确保 Mobject 完全在安全区域内。
        自动按需缩放 + 位移。
        """
        if bounds is None:
            bounds = (self.safe_left, self.safe_right, self.safe_top, self.safe_bottom)
        left, right, top, bottom = bounds
        max_w = right - left
        max_h = top - bottom

        self.fit_to_width(mob, max_w)
        self.fit_to_height(mob, max_h)
        self.clamp(mob, bounds)
        return mob

    def fit_content(self, mob):
        """先缩放再约束到内容区域。"""
        return self.fit_safe(mob, bounds=(
            self.safe_left, self.safe_right,
            self.content_top, self.safe_bottom,
        ))

    # ── 安全定位方法 ───────────────────────────────────────────

    def safe_to_edge(self, mob, direction, buff=0.3):
        """
        将 Mobject 移到安全区域边缘，而非画面边缘。
        direction: UP / DOWN / LEFT / RIGHT / UL / UR / DL / DR 等
        """
        m = self.MARGIN
        hw = self.FRAME_W / 2 - m
        hh_content = self.content_top if direction[1] > 0 else self.FRAME_H / 2 - m

        if direction == UP:
            mob.to_edge(UP, buff=m + buff)
        elif direction == DOWN:
            mob.to_edge(DOWN, buff=m + buff)
        elif direction == LEFT:
            mob.to_edge(LEFT, buff=m + buff)
        elif direction == RIGHT:
            mob.to_edge(RIGHT, buff=m + buff)
        elif direction == UP + LEFT:
            mob.to_corner(UP + LEFT, buff=m + buff)
        elif direction == UP + RIGHT:
            mob.to_corner(UP + RIGHT, buff=m + buff)
        elif direction == DOWN + LEFT:
            mob.to_corner(DOWN + LEFT, buff=m + buff)
        elif direction == DOWN + RIGHT:
            mob.to_corner(DOWN + RIGHT, buff=m + buff)
        else:
            mob.to_edge(direction, buff=m + buff)

        return self.clamp(mob)

    def safe_title_hint(self, text, font_size=30, color=WHITE):
        """
        在标题常驻区下方显示提示文字（紧接标题 group 下方）。
        适用于演示过程中的阶段性提示。
        """
        t = Text(text, font_size=font_size, color=color, font=self.DEFAULT_FONT)
        if self._title_group is not None:
            t.next_to(self._title_group, DOWN, buff=0.35)
        else:
            t.move_to([0, self.content_top - 0.3, 0])
        return self.clamp(t)

    def safe_text(self, text, font_size=36, color=WHITE, **kw):
        """创建自动约束到安全区域的 Text。"""
        t = Text(text, font_size=font_size, color=color, font=self.DEFAULT_FONT, **kw)
        return t

    def safe_wrapped_text(
        self,
        text: str,
        *,
        font_size: int = 28,
        color=WHITE,
        max_width: float | None = None,
        line_buff: float = 0.28,
    ) -> VGroup:
        """
        按安全区宽度自动折行；文本中的 \\n 强制换行。
        返回多行 VGroup，每行水平居中排列。
        """
        if max_width is None:
            max_width = (self.safe_right - self.safe_left) - 1.2

        lines: list[str] = []
        for paragraph in text.split("\n"):
            if not paragraph:
                continue
            current = ""
            for ch in paragraph:
                probe = current + ch
                probe_w = Text(
                    probe, font_size=font_size, color=color, font=self.DEFAULT_FONT,
                ).width
                if probe_w > max_width and current:
                    lines.append(current)
                    current = ch
                else:
                    current = probe
            if current:
                lines.append(current)

        if not lines:
            return VGroup()

        line_mobs = [
            Text(line, font_size=font_size, color=color, font=self.DEFAULT_FONT)
            for line in lines
        ]
        group = VGroup(*line_mobs).arrange(DOWN, buff=line_buff)
        for mob in line_mobs:
            mob.move_to(np.array([0, mob.get_center()[1], 0]))
        group.move_to(ORIGIN)
        return group

    def safe_mathtex(self, tex, font_size=48, **kw):
        """创建 MathTex（不自动约束，因数学公式通常需要精确定位）。"""
        return MathTex(tex, font_size=font_size, **kw)

    def safe_subtitle(self, content, wait=3.5, font_size=28, color=WHITE):
        """
        底部安全字幕：淡入 - 停留 - 淡出。
        位置在安全区域底部上方。
        """
        sub = Text(content, font_size=font_size, color=color, font=self.DEFAULT_FONT)
        sub_y = self.safe_bottom + self.SUBTITLE_BOTTOM_OFFSET
        sub.move_to([0, sub_y, 0])
        self.clamp(sub)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.4)
        self.wait(wait)
        self.play(FadeOut(sub, shift=DOWN * 0.2), run_time=0.4)

    # ── 动画辅助 ───────────────────────────────────────────────

    def safe_add(self, *mobs):
        """添加到场景前自动约束到安全区域。"""
        for mob in mobs:
            self.clamp(mob)
        self.add(*mobs)

    def safe_play(self, *animations, **kwargs):
        """
        播放动画，结束后对产物 Mobject 做安全约束。
        仅对无动画状态的静态对象 clamp。
        """
        self.play(*animations, **kwargs)
        for anim in animations:
            mob = anim.mobject
            if mob is not None:
                self.clamp(mob)

    # ── 片头标题 ───────────────────────────────────────────────

    def show_title(self, title, subtitle=None, *,
                   title_color=YELLOW, subtitle_color=WHITE,
                   title_font_size=80, subtitle_font_size=52,
                   bgm=None, stay=2.0):
        """
        片头动画：标题 + 副标题 居中展示 → 缩移到左上角常驻（同行排列）。
        返回标题 VGroup，后续可通过 self._title_group 访问。
        """
        # 创建主标题
        title_text = Text(title, font_size=title_font_size, color=title_color, font=self.DEFAULT_FONT)

        # 创建副标题
        if subtitle is not None:
            subt = Text(subtitle, font_size=subtitle_font_size, color=subtitle_color, font=self.DEFAULT_FONT)
            subt.next_to(title_text, DOWN, buff=0.5)
            center_group = VGroup(title_text, subt)
        else:
            subt = None
            center_group = VGroup(title_text)

        # 居中时也要约束（极端字体大小情况）
        center_group.move_to(ORIGIN)
        self.fit_safe(center_group)

        # 淡入中央
        self.play(FadeIn(title_text, shift=UP * 0.3), run_time=1)
        if subt is not None:
            self.play(FadeIn(subt, shift=UP * 0.2), run_time=0.8)

        # 背景音乐
        if bgm is not None:
            self.add_sound(bgm)
            self.wait(1)

        # 中央停留
        self.wait(stay)

        # 缩移到左上角：主标题 + 副标题同一行，副标题略小
        corner_title_fs = 34
        corner_subtitle_fs = 28

        title_target = Text(
            title, font_size=corner_title_fs, color=title_color, font=self.DEFAULT_FONT,
        )
        if subt is not None:
            subt_target = Text(
                subtitle, font_size=corner_subtitle_fs, color=subtitle_color, font=self.DEFAULT_FONT,
            )
            row = VGroup(title_target, subt_target).arrange(RIGHT, buff=0.35)
        else:
            subt_target = None
            row = VGroup(title_target)

        row.to_corner(UP + LEFT, buff=0.35)
        row.align_to(np.array([self.safe_left + 0.3, 0, 0]), LEFT)
        row.align_to(np.array([0, self.safe_top - 0.25, 0]), UP)

        if subt is not None:
            self.play(
                Transform(title_text, title_target),
                Transform(subt, subt_target),
                run_time=1.2,
            )
        else:
            self.play(Transform(title_text, title_target), run_time=1.2)

        self.wait(1)

        result = VGroup(title_text)
        if subt is not None:
            result.add(subt)
        self._title_group = result
        return result

    # ── 片尾字幕 ───────────────────────────────────────────────

    def show_credits(self, credits="", *,
                     credit_color=TEAL_D,
                     author="@Sogrey",
                     author_color=TEAL_D):
        """
        片尾动画：显示结束语 → 署名 → 淡出。
        """
        self.clear()

        if not credits:
            credits = "THE END"

        credit_text = Text(credits, font_size=60, color=credit_color, font=self.DEFAULT_FONT)
        self.fit_safe(credit_text)

        author_text = Text(author, font_size=36, color=author_color, font=self.DEFAULT_FONT)
        self.fit_safe(author_text)

        self.play(FadeIn(credit_text, shift=DOWN, scale=0.66))
        self.wait(2)
        self.play(ReplacementTransform(credit_text, author_text))
        self.wait(2)
        self.play(FadeOut(author_text, shift=DOWN * 2, scale=1.5))

    # ── 一键编排 ───────────────────────────────────────────────

    def page(self, title, subtitle=None, body_fn=None, *,
             bgm=None, credits="", **title_kw):
        """一站式：show_title → body_fn → show_credits"""
        self.show_title(title, subtitle, bgm=bgm, **title_kw)
        if body_fn is not None:
            body_fn()
        self.wait(3)
        self.show_credits(credits)


# ═══════════════════════════════════════════════════════════════
#  独立函数版本（兼容不继承 SafeScene 的脚本）
# ═══════════════════════════════════════════════════════════════

def Title(self, title, subtitle=None, **kw):
    """兼容旧脚本的函数式调用，自动委托给 SafeScene.show_title。"""
    if isinstance(self, SafeScene):
        return self.show_title(title, subtitle, **kw)
    # fallback: 非 SafeScene 时按旧逻辑处理
    return _legacy_title(self, title, subtitle, **kw)

def Credits(self, credits="", **kw):
    if isinstance(self, SafeScene):
        return self.show_credits(credits, **kw)
    return _legacy_credits(self, credits, **kw)

def Subtitle(self, content, wait=3.5, **kw):
    if isinstance(self, SafeScene):
        return self.safe_subtitle(content, wait, **kw)
    return _legacy_subtitle(self, content, wait, **kw)


# ── legacy fallback（与原 titles_credits.py 兼容）───────────

def _legacy_title(self, title, subtitle=None, *,
                  font="Microsoft YaHei",
                  title_color=YELLOW, subtitle_color=WHITE,
                  title_font_size=80, subtitle_font_size=52,
                  bgm=None, stay=2.0):
    title_text = Text(title, font_size=title_font_size, color=title_color, font=font)
    if subtitle is not None:
        subt = Text(subtitle, font_size=subtitle_font_size, color=subtitle_color, font=font)
        subt.next_to(title_text, DOWN, buff=0.5)
        center_group = VGroup(title_text, subt)
    else:
        subt = None
        center_group = VGroup(title_text)
    center_group.move_to(ORIGIN)
    self.play(FadeIn(title_text, shift=UP * 0.3), run_time=1)
    if subt is not None:
        self.play(FadeIn(subt, shift=UP * 0.2), run_time=0.8)
    if bgm is not None:
        self.add_sound(bgm)
        self.wait(1)
    self.wait(stay)
    corner_title_fs = 34
    corner_subtitle_fs = 28
    title_target = Text(title, font_size=corner_title_fs, color=title_color, font=font)
    if subt is not None:
        subt_target = Text(subtitle, font_size=corner_subtitle_fs, color=subtitle_color, font=font)
        row = VGroup(title_target, subt_target).arrange(RIGHT, buff=0.35)
    else:
        subt_target = None
        row = VGroup(title_target)
    row.to_corner(UP + LEFT, buff=0.35)
    if subt is not None:
        self.play(Transform(title_text, title_target), Transform(subt, subt_target), run_time=1.2)
    else:
        self.play(Transform(title_text, title_target), run_time=1.2)
    self.wait(1)
    result = VGroup(title_text)
    if subt is not None:
        result.add(subt)
    return result

def _legacy_credits(self, credits="", *, font="Microsoft YaHei", credit_color=TEAL_D, author="@Sogrey", author_color=TEAL_D):
    self.clear()
    if not credits:
        credits = "THE END"
    credit_text = Text(credits, font_size=60, color=credit_color, font=font)
    author_text = Text(author, font_size=36, color=author_color, font=font)
    self.play(FadeIn(credit_text, shift=DOWN, scale=0.66))
    self.wait(2)
    self.play(ReplacementTransform(credit_text, author_text))
    self.wait(2)
    self.play(FadeOut(author_text, shift=DOWN * 2, scale=1.5))

def _legacy_subtitle(self, content, wait=3.5, *, font="Microsoft YaHei", font_size=28, color=WHITE):
    sub = Text(content, font_size=font_size, color=color, font=font)
    sub.move_to([0, -3.5, 0])
    self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.4)
    self.wait(wait)
    self.play(FadeOut(sub, shift=DOWN * 0.2), run_time=0.4)


# ═══════════════════════════════════════════════════════════════
#  测试场景
# ═══════════════════════════════════════════════════════════════

class SafeVideoTest(SafeScene):
    """运行: manim safe_video.py SafeVideoTest -pqm"""

    def construct(self):
        # 片头
        self.show_title("安全区域测试", subtitle="所有内容不超出画面")

        # 测试：大文字
        big = Text("这段文字很长很长很长很长", font_size=42, color=WHITE, font=self.DEFAULT_FONT)
        self.fit_content(big)
        big.move_to(self.content_center)
        self.play(FadeIn(big))
        self.wait(1)
        self.play(FadeOut(big))

        # 测试：提示文字
        hint = self.safe_title_hint("提示文字紧随标题下方")
        self.play(FadeIn(hint))
        self.wait(1)
        self.play(FadeOut(hint))

        # 测试：底部字幕
        self.safe_subtitle("底部安全字幕", wait=2)

        # 测试：大图形
        sq = Square(side_length=6, color=BLUE)
        self.fit_content(sq)
        sq.move_to(self.content_center)
        self.play(Create(sq))
        self.wait(1)
        self.play(FadeOut(sq))

        # 片尾
        self.show_credits("THE END")
