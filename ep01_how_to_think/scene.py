"""
EP01 · 如何思考：根本 / 角度 / 结构化拆解
渲染：manim -pql ep01_how_to_think/scene.py HowToThink
高清：manim -qh ep01_how_to_think/scene.py HowToThink

专业动画版：更长时间、更多过渡、3D视角切换、丰富的运动设计。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from manim import (
    Scene, ThreeDScene, MovingCameraScene,
    MoveAlongPath, GrowArrow, GrowFromCenter, ShrinkToCenter,
    Circle, Square, Triangle, RegularPolygon, Annulus,
    NumberPlane, Axes, ParametricFunction,
    Rotate, Indicate, Flash, Circumscribe, Wiggle,
    AnimationGroup, LaggedStart, LaggedStartMap, Succession,
    SpiralIn, SpinInFromNothing,
    DecimalNumber, Integer, ValueTracker,
    always_redraw, rate_functions,
    TAU, PI, DEGREES,
    ThreeDAxes, Surface, ParametricFunction as PF,
    RIGHT as R, LEFT as L, UP as U, DOWN as D,
    TracedPath, Uncreate, DrawBorderThenFill,
    ShowPassingFlash, MathTex,
)

from theme import (
    Text, VGroup, Rectangle, RoundedRectangle, Line, Dot, Arrow,
    FadeIn, FadeOut, Write, Create, Transform, ReplacementTransform,
    AnimationGroup, UP, DOWN, LEFT, RIGHT, ORIGIN,
    C_BLUE, C_BLUE_DEEP, C_GREEN, C_YELLOW, C_ORANGE, C_RED, C_PURPLE,
    C_TEXT, C_TEXT_DIM, C_HIGHLIGHT,
    cn, cn_bold, title, bullet, highlight_box, footer, chapter_card, fade_in_up,
)


SERIES = "方法论启蒙"
EPISODE = "EP01 · 如何思考"


class HowToThink(MovingCameraScene):
    """主场景：专业动画版 — 约 8-10 分钟渲染时长。"""

    def construct(self):
        self.add(footer(SERIES, EPISODE))
        self.cold_open()
        self.title_card()
        self.pillar_one_root()
        self.pillar_two_angle()
        self.pillar_three_structure()
        self.synthesis()
        self.outro()

    # ================================================================
    # 0. COLD OPEN — 三个问题（约 35 秒）
    # ================================================================
    def cold_open(self):
        qs = [
            "先有鸡，还是先有蛋？",
            "没砝码，用天平称三次，\n从 12 个球里找出质量异常那一个。",
            "高考作文给你几张图，\n题目只有两个字：'自选角度'。",
        ]

        for i, q in enumerate(qs):
            t = cn(q, size=40, color=C_TEXT)
            # 每个问题从不同方向入场
            directions = [LEFT * 8, RIGHT * 8, DOWN * 5]
            t.move_to(directions[i])
            self.play(
                t.animate.move_to(ORIGIN),
                run_time=1.2,
                rate_func=rate_functions.ease_out_cubic,
            )
            self.wait(1.5)
            # 退场动画：缩小 + 旋转消失
            self.play(
                t.animate.scale(0.1).rotate(PI / 4).set_opacity(0),
                run_time=0.8,
            )
            self.remove(t)

        # 汇总钩子
        hook1 = cn_bold("同样的知识，", size=52, color=C_TEXT)
        hook2 = cn_bold("为什么有人能用，有人用不出？", size=52, color=C_YELLOW)
        hook2.next_to(hook1, DOWN, buff=0.4)
        grp = VGroup(hook1, hook2).move_to(ORIGIN)

        self.play(
            LaggedStart(
                Write(hook1, run_time=1.5),
                Write(hook2, run_time=1.8),
                lag_ratio=0.4,
            )
        )
        # 相机推近
        self.play(
            self.camera.frame.animate.scale(0.85).move_to(grp),
            run_time=1.5,
        )
        self.wait(2.0)
        # 相机拉回
        self.play(
            self.camera.frame.animate.scale(1 / 0.85).move_to(ORIGIN),
            FadeOut(grp, shift=UP * 0.5),
            run_time=1.2,
        )

    # ================================================================
    # 1. TITLE CARD（约 30 秒）
    # ================================================================
    def title_card(self):
        big = cn_bold("如何思考", size=96, color=C_BLUE)
        sub = cn("方法论操作系统", size=36, color=C_TEXT_DIM)
        sub.next_to(big, DOWN, buff=0.4)
        head = VGroup(big, sub).move_to(ORIGIN + UP * 0.8)

        # 标题旋入
        self.play(SpinInFromNothing(big, run_time=1.8))
        self.play(fade_in_up(sub, shift=0.5), run_time=1.0)

        # 上方方法论 chips
        logos = ["5Why", "5W2H", "SWOT", "PEST", "KANO", "MAT", "PDCA"]
        chips = VGroup(*[
            RoundedRectangle(
                corner_radius=0.15, width=1.3, height=0.55,
                stroke_color=C_TEXT_DIM, stroke_width=1.5,
                fill_color=C_BLUE_DEEP, fill_opacity=0.15,
            ) for _ in logos
        ])
        chip_labels = VGroup(*[cn(w, size=20, color=C_TEXT) for w in logos])
        for c, l in zip(chips, chip_labels):
            l.move_to(c)
        chip_group = VGroup(*[VGroup(c, l) for c, l in zip(chips, chip_labels)])
        chip_group.arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.5)
        self.play(LaggedStartMap(FadeIn, chip_group, shift=DOWN * 0.3, lag_ratio=0.1), run_time=2.0)

        # 三张核心卡
        pillars = [("① 根本", C_YELLOW), ("② 角度", C_BLUE), ("③ 结构化", C_GREEN)]
        cards = VGroup()
        for text, color in pillars:
            card = RoundedRectangle(
                corner_radius=0.2, width=3.3, height=1.5,
                stroke_color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.08,
            )
            lbl = cn_bold(text, size=40, color=color).move_to(card)
            cards.add(VGroup(card, lbl))
        cards.arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.9)

        # 卡片逐张翻转入场
        for card in cards:
            card.save_state()
            card.scale(0).rotate(PI / 2)
        self.play(
            LaggedStart(*[Succession(
                card.animate.restore(),
            ) for card in cards], lag_ratio=0.3),
            run_time=2.5,
        )
        self.wait(2.0)

        # 相机稍微后拉展示全景
        self.play(
            self.camera.frame.animate.scale(1.1),
            run_time=1.0,
        )
        self.wait(1.0)
        self.play(
            FadeOut(VGroup(head, chip_group, cards), shift=UP),
            self.camera.frame.animate.scale(1 / 1.1),
            run_time=1.2,
        )


    # ================================================================
    # 2. PILLAR ONE · 根本（约 2.5 分钟）
    # ================================================================
    def pillar_one_root(self):
        chapter_card(self, "第一板斧", "根本", "根本定义 · 根本目的 · 根本原因")

        # 顶部标签
        tag = cn_bold("① 根本", size=34, color=C_YELLOW)
        tag_box = highlight_box(tag, color=C_YELLOW, opacity=0.22, pad=0.25)
        head = VGroup(tag_box, tag).to_edge(UP, buff=0.5)
        self.play(FadeIn(head, shift=DOWN * 0.3), run_time=0.8)

        # 三行要点 — 逐条带动画
        items = VGroup(
            bullet("根本定义：它到底是什么？边界在哪里？"),
            bullet("根本目的：为什么要做？终极指向是什么？"),
            bullet("根本原因：到底什么力量在驱动这个结果？"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.8)

        for it in items:
            self.play(
                fade_in_up(it, shift=0.3),
                run_time=0.8,
            )
            self.wait(0.8)

        self.wait(1.0)
        self.play(FadeOut(items, shift=LEFT * 2), run_time=0.8)

        # --- 股票案例 ---
        # 坐标轴：带随机噪声的股价曲线
        ax = Axes(
            x_range=[0, 12, 1], y_range=[0, 6, 1],
            x_length=6, y_length=3.2,
            tips=False,
            axis_config={"stroke_color": C_TEXT_DIM, "include_numbers": False},
        ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax_title = cn("股价", size=22, color=C_TEXT_DIM).next_to(ax, UP, buff=0.1)

        # 带噪声的曲线
        rng = np.random.default_rng(42)
        noise = rng.normal(0, 0.15, size=100)

        def stock_curve(x):
            idx = int(min(x / 12 * 99, 99))
            return 1.5 + 0.3 * x + 0.8 * np.sin(x * 0.7) + noise[idx]

        curve = ax.plot(stock_curve, x_range=[0, 12], color=C_GREEN, stroke_width=3)

        # 预期线（虚线）
        expectation_line = ax.plot(
            lambda x: 1.5 + 0.3 * x,
            x_range=[0, 12], color=C_TEXT_DIM, stroke_width=2,
        )
        expectation_line.set_stroke(opacity=0.5)
        exp_label = cn("市场预期", size=18, color=C_TEXT_DIM).next_to(
            ax.c2p(11, 1.5 + 0.3 * 11), UP, buff=0.15
        )

        self.play(Create(ax, run_time=1.5), Write(ax_title, run_time=0.8))
        self.play(Create(curve, run_time=3.0))
        self.wait(0.5)
        self.play(Create(expectation_line, run_time=1.5), Write(exp_label, run_time=0.8))
        self.wait(1.0)

        # 右侧：信心节点图
        confidence = cn_bold("信 心", size=44, color=C_YELLOW).shift(RIGHT * 3.0 + UP * 0.5)
        conf_box = highlight_box(confidence, pad=0.2)
        self.play(
            DrawBorderThenFill(conf_box, run_time=1.0),
            Write(confidence, run_time=1.2),
        )

        sources = [("财报", C_BLUE), ("舆论", C_PURPLE), ("满意度", C_ORANGE)]
        src_mobs = VGroup()
        for t, c in sources:
            m = cn(t, size=28, color=c)
            src_mobs.add(m)
        src_mobs.arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(confidence, RIGHT, buff=1.5)

        arrows = VGroup()
        for m in src_mobs:
            a = Arrow(m.get_left(), confidence.get_right(),
                      buff=0.15, stroke_width=3, color=C_TEXT_DIM,
                      max_tip_length_to_length_ratio=0.1)
            arrows.add(a)

        self.play(
            LaggedStart(*[fade_in_up(m) for m in src_mobs], lag_ratio=0.3),
            run_time=2.0,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3),
            run_time=2.0,
        )

        # 信心 → 股价
        to_price = Arrow(
            confidence.get_left(), ax.c2p(8, stock_curve(8)),
            buff=0.2, stroke_width=4, color=C_YELLOW,
            max_tip_length_to_length_ratio=0.08,
        )
        self.play(GrowArrow(to_price, run_time=1.5))
        self.wait(1.5)

        # 反转句
        punch = cn_bold("财报好 ≠ 股价涨", size=42, color=C_RED)
        punch.to_edge(DOWN, buff=0.9)
        self.play(fade_in_up(punch), run_time=1.0)
        self.play(Flash(punch, color=C_RED, flash_radius=1.5, run_time=0.8))
        self.play(Circumscribe(punch, color=C_RED, run_time=1.2))
        self.wait(2.0)

        # 清场
        all_stock = VGroup(ax, ax_title, curve, expectation_line, exp_label,
                           conf_box, confidence, src_mobs, arrows, to_price, punch)
        self.play(FadeOut(all_stock, shift=DOWN), run_time=1.2)

        # --- App 案例 ---
        chain_items = ["氛围", "停留", "浏览", "成交"]
        chain_colors = [C_BLUE, C_GREEN, C_ORANGE, C_YELLOW]
        chain_boxes = VGroup()
        chain_arrows = VGroup()

        for i, (text, color) in enumerate(zip(chain_items, chain_colors)):
            box = RoundedRectangle(
                corner_radius=0.12, width=2.0, height=0.9,
                stroke_color=color, stroke_width=2.5,
                fill_color=color, fill_opacity=0.1,
            )
            lbl = cn_bold(text, size=28, color=color).move_to(box)
            chain_boxes.add(VGroup(box, lbl))

        chain_boxes.arrange(RIGHT, buff=1.0).move_to(ORIGIN + UP * 0.3)

        for i in range(len(chain_boxes) - 1):
            a = Arrow(
                chain_boxes[i][0].get_right(), chain_boxes[i + 1][0].get_left(),
                buff=0.1, stroke_width=3, color=C_TEXT_DIM,
                max_tip_length_to_length_ratio=0.12,
            )
            chain_arrows.add(a)

        self.play(
            LaggedStart(*[DrawBorderThenFill(b) for b in chain_boxes], lag_ratio=0.3),
            run_time=3.0,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in chain_arrows], lag_ratio=0.3),
            run_time=2.0,
        )

        # 高亮最后一个
        self.play(
            Indicate(chain_boxes[-1], color=C_YELLOW, scale_factor=1.15),
            run_time=1.2,
        )

        q = cn_bold("如果成交没涨——所有动作都是自嗨。", size=32, color=C_YELLOW)
        q.to_edge(DOWN, buff=0.6)
        self.play(Write(q, run_time=1.5))
        self.wait(2.0)

        self.play(FadeOut(VGroup(head, chain_boxes, chain_arrows, q), shift=UP), run_time=1.0)


    # ================================================================
    # 3. PILLAR TWO · 角度（约 2.5 分钟）
    # ================================================================
    def pillar_two_angle(self):
        chapter_card(self, "第二板斧", "不同角度", "身份 · 时代 · 抽象层次")

        tag = cn_bold("② 角度", size=34, color=C_BLUE)
        tag_box = highlight_box(tag, color=C_BLUE, opacity=0.22, pad=0.25)
        head = VGroup(tag_box, tag).to_edge(UP, buff=0.5)
        self.play(FadeIn(head, shift=DOWN * 0.3), run_time=0.8)

        # 中央问题圆
        center = Circle(radius=0.8, color=C_TEXT, fill_opacity=0.05, stroke_width=2)
        center_lbl = cn_bold("问题", size=30, color=C_TEXT).move_to(center)
        problem = VGroup(center, center_lbl)
        self.play(
            GrowFromCenter(center, run_time=1.2),
            Write(center_lbl, run_time=1.0),
        )

        # 三个角度 — 从中心发射
        angles_data = [
            ("身份角度", C_BLUE, np.array([-4.5, 1.5, 0]), "用户 · 供应商 · 平台"),
            ("时代角度", C_GREEN, np.array([4.5, 1.5, 0]), "卖方说 → 买方说"),
            ("抽象层次", C_PURPLE, np.array([0, -2.8, 0]), "现象 → 规律 → 元规律"),
        ]

        node_groups = []
        for t, c, pos, sub in angles_data:
            box = RoundedRectangle(
                corner_radius=0.15, width=3.6, height=1.4,
                stroke_color=c, stroke_width=2.5,
                fill_color=c, fill_opacity=0.08,
            ).move_to(pos)
            name = cn_bold(t, size=26, color=c).move_to(box.get_top() + DOWN * 0.35)
            sub_t = cn(sub, size=20, color=C_TEXT_DIM).move_to(box.get_bottom() + UP * 0.35)
            node = VGroup(box, name, sub_t)
            node_groups.append(node)

            # 从中心发射箭头 + 节点
            a = Arrow(
                problem.get_center(), box.get_center(),
                buff=0.9, stroke_width=3, color=c,
                max_tip_length_to_length_ratio=0.08,
            )
            self.play(
                GrowArrow(a, run_time=1.0),
                FadeIn(node, shift=(pos - ORIGIN) * 0.1, run_time=1.2),
            )
            self.wait(0.8)

        self.wait(1.5)

        # --- 抽象层次动画：阶梯 ---
        self.play(FadeOut(VGroup(problem, *node_groups), shift=UP * 0.5), run_time=0.8)

        levels = ["具体现象", "规律", "元规律", "数学公式"]
        colors = [C_TEXT_DIM, C_BLUE, C_PURPLE, C_YELLOW]
        stairs = VGroup()
        for i, (lv, c) in enumerate(zip(levels, colors)):
            step = RoundedRectangle(
                corner_radius=0.1,
                width=4.0 - i * 0.6,
                height=0.8,
                stroke_color=c, stroke_width=2,
                fill_color=c, fill_opacity=0.12,
            )
            lbl = cn(lv, size=24, color=c).move_to(step)
            stairs.add(VGroup(step, lbl))

        stairs.arrange(UP, buff=0.15).move_to(ORIGIN)

        for i, stair in enumerate(stairs):
            self.play(
                fade_in_up(stair, shift=0.4),
                run_time=0.8,
            )
            if i > 0:
                # 连接箭头
                a = Arrow(
                    stairs[i - 1].get_top(), stair.get_bottom(),
                    buff=0.05, stroke_width=2, color=colors[i],
                    max_tip_length_to_length_ratio=0.15,
                )
                self.play(GrowArrow(a, run_time=0.5))
            self.wait(0.5)

        conclusion = cn_bold("每升高一层：变量更少，通用性更强。",
                             size=30, color=C_YELLOW).to_edge(DOWN, buff=0.5)
        self.play(Write(conclusion, run_time=1.5))
        self.play(Indicate(conclusion, color=C_YELLOW, run_time=1.0))
        self.wait(2.0)

        # 相机缓慢推近阶梯顶端
        self.play(
            self.camera.frame.animate.scale(0.8).move_to(stairs[-1]),
            run_time=2.0,
        )
        self.wait(1.0)
        self.play(
            self.camera.frame.animate.scale(1 / 0.8).move_to(ORIGIN),
            run_time=1.5,
        )

        self.play(FadeOut(VGroup(head, stairs, conclusion), shift=UP), run_time=1.0)


    # ================================================================
    # 4. PILLAR THREE · 结构化拆解（约 2 分钟）
    # ================================================================
    def pillar_three_structure(self):
        chapter_card(self, "第三板斧", "结构化拆解", "不重不漏 · 按维度切")

        tag = cn_bold("③ 结构化", size=34, color=C_GREEN)
        tag_box = highlight_box(tag, color=C_GREEN, opacity=0.22, pad=0.25)
        head = VGroup(tag_box, tag).to_edge(UP, buff=0.5)
        self.play(FadeIn(head, shift=DOWN * 0.3), run_time=0.8)

        # 顶部问题
        root = RoundedRectangle(
            corner_radius=0.15, width=4.0, height=1.0,
            stroke_color=C_TEXT, stroke_width=2,
            fill_color=C_BLUE_DEEP, fill_opacity=0.15,
        )
        root_lbl = cn_bold("打车 · 搜索无结果", size=28, color=C_TEXT).move_to(root)
        top = VGroup(root, root_lbl).to_edge(UP, buff=1.8)
        self.play(DrawBorderThenFill(root, run_time=1.0), Write(root_lbl, run_time=1.0))

        # 三个子维度
        dims = [
            ("地点", "没有运力覆盖", C_BLUE),
            ("时间", "高峰全被占用", C_ORANGE),
            ("用户", "被风控拦截", C_RED),
        ]
        children = VGroup()
        for name, sub, c in dims:
            box = RoundedRectangle(
                corner_radius=0.12, width=3.2, height=1.5,
                stroke_color=c, stroke_width=2.5,
                fill_color=c, fill_opacity=0.1,
            )
            n = cn_bold(name, size=28, color=c).move_to(box.get_top() + DOWN * 0.4)
            s = cn(sub, size=20, color=C_TEXT_DIM).move_to(box.get_bottom() + UP * 0.35)
            children.add(VGroup(box, n, s))
        children.arrange(RIGHT, buff=0.5).next_to(top, DOWN, buff=1.5)

        # 连线 + 子节点逐个展开
        lines = VGroup()
        for child in children:
            line = Line(
                top.get_bottom(), child[0].get_top(),
                stroke_color=C_TEXT_DIM, stroke_width=2,
            )
            lines.add(line)

        for i, (line, child) in enumerate(zip(lines, children)):
            self.play(
                Create(line, run_time=0.8),
                DrawBorderThenFill(child[0], run_time=1.0),
                Write(child[1], run_time=0.8),
                fade_in_up(child[2], shift=0.2),
                run_time=1.2,
            )
            self.wait(0.6)

        # MECE 视觉：三个块合起来 = 覆盖全部
        mece_bar = Rectangle(
            width=children.width + 0.4, height=0.08,
            fill_color=C_GREEN, fill_opacity=0.8, stroke_width=0,
        ).next_to(children, DOWN, buff=0.3)
        mece_lbl = cn_bold("M E C E ：不重叠 · 全覆盖",
                           size=26, color=C_GREEN).next_to(mece_bar, DOWN, buff=0.2)

        self.play(
            Create(mece_bar, run_time=1.5),
            Write(mece_lbl, run_time=1.2),
        )
        self.wait(1.5)

        # 总结句
        punch = cn_bold("先根本，再角度，最后拆解。三步到位。",
                        size=36, color=C_YELLOW).move_to(ORIGIN + DOWN * 2.8)
        self.play(FadeOut(VGroup(top, children, lines, mece_bar, mece_lbl), run_time=0.8))
        self.play(Write(punch, run_time=1.5))
        self.play(
            Indicate(punch, color=C_YELLOW, scale_factor=1.08, run_time=1.0),
            Flash(punch, color=C_YELLOW, flash_radius=2.0, run_time=0.8),
        )
        self.wait(2.0)
        self.play(FadeOut(VGroup(head, punch), shift=UP), run_time=1.0)

    # ================================================================
    # 5. SYNTHESIS — 综合演练（约 1.5 分钟）
    # ================================================================
    def synthesis(self):
        chapter_card(self, "综合演练", "回到开场那三题", "三板斧上场")

        rows_data = [
            ("先有鸡还是先有蛋？", "① 根本定义", "定义清楚 ⇒ 先有蛋。", C_YELLOW),
            ("12 球找异常？", "③ 结构化拆解", "3³=27 > 24，三等分切。", C_GREEN),
            ("作文如何破题？", "② 角度", "选穿透力最强的角度展开。", C_BLUE),
        ]

        all_rows = VGroup()
        for q, method, answer, c in rows_data:
            # 问题
            tq = cn_bold(q, size=28, color=C_TEXT)
            # 方法标签
            tag = RoundedRectangle(
                corner_radius=0.1, width=2.4, height=0.6,
                stroke_color=c, stroke_width=2,
                fill_color=c, fill_opacity=0.15,
            )
            tag_lbl = cn(method, size=20, color=c).move_to(tag)
            tag_grp = VGroup(tag, tag_lbl).next_to(tq, RIGHT, buff=0.5)
            # 答案
            ta = cn(answer, size=22, color=C_TEXT_DIM).next_to(tag_grp, RIGHT, buff=0.5)
            row = VGroup(tq, tag_grp, ta)
            all_rows.add(row)

        all_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.8).move_to(ORIGIN)

        for row in all_rows:
            self.play(
                LaggedStart(
                    fade_in_up(row[0]),
                    DrawBorderThenFill(row[1][0]),
                    Write(row[1][1]),
                    fade_in_up(row[2]),
                    lag_ratio=0.2,
                ),
                run_time=2.0,
            )
            self.wait(1.2)

        self.wait(2.0)
        self.play(FadeOut(all_rows, shift=DOWN * 0.5), run_time=1.0)

    # ================================================================
    # 6. OUTRO（约 30 秒）
    # ================================================================
    def outro(self):
        # 三板斧合体
        pillars = [("根本", C_YELLOW), ("角度", C_BLUE), ("结构化", C_GREEN)]
        final_cards = VGroup()
        for text, color in pillars:
            card = RoundedRectangle(
                corner_radius=0.15, width=2.5, height=1.2,
                stroke_color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.12,
            )
            lbl = cn_bold(text, size=32, color=color).move_to(card)
            final_cards.add(VGroup(card, lbl))
        final_cards.arrange(RIGHT, buff=0.4).move_to(ORIGIN + UP * 1.0)

        # 连接箭头形成链
        chain_arrows = VGroup()
        for i in range(2):
            a = Arrow(
                final_cards[i][0].get_right(), final_cards[i + 1][0].get_left(),
                buff=0.08, stroke_width=4, color=C_TEXT_DIM,
                max_tip_length_to_length_ratio=0.12,
            )
            chain_arrows.add(a)

        self.play(
            LaggedStart(*[SpinInFromNothing(c, run_time=1.5) for c in final_cards], lag_ratio=0.3),
            run_time=3.0,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in chain_arrows], lag_ratio=0.3),
            run_time=1.5,
        )
        self.wait(1.5)

        # 总金句
        slogan = cn_bold("先问根本 → 再换角度 → 最后结构化拆解。",
                         size=38, color=C_YELLOW).next_to(final_cards, DOWN, buff=1.0)
        self.play(Write(slogan, run_time=2.0))
        self.play(Indicate(slogan, color=C_YELLOW, run_time=1.0))
        self.wait(2.0)

        # 下集预告
        teaser = cn("下集预告 · 自然启蒙：什么在变，什么不变？",
                    size=28, color=C_BLUE).next_to(slogan, DOWN, buff=0.6)
        self.play(fade_in_up(teaser), run_time=1.2)
        self.wait(3.0)

        # 最终淡出
        self.play(
            FadeOut(VGroup(final_cards, chain_arrows, slogan, teaser)),
            run_time=2.0,
        )
        self.wait(1.0)
