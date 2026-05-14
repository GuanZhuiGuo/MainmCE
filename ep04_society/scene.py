"""
EP04 · 社会启蒙：个体 / 交互 / 激励 / 涌现
渲染：manim -pql ep04_society/scene.py Society
高清：manim -qh ep04_society/scene.py Society

专业动画版：ThreeDScene + 3D 网格涌现 + 相机旋转 + 丰富博弈视觉。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from manim import (
    ThreeDScene, MovingCameraScene,
    ThreeDAxes, Surface, Sphere, Cube, Prism,
    Axes, ParametricFunction,
    ValueTracker, always_redraw, DecimalNumber,
    MoveAlongPath, GrowArrow, Flash, Indicate, Circumscribe,
    Circle, Square, Dot as MDot, Polygon,
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
    C_TEXT, C_TEXT_DIM, C_HIGHLIGHT, C_BG,
    cn, cn_bold, bullet, highlight_box, footer, chapter_card, fade_in_up,
)


SERIES = "社会启蒙"
EPISODE = "EP04 · 从个体到社会"


class Society(ThreeDScene):
    """主场景：3D 涌现网格 + 博弈矩阵 + 激励曲线 + 相机旋转。"""

    def construct(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)
        self.cold_open()
        self.title_card()
        self.individual_distribution()
        self.interactions_game()
        self.incentives_matter()
        self.emergence_3d()
        self.closing()

    # ================================================================
    # 0. COLD OPEN（约 50 秒）
    # ================================================================
    def cold_open(self):
        lines = [
            "十字路口没人指挥，车流井井有条。",
            "奶茶店没人发号码牌，队伍自己排好。",
            "千万人同时刷视频，爆款一遍遍涌现。",
        ]

        for i, l in enumerate(lines):
            t = cn(l, size=36, color=C_TEXT)
            # 从下方弹入
            t.move_to(DOWN * 6)
            self.play(
                t.animate.move_to(ORIGIN),
                run_time=1.3,
                rate_func=rate_functions.ease_out_back,
            )
            self.wait(1.2)
            self.play(
                t.animate.move_to(UP * 5).set_opacity(0),
                run_time=0.7,
            )
            self.remove(t)

        # 钩子
        hook1 = cn("单看每个人，都是乱的。", size=38, color=C_TEXT_DIM)
        hook2 = cn_bold("合在一起——居然有规律。", size=44, color=C_YELLOW)
        hook2.next_to(hook1, DOWN, buff=0.5)
        grp = VGroup(hook1, hook2).move_to(ORIGIN)

        self.play(Write(hook1, run_time=1.5))
        self.play(Write(hook2, run_time=1.8))
        self.wait(2.5)

        # 亚当·斯密引言
        smith = cn('"看不见的手" — Adam Smith, 1776',
                   size=22, color=C_TEXT_DIM).to_edge(DOWN, buff=0.5)
        self.play(fade_in_up(smith), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(VGroup(grp, smith), shift=UP), run_time=1.0)

    # ================================================================
    # 1. TITLE CARD（约 30 秒）
    # ================================================================
    def title_card(self):
        big = cn_bold("社会启蒙", size=88, color=C_BLUE)
        sub = cn("个体如何涌现为群体秩序", size=30, color=C_TEXT_DIM)
        sub.next_to(big, DOWN, buff=0.4)
        head = VGroup(big, sub).move_to(ORIGIN + UP * 0.6)

        self.play(SpinInFromNothing(big, run_time=1.8))
        self.play(fade_in_up(sub, shift=0.5), run_time=1.0)

        # 四锚
        anchors = [("个体", C_BLUE), ("交互", C_GREEN),
                   ("激励", C_ORANGE), ("涌现", C_YELLOW)]
        cards = VGroup()
        for a, c in anchors:
            card = RoundedRectangle(corner_radius=0.15, width=2.3, height=1.1,
                                    stroke_color=c, stroke_width=2.5,
                                    fill_color=c, fill_opacity=0.1)
            lbl = cn_bold(a, size=30, color=c).move_to(card)
            cards.add(VGroup(card, lbl))
        cards.arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=1.0)

        chain_arrows = VGroup()
        for i in range(len(cards) - 1):
            a = Arrow(cards[i][0].get_right(), cards[i + 1][0].get_left(),
                      buff=0.08, stroke_width=3, color=C_TEXT_DIM,
                      max_tip_length_to_length_ratio=0.15)
            chain_arrows.add(a)

        self.play(LaggedStart(*[DrawBorderThenFill(c) for c in cards], lag_ratio=0.2), run_time=2.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in chain_arrows], lag_ratio=0.2), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(VGroup(head, cards, chain_arrows), shift=UP), run_time=1.0)

    # ================================================================
    # 2. 个体 · 正态分布 3D（约 2 分钟）
    # ================================================================
    def individual_distribution(self):
        chapter_card(self, "第一根支柱", "个体", "没有两个人完全一样")

        # 2D axes
        ax = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.5, 0.1],
            x_length=10, y_length=3.5,
            tips=False,
            axis_config={"stroke_color": C_TEXT_DIM},
        ).move_to(ORIGIN + DOWN * 0.3)
        self.play(Create(ax, run_time=1.5))

        # 随机点云
        rng = np.random.default_rng(42)
        n = 150
        xs = rng.normal(0, 1.1, size=n)
        raw_pts = VGroup(*[
            Dot(ax.c2p(x, rng.uniform(0.02, 0.42)),
                radius=0.04, color=C_BLUE_DEEP)
            for x in xs
        ])
        self.play(LaggedStartMap(FadeIn, raw_pts, scale=0.3, lag_ratio=0.005), run_time=2.5)
        self.wait(1.0)

        # 落到分布位置
        def pdf(x):
            return np.exp(-x * x / 2) / np.sqrt(2 * np.pi)

        anims = []
        for dot, x in zip(raw_pts, xs):
            target_y = pdf(x) * (0.85 + rng.uniform(-0.05, 0.05))
            anims.append(dot.animate.move_to(ax.c2p(x, target_y)).set_color(C_YELLOW))

        self.play(AnimationGroup(*anims, lag_ratio=0.003), run_time=4.0)
        self.wait(0.5)

        # 正态曲线覆盖
        curve = ax.plot(pdf, x_range=[-3.8, 3.8], color=C_YELLOW, stroke_width=3)
        formula = MathTex(
            r"f(x)=\frac{1}{\sqrt{2\pi}}\,e^{-x^{2}/2}",
            color=C_YELLOW, font_size=30,
        ).to_edge(UP, buff=0.5)
        self.play(Create(curve, run_time=2.5), Write(formula, run_time=1.5))
        self.wait(1.5)

        # 3D 视角展示正态 bell
        self.play(FadeOut(VGroup(raw_pts, curve, formula), run_time=0.8))
        self.move_camera(phi=55 * DEGREES, theta=-50 * DEGREES, run_time=2.0)

        axes_3d = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[0, 0.5, 0.1],
            x_length=5, y_length=5, z_length=3,
            axis_config={"stroke_color": C_TEXT_DIM, "stroke_width": 1.5},
        )
        self.play(Create(axes_3d, run_time=1.5))

        # 2D 正态 bell surface
        bell_surface = Surface(
            lambda u, v: axes_3d.c2p(u, v, np.exp(-(u**2 + v**2) / 2) / (2 * np.pi)),
            u_range=[-2.8, 2.8], v_range=[-2.8, 2.8],
            resolution=(30, 30),
            fill_color=C_YELLOW, fill_opacity=0.35,
            stroke_color=C_YELLOW, stroke_width=0.3,
        )
        self.play(Create(bell_surface, run_time=3.5))

        # 旋转展示
        self.play(
            self.camera.animate.set_theta(-130 * DEGREES),
            run_time=5.0,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(1.0)

        # 回到 2D
        self.play(FadeOut(VGroup(axes_3d, bell_surface, ax), run_time=1.0))
        self.move_camera(phi=0, theta=-PI / 2, run_time=1.5)

        punch = cn_bold("大量独立因素叠加 → 正态分布是数学必然。",
                        size=28, color=C_YELLOW)
        self.play(Write(punch, run_time=1.5))
        self.play(Indicate(punch, color=C_YELLOW, run_time=1.0))
        self.wait(2.0)
        self.play(FadeOut(punch, run_time=0.8))


    # ================================================================
    # 3. 博弈 · 囚徒困境（约 2.5 分钟）
    # ================================================================
    def interactions_game(self):
        chapter_card(self, "第二根支柱", "交互", "博弈论 · 囚徒困境")

        # 2x2 收益矩阵 — 手动构建可控动画
        cell_size = 1.8
        grid_origin = LEFT * 1.5 + UP * 0.3

        # 表头
        header_col = cn_bold("合作", size=22, color=C_GREEN)
        header_col2 = cn_bold("背叛", size=22, color=C_RED)
        header_row = cn_bold("合作", size=22, color=C_GREEN)
        header_row2 = cn_bold("背叛", size=22, color=C_RED)

        # 格子
        cells_data = [
            [(3, 3, C_GREEN), (0, 5, C_ORANGE)],
            [(5, 0, C_ORANGE), (1, 1, C_RED)],
        ]

        all_cells = VGroup()
        for r in range(2):
            for c in range(2):
                sq = Square(side_length=cell_size,
                            stroke_color=C_TEXT_DIM, stroke_width=1.5,
                            fill_color=cells_data[r][c][2], fill_opacity=0.08)
                sq.move_to(grid_origin + np.array([
                    (c + 0.5) * cell_size,
                    -(r + 0.5) * cell_size, 0
                ]))
                vals = cells_data[r][c]
                lbl = cn(f"({vals[0]}, {vals[1]})", size=24, color=cells_data[r][c][2])
                lbl.move_to(sq)
                all_cells.add(VGroup(sq, lbl))

        # 表头位置
        header_col.move_to(grid_origin + np.array([0.5 * cell_size, 0.5 * cell_size, 0]))
        header_col2.move_to(grid_origin + np.array([1.5 * cell_size, 0.5 * cell_size, 0]))
        header_row.move_to(grid_origin + np.array([-0.5 * cell_size, -0.5 * cell_size, 0]))
        header_row2.move_to(grid_origin + np.array([-0.5 * cell_size, -1.5 * cell_size, 0]))

        headers = VGroup(header_col, header_col2, header_row, header_row2)

        # 玩家标签
        player_b = cn("玩家 B →", size=18, color=C_TEXT_DIM)
        player_b.next_to(header_col, UP, buff=0.3).shift(RIGHT * 0.9)
        player_a = cn("玩家 A ↓", size=18, color=C_TEXT_DIM)
        player_a.next_to(header_row, LEFT, buff=0.3).shift(DOWN * 0.9)

        # 逐格动画
        self.play(Write(player_a, run_time=0.8), Write(player_b, run_time=0.8))
        self.play(LaggedStart(*[Write(h) for h in headers], lag_ratio=0.2), run_time=1.5)

        for cell in all_cells:
            self.play(DrawBorderThenFill(cell[0], run_time=0.6), Write(cell[1], run_time=0.6))
            self.wait(0.3)

        self.wait(1.5)

        # 高亮 (背叛, 背叛) — 纳什均衡
        defect_cell = all_cells[3]  # row=1, col=1
        self.play(
            Indicate(defect_cell[0], color=C_RED, scale_factor=1.15, run_time=1.2),
        )
        self.play(Flash(defect_cell[1], color=C_RED, flash_radius=1.0, run_time=0.8))

        nash = cn_bold("纳什均衡", size=36, color=C_YELLOW)
        nash_sub = cn("没人想单方面改变 → 稳定但非最优", size=22, color=C_TEXT_DIM)
        nash_grp = VGroup(nash, nash_sub).arrange(DOWN, buff=0.2)
        nash_grp.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.5)

        self.play(Write(nash, run_time=1.2))
        self.play(fade_in_up(nash_sub), run_time=0.8)
        self.play(Circumscribe(nash, color=C_YELLOW, run_time=1.2))
        self.wait(2.0)

        # 重复博弈 Tit-for-Tat
        self.play(FadeOut(VGroup(all_cells, headers, player_a, player_b, nash_grp), run_time=0.8))

        tit_title = cn_bold("重复博弈 · Tit-for-Tat", size=30, color=C_GREEN)
        tit_title.to_edge(UP, buff=0.6)
        self.play(Write(tit_title, run_time=1.2))

        # 时间轴：显示多轮合作
        timeline = Line(LEFT * 5, RIGHT * 5, color=C_TEXT_DIM, stroke_width=2)
        timeline.move_to(ORIGIN)
        self.play(Create(timeline, run_time=1.5))

        rounds = ["C", "C", "C", "D", "D", "C", "C", "C"]
        round_colors = [C_GREEN, C_GREEN, C_GREEN, C_RED, C_RED, C_GREEN, C_GREEN, C_GREEN]
        round_dots = VGroup()
        for i, (r, c) in enumerate(zip(rounds, round_colors)):
            x_pos = -4.5 + i * 1.2
            dot = Dot(np.array([x_pos, 0, 0]), color=c, radius=0.12)
            lbl = cn(r, size=18, color=c).next_to(dot, UP, buff=0.2)
            round_dots.add(VGroup(dot, lbl))

        self.play(LaggedStartMap(FadeIn, round_dots, scale=0.5, lag_ratio=0.1), run_time=3.0)
        self.wait(1.0)

        # 条件
        conditions = VGroup(
            cn("有信任", size=24, color=C_GREEN),
            cn("有反馈", size=24, color=C_BLUE),
            cn("有未来", size=24, color=C_ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.5)

        self.play(LaggedStart(*[fade_in_up(c) for c in conditions], lag_ratio=0.3), run_time=2.0)
        self.wait(2.5)

        self.play(FadeOut(VGroup(tit_title, timeline, round_dots, conditions), run_time=1.0))

    # ================================================================
    # 4. 激励（约 1.5 分钟）
    # ================================================================
    def incentives_matter(self):
        chapter_card(self, "第三根支柱", "激励", "制度比人重要")

        ax = Axes(
            x_range=[0, 10, 1], y_range=[0, 6, 1],
            x_length=9, y_length=4.5,
            tips=False,
            axis_config={"stroke_color": C_TEXT_DIM},
        ).move_to(ORIGIN + DOWN * 0.2)

        y_label = cn("产出", size=20, color=C_TEXT_DIM).next_to(ax, UP, buff=0.1)
        x_label = cn("时间", size=20, color=C_TEXT_DIM).next_to(ax, DOWN, buff=0.1).shift(RIGHT * 3.5)
        self.play(Create(ax, run_time=1.5), Write(y_label), Write(x_label))

        # 三条曲线
        slow = ax.plot(lambda t: 0.2 * t + 0.8, x_range=[0, 10], color=C_RED, stroke_width=3)
        slow_lbl = cn("按工时", size=20, color=C_RED).next_to(ax.c2p(10, 2.8), RIGHT, buff=0.2)

        medium = ax.plot(lambda t: 0.38 * t + 0.5 + 0.2 * np.sin(t),
                         x_range=[0, 10], color=C_ORANGE, stroke_width=3)
        medium_lbl = cn("按件", size=20, color=C_ORANGE).next_to(ax.c2p(10, 4.3), RIGHT, buff=0.2)

        fast = ax.plot(lambda t: 0.5 * t + 0.3 + 0.15 * np.sin(1.5 * t),
                       x_range=[0, 10], color=C_GREEN, stroke_width=3)
        fast_lbl = cn("计件+质检", size=20, color=C_GREEN).next_to(ax.c2p(10, 5.5), RIGHT, buff=0.2)

        # 逐条描画
        self.play(Create(slow, run_time=2.5), Write(slow_lbl, run_time=1.0))
        self.wait(0.8)
        self.play(Create(medium, run_time=2.5), Write(medium_lbl, run_time=1.0))
        self.wait(0.8)
        self.play(Create(fast, run_time=2.5), Write(fast_lbl, run_time=1.0))
        self.wait(1.5)

        # 高亮差异
        diff_arrow = Arrow(
            ax.c2p(9, 0.2 * 9 + 0.8), ax.c2p(9, 0.5 * 9 + 0.3),
            buff=0.1, stroke_width=4, color=C_YELLOW,
            max_tip_length_to_length_ratio=0.1,
        )
        diff_label = cn_bold("同一批人\n不同激励", size=22, color=C_YELLOW).next_to(diff_arrow, LEFT, buff=0.2)
        self.play(GrowArrow(diff_arrow, run_time=1.2), Write(diff_label, run_time=1.0))
        self.wait(1.5)

        # 激励相容引言
        punch = cn_bold("让每个人追求自己利益时，顺便把集体的事做了。",
                        size=26, color=C_YELLOW).to_edge(DOWN, buff=0.3)
        self.play(Write(punch, run_time=2.0))
        self.play(Indicate(punch, color=C_YELLOW, run_time=1.0))
        self.wait(2.5)

        self.play(FadeOut(VGroup(
            ax, y_label, x_label, slow, slow_lbl,
            medium, medium_lbl, fast, fast_lbl,
            diff_arrow, diff_label, punch,
        ), run_time=1.2))


    # ================================================================
    # 5. 涌现 · 3D 生命游戏（约 2.5 分钟 — 重头戏）
    # ================================================================
    def emergence_3d(self):
        chapter_card(self, "第四根支柱", "涌现", "简单规则 · 大量交互 · 复杂秩序")

        # 切换到 3D
        self.move_camera(phi=55 * DEGREES, theta=-50 * DEGREES, run_time=2.0)

        # 3D 网格 — 每个活细胞是一个小方块
        cols, rows = 16, 10
        cell_size = 0.4
        grid_width = cols * cell_size
        grid_height = rows * cell_size

        rng = np.random.default_rng(3)
        state = rng.integers(0, 2, size=(rows, cols))

        def state_to_cubes(s):
            cubes = VGroup()
            for r in range(rows):
                for c in range(cols):
                    if s[r, c] == 1:
                        cube = Cube(side_length=cell_size * 0.85, fill_color=C_YELLOW, fill_opacity=0.85)
                        cube.set_stroke(color=C_YELLOW, width=0.5)
                        cube.move_to(np.array([
                            (c - cols / 2) * cell_size,
                            (r - rows / 2) * cell_size,
                            0,
                        ]))
                        cubes.add(cube)
            return cubes

        grid = state_to_cubes(state)
        self.play(LaggedStartMap(FadeIn, grid, scale=0.3, lag_ratio=0.005), run_time=2.5)
        self.wait(1.0)

        # 生命游戏规则
        def step(s):
            new = np.zeros_like(s)
            for r in range(rows):
                for c in range(cols):
                    n = 0
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            if dr == 0 and dc == 0:
                                continue
                            rr = (r + dr) % rows
                            cc = (c + dc) % cols
                            n += s[rr, cc]
                    if s[r, c] == 1 and n in (2, 3):
                        new[r, c] = 1
                    elif s[r, c] == 0 and n == 3:
                        new[r, c] = 1
            return new

        # 演化 8 代，每代同时旋转相机
        theta_start = -50
        for gen in range(8):
            state = step(state)
            new_grid = state_to_cubes(state)
            theta_end = theta_start - 15
            self.play(
                Transform(grid, new_grid, run_time=1.2),
                self.camera.animate.set_theta(theta_end * DEGREES),
                rate_func=rate_functions.ease_in_out_sine,
            )
            theta_start = theta_end
            self.wait(0.4)

        self.wait(1.0)

        # 俯视展示最终状态
        self.play(
            self.camera.animate.set_phi(80 * DEGREES).set_theta(-90 * DEGREES),
            run_time=2.5,
        )
        self.wait(1.5)

        # 回到侧视
        self.play(
            self.camera.animate.set_phi(45 * DEGREES).set_theta(-60 * DEGREES),
            run_time=2.0,
        )
        self.wait(1.0)

        # 回到 2D 显示结论
        self.play(FadeOut(grid, run_time=1.0))
        self.move_camera(phi=0, theta=-PI / 2, run_time=1.5)

        punch = cn_bold("简单规则 + 大量交互 + 时间 = 不可预测的复杂秩序。",
                        size=28, color=C_YELLOW)
        self.play(Write(punch, run_time=2.0))
        self.play(
            Indicate(punch, color=C_YELLOW, run_time=1.0),
            Flash(punch, color=C_YELLOW, flash_radius=2.0, run_time=0.8),
        )
        self.wait(2.5)

        # 个人启发
        tips = VGroup(
            cn("1. 把自己放进对的交互场", size=24, color=C_BLUE),
            cn("2. 设置正确的自我激励", size=24, color=C_GREEN),
            cn("3. 给时间", size=24, color=C_ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(punch, DOWN, buff=0.6)

        self.play(LaggedStart(*[fade_in_up(t) for t in tips], lag_ratio=0.3), run_time=2.0)
        self.wait(2.5)

        self.play(FadeOut(VGroup(punch, tips), run_time=1.0))

    # ================================================================
    # 6. 收束（约 1 分钟）
    # ================================================================
    def closing(self):
        title_ = cn_bold("四集 · 一条链", size=42, color=C_BLUE)
        self.play(Write(title_, run_time=1.5))
        self.play(title_.animate.to_edge(UP, buff=0.8), run_time=0.8)

        items = [
            ("如何思考", "拆问题", C_YELLOW),
            ("自然启蒙", "变与不变", C_GREEN),
            ("数学启蒙", "描述的语言", C_ORANGE),
            ("社会启蒙", "个体→群体", C_BLUE),
        ]

        cards = VGroup()
        for name, desc, c in items:
            card = RoundedRectangle(
                corner_radius=0.12, width=2.8, height=1.4,
                stroke_color=c, stroke_width=2.5,
                fill_color=c, fill_opacity=0.1,
            )
            name_lbl = cn_bold(name, size=22, color=c).move_to(card.get_top() + DOWN * 0.4)
            desc_lbl = cn(desc, size=18, color=C_TEXT_DIM).move_to(card.get_bottom() + UP * 0.35)
            cards.add(VGroup(card, name_lbl, desc_lbl))

        cards.arrange(RIGHT, buff=0.3).move_to(ORIGIN)

        # 连接箭头
        conn_arrows = VGroup()
        for i in range(len(cards) - 1):
            a = Arrow(
                cards[i][0].get_right(), cards[i + 1][0].get_left(),
                buff=0.05, stroke_width=3, color=C_TEXT_DIM,
                max_tip_length_to_length_ratio=0.12,
            )
            conn_arrows.add(a)

        # 首尾相连的弧形箭头
        loop_arrow = Arrow(
            cards[-1][0].get_bottom() + DOWN * 0.2,
            cards[0][0].get_bottom() + DOWN * 0.2,
            buff=0.3, stroke_width=2, color=C_PURPLE,
            max_tip_length_to_length_ratio=0.08,
        ).shift(DOWN * 0.5)

        self.play(LaggedStart(*[DrawBorderThenFill(c) for c in cards], lag_ratio=0.2), run_time=3.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in conn_arrows], lag_ratio=0.2), run_time=2.0)
        self.play(GrowArrow(loop_arrow, run_time=1.5))
        self.wait(2.0)

        # 留问
        question = cn_bold("既然社会靠涌现运行——你怎么找到自己的位置？",
                           size=26, color=C_YELLOW).to_edge(DOWN, buff=1.0)
        self.play(Write(question, run_time=2.0))
        self.wait(2.5)

        # 下季预告
        teaser = cn("下一季：知识 · 组织 · 成长。",
                    size=24, color=C_BLUE).next_to(question, DOWN, buff=0.3)
        self.play(fade_in_up(teaser), run_time=1.2)
        self.wait(3.0)

        # 最终渐隐
        self.play(
            FadeOut(VGroup(title_, cards, conn_arrows, loop_arrow, question, teaser)),
            run_time=2.5,
        )
        self.wait(1.0)
