"""
EP02 · 自然启蒙：变与不变 / 守恒
渲染：manim -pql ep02_nature/scene.py Nature
高清：manim -qh ep02_nature/scene.py Nature

专业动画版：ThreeDScene + 相机旋转 + 长时间动画 + 丰富过渡。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from manim import (
    ThreeDScene, MovingCameraScene,
    ThreeDAxes, Surface, Sphere,
    MoveAlongPath, GrowArrow, Flash, Indicate, Circumscribe,
    Circle, Square, Dot as MDot, Axes, ParametricFunction,
    ValueTracker, always_redraw, DecimalNumber,
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


SERIES = "自然启蒙"
EPISODE = "EP02 · 守恒"


class Nature(ThreeDScene):
    """主场景：3D + 2D 混合，相机旋转，约 8-10 分钟渲染。"""

    def construct(self):
        # 先以 2D 视角开始
        self.set_camera_orientation(phi=0, theta=-PI / 2)
        self.cold_open()
        self.bouncing_ball_energy()
        self.conservation_list()
        self.entropy_and_life()
        self.e_equals_mc2()
        self.closing()

    # ================================================================
    # 0. COLD OPEN（约 45 秒）
    # ================================================================
    def cold_open(self):
        lines = [
            "一只苹果从枝头落下。",
            "一道海浪从远处涌来、拍碎。",
            "一杯冰水慢慢变成室温。",
        ]

        for i, l in enumerate(lines):
            t = cn(l, size=40, color=C_TEXT)
            # 从不同方向滑入
            start_positions = [LEFT * 10, RIGHT * 10, UP * 6]
            t.move_to(start_positions[i])
            self.play(
                t.animate.move_to(ORIGIN),
                run_time=1.5,
                rate_func=rate_functions.ease_out_back,
            )
            self.wait(1.2)
            self.play(FadeOut(t, shift=DOWN * 0.5), run_time=0.6)

        # 核心问句
        q1 = cn_bold("什么在变？", size=56, color=C_YELLOW)
        q2 = cn_bold("什么不变？", size=56, color=C_GREEN)
        q2.next_to(q1, DOWN, buff=0.5)
        grp = VGroup(q1, q2).move_to(ORIGIN)

        self.play(Write(q1, run_time=1.5))
        self.play(Write(q2, run_time=1.5))
        self.wait(2.0)

        # 答案浮现
        ans = cn_bold("守 恒", size=80, color=C_YELLOW)
        ans.move_to(ORIGIN)
        self.play(
            ReplacementTransform(grp, ans),
            run_time=2.0,
        )
        self.play(Flash(ans, color=C_YELLOW, flash_radius=2.0, run_time=1.0))
        self.wait(1.5)
        self.play(FadeOut(ans, shift=UP), run_time=1.0)

    # ================================================================
    # 1. 机械能守恒 · 3D 小球弹跳（约 2.5 分钟）
    # ================================================================
    def bouncing_ball_energy(self):
        chapter_card(self, "第一幕", "机械能守恒", "动能 + 势能 = 常数")

        # 切换到 3D 视角
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, run_time=2.0)

        # 3D 坐标轴
        axes_3d = ThreeDAxes(
            x_range=[-1, 8, 1], y_range=[-1, 5, 1], z_range=[-1, 4, 1],
            x_length=7, y_length=4, z_length=3,
            axis_config={"stroke_color": C_TEXT_DIM, "stroke_width": 1.5},
        )
        self.play(Create(axes_3d, run_time=2.0))

        # 小球抛物轨迹（3D 中展示）
        def ball_path(t):
            x = t
            y = 4 - 0.12 * (t - 4) ** 2  # 抛物线
            z = 0.3 * np.sin(t * 0.8)     # 轻微 z 摆动增加 3D 感
            return axes_3d.c2p(x, max(y, 0), z)

        path_curve = ParametricFunction(
            ball_path, t_range=[0, 8],
            color=C_BLUE_DEEP, stroke_width=2,
        )
        self.play(Create(path_curve, run_time=2.5))

        # 小球
        ball = Sphere(radius=0.15, resolution=(16, 16))
        ball.set_color(C_BLUE)
        ball.move_to(ball_path(0))
        self.play(FadeIn(ball, scale=0.5, run_time=0.8))

        # 沿路径运动 + 相机跟踪
        tracker = ValueTracker(0)
        ball.add_updater(lambda m: m.move_to(ball_path(tracker.get_value())))

        # 相机缓慢旋转
        self.play(
            tracker.animate.set_value(8),
            self.camera.animate.set_theta(-90 * DEGREES),
            run_time=6.0,
            rate_func=rate_functions.ease_in_out_sine,
        )
        ball.clear_updaters()
        self.wait(1.0)

        # 回到 2D 展示能量柱
        self.play(
            FadeOut(VGroup(axes_3d, path_curve, ball), run_time=1.0),
        )
        self.move_camera(phi=0, theta=-PI / 2, run_time=1.5)

        # 2D 能量守恒演示
        ax = Axes(
            x_range=[0, 8, 1], y_range=[0, 4, 1],
            x_length=6, y_length=3,
            tips=False,
            axis_config={"stroke_color": C_TEXT_DIM},
        ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)

        def y_of_t(t):
            return max(4 - 0.12 * (t - 4) ** 2, 0)

        path_2d = ax.plot(y_of_t, x_range=[0, 8], color=C_BLUE, stroke_width=3)
        ball_2d = Dot(color=C_BLUE, radius=0.12).move_to(ax.c2p(0, y_of_t(0)))

        self.play(Create(ax, run_time=1.5), Create(path_2d, run_time=2.0))
        self.play(FadeIn(ball_2d, scale=0.5))

        # 右侧柱状图
        bar_origin = np.array([3.5, -1.5, 0])
        max_h = 2.8

        ke_label = cn("KE", size=20, color=C_BLUE)
        pe_label = cn("PE", size=20, color=C_ORANGE)
        tot_label = cn("总能量", size=20, color=C_GREEN)

        labels = VGroup(ke_label, pe_label, tot_label)
        labels.arrange(RIGHT, buff=1.5).move_to(bar_origin + DOWN * 0.3)
        self.play(FadeIn(labels))

        tracker2 = ValueTracker(0)

        def make_bars():
            t = tracker2.get_value()
            y = y_of_t(t)
            pe_ratio = y / 4.0
            ke_ratio = 1.0 - pe_ratio

            ke_bar = Rectangle(
                width=0.6, height=max(ke_ratio * max_h, 0.01),
                fill_color=C_BLUE, fill_opacity=0.8, stroke_width=0,
            ).move_to(bar_origin + LEFT * 1.5 + UP * ke_ratio * max_h / 2)

            pe_bar = Rectangle(
                width=0.6, height=max(pe_ratio * max_h, 0.01),
                fill_color=C_ORANGE, fill_opacity=0.8, stroke_width=0,
            ).move_to(bar_origin + UP * pe_ratio * max_h / 2)

            tot_bar = Rectangle(
                width=0.6, height=max_h,
                fill_color=C_GREEN, fill_opacity=0.8, stroke_width=0,
            ).move_to(bar_origin + RIGHT * 1.5 + UP * max_h / 2)

            return VGroup(ke_bar, pe_bar, tot_bar)

        bars = always_redraw(make_bars)
        self.add(bars)

        # 基准线
        base_line = Line(
            bar_origin + RIGHT * 0.9 + UP * max_h,
            bar_origin + RIGHT * 2.1 + UP * max_h,
            color=C_YELLOW, stroke_width=4,
        )
        bl_label = cn("不变!", size=18, color=C_YELLOW).next_to(base_line, RIGHT, buff=0.1)
        self.play(Create(base_line), Write(bl_label))

        ball_2d.add_updater(
            lambda m: m.move_to(ax.c2p(tracker2.get_value(), y_of_t(tracker2.get_value())))
        )

        # 缓慢运动，让观众看清柱的变化
        self.play(tracker2.animate.set_value(8), run_time=8.0,
                  rate_func=rate_functions.ease_in_out_sine)
        ball_2d.clear_updaters()
        self.wait(1.0)

        # 结论
        punch = cn_bold("KE + PE = 常数。不变。", size=42, color=C_YELLOW)
        punch.to_edge(DOWN, buff=0.4)
        self.play(Write(punch, run_time=1.5))
        self.play(Circumscribe(punch, color=C_YELLOW, run_time=1.5))
        self.wait(2.0)

        self.play(FadeOut(VGroup(ax, path_2d, ball_2d, bars, labels,
                                  base_line, bl_label, punch), run_time=1.2))


    # ================================================================
    # 2. 四条守恒律 + 诺特定理（约 2 分钟）
    # ================================================================
    def conservation_list(self):
        chapter_card(self, "第二幕", "守恒律", "物理学最硬的骨头")

        items = [
            ("能量守恒", "时间平移对称", C_BLUE),
            ("动量守恒", "空间平移对称", C_GREEN),
            ("角动量守恒", "空间旋转对称", C_ORANGE),
            ("电荷守恒", "规范对称", C_PURPLE),
        ]

        cards = VGroup()
        for cn_name, sym, c in items:
            card = RoundedRectangle(
                corner_radius=0.15, width=3.0, height=2.2,
                stroke_color=c, stroke_width=2.5,
                fill_color=c, fill_opacity=0.08,
            )
            t_cn = cn_bold(cn_name, size=24, color=c)
            t_cn.move_to(card.get_top() + DOWN * 0.5)
            divider = Line(
                card.get_left() + RIGHT * 0.3 + DOWN * 0.2,
                card.get_right() + LEFT * 0.3 + DOWN * 0.2,
                stroke_color=c, stroke_width=1, stroke_opacity=0.4,
            )
            t_sym = cn(sym, size=18, color=C_TEXT_DIM).move_to(card.get_bottom() + UP * 0.6)
            cards.add(VGroup(card, t_cn, divider, t_sym))

        cards.arrange(RIGHT, buff=0.35).move_to(ORIGIN + UP * 0.5)

        # 卡片逐张旋入
        for card in cards:
            self.play(SpinInFromNothing(card, run_time=1.2))
            self.wait(0.5)

        self.wait(1.0)

        # 连接线：对称 ↔ 守恒
        connector_label = cn_bold("诺 特 定 理", size=42, color=C_YELLOW)
        connector_sub = cn("对称性 ⇔ 守恒律", size=28, color=C_TEXT)
        connector_sub2 = cn("— Emmy Noether, 1918", size=20, color=C_TEXT_DIM)
        connector = VGroup(connector_label, connector_sub, connector_sub2)
        connector.arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)

        self.play(Write(connector_label, run_time=1.5))
        self.play(Write(connector_sub, run_time=1.2))
        self.play(fade_in_up(connector_sub2), run_time=0.8)
        self.play(Flash(connector_label, color=C_YELLOW, flash_radius=1.8, run_time=1.0))
        self.wait(2.5)

        # 3D 旋转展示对称性
        self.play(FadeOut(VGroup(cards, connector), run_time=1.0))

        # 短暂 3D 展示：旋转对称 → 角动量
        self.move_camera(phi=50 * DEGREES, theta=-60 * DEGREES, run_time=2.0)

        ring = Circle(radius=1.5, color=C_ORANGE, stroke_width=4)
        ring.rotate(PI / 6, axis=RIGHT)
        dot_on_ring = Dot(ring.point_from_proportion(0), color=C_YELLOW, radius=0.12)
        trace = TracedPath(dot_on_ring.get_center, stroke_color=C_YELLOW, stroke_width=2)

        self.play(Create(ring, run_time=1.5))
        self.add(trace)
        self.play(
            MoveAlongPath(dot_on_ring, ring, run_time=4.0, rate_func=rate_functions.linear),
            self.camera.animate.set_theta(-120 * DEGREES),
        )
        self.remove(trace)

        ang_label = cn_bold("旋转对称 → 角动量守恒", size=28, color=C_ORANGE)
        ang_label.to_edge(DOWN, buff=0.5)
        # Move back to 2D to show label
        self.move_camera(phi=0, theta=-PI / 2, run_time=1.5)
        self.play(Write(ang_label, run_time=1.2))
        self.wait(2.0)

        self.play(FadeOut(VGroup(ring, dot_on_ring, ang_label), run_time=1.0))

    # ================================================================
    # 3. 熵与生命（约 2 分钟）
    # ================================================================
    def entropy_and_life(self):
        chapter_card(self, "第三幕", "熵与生命", "局部秩序的代价")

        # 粒子盒：从聚集到扩散
        box = Square(side_length=3.5, color=C_TEXT_DIM, stroke_width=2).to_edge(LEFT, buff=0.8)
        self.play(Create(box, run_time=1.2))

        rng = np.random.default_rng(7)
        n = 30
        start_pts = [
            box.get_corner(UP + LEFT) + np.array([
                rng.uniform(0.2, 0.9),
                -rng.uniform(0.2, 0.9),
                0,
            ]) for _ in range(n)
        ]
        dots = VGroup(*[Dot(p, radius=0.06, color=C_BLUE) for p in start_pts])
        self.play(LaggedStartMap(FadeIn, dots, scale=0.3, lag_ratio=0.03), run_time=1.5)
        self.wait(1.0)

        # 扩散动画 — 分两步（更有戏剧性）
        mid_pts = [
            box.get_center() + np.array([
                rng.uniform(-1.0, 1.0),
                rng.uniform(-0.5, 0.5),
                0,
            ]) for _ in range(n)
        ]
        end_pts = [
            box.get_center() + np.array([
                rng.uniform(-1.6, 1.6),
                rng.uniform(-1.6, 1.6),
                0,
            ]) for _ in range(n)
        ]

        self.play(
            AnimationGroup(*[d.animate.move_to(p) for d, p in zip(dots, mid_pts)], lag_ratio=0.02),
            run_time=2.0,
        )
        self.play(
            AnimationGroup(*[d.animate.move_to(p).set_color(C_PURPLE) for d, p in zip(dots, end_pts)], lag_ratio=0.02),
            run_time=2.5,
        )

        # 右侧熵曲线
        ax = Axes(
            x_range=[0, 12, 2], y_range=[0, 4.5, 1],
            x_length=5.5, y_length=3.0,
            tips=False,
            axis_config={"stroke_color": C_TEXT_DIM},
        ).to_edge(RIGHT, buff=0.7).shift(UP * 0.3)

        ax_title = cn("熵 S(t)", size=24, color=C_PURPLE).next_to(ax, UP, buff=0.1)
        self.play(Create(ax, run_time=1.5), Write(ax_title, run_time=1.0))

        entropy_curve = ax.plot(
            lambda x: 4.0 * (1 - np.exp(-x / 3.0)),
            x_range=[0, 12], color=C_PURPLE, stroke_width=3,
        )
        # 描画曲线（慢速，让观众看到上升过程）
        self.play(Create(entropy_curve, run_time=4.0, rate_func=rate_functions.linear))
        self.wait(1.0)

        # 第二定律文字
        law = cn("热力学第二定律：封闭系统，熵只增不减。",
                 size=24, color=C_TEXT_DIM).to_edge(DOWN, buff=1.2)
        self.play(Write(law, run_time=1.5))
        self.wait(1.5)

        # 生命 = 反熵
        life_text = cn_bold("生命 = 局部反熵。代价：把混乱推到体外。",
                            size=30, color=C_YELLOW).to_edge(DOWN, buff=0.4)
        self.play(
            ReplacementTransform(law, life_text),
            run_time=1.5,
        )
        self.play(Indicate(life_text, color=C_YELLOW, run_time=1.2))
        self.wait(2.5)

        self.play(FadeOut(VGroup(box, dots, ax, ax_title, entropy_curve, life_text), run_time=1.2))

    # ================================================================
    # 4. E = mc²（约 1.5 分钟）
    # ================================================================
    def e_equals_mc2(self):
        chapter_card(self, "第四幕", "质能等价", "E = mc²")

        # 3D 展示：质量方块旋转 → 能量球脉动
        self.move_camera(phi=45 * DEGREES, theta=-60 * DEGREES, run_time=2.0)

        # 质量方块
        from manim import Cube
        mass_cube = Cube(side_length=1.2, fill_color=C_BLUE, fill_opacity=0.6)
        mass_cube.set_stroke(color=C_BLUE, width=2)
        mass_cube.shift(LEFT * 3)

        # 能量球
        energy_sphere = Sphere(radius=0.8, resolution=(24, 24))
        energy_sphere.set_color(C_YELLOW)
        energy_sphere.set_opacity(0.6)
        energy_sphere.shift(RIGHT * 3)

        self.play(
            FadeIn(mass_cube, scale=0.5, run_time=1.5),
            FadeIn(energy_sphere, scale=0.5, run_time=1.5),
        )

        # 旋转两者
        self.play(
            mass_cube.animate.rotate(TAU, axis=UP),
            energy_sphere.animate.rotate(TAU, axis=np.array([1, 1, 0])),
            self.camera.animate.set_theta(-120 * DEGREES),
            run_time=4.0,
        )

        # 回到 2D 显示公式
        self.play(
            FadeOut(mass_cube), FadeOut(energy_sphere),
            run_time=0.8,
        )
        self.move_camera(phi=0, theta=-PI / 2, run_time=1.5)

        # 大公式
        formula = MathTex("E", "=", "m", "c^{2}", font_size=96)
        formula[0].set_color(C_YELLOW)
        formula[2].set_color(C_BLUE)
        formula[3].set_color(C_ORANGE)
        formula.move_to(ORIGIN + UP * 0.5)

        self.play(Write(formula, run_time=3.0))
        self.play(Flash(formula, color=C_YELLOW, flash_radius=2.5, run_time=1.2))
        self.wait(1.0)

        # 事实补充
        fact = cn("太阳每秒将 430 万吨物质转化为光和热。质能总量不差分毫。",
                  size=24, color=C_TEXT_DIM).to_edge(DOWN, buff=0.5)
        self.play(Write(fact, run_time=2.0))
        self.wait(3.0)

        self.play(FadeOut(VGroup(formula, fact), run_time=1.2))

    # ================================================================
    # 5. 回收 + 收束（约 1 分钟）
    # ================================================================
    def closing(self):
        lines = [
            ("苹果下落", "KE + PE = 常数", C_BLUE),
            ("海浪翻涌", "波能周期互换", C_GREEN),
            ("冰水变温", "能量守恒 + 熵增", C_PURPLE),
        ]

        rows = VGroup()
        for a, b, c in lines:
            ta = cn_bold(a, size=32, color=c)
            arrow = Arrow(ORIGIN, RIGHT * 0.8, stroke_width=3, color=c,
                          max_tip_length_to_length_ratio=0.15)
            arrow.next_to(ta, RIGHT, buff=0.3)
            tb = cn(b, size=26, color=C_TEXT).next_to(arrow, RIGHT, buff=0.3)
            rows.add(VGroup(ta, arrow, tb))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(ORIGIN + UP * 0.5)

        for r in rows:
            self.play(
                LaggedStart(
                    Write(r[0], run_time=0.8),
                    GrowArrow(r[1], run_time=0.6),
                    Write(r[2], run_time=0.8),
                    lag_ratio=0.3,
                ),
                run_time=1.8,
            )
            self.wait(0.8)

        self.wait(1.5)

        # 金句
        slogan = cn_bold("别追着变化跑。转身，找那个不动的。",
                         size=36, color=C_YELLOW).to_edge(DOWN, buff=1.0)
        self.play(Write(slogan, run_time=2.0))
        self.play(Indicate(slogan, color=C_YELLOW, run_time=1.2))
        self.wait(2.0)

        # 下集预告
        teaser = cn("下集 · 数学启蒙：描述不变的语言。",
                    size=26, color=C_BLUE).next_to(slogan, DOWN, buff=0.4)
        self.play(fade_in_up(teaser), run_time=1.2)
        self.wait(3.0)

        self.play(FadeOut(VGroup(rows, slogan, teaser), run_time=2.0))
        self.wait(1.0)
