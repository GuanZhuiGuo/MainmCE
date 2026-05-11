"""
MainmCE 统一视觉主题
====================

所有 scene.py 通过 `from theme import *` 共享一致的：
- 配色（深色背景 + 3Blue1Brown 风蓝/绿/黄/红）
- 字体（中文 CJK_FONT，英文/数学默认 LaTeX）
- 通用 Mobject：Title、Callout、Bullet
- 通用转场：fade_in_up、chapter_card

如果本机没有安装 `Source Han Sans CN`，把 CJK_FONT 改成
系统已有的中文字体（如 "PingFang SC"、"Microsoft YaHei"、"Noto Sans CJK SC"）。
"""

from __future__ import annotations

from manim import (
    config,
    Text,
    Tex,
    MathTex,
    VGroup,
    Rectangle,
    RoundedRectangle,
    Line,
    Dot,
    Arrow,
    FadeIn,
    FadeOut,
    Write,
    Create,
    Transform,
    ReplacementTransform,
    AnimationGroup,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    PI,
    WHITE,
    BLACK,
    GREY_A,
    GREY_B,
    GREY_D,
    GREY_E,
)

# ---------- 全局配置 ----------
config.background_color = "#0E1117"          # 接近 3b1b 的深蓝黑
config.frame_height = 8.0
config.frame_width = 14.22                   # 16:9 @ frame_height=8

# ---------- 字体 ----------
CJK_FONT = "Source Han Sans CN"              # 改成你机器上的中文字体

# ---------- 配色（向 3Blue1Brown 靠拢） ----------
C_BG         = "#0E1117"
C_TEXT       = "#E5E7EB"
C_TEXT_DIM   = "#9CA3AF"
C_BLUE       = "#58C4DD"
C_BLUE_DEEP  = "#1F6FEB"
C_GREEN      = "#83C167"
C_YELLOW     = "#FFD866"
C_ORANGE     = "#F59E0B"
C_RED        = "#FC6255"
C_PURPLE     = "#C792EA"
C_HIGHLIGHT  = "#FACC15"   # 黄色高亮底纹


# ---------- 便捷构造 ----------
def cn(text: str, size: int = 36, color: str = C_TEXT, weight: str = "NORMAL") -> Text:
    """中文文本快捷方式。"""
    return Text(text, font=CJK_FONT, font_size=size, color=color, weight=weight)


def cn_bold(text: str, size: int = 40, color: str = C_TEXT) -> Text:
    return cn(text, size=size, color=color, weight="BOLD")


def title(text: str, size: int = 56, color: str = C_BLUE) -> Text:
    """章节标题。"""
    return cn(text, size=size, color=color, weight="BOLD")


def bullet(text: str, size: int = 32, color: str = C_TEXT) -> VGroup:
    """带圆点的一条要点。"""
    dot = Dot(radius=0.08, color=C_BLUE).set_z_index(1)
    t = cn(text, size=size, color=color)
    t.next_to(dot, RIGHT, buff=0.3)
    return VGroup(dot, t)


def highlight_box(mobj, color: str = C_HIGHLIGHT, opacity: float = 0.25, pad: float = 0.12):
    """在 mobj 背后画一块黄色高亮底。"""
    box = RoundedRectangle(
        corner_radius=0.1,
        width=mobj.width + pad * 2,
        height=mobj.height + pad,
        stroke_width=0,
        fill_color=color,
        fill_opacity=opacity,
    ).move_to(mobj)
    return box


def footer(series: str, episode: str) -> VGroup:
    """右下角水印。"""
    s = cn(f"{series}  ·  {episode}", size=18, color=C_TEXT_DIM)
    s.to_corner(DOWN + RIGHT, buff=0.25)
    return s


def chapter_card(scene, number: str, cn_title: str, subtitle: str = ""):
    """章节封面卡片，用于小节切换。"""
    num = cn(number, size=30, color=C_TEXT_DIM)
    t = cn_bold(cn_title, size=64, color=C_BLUE)
    t.next_to(num, DOWN, buff=0.3)
    g = VGroup(num, t).move_to(ORIGIN)
    if subtitle:
        sub = cn(subtitle, size=28, color=C_TEXT_DIM)
        sub.next_to(t, DOWN, buff=0.45)
        g.add(sub)
    scene.play(FadeIn(num, shift=UP * 0.2))
    scene.play(Write(t))
    if subtitle:
        scene.play(FadeIn(sub, shift=UP * 0.2))
    scene.wait(1.2)
    scene.play(FadeOut(g))


def fade_in_up(mobj, shift: float = 0.4):
    """一个朝上的 FadeIn，常用于字幕/要点入场。"""
    return FadeIn(mobj, shift=UP * shift)


# ---------- 导出 ----------
__all__ = [
    "config",
    # manim 直通
    "Text", "Tex", "MathTex", "VGroup",
    "Rectangle", "RoundedRectangle", "Line", "Dot", "Arrow",
    "FadeIn", "FadeOut", "Write", "Create", "Transform",
    "ReplacementTransform", "AnimationGroup",
    "UP", "DOWN", "LEFT", "RIGHT", "ORIGIN", "PI",
    "WHITE", "BLACK", "GREY_A", "GREY_B", "GREY_D", "GREY_E",
    # 自定义
    "CJK_FONT",
    "C_BG", "C_TEXT", "C_TEXT_DIM",
    "C_BLUE", "C_BLUE_DEEP", "C_GREEN", "C_YELLOW",
    "C_ORANGE", "C_RED", "C_PURPLE", "C_HIGHLIGHT",
    "cn", "cn_bold", "title", "bullet", "highlight_box", "footer",
    "chapter_card", "fade_in_up",
]
