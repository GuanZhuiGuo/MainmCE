"""
EP03 · 数学启蒙：数字 / 单位 / 关系 / 函数
渲染：manim -pql ep03_math/scene.py Mathematics
高清：manim -qh ep03_math/scene.py Mathematics

专业动画版：ThreeDScene + 3D 坐标 + 相机旋转 + 长时间导数/积分动画。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from manim import (
    ThreeDScene, MovingCameraScene,
    ThreeDAxes, Surface, Sphere,
    NumberLine, Axes, ParametricFunction,
    ValueTracker, always_redraw, DecimalNumber, TangentLine,
    MoveAlongPath, GrowArrow, Flash, Indicate, Circumscribe,
    Circle, Square, Dot as MDot,
    LaggedStart, LaggedStartMap, Succession,
    SpinInFromNothing, DrawBorderThenFill, ShrinkToCenter,
    ShowPassingFlash, TracedPath,
    MathTex, rate_functions,
    TAU, PI, DEGREES,
    RIGHT as R, LEFT as L, UP as U, DOWN as D,
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


class Mathematics(ThreeDScene):
    """主场景：3D 坐标系 + 导数切线 + 积分面积 + 相机旋转。"""

    def construct(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)
        self.cold_open()
        self.title_card()
        self.numbers_zoo()
        self.units_matter()
        self.equations_3d()
        self.functions_and_derivatives()
        self.closing()

    # ================================================================
    # 0. COLD OPEN（约 40 秒）
    # ================================================================
    def cold_open(self):
        lines = [
            "一块三角地的面积，可以用数学算。",
            "七天气温的走势，可以用数学算。",
            "一支股票的涨跌概率，可以用数学算。",
            "你心跳加速的那 0.3 秒——也是一条曲线。",
        ]

        for i, l in enumerate(lines):
            t = cn(l, size=36, color=C_TEXT)
            # 交替从左右入场
            direction = LEFT * 10 if i % 2 == 0 else RIGHT * 10
            t.move_to(direction)
            self.play(
                t.animate.move_to(ORIGIN),
                run_time=1.3,
                rate_func=rate_functions.ease_out_cubic,
            )
            self.wait(1.0)
            self.play(FadeOut(t, shift=UP * 0.4), run_time=0.5)

        hook = cn_bold("为什么一切现象，最终都落在数学上？",
                       size=44, color=C_YELLOW)
        self.play(Write(hook, run_time=2.0))
        self.wait(2.0)
        self.play(FadeOut(hook, shift=UP), run_time=1.0)

    # ================================================================
    # 1. TITLE CARD（约 25 秒）
    # ================================================================
    def title_card(self):
        big = cn_bold("数学启蒙", size=88, color=C_BLUE)
        sub = cn("描述世界的语言", size=34, color=C_TEXT_DIM)
        sub.next_to(big, DOWN, buff=0.4)
        head = VGroup(big, sub).move_to(ORIGIN + UP * 0.6)

        self.play(SpinInFromNothing(big, run_time=1.8))
        self.play(fade_in_up(sub, shift=0.5), run_time=1.0)

        # 四步路线图
        steps = [("数字", C_YELLOW), ("单位", C_ORANGE),
                 ("关系", C_GREEN), ("函数", C_BLUE)]
        boxes = VGroup()
        for s, c in steps:
            b = RoundedRectangle(corner_radius=0.15, width=2.3, height=1.1,
                                 stroke_color=c, stroke_width=2.5,
                                 fill_color=c, fill_opacity=0.1)
            lbl = cn_bold(s, size=30, color=c).move_to(b)
            boxes.add(VGroup(b, lbl))
        boxes.arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=1.0)

        step_arrows = VGroup()
        for i in range(len(boxes) - 1):
            a = Arrow(boxes[i][0].get_right(), boxes[i + 1][0].get_left(),
                      buff=0.08, stroke_width=3, color=C_TEXT_DIM,
                      max_tip_length_to_length_ratio=0.15)
            step_arrows.add(a)

        self.play(LaggedStart(*[DrawBorderThenFill(b) for b in boxes], lag_ratio=0.25), run_time=3.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in step_arrows], lag_ratio=0.25), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(VGroup(head, boxes, step_arrows), shift=UP), run_time=1.0)

    # ================================================================
    # 2. 数字（约 2 分钟）
    # ================================================================
    def numbers_zoo(self):
        chapter_card(self, "第一步", "数字", "语言的第一批词汇")

        # 数轴
        nl = NumberLine(
            x_range=[-5, 5, 1], length=12,
            include_numbers=True, include_tip=True,
            color=C_TEXT_DIM, font_size=20,
            label_direction=DOWN,
        ).move_to(ORIGIN)
        self.play(Create(nl, run_time=2.5))
        self.wait(0.5)

        # 自然数：逐个出现
        nat_colors = [C_YELLOW] * 5
        nat_dots = VGroup()
        for i in range(1, 6):
            d = Dot(nl.n2p(min(i, 4.8)), color=C_YELLOW, radius=0.1)
            nat_dots.add(d)
        nat_label = cn("自然数 ℕ", size=22, color=C_YELLOW).next_to(nl.n2p(3), UP, buff=0.5)

        self.play(LaggedStartMap(FadeIn, nat_dots, scale=0.3, lag_ratio=0.15), run_time=2.0)
        self.play(Write(nat_label, run_time=1.0))
        self.wait(1.0)

        # 零
        zero_dot = Dot(nl.n2p(0), color=C_BLUE, radius=0.13)
        zero_label = cn("0 · 空集", size=20, color=C_BLUE).next_to(zero_dot, UP, buff=0.3)
        self.play(FadeIn(zero_dot, scale=2.0, run_time=1.0), Write(zero_label, run_time=0.8))
        self.wait(0.8)

        # 负数
        neg_dots = VGroup(*[Dot(nl.n2p(-i), color=C_RED, radius=0.1) for i in range(1, 5)])
        neg_label = cn("负数 ℤ⁻", size=22, color=C_RED).next_to(nl.n2p(-3), UP, buff=0.5)
        self.play(LaggedStartMap(FadeIn, neg_dots, scale=0.3, lag_ratio=0.15), run_time=1.5)
        self.play(Write(neg_label, run_time=1.0))
        self.wait(0.8)

        # 分数
        frac_dots = VGroup(
            Dot(nl.n2p(0.5), color=C_GREEN, radius=0.07),
            Dot(nl.n2p(1.5), color=C_GREEN, radius=0.07),
            Dot(nl.n2p(-0.5), color=C_GREEN, radius=0.07),
        )
        frac_label = MathTex(r"\mathbb{Q}", color=C_GREEN, font_size=30).next_to(nl.n2p(0.5), DOWN, buff=0.6)
        self.play(FadeIn(frac_dots, lag_ratio=0.2, run_time=1.0), Write(frac_label))
        self.wait(0.8)

        # 无理数
        sqrt2_dot = Dot(nl.n2p(np.sqrt(2)), color=C_PURPLE, radius=0.1)
        sqrt2_label = MathTex(r"\sqrt{2}", color=C_PURPLE, font_size=32).next_to(sqrt2_dot, UP, buff=0.35)
        pi_dot = Dot(nl.n2p(np.pi), color=C_PURPLE, radius=0.1)
        pi_label = MathTex(r"\pi", color=C_PURPLE, font_size=32).next_to(pi_dot, UP, buff=0.35)

        self.play(
            FadeIn(sqrt2_dot, scale=2.0, run_time=1.0), Write(sqrt2_label),
            FadeIn(pi_dot, scale=2.0, run_time=1.0), Write(pi_label),
        )
        self.wait(1.5)

        # 结论
        punch = cn_bold("每次扩张 = 旧语言说不清新事实。",
                        size=30, color=C_YELLOW).to_edge(DOWN, buff=0.4)
        self.play(Write(punch, run_time=1.5))
        self.play(Indicate(punch, color=C_YELLOW, run_time=1.0))
        self.wait(2.0)

        self.play(FadeOut(VGroup(
            nl, nat_dots, nat_label, zero_dot, zero_label,
            neg_dots, neg_label, frac_dots, frac_label,
            sqrt2_dot, sqrt2_label, pi_dot, pi_label, punch,
        ), run_time=1.2))


    # ================================================================
    # 3. 单位（约 1.5 分钟）
    # ================================================================
    def units_matter(self):
        chapter_card(self, "第二步", "单位", "给数字一把尺")

        # 大 "50"
        num = cn_bold("50", size=140, color=C_YELLOW).move_to(ORIGIN + UP * 0.5)
        q = cn("—— 什么 50 ？", size=30, color=C_TEXT_DIM).next_to(num, DOWN, buff=0.6)
        self.play(Write(num, run_time=1.5))
        self.play(Write(q, run_time=1.0))
        self.wait(1.5)

        # 单位翻牌
        variants = [
            ("50 米", C_BLUE, LEFT * 4.5),
            ("50 秒", C_GREEN, LEFT * 1.5),
            ("50 元", C_ORANGE, RIGHT * 1.5),
            ("50 度", C_RED, RIGHT * 4.5),
        ]
        chips = VGroup()
        for text, color, pos in variants:
            chip = RoundedRectangle(
                corner_radius=0.12, width=2.2, height=0.9,
                stroke_color=color, stroke_width=2.5,
                fill_color=color, fill_opacity=0.12,
            ).move_to(pos + DOWN * 1.8)
            lbl = cn_bold(text, size=28, color=color).move_to(chip)
            chips.add(VGroup(chip, lbl))

        # 每个 chip 从数字"50"位置飞出
        for chip in chips:
            chip.save_state()
            chip.move_to(num).scale(0.3).set_opacity(0)

        self.play(
            LaggedStart(*[chip.animate.restore() for chip in chips], lag_ratio=0.2),
            run_time=3.0,
        )
        self.wait(1.5)

        # 量纲荒谬示例
        self.play(FadeOut(VGroup(num, q), run_time=0.8))

        wrong = MathTex(r"50\,\text{m} + 50\,\text{s} = \, ???",
                        color=C_RED, font_size=42).move_to(ORIGIN + UP * 1.5)
        self.play(Write(wrong, run_time=1.5))
        self.play(Flash(wrong, color=C_RED, flash_radius=1.5, run_time=0.8))
        self.wait(1.5)

        # 结论
        punch = cn_bold("单位不对，公式一定错。量纲分析是第一道防线。",
                        size=28, color=C_YELLOW).to_edge(DOWN, buff=0.4)
        self.play(Write(punch, run_time=1.5))
        self.play(Indicate(punch, color=C_YELLOW, run_time=1.0))
        self.wait(2.0)

        self.play(FadeOut(VGroup(chips, wrong, punch), run_time=1.0))

    # ================================================================
    # 4. 关系 · 3D 线性平面（约 2 分钟）
    # ================================================================
    def equations_3d(self):
        chapter_card(self, "第三步", "关系", "用等号绑住世界")

        # 先展示 2D 方程
        equations = [
            (r"s = v \cdot t", C_BLUE),
            (r"F = m \cdot a", C_GREEN),
            (r"\text{利润} = \text{收入} - \text{成本}", C_ORANGE),
        ]
        eq_group = VGroup(*[MathTex(e, color=c, font_size=38) for e, c in equations])
        eq_group.arrange(DOWN, buff=0.5).to_edge(LEFT, buff=1.0)

        for eq in eq_group:
            self.play(Write(eq, run_time=1.2))
            self.wait(0.6)
        self.wait(1.0)

        self.play(FadeOut(eq_group, shift=LEFT * 2), run_time=0.8)

        # 3D 展示：y = kx + b 变成一个平面 z = ax + by
        self.move_camera(phi=55 * DEGREES, theta=-50 * DEGREES, run_time=2.5)

        axes_3d = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-2, 4, 1],
            x_length=5, y_length=5, z_length=4,
            axis_config={"stroke_color": C_TEXT_DIM, "stroke_width": 1.5},
        )
        self.play(Create(axes_3d, run_time=2.0))

        # 线性平面 z = 0.5x + 0.8y + 0.5
        surface = Surface(
            lambda u, v: axes_3d.c2p(u, v, 0.5 * u + 0.8 * v + 0.5),
            u_range=[-2.5, 2.5], v_range=[-2.5, 2.5],
            resolution=(20, 20),
            fill_color=C_GREEN, fill_opacity=0.3,
            stroke_color=C_GREEN, stroke_width=0.5,
        )
        self.play(Create(surface, run_time=3.0))

        # 相机绕轴旋转展示 3D
        self.play(
            self.camera.animate.set_theta(-130 * DEGREES),
            run_time=4.0,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(1.0)

        # 平面上放一个点沿对角线运动
        tracker = ValueTracker(-2.0)
        moving_dot = always_redraw(
            lambda: Sphere(radius=0.1, resolution=(8, 8)).set_color(C_YELLOW).move_to(
                axes_3d.c2p(
                    tracker.get_value(),
                    tracker.get_value(),
                    0.5 * tracker.get_value() + 0.8 * tracker.get_value() + 0.5,
                )
            )
        )
        self.add(moving_dot)
        self.play(tracker.animate.set_value(2.0), run_time=3.0)
        self.wait(0.5)

        label_3d = cn_bold("线性关系 = 一个平面", size=26, color=C_GREEN)
        label_3d.to_edge(DOWN, buff=0.3)
        # Fix: need to go back to 2D briefly to show label
        self.move_camera(phi=0, theta=-PI / 2, run_time=1.5)
        self.play(Write(label_3d, run_time=1.2))
        self.wait(2.0)

        self.play(FadeOut(VGroup(axes_3d, surface, moving_dot, label_3d), run_time=1.0))


    # ================================================================
    # 5. 函数 & 导数 & 积分（约 3 分钟 — 重头戏）
    # ================================================================
    def functions_and_derivatives(self):
        chapter_card(self, "第四步", "函数与导数", "从静态关系到动态变化")

        # 2D Axes
        ax = Axes(
            x_range=[-0.5, 5, 1], y_range=[-0.5, 6, 1],
            x_length=9, y_length=5,
            tips=True,
            axis_config={"stroke_color": C_TEXT_DIM},
        ).move_to(ORIGIN + DOWN * 0.2)

        x_label = ax.get_x_axis_label("x", direction=DOWN)
        y_label = ax.get_y_axis_label("f(x)", direction=LEFT)
        self.play(Create(ax, run_time=2.0), Write(x_label), Write(y_label))

        # 曲线 f(x) = 0.3x² + 0.2sin(2x)
        def f(x):
            return 0.3 * x ** 2 + 0.2 * np.sin(2 * x)

        curve = ax.plot(f, x_range=[0, 4.8], color=C_BLUE, stroke_width=3)
        curve_label = MathTex(r"f(x) = 0.3x^2 + 0.2\sin(2x)",
                              color=C_BLUE, font_size=30).to_corner(UP + LEFT, buff=0.5)

        # 缓慢描画曲线
        self.play(Create(curve, run_time=3.5, rate_func=rate_functions.linear))
        self.play(Write(curve_label, run_time=1.2))
        self.wait(1.0)

        # --- 导数：切线随动 ---
        x_tracker = ValueTracker(0.3)

        # 运动点
        moving_dot = always_redraw(
            lambda: Dot(
                ax.c2p(x_tracker.get_value(), f(x_tracker.get_value())),
                color=C_YELLOW, radius=0.1,
            )
        )

        # 切线
        def get_tangent():
            x = x_tracker.get_value()
            # 数值导数
            h = 0.001
            slope = (f(x + h) - f(x - h)) / (2 * h)
            # 切线长度
            dx = 1.5
            x1, x2 = x - dx, x + dx
            y1 = f(x) + slope * (x1 - x)
            y2 = f(x) + slope * (x2 - x)
            return Line(
                ax.c2p(x1, y1), ax.c2p(x2, y2),
                color=C_YELLOW, stroke_width=3,
            )

        tangent = always_redraw(get_tangent)

        # 斜率数字
        slope_display = always_redraw(
            lambda: MathTex(
                f"f'(x) = {(f(x_tracker.get_value() + 0.001) - f(x_tracker.get_value() - 0.001)) / 0.002:.2f}",
                color=C_YELLOW, font_size=28,
            ).to_corner(UP + RIGHT, buff=0.5)
        )

        self.play(FadeIn(moving_dot), Create(tangent), Write(slope_display))
        self.wait(0.5)

        # 慢速移动 — 让观众看清切线旋转
        self.play(
            x_tracker.animate.set_value(4.5),
            run_time=8.0,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(1.5)

        # 导数为零的点
        # f'(x) = 0.6x + 0.4cos(2x) ≈ 0 at x ≈ 0 (近似)
        self.play(x_tracker.animate.set_value(0.0), run_time=2.0)
        zero_note = cn("导数 ≈ 0 → 极值点", size=22, color=C_TEXT_DIM)
        zero_note.next_to(moving_dot, DOWN, buff=0.5)
        self.play(Write(zero_note, run_time=1.0))
        self.play(Flash(moving_dot, color=C_YELLOW, run_time=0.8))
        self.wait(1.5)
        self.play(FadeOut(zero_note))

        # --- 积分：面积填充 ---
        self.play(x_tracker.animate.set_value(0.3), run_time=1.0)

        # 移除切线显示
        self.play(FadeOut(VGroup(tangent, slope_display, moving_dot)), run_time=0.8)

        # 积分面积（从 0 到 x，逐步填充）
        fill_tracker = ValueTracker(0.1)

        def get_area():
            return ax.get_area(
                curve,
                x_range=[0, fill_tracker.get_value()],
                color=C_BLUE,
                opacity=0.3,
            )

        area = always_redraw(get_area)
        self.add(area)

        # 积分公式
        integral_label = MathTex(
            r"\int_0^x f(t)\,dt",
            color=C_BLUE, font_size=36,
        ).to_corner(UP + RIGHT, buff=0.5)
        self.play(Write(integral_label, run_time=1.2))

        # 面积值
        area_value = always_redraw(
            lambda: DecimalNumber(
                # 近似积分 ∫0→x 0.3t² dt = 0.1x³
                0.1 * fill_tracker.get_value() ** 3,
                num_decimal_places=2,
                color=C_BLUE,
                font_size=28,
            ).next_to(integral_label, DOWN, buff=0.3)
        )
        self.add(area_value)

        # 缓慢填充面积
        self.play(
            fill_tracker.animate.set_value(4.5),
            run_time=6.0,
            rate_func=rate_functions.linear,
        )
        self.wait(1.5)

        # 结论
        punch1 = cn_bold("导数 = 变化的速率。", size=32, color=C_YELLOW)
        punch2 = cn_bold("积分 = 变化的累积。", size=32, color=C_BLUE)
        punch2.next_to(punch1, DOWN, buff=0.3)
        pgroup = VGroup(punch1, punch2).to_edge(DOWN, buff=0.3)

        self.play(Write(punch1, run_time=1.5))
        self.play(Write(punch2, run_time=1.5))
        self.play(
            Indicate(punch1, color=C_YELLOW, run_time=0.8),
            Indicate(punch2, color=C_BLUE, run_time=0.8),
        )
        self.wait(2.5)

        # 3D 展示：把曲线拉到 3D 空间旋转一圈
        self.play(FadeOut(VGroup(
            ax, x_label, y_label, curve, curve_label,
            area, integral_label, area_value, pgroup,
        ), run_time=1.0))

        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, run_time=2.0)

        axes_3d = ThreeDAxes(
            x_range=[0, 5, 1], y_range=[-3, 3, 1], z_range=[0, 6, 1],
            x_length=5, y_length=4, z_length=4,
            axis_config={"stroke_color": C_TEXT_DIM, "stroke_width": 1.5},
        )
        self.play(Create(axes_3d, run_time=1.5))

        # 旋转体：f(x) 绕 x 轴旋转
        revolution_surface = Surface(
            lambda u, v: axes_3d.c2p(
                u,
                f(u) * np.cos(v),
                f(u) * np.sin(v),
            ),
            u_range=[0.1, 4], v_range=[0, TAU],
            resolution=(30, 30),
            fill_color=C_BLUE, fill_opacity=0.25,
            stroke_color=C_BLUE, stroke_width=0.3,
        )
        self.play(Create(revolution_surface, run_time=4.0))

        # 相机旋转 360°
        self.play(
            self.camera.animate.set_theta(-45 * DEGREES + TAU),
            run_time=6.0,
            rate_func=rate_functions.linear,
        )
        self.wait(1.0)

        vol_label = cn_bold("积分 → 旋转体体积", size=26, color=C_BLUE)
        vol_label.to_edge(DOWN, buff=0.3)
        self.move_camera(phi=0, theta=-PI / 2, run_time=1.5)
        self.play(Write(vol_label, run_time=1.2))
        self.wait(2.0)

        self.play(FadeOut(VGroup(axes_3d, revolution_surface, vol_label), run_time=1.2))

    # ================================================================
    # 6. 收束（约 1 分钟）
    # ================================================================
    def closing(self):
        lines = [
            ("面积", "= 积分", C_BLUE),
            ("气温", "= 函数 T(t)", C_GREEN),
            ("股票", "= 随机过程", C_ORANGE),
            ("心跳", "= 周期函数", C_RED),
        ]
        rows = VGroup()
        for a, b, c in lines:
            ta = cn_bold(a, size=32, color=c)
            arrow = Arrow(ORIGIN, RIGHT * 0.8, stroke_width=3, color=c,
                          max_tip_length_to_length_ratio=0.15)
            arrow.next_to(ta, RIGHT, buff=0.3)
            tb = cn(b, size=26, color=C_TEXT).next_to(arrow, RIGHT, buff=0.3)
            rows.add(VGroup(ta, arrow, tb))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN + UP * 0.5)

        for r in rows:
            self.play(
                LaggedStart(
                    Write(r[0], run_time=0.8),
                    GrowArrow(r[1], run_time=0.5),
                    Write(r[2], run_time=0.8),
                    lag_ratio=0.2,
                ),
                run_time=1.5,
            )
            self.wait(0.6)

        self.wait(1.5)

        slogan = cn_bold("数字 · 单位 · 关系 · 函数 → 描述世界的梯子。",
                         size=30, color=C_YELLOW).to_edge(DOWN, buff=1.0)
        self.play(Write(slogan, run_time=2.0))
        self.play(Indicate(slogan, color=C_YELLOW, run_time=1.0))
        self.wait(2.0)

        teaser = cn("下集 · 社会启蒙：个体如何凑出社会？",
                    size=26, color=C_BLUE).next_to(slogan, DOWN, buff=0.4)
        self.play(fade_in_up(teaser), run_time=1.2)
        self.wait(3.0)

        self.play(FadeOut(VGroup(rows, slogan, teaser), run_time=2.0))
        self.wait(1.0)
