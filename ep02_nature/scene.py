"""
EP02 · 自然启蒙：变与不变 / 守恒
渲染：manim -pql ep02_nature/scene.py Nature
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from manim import (
    Scene, MoveAlongPath, GrowArrow, Flash, Indicate, Rotate,
    Circle, Square, Dot as MDot, Axes, ParametricFunction,
    NumberPlane, ValueTracker, always_redraw, DecimalNumber,
    RIGHT as R, LEFT as L, UP as U, DOWN as D,
    MathTex,
)

from theme import (
    Text, VGroup, Rectangle, RoundedRectangle, Line, Dot, Arrow,
    FadeIn, FadeOut, Write, Create, Transform, ReplacementTransform,
    AnimationGroup, UP, DOWN, LEFT, RIGHT, ORIGIN,
    C_BLUE, C_BLUE_DEEP, C_GREEN, C_YELLOW, C_ORANGE, C_RED, C_PURPLE,
    C_TEXT, C_TEXT_DIM, C_HIGHLIGHT,
    cn, cn_bold, bullet, highlight_box, footer, chapter_card, fade_in_up,
)


SERIES = "自然启蒙"
EPISODE = "EP02 · 守恒"


class Nature(Scene):
    def construct(self):
        self.add(footer(SERIES, EPISODE))
        self.cold_open()
        self.bouncing_ball_energy()
        self.conservation_list()
        self.entropy_and_life()
        self.e_equals_mc2()
        self.closing()

    # ---------- 0. Cold Open ----------
    def cold_open(self):
        lines = [
            "一只苹果从树上落下。",
            "一朵海浪拍上沙滩。",
            "一杯冰水慢慢变温。",
        ]
        for l in lines:
            t = cn(l, size=40, color=C_TEXT)
            self.play(fade_in_up(t), run_time=0.55)
            self.wait(0.8)
            self.play(FadeOut(t, shift=UP * 0.3), run_time=0.35)

        q1 = cn_bold("什么在变？", size=52, color=C_YELLOW)
        q2 = cn_bold("什么不变？", size=52, color=C_GREEN)
        q2.next_to(q1, DOWN, buff=0.4)
        grp = VGroup(q1, q2).move_to(ORIGIN)
        self.play(Write(q1))
        self.play(Write(q2))
        self.wait(1.3)
        self.play(FadeOut(grp))

    # ---------- 1. 小球自由落体 · 动能 + 势能 守恒 ----------
    def bouncing_ball_energy(self):
        chapter_card(self, "第一幕", "变与不变", "动能 + 势能 = 常数")

        # 左侧抛物轨迹
        ax = Axes(
            x_range=[0, 6, 1], y_range=[0, 3.2, 1],
            x_length=5.2, y_length=2.6,
            tips=False,
            axis_config={"stroke_color": C_TEXT_DIM},
        ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)

        ax_label = cn("小球抛物", size=22, color=C_TEXT_DIM).next_to(ax, UP, buff=0.1)
        self.play(Create(ax), Write(ax_label))

        # y(x) = 3 - 0.35*(x-3)^2   下落 + 反弹
        def y_of_x(x):
            return max(3 - 0.35 * (x - 3) ** 2, 0.0)

        path = ax.plot(y_of_x, x_range=[0, 6], color=C_BLUE_DEEP, stroke_width=2)
        self.play(Create(path), run_time=1.0)

        ball = Dot(color=C_BLUE, radius=0.12).move_to(ax.c2p(0, y_of_x(0)))
        self.play(FadeIn(ball, scale=0.5))

        # 右侧柱状：KE / PE / Total
        bars_origin = np.array([3.2, -0.6, 0])
        max_h = 2.6

        def make_bar(color, x_offset):
            return Rectangle(
                width=0.6, height=0.01,
                stroke_width=0, fill_color=color, fill_opacity=0.85,
            ).move_to(bars_origin + np.array([x_offset, max_h / 2, 0]),
                      aligned_edge=DOWN)

        ke_bar = make_bar(C_BLUE, 0.0)
        pe_bar = make_bar(C_ORANGE, 1.0)
        tot_bar = make_bar(C_GREEN, 2.0)

        # 标签
        ke_lbl = cn("KE", size=20, color=C_BLUE).next_to(ke_bar, DOWN, buff=0.15)
        pe_lbl = cn("PE", size=20, color=C_ORANGE).next_to(pe_bar, DOWN, buff=0.15)
        tot_lbl = cn("总能量", size=20, color=C_GREEN).next_to(tot_bar, DOWN, buff=0.15)

        self.play(
            *[FadeIn(m) for m in (ke_bar, pe_bar, tot_bar, ke_lbl, pe_lbl, tot_lbl)]
        )

        # 参数化：沿 path 移动小球，同时更新柱高
        tracker = ValueTracker(0.0)

        def get_energies(x):
            # 取归一化：KE = 1 - y/3 ， PE = y/3 ， Total = 1
            y = y_of_x(x)
            pe = y / 3.0
            ke = 1.0 - pe
            return ke, pe, 1.0

        def bar_updater(bar, idx, color):
            def upd(b):
                x = tracker.get_value()
                energies = get_energies(x)
                h = max(energies[idx], 0.01) * max_h
                new_bar = Rectangle(
                    width=0.6, height=h,
                    stroke_width=0, fill_color=color, fill_opacity=0.85,
                ).move_to(bars_origin + np.array([idx * 1.0, 0, 0]),
                          aligned_edge=DOWN)
                b.become(new_bar)
            return upd

        ke_bar.add_updater(bar_updater(ke_bar, 0, C_BLUE))
        pe_bar.add_updater(bar_updater(pe_bar, 1, C_ORANGE))
        tot_bar.add_updater(bar_updater(tot_bar, 2, C_GREEN))

        ball.add_updater(
            lambda m: m.move_to(ax.c2p(tracker.get_value(), y_of_x(tracker.get_value())))
        )

        # 在 Total 柱上画一条"不动的基准线"
        base_line = Line(
            bars_origin + np.array([1.65, max_h, 0]),
            bars_origin + np.array([2.35, max_h, 0]),
            color=C_YELLOW, stroke_width=4,
        )
        self.play(Create(base_line))

        self.play(tracker.animate.set_value(6.0), run_time=4.5)

        ke_bar.clear_updaters()
        pe_bar.clear_updaters()
        tot_bar.clear_updaters()
        ball.clear_updaters()

        # 结论句
        punch = cn_bold("KE + PE = 不变。", size=44, color=C_YELLOW).to_edge(DOWN, buff=0.5)
        self.play(fade_in_up(punch))
        self.play(Indicate(punch, color=C_YELLOW))
        self.wait(1.0)

        self.play(FadeOut(VGroup(
            ax, ax_label, path, ball,
            ke_bar, pe_bar, tot_bar, ke_lbl, pe_lbl, tot_lbl,
            base_line, punch,
        )))

    # ---------- 2. 四条守恒律 ----------
    def conservation_list(self):
        chapter_card(self, "第二幕", "守恒律", "物理学最硬的骨头")

        items = [
            ("能量守恒", "Energy", "时间平移对称", C_BLUE),
            ("动量守恒", "Momentum", "空间平移对称", C_GREEN),
            ("角动量守恒", "Angular", "空间旋转对称", C_ORANGE),
            ("电荷守恒", "Charge", "规范对称", C_PURPLE),
        ]
        cards = VGroup()
        for cn_name, en, sym, c in items:
            card = RoundedRectangle(
                corner_radius=0.15, width=3.1, height=2.0,
                stroke_color=c, stroke_width=2.5,
                fill_color=c, fill_opacity=0.08,
            )
            t_cn = cn_bold(cn_name, size=26, color=c)
            t_cn.move_to(card.get_top() + DOWN * 0.45)
            t_en = cn(en, size=20, color=C_TEXT_DIM).next_to(t_cn, DOWN, buff=0.15)
            t_sym = cn(sym, size=20, color=C_TEXT).next_to(t_en, DOWN, buff=0.25)
            cards.add(VGroup(card, t_cn, t_en, t_sym))

        cards.arrange(RIGHT, buff=0.4).move_to(ORIGIN)
        self.play(AnimationGroup(*[fade_in_up(c) for c in cards], lag_ratio=0.18))
        self.wait(0.8)

        # 诺特定理
        noether_label = cn_bold("诺 特 定 理", size=38, color=C_YELLOW)
        noether_sub = cn("对称性 ⇔ 守恒律", size=30, color=C_TEXT)
        group = VGroup(noether_label, noether_sub).arrange(DOWN, buff=0.3)
        group.to_edge(DOWN, buff=0.5)
        self.play(Write(noether_label))
        self.play(fade_in_up(noether_sub))
        self.play(Flash(noether_label, color=C_YELLOW, flash_radius=1.3))
        self.wait(1.1)

        self.play(FadeOut(VGroup(cards, group)))

    # ---------- 3. 熵与生命 ----------
    def entropy_and_life(self):
        chapter_card(self, "第三幕", "熵与生命", "局部秩序的代价")

        # 左：粒子盒 · 从聚集到扩散
        box = Square(side_length=3.0, color=C_TEXT_DIM,
                     stroke_width=2).to_edge(LEFT, buff=1.0)
        self.play(Create(box))

        rng = np.random.default_rng(7)
        n = 24
        start_pts = [
            box.get_corner(UP + LEFT) + np.array([
                rng.uniform(0.2, 0.8),
                -rng.uniform(0.2, 0.8),
                0,
            ]) for _ in range(n)
        ]
        dots = VGroup(*[Dot(p, radius=0.06, color=C_BLUE) for p in start_pts])
        self.play(FadeIn(dots, lag_ratio=0.05))
        self.wait(0.4)

        # 扩散到盒内均匀
        end_pts = [
            box.get_center() + np.array([
                rng.uniform(-1.35, 1.35),
                rng.uniform(-1.35, 1.35),
                0,
            ]) for _ in range(n)
        ]
        self.play(AnimationGroup(
            *[d.animate.move_to(p) for d, p in zip(dots, end_pts)],
            lag_ratio=0.02,
        ), run_time=2.5)

        # 右：熵曲线上升
        ax = Axes(
            x_range=[0, 10, 1], y_range=[0, 4, 1],
            x_length=4.8, y_length=2.6,
            tips=False,
            axis_config={"stroke_color": C_TEXT_DIM},
        ).to_edge(RIGHT, buff=0.8).shift(UP * 0.2)

        ax_title = cn("熵 S(t)", size=24, color=C_PURPLE).next_to(ax, UP, buff=0.1)
        self.play(Create(ax), Write(ax_title))
        curve = ax.plot(lambda x: 3.6 * (1 - np.exp(-x / 2.5)),
                        x_range=[0, 10], color=C_PURPLE)
        self.play(Create(curve), run_time=1.8)

        # 下方文字
        t1 = cn("封闭系统：熵只增不减（热力学第二定律）。",
                size=26, color=C_TEXT_DIM)
        t1.to_edge(DOWN, buff=0.9)
        self.play(fade_in_up(t1))
        self.wait(0.6)

        # 生命注解
        t2 = cn_bold("生命 = 局部反熵，把混乱推到体外。",
                     size=32, color=C_YELLOW).to_edge(DOWN, buff=0.35)
        self.play(fade_in_up(t2))
        self.play(Indicate(t2, color=C_YELLOW))
        self.wait(1.2)

        self.play(FadeOut(VGroup(box, dots, ax, ax_title, curve, t1, t2)))

    # ---------- 4. E = m c² ----------
    def e_equals_mc2(self):
        chapter_card(self, "第四幕", "质能等价", "E = m c²")

        # 左侧 m（方块）， 右侧 E（圆波纹），中间等号
        m_box = Square(side_length=1.6, color=C_BLUE, fill_opacity=0.2,
                       stroke_width=3).shift(LEFT * 3)
        m_lbl = cn_bold("m", size=44, color=C_BLUE).move_to(m_box)

        eq = cn_bold("=", size=56, color=C_TEXT)

        e_circle = Circle(radius=0.9, color=C_YELLOW, fill_opacity=0.2,
                          stroke_width=3).shift(RIGHT * 3)
        e_lbl = cn_bold("E", size=44, color=C_YELLOW).move_to(e_circle)

        self.play(FadeIn(m_box), Write(m_lbl))
        self.play(Write(eq))
        self.play(FadeIn(e_circle), Write(e_lbl))
        self.wait(0.5)

        formula = MathTex("E = m c^{2}", font_size=72, color=C_YELLOW).to_edge(DOWN, buff=1.2)
        self.play(Write(formula))
        self.play(Flash(formula, color=C_YELLOW, flash_radius=1.5))
        self.wait(0.6)

        punch = cn("质量与能量，本质同一物。", size=28, color=C_TEXT_DIM)
        punch.next_to(formula, DOWN, buff=0.35)
        self.play(fade_in_up(punch))
        self.wait(1.2)

        self.play(FadeOut(VGroup(m_box, m_lbl, eq, e_circle, e_lbl, formula, punch)))

    # ---------- 5. 回收 + 预告 ----------
    def closing(self):
        lines = [
            ("苹果下落", "动能 + 势能 = 常数", C_BLUE),
            ("海浪翻涌", "波能在动/势间周期互换", C_GREEN),
            ("冰水变温", "熵增 → 平衡态", C_PURPLE),
        ]
        rows = VGroup()
        for a, b, c in lines:
            ta = cn_bold(a, size=30, color=c)
            tb = cn(b, size=26, color=C_TEXT)
            tb.next_to(ta, RIGHT, buff=0.6)
            rows.add(VGroup(ta, tb))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN + UP * 0.5)
        for r in rows:
            self.play(fade_in_up(r), run_time=0.6)

        slogan = cn_bold("停止追着变化跑，转身去找那个不动的。",
                         size=36, color=C_YELLOW).to_edge(DOWN, buff=1.2)
        self.play(fade_in_up(slogan))
        self.wait(1.4)

        teaser = cn("下集预告 · 数学启蒙：描述不变的语言。",
                    size=26, color=C_BLUE).next_to(slogan, DOWN, buff=0.4)
        self.play(fade_in_up(teaser))
        self.wait(2.0)
        self.play(FadeOut(VGroup(rows, slogan, teaser)))
