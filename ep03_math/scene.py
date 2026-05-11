"""
EP03 · 数学启蒙：数字 / 单位 / 关系 / 函数
渲染：manim -pql ep03_math/scene.py Mathematics
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from manim import (
    Scene, NumberLine, Axes, ValueTracker, always_redraw,
    Dot as MDot, Circle, Square, MathTex, Indicate, Flash,
    TangentLine, RIGHT as R, LEFT as L, UP as U, DOWN as D,
)

from theme import (
    Text, VGroup, Rectangle, RoundedRectangle, Line, Dot, Arrow,
    FadeIn, FadeOut, Write, Create, Transform, ReplacementTransform,
    AnimationGroup, UP, DOWN, LEFT, RIGHT, ORIGIN,
    C_BLUE, C_BLUE_DEEP, C_GREEN, C_YELLOW, C_ORANGE, C_RED, C_PURPLE,
    C_TEXT, C_TEXT_DIM, C_HIGHLIGHT,
    cn, cn_bold, bullet, highlight_box, footer, chapter_card, fade_in_up,
)


SERIES = "数学启蒙"
EPISODE = "EP03 · 描述世界的语言"


class Mathematics(Scene):
    def construct(self):
        self.add(footer(SERIES, EPISODE))
        self.cold_open()
        self.title_card()
        self.numbers_zoo()
        self.units_matter()
        self.equations()
        self.functions_and_derivatives()
        self.closing()

    # ---------- 0. Cold Open ----------
    def cold_open(self):
        lines = [
            "一块地的面积，可以用数学算。",
            "一段天气的变化，可以用数学算。",
            "一支股票的涨跌，可以用数学算。",
            "你心跳加速的那一下——也是一条曲线。",
        ]
        for l in lines:
            t = cn(l, size=36, color=C_TEXT)
            self.play(fade_in_up(t), run_time=0.55)
            self.wait(0.75)
            self.play(FadeOut(t, shift=UP * 0.3), run_time=0.35)

        hook = cn_bold("为什么一切现象，最后都落在数学上？",
                       size=44, color=C_YELLOW)
        self.play(Write(hook))
        self.wait(1.3)
        self.play(FadeOut(hook))

    # ---------- 1. Title Card ----------
    def title_card(self):
        big = cn_bold("数学启蒙", size=88, color=C_BLUE)
        sub = cn("描述世界的语言", size=34, color=C_TEXT_DIM)
        sub.next_to(big, DOWN, buff=0.35)
        head = VGroup(big, sub).move_to(ORIGIN + UP * 0.6)
        self.play(Write(big))
        self.play(fade_in_up(sub))

        steps = [("数字", C_YELLOW), ("单位", C_ORANGE),
                 ("关系", C_GREEN), ("函数", C_BLUE)]
        boxes = VGroup()
        arrows = VGroup()
        for s, c in steps:
            b = RoundedRectangle(corner_radius=0.15, width=2.3, height=1.1,
                                 stroke_color=c, stroke_width=2.5,
                                 fill_color=c, fill_opacity=0.1)
            lbl = cn_bold(s, size=32, color=c).move_to(b)
            boxes.add(VGroup(b, lbl))
        boxes.arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=0.9)

        for i in range(len(boxes) - 1):
            a = Arrow(boxes[i][0].get_right(), boxes[i + 1][0].get_left(),
                      buff=0.08, stroke_width=3, color=C_TEXT_DIM,
                      max_tip_length_to_length_ratio=0.15)
            arrows.add(a)

        self.play(AnimationGroup(*[fade_in_up(b) for b in boxes], lag_ratio=0.2))
        self.play(AnimationGroup(*[FadeIn(a) for a in arrows], lag_ratio=0.2))
        self.wait(1.0)
        self.play(FadeOut(VGroup(head, boxes, arrows)))

    # ---------- 2. 数字扩张 ----------
    def numbers_zoo(self):
        chapter_card(self, "第一步", "数字", "语言的第一批词汇")

        nl = NumberLine(
            x_range=[-4, 4, 1], length=10,
            include_numbers=True, include_tip=False,
            color=C_TEXT_DIM,
            label_direction=DOWN,
            font_size=22,
        ).move_to(ORIGIN)
        self.play(Create(nl))

        # 自然数 1,2,3
        nat = VGroup(*[Dot(nl.n2p(i), color=C_YELLOW, radius=0.08)
                       for i in [1, 2, 3]])
        nat_lbl = cn("自然数", size=24, color=C_YELLOW).next_to(nl, UP, buff=0.5).shift(RIGHT * 2)
        self.play(FadeIn(nat, lag_ratio=0.2), fade_in_up(nat_lbl))
        self.wait(0.5)

        # 0
        zero = Dot(nl.n2p(0), color=C_BLUE, radius=0.1)
        zero_lbl = cn("0 · 无", size=22, color=C_BLUE).next_to(zero, UP, buff=0.25)
        self.play(FadeIn(zero, scale=0.5), fade_in_up(zero_lbl))
        self.wait(0.4)

        # 负数
        negs = VGroup(*[Dot(nl.n2p(i), color=C_RED, radius=0.08)
                        for i in [-1, -2, -3]])
        neg_lbl = cn("负数", size=24, color=C_RED).next_to(nl, UP, buff=0.5).shift(LEFT * 2)
        self.play(FadeIn(negs, lag_ratio=0.2), fade_in_up(neg_lbl))
        self.wait(0.4)

        # 分数 1/2, 3/2
        frac_pts = VGroup(Dot(nl.n2p(0.5), color=C_GREEN, radius=0.06),
                          Dot(nl.n2p(1.5), color=C_GREEN, radius=0.06))
        frac_lbl = MathTex(r"\tfrac{1}{2},\ \tfrac{3}{2}",
                           color=C_GREEN, font_size=28).next_to(nl, DOWN, buff=0.7)
        self.play(FadeIn(frac_pts, lag_ratio=0.2), fade_in_up(frac_lbl))
        self.wait(0.3)

        # 无理数
        irr = Dot(nl.n2p(np.sqrt(2)), color=C_PURPLE, radius=0.08)
        irr_lbl = MathTex(r"\sqrt{2}", color=C_PURPLE,
                          font_size=34).next_to(irr, UP, buff=0.4)
        self.play(FadeIn(irr, scale=0.5), Write(irr_lbl))
        pi_dot = Dot(nl.n2p(np.pi), color=C_PURPLE, radius=0.08)
        pi_lbl = MathTex(r"\pi", color=C_PURPLE,
                         font_size=34).next_to(pi_dot, UP, buff=0.4)
        self.play(FadeIn(pi_dot, scale=0.5), Write(pi_lbl))
        self.wait(0.7)

        punch = cn_bold("每次扩张，都因为旧语言说不清新事实。",
                        size=32, color=C_YELLOW).to_edge(DOWN, buff=0.6)
        self.play(fade_in_up(punch))
        self.wait(1.2)

        self.play(FadeOut(VGroup(
            nl, nat, nat_lbl, zero, zero_lbl, negs, neg_lbl,
            frac_pts, frac_lbl, irr, irr_lbl, pi_dot, pi_lbl, punch,
        )))

    # ---------- 3. 单位 ----------
    def units_matter(self):
        chapter_card(self, "第二步", "单位", "把量放进同一张尺子")

        num = cn_bold("50", size=120, color=C_YELLOW).move_to(ORIGIN + UP * 0.2)
        q = cn("——什么 50？", size=30, color=C_TEXT_DIM).next_to(num, DOWN, buff=0.6)
        self.play(Write(num))
        self.play(fade_in_up(q))
        self.wait(0.8)

        variants = [
            ("50 米", C_BLUE, LEFT * 4 + DOWN * 0.6),
            ("50 秒", C_GREEN, LEFT * 1.3 + DOWN * 0.6),
            ("50 元", C_ORANGE, RIGHT * 1.3 + DOWN * 0.6),
            ("50 度", C_RED, RIGHT * 4 + DOWN * 0.6),
        ]
        chips = VGroup()
        for text, color, pos in variants:
            chip = RoundedRectangle(corner_radius=0.12, width=2.0, height=0.8,
                                    stroke_color=color, stroke_width=2,
                                    fill_color=color, fill_opacity=0.1).move_to(pos)
            lbl = cn_bold(text, size=28, color=color).move_to(chip)
            chips.add(VGroup(chip, lbl))

        self.play(AnimationGroup(*[fade_in_up(c) for c in chips], lag_ratio=0.15))
        self.wait(0.7)

        punch = cn_bold("单位不对，公式一定错。",
                        size=36, color=C_YELLOW).to_edge(DOWN, buff=0.5)
        self.play(fade_in_up(punch))
        self.play(Indicate(punch, color=C_YELLOW))
        self.wait(1.0)

        self.play(FadeOut(VGroup(num, q, chips, punch)))

    # ---------- 4. 关系 · 方程 ----------
    def equations(self):
        chapter_card(self, "第三步", "关系", "用等号把两件事绑起来")

        examples = [
            (r"\text{路程} = \text{速度} \times \text{时间}", C_BLUE),
            (r"F = m\,a", C_GREEN),
            (r"\text{利润} = \text{收入} - \text{成本}", C_ORANGE),
        ]
        eqs = VGroup(*[MathTex(e, color=c, font_size=40) for e, c in examples])
        eqs.arrange(DOWN, buff=0.6).to_edge(LEFT, buff=1.0)
        for e in eqs:
            self.play(Write(e), run_time=0.8)
        self.wait(0.5)

        # 右侧：y = k x + b 的几何
        ax = Axes(
            x_range=[-1, 5, 1], y_range=[-1, 5, 1],
            x_length=5, y_length=4,
            tips=False,
            axis_config={"stroke_color": C_TEXT_DIM},
        ).to_edge(RIGHT, buff=0.8)
        k_tracker = ValueTracker(1.2)
        b_tracker = ValueTracker(0.3)

        def line_func(x):
            return k_tracker.get_value() * x + b_tracker.get_value()

        line = always_redraw(
            lambda: ax.plot(line_func, x_range=[-1, 5], color=C_YELLOW)
        )
        eq_label = always_redraw(
            lambda: MathTex(
                f"y = {k_tracker.get_value():.1f}\\,x + {b_tracker.get_value():.1f}",
                color=C_YELLOW, font_size=34,
            ).next_to(ax, UP, buff=0.15)
        )
        self.play(Create(ax), Create(line), Write(eq_label))

        # 参数变动
        self.play(k_tracker.animate.set_value(0.4), run_time=1.4)
        self.play(b_tracker.animate.set_value(2.0), run_time=1.2)
        self.play(k_tracker.animate.set_value(1.8),
                  b_tracker.animate.set_value(-0.5), run_time=1.4)
        self.wait(0.6)

        punch = cn("世界第一层的规律，通常都是先用线性近似看清的。",
                   size=26, color=C_TEXT_DIM).to_edge(DOWN, buff=0.35)
        self.play(fade_in_up(punch))
        self.wait(1.0)

        self.play(FadeOut(VGroup(eqs, ax, line, eq_label, punch)))

    # ---------- 5. 函数与导数 ----------
    def functions_and_derivatives(self):
        chapter_card(self, "第四步", "函数 与 导数", "从静态关系到动态变化")

        ax = Axes(
            x_range=[-0.5, 4.5, 1], y_range=[-0.5, 5, 1],
            x_length=8, y_length=4.2,
            tips=False,
            axis_config={"stroke_color": C_TEXT_DIM},
        ).move_to(ORIGIN + DOWN * 0.3)
        self.play(Create(ax))

        def f(x):
            return 0.4 * x * x

        curve = ax.plot(f, x_range=[0, 4], color=C_BLUE)
        curve_label = MathTex("f(x) = 0.4 x^{2}",
                              color=C_BLUE, font_size=36).to_edge(UP, buff=0.7)
        self.play(Create(curve), Write(curve_label))
        self.wait(0.4)

        # 运动点 + 切线
        x_tracker = ValueTracker(0.2)

        point = always_redraw(
            lambda: Dot(ax.c2p(x_tracker.get_value(), f(x_tracker.get_value())),
                        color=C_YELLOW, radius=0.1)
        )
        tangent = always_redraw(
            lambda: TangentLine(curve, alpha=x_tracker.get_value() / 4,
                                length=3.2, color=C_YELLOW, stroke_width=3)
        )
        slope_label = always_redraw(
            lambda: MathTex(
                f"f'(x) = {0.8 * x_tracker.get_value():.2f}",
                color=C_YELLOW, font_size=32,
            ).to_corner(UP + RIGHT, buff=0.6)
        )
        self.play(FadeIn(point), Create(tangent), Write(slope_label))

        self.play(x_tracker.animate.set_value(3.5), run_time=3.5)
        self.wait(0.5)

        punch = cn_bold("导数 = 变化的速率。",
                        size=34, color=C_YELLOW).to_edge(DOWN, buff=0.3)
        self.play(fade_in_up(punch))
        self.play(Indicate(punch, color=C_YELLOW))
        self.wait(1.0)

        self.play(FadeOut(VGroup(
            ax, curve, curve_label, point, tangent, slope_label, punch,
        )))

    # ---------- 6. 收束 ----------
    def closing(self):
        lines = [
            ("面积", "= 积分", C_BLUE),
            ("天气", "= 函数 T(t)", C_GREEN),
            ("股票", "= 时间序列", C_ORANGE),
            ("心跳", "= 周期函数", C_RED),
        ]
        rows = VGroup()
        for a, b, c in lines:
            ta = cn_bold(a, size=30, color=c)
            tb = cn(b, size=26, color=C_TEXT)
            tb.next_to(ta, RIGHT, buff=0.5)
            rows.add(VGroup(ta, tb))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(ORIGIN + UP * 0.4)
        for r in rows:
            self.play(fade_in_up(r), run_time=0.55)

        slogan = cn_bold("数字 · 单位 · 关系 · 函数  →  搭起描述世界的梯子。",
                         size=30, color=C_YELLOW).to_edge(DOWN, buff=1.3)
        self.play(fade_in_up(slogan))
        self.wait(1.3)

        teaser = cn("下集预告 · 社会启蒙：个体如何凑出社会？",
                    size=26, color=C_BLUE).next_to(slogan, DOWN, buff=0.3)
        self.play(fade_in_up(teaser))
        self.wait(2.0)
        self.play(FadeOut(VGroup(rows, slogan, teaser)))
