"""
EP04 · 社会启蒙：个体 / 交互 / 激励 / 涌现
渲染：manim -pql ep04_society/scene.py Society
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from manim import (
    Scene, Axes, ValueTracker, always_redraw, ParametricFunction,
    MathTex, Indicate, Flash, Circle, Square, Dot as MDot,
    Table, MobjectTable, MarkupText, Polygon,
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


SERIES = "社会启蒙"
EPISODE = "EP04 · 从个体到社会"


class Society(Scene):
    def construct(self):
        self.add(footer(SERIES, EPISODE))
        self.cold_open()
        self.title_card()
        self.individual_distribution()
        self.interactions_game()
        self.incentives_matter()
        self.emergence()
        self.closing()

    # ---------- 0. Cold Open ----------
    def cold_open(self):
        lines = [
            "十字路口没人指挥，车流井井有条。",
            "奶茶店没人维持秩序，队伍自己长出来。",
            "手机前千万人同时点赞，爆款一次次重演。",
        ]
        for l in lines:
            t = cn(l, size=34, color=C_TEXT)
            self.play(fade_in_up(t), run_time=0.55)
            self.wait(0.8)
            self.play(FadeOut(t, shift=UP * 0.3), run_time=0.35)

        hook1 = cn("单看每个人，都是乱的。", size=40, color=C_TEXT_DIM)
        hook2 = cn_bold("合在一起——居然有规律。", size=44, color=C_YELLOW)
        hook2.next_to(hook1, DOWN, buff=0.4)
        grp = VGroup(hook1, hook2).move_to(ORIGIN)
        self.play(Write(hook1))
        self.play(Write(hook2))
        self.wait(1.2)
        self.play(FadeOut(grp))

    # ---------- 1. Title ----------
    def title_card(self):
        big = cn_bold("社会启蒙", size=88, color=C_BLUE)
        sub = cn("个体如何涌现为群体", size=30, color=C_TEXT_DIM)
        sub.next_to(big, DOWN, buff=0.35)
        head = VGroup(big, sub).move_to(ORIGIN + UP * 0.6)
        self.play(Write(big), run_time=1.0)
        self.play(fade_in_up(sub))

        anchors = [("个体", C_BLUE), ("交互", C_GREEN),
                   ("激励", C_ORANGE), ("涌现", C_YELLOW)]
        cards = VGroup()
        for a, c in anchors:
            card = RoundedRectangle(corner_radius=0.15, width=2.3, height=1.1,
                                    stroke_color=c, stroke_width=2.5,
                                    fill_color=c, fill_opacity=0.1)
            lbl = cn_bold(a, size=32, color=c).move_to(card)
            cards.add(VGroup(card, lbl))
        cards.arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=0.9)

        arrows = VGroup()
        for i in range(len(cards) - 1):
            a = Arrow(cards[i][0].get_right(), cards[i + 1][0].get_left(),
                      buff=0.08, stroke_width=3, color=C_TEXT_DIM,
                      max_tip_length_to_length_ratio=0.15)
            arrows.add(a)

        self.play(AnimationGroup(*[fade_in_up(c) for c in cards], lag_ratio=0.2))
        self.play(AnimationGroup(*[FadeIn(a) for a in arrows], lag_ratio=0.2))
        self.wait(1.0)
        self.play(FadeOut(VGroup(head, cards, arrows)))

    # ---------- 2. 个体 · 正态分布 ----------
    def individual_distribution(self):
        chapter_card(self, "第一锚", "个体", "没有两个人完全一样")

        ax = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.55, 0.1],
            x_length=10, y_length=3.2,
            tips=False,
            axis_config={"stroke_color": C_TEXT_DIM},
        ).move_to(ORIGIN + DOWN * 0.2)
        self.play(Create(ax))

        # 先撒一堆随机点（看起来无序）
        rng = np.random.default_rng(42)
        n = 140
        xs = rng.normal(0, 1.1, size=n)
        raw_pts = VGroup(*[
            Dot(ax.c2p(x, rng.uniform(0.05, 0.45)),
                radius=0.045, color=C_BLUE_DEEP)
            for x in xs
        ])
        self.play(FadeIn(raw_pts, lag_ratio=0.01), run_time=1.8)
        self.wait(0.4)

        # 落回到分布曲线下的直方结构（用 y = pdf(x) 高度）
        def pdf(x):
            return np.exp(-x * x / 2) / np.sqrt(2 * np.pi)

        def fall_target(x):
            return ax.c2p(x, min(pdf(x) * 0.9 + rng.uniform(0, 0.05), 0.5))

        anims = []
        for dot, x in zip(raw_pts, xs):
            anims.append(dot.animate.move_to(fall_target(x)).set_color(C_YELLOW))
        self.play(AnimationGroup(*anims, lag_ratio=0.005), run_time=2.4)

        # 覆盖一条正态分布曲线
        curve = ax.plot(lambda x: pdf(x), x_range=[-3.8, 3.8],
                        color=C_YELLOW, stroke_width=3)
        label = MathTex(
            r"f(x)=\tfrac{1}{\sqrt{2\pi}}\,e^{-x^{2}/2}",
            color=C_YELLOW, font_size=32,
        ).to_edge(UP, buff=0.8)
        self.play(Create(curve), Write(label))
        self.wait(0.6)

        punch = cn_bold("承认个体差异，但相信整体分布。",
                        size=32, color=C_YELLOW).to_edge(DOWN, buff=0.3)
        self.play(fade_in_up(punch))
        self.wait(1.2)

        self.play(FadeOut(VGroup(ax, raw_pts, curve, label, punch)))

    # ---------- 3. 囚徒困境 ----------
    def interactions_game(self):
        chapter_card(self, "第二锚", "交互", "博弈论 · 囚徒困境")

        # 2x2 payoff
        header_row = ["", "合作", "背叛"]
        row1 = ["合作", "(3, 3)", "(0, 5)"]
        row2 = ["背叛", "(5, 0)", "(1, 1)"]

        cell_size = 1.5
        grid = VGroup()
        texts = [[header_row[0], header_row[1], header_row[2]],
                 [row1[0], row1[1], row1[2]],
                 [row2[0], row2[1], row2[2]]]
        colors = [[C_TEXT_DIM, C_BLUE, C_RED],
                  [C_BLUE, C_GREEN, C_ORANGE],
                  [C_RED, C_ORANGE, C_RED]]

        for i in range(3):
            for j in range(3):
                cell = Square(side_length=cell_size,
                              stroke_color=C_TEXT_DIM, stroke_width=1.5,
                              fill_color=colors[i][j], fill_opacity=0.08)
                cell.move_to(np.array([(j - 1) * cell_size, (1 - i) * cell_size, 0]))
                lbl = cn(texts[i][j], size=24, color=colors[i][j]).move_to(cell)
                grid.add(VGroup(cell, lbl))

        grid.move_to(ORIGIN).shift(LEFT * 2)

        caption_top = cn("列：玩家 B", size=22, color=C_TEXT_DIM).next_to(grid, UP, buff=0.25)
        caption_left = cn("行：玩家 A", size=22, color=C_TEXT_DIM)
        caption_left.rotate(np.pi / 2).next_to(grid, LEFT, buff=0.25)

        self.play(AnimationGroup(*[FadeIn(c) for c in grid], lag_ratio=0.05))
        self.play(Write(caption_top), Write(caption_left))

        # 右侧文字推演
        right_top = cn_bold("「合作」对双方最好。", size=26, color=C_GREEN)
        right_mid = cn("但只要一方背叛，对方就吃亏。", size=24, color=C_TEXT_DIM)
        right_bot = cn_bold("结果：(背叛, 背叛) 成了均衡。", size=26, color=C_RED)
        right = VGroup(right_top, right_mid, right_bot).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35
        ).to_edge(RIGHT, buff=0.6)

        for m in right:
            self.play(fade_in_up(m), run_time=0.7)

        # 高亮 (背叛, 背叛)
        defect_cell = grid[-1]  # (2,2)
        self.play(Indicate(defect_cell[0], color=C_RED, scale_factor=1.1))
        self.play(Flash(defect_cell[1], color=C_RED, flash_radius=0.8))

        nash = cn_bold("纳什均衡：没人想单方面改变。",
                       size=30, color=C_YELLOW).to_edge(DOWN, buff=0.3)
        self.play(fade_in_up(nash))
        self.wait(1.3)

        self.play(FadeOut(VGroup(grid, caption_top, caption_left, right, nash)))

    # ---------- 4. 激励 ----------
    def incentives_matter(self):
        chapter_card(self, "第三锚", "激励", "制度比人重要")

        ax = Axes(
            x_range=[0, 10, 1], y_range=[0, 5, 1],
            x_length=8, y_length=3.5,
            tips=False,
            axis_config={"stroke_color": C_TEXT_DIM},
        ).move_to(ORIGIN + DOWN * 0.2)
        self.play(Create(ax))

        # 两条轨迹：同一人群 x 时间，不同激励下的产出
        slow = ax.plot(lambda t: 0.25 * t + 0.5, x_range=[0, 10],
                       color=C_RED, stroke_width=3)
        slow_lbl = cn("按工时", size=22, color=C_RED).next_to(
            ax.c2p(10, 0.25 * 10 + 0.5), RIGHT, buff=0.2
        )
        fast = ax.plot(lambda t: 0.35 * t + 0.3 * np.sin(t) + 0.5,
                       x_range=[0, 10], color=C_GREEN, stroke_width=3)
        # Correct fast to end higher
        fast = ax.plot(lambda t: 0.45 * t + 0.15 * np.sin(t) + 0.3,
                       x_range=[0, 10], color=C_GREEN, stroke_width=3)
        fast_lbl = cn("按成果", size=22, color=C_GREEN).next_to(
            ax.c2p(10, 0.45 * 10 + 0.3), RIGHT, buff=0.2
        )

        self.play(Create(slow), Write(slow_lbl))
        self.play(Create(fast), Write(fast_lbl))
        self.wait(0.5)

        y_label = cn("产出", size=22, color=C_TEXT_DIM).next_to(ax, UP, buff=0.1)
        x_label = cn("时间", size=22, color=C_TEXT_DIM).next_to(ax, DOWN, buff=0.1).shift(RIGHT * 3)
        self.play(FadeIn(y_label), FadeIn(x_label))

        punch = cn_bold("同一批人，不同激励，完全不同的社会。",
                        size=30, color=C_YELLOW).to_edge(DOWN, buff=0.3)
        self.play(fade_in_up(punch))
        self.play(Indicate(punch, color=C_YELLOW))
        self.wait(1.2)

        self.play(FadeOut(VGroup(ax, slow, slow_lbl, fast, fast_lbl,
                                 y_label, x_label, punch)))

    # ---------- 5. 涌现 · 网格演化 ----------
    def emergence(self):
        chapter_card(self, "第四锚", "涌现", "简单规则 · 大量交互 · 复杂秩序")

        # 展示一个 18x10 网格，按一个简单规则演化几步
        cols, rows = 18, 10
        cell = 0.45
        origin = np.array([-cols * cell / 2 + cell / 2,
                           -rows * cell / 2 + cell / 2, 0])

        rng = np.random.default_rng(3)
        state = rng.integers(0, 2, size=(rows, cols))

        def draw_grid(state):
            grid = VGroup()
            for r in range(rows):
                for c in range(cols):
                    alive = bool(state[r, c])
                    sq = Square(side_length=cell * 0.92,
                                stroke_color=C_TEXT_DIM, stroke_width=0.6,
                                fill_color=C_YELLOW if alive else C_BG,
                                fill_opacity=0.9 if alive else 0.1)
                    sq.move_to(origin + np.array([c * cell, r * cell, 0]))
                    grid.add(sq)
            return grid

        grid = draw_grid(state)
        self.play(FadeIn(grid, lag_ratio=0.003), run_time=1.2)
        self.wait(0.4)

        # 演化规则：生命游戏简化版
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

        for _ in range(5):
            state = step(state)
            new_grid = draw_grid(state)
            self.play(Transform(grid, new_grid), run_time=0.8)

        punch = cn_bold("简单规则 + 大量交互 = 复杂秩序。",
                        size=32, color=C_YELLOW).to_edge(DOWN, buff=0.3)
        self.play(fade_in_up(punch))
        self.play(Indicate(punch, color=C_YELLOW))
        self.wait(1.3)
        self.play(FadeOut(VGroup(grid, punch)))

    # ---------- 6. 收束 ----------
    def closing(self):
        title_ = cn_bold("四集合一", size=44, color=C_BLUE)
        self.play(Write(title_))
        self.play(title_.animate.to_edge(UP, buff=0.8))

        items = [
            ("如何思考", "拆问题", C_YELLOW),
            ("自然启蒙", "变与不变", C_GREEN),
            ("数学启蒙", "描述的语言", C_ORANGE),
            ("社会启蒙", "个体 → 群体", C_BLUE),
        ]
        rows = VGroup()
        for a, b, c in items:
            ta = cn_bold(a, size=30, color=c)
            ta_ = cn("·", size=30, color=C_TEXT_DIM).next_to(ta, RIGHT, buff=0.3)
            tb = cn(b, size=26, color=C_TEXT).next_to(ta_, RIGHT, buff=0.3)
            rows.add(VGroup(ta, ta_, tb))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(ORIGIN + UP * 0.1)
        for r in rows:
            self.play(fade_in_up(r), run_time=0.55)

        slogan = cn_bold("四把钥匙，都在你手里了。",
                         size=34, color=C_YELLOW).to_edge(DOWN, buff=1.1)
        self.play(fade_in_up(slogan))
        self.wait(1.2)

        teaser = cn("下一季 · 知识 · 组织 · 成长。",
                    size=26, color=C_BLUE).next_to(slogan, DOWN, buff=0.3)
        self.play(fade_in_up(teaser))
        self.wait(2.0)
        self.play(FadeOut(VGroup(title_, rows, slogan, teaser)))
