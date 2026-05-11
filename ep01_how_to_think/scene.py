"""
EP01 · 如何思考：根本 / 角度 / 结构化拆解
渲染：manim -pql ep01_how_to_think/scene.py HowToThink
"""

from __future__ import annotations

import sys
from pathlib import Path

# 允许从仓库根导入 theme.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from manim import (
    Scene, MoveAlongPath, GrowArrow, GrowFromCenter,
    Circle, Square, Triangle, RegularPolygon,
    NumberPlane, Axes, ParametricFunction,
    Rotate, Indicate, Flash,
    RIGHT as R, LEFT as L, UP as U, DOWN as D,
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


class HowToThink(Scene):
    """主场景：从冷开场一路到片尾。"""

    def construct(self):
        self.add(footer(SERIES, EPISODE))
        self.cold_open()
        self.title_card()
        self.pillar_one_root()
        self.pillar_two_angle()
        self.pillar_three_structure()
        self.synthesis()
        self.outro()

    # ---------- 0. Cold Open ----------
    def cold_open(self):
        qs = [
            "先有鸡，还是先有蛋？",
            "没砝码，用天平称三次，12 个球里找出质量异常那一个。",
            "作文题给你几张图，你怎么破题？",
        ]
        for q in qs:
            t = cn(q, size=44, color=C_TEXT)
            self.play(fade_in_up(t), run_time=0.55)
            self.wait(0.9)
            self.play(FadeOut(t, shift=UP * 0.3), run_time=0.4)

        hook = cn_bold("同样的知识，", size=52, color=C_TEXT)
        hook2 = cn_bold("为什么有人能用，有人用不出？", size=52, color=C_YELLOW)
        hook2.next_to(hook, DOWN, buff=0.35)
        grp = VGroup(hook, hook2).move_to(ORIGIN)
        self.play(Write(hook), run_time=0.9)
        self.play(Write(hook2), run_time=1.0)
        self.wait(1.4)
        self.play(FadeOut(grp))

    # ---------- 1. Title Card ----------
    def title_card(self):
        big = cn_bold("如何思考", size=96, color=C_BLUE)
        sub = cn("方法论三板斧", size=36, color=C_TEXT_DIM)
        sub.next_to(big, DOWN, buff=0.35)
        head = VGroup(big, sub).move_to(ORIGIN + UP * 0.8)

        self.play(Write(big), run_time=1.0)
        self.play(fade_in_up(sub))

        # 上方 logos
        logos = ["5Why", "5W2H", "SWOT", "PEST", "KANO", "MAT", "PDCA"]
        chips = VGroup(*[
            RoundedRectangle(
                corner_radius=0.15, width=1.2, height=0.55,
                stroke_color=C_TEXT_DIM, stroke_width=1.5,
                fill_color=C_BLUE_DEEP, fill_opacity=0.15,
            ) for _ in logos
        ])
        chip_labels = VGroup(*[cn(w, size=22, color=C_TEXT) for w in logos])
        for c, l in zip(chips, chip_labels):
            l.move_to(c)
        chip_group = VGroup(*[VGroup(c, l) for c, l in zip(chips, chip_labels)])
        chip_group.arrange(RIGHT, buff=0.22).to_edge(UP, buff=0.6)
        self.play(FadeIn(chip_group, lag_ratio=0.08), run_time=1.2)

        # 三张小卡
        pillars = [("① 根本", C_YELLOW),
                   ("② 角度", C_BLUE),
                   ("③ 结构化", C_GREEN)]
        cards = VGroup()
        for text, color in pillars:
            card = RoundedRectangle(
                corner_radius=0.2, width=3.3, height=1.5,
                stroke_color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.08,
            )
            lbl = cn_bold(text, size=40, color=color).move_to(card)
            cards.add(VGroup(card, lbl))
        cards.arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.8)
        self.play(AnimationGroup(*[fade_in_up(c) for c in cards], lag_ratio=0.2))
        self.wait(1.2)

        self.play(FadeOut(VGroup(head, chip_group, cards)))

    # ---------- 2. Pillar One · 根本 ----------
    def pillar_one_root(self):
        chapter_card(self, "第一板斧", "根本", "根本定义 · 根本目的 · 根本原因")

        # 顶部标签条
        tag = cn_bold("① 根本", size=34, color=C_YELLOW)
        tag_box = highlight_box(tag, color=C_YELLOW, opacity=0.22, pad=0.25)
        head = VGroup(tag_box, tag).to_edge(UP, buff=0.5)
        self.play(FadeIn(head))

        items = VGroup(
            bullet("根本定义：它到底是什么？"),
            bullet("根本目的：为什么要做？"),
            bullet("根本原因：真正驱动它的是什么？"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.7)
        for it in items:
            self.play(fade_in_up(it, shift=0.2), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(items))

        # 股票案例：财报 / 舆论 / 满意度 → 信心 → 股价
        ax = Axes(
            x_range=[0, 10, 1], y_range=[0, 5, 1],
            x_length=5, y_length=2.6,
            tips=False,
            axis_config={"stroke_color": C_TEXT_DIM, "include_numbers": False},
        ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        curve = ax.plot(lambda x: 1 + 0.35 * x + 0.5 * np.sin(x * 0.9),
                        x_range=[0, 10], color=C_GREEN)
        ax_title = cn("股价", size=22, color=C_TEXT_DIM).next_to(ax, UP, buff=0.1)
        self.play(Create(ax), Write(ax_title))
        self.play(Create(curve), run_time=1.4)

        confidence = cn_bold("信 心", size=44, color=C_YELLOW).shift(RIGHT * 2.2 + UP * 0.4)
        conf_box = highlight_box(confidence, pad=0.2)
        self.play(FadeIn(conf_box), Write(confidence))

        # 三个来源
        sources = [("财报", C_BLUE), ("舆论", C_PURPLE), ("满意度", C_ORANGE)]
        src_mobs = VGroup()
        for i, (t, c) in enumerate(sources):
            m = cn(t, size=28, color=c)
            src_mobs.add(m)
        src_mobs.arrange(DOWN, aligned_edge=LEFT, buff=0.55).next_to(confidence, RIGHT, buff=1.2)

        arrows = VGroup()
        for m in src_mobs:
            a = Arrow(m.get_left(), confidence.get_right(),
                      buff=0.15, stroke_width=3, color=C_TEXT_DIM,
                      max_tip_length_to_length_ratio=0.1)
            arrows.add(a)

        self.play(AnimationGroup(*[fade_in_up(m) for m in src_mobs], lag_ratio=0.15))
        self.play(AnimationGroup(*[GrowArrow(a) for a in arrows], lag_ratio=0.15))

        # 信心 → 股价
        to_price = Arrow(
            confidence.get_left(), ax.c2p(6, 3.5),
            buff=0.2, stroke_width=4, color=C_YELLOW,
            max_tip_length_to_length_ratio=0.08,
        )
        self.play(GrowArrow(to_price))
        self.wait(0.4)

        # 反转：财报好 ≠ 股价涨
        punch = cn_bold("财报好 ≠ 股价涨", size=38, color=C_RED).to_edge(DOWN, buff=1.1)
        self.play(fade_in_up(punch))
        self.play(Flash(punch, color=C_RED, flash_radius=1.2))
        self.wait(1.0)
        self.play(FadeOut(VGroup(ax, ax_title, curve, conf_box, confidence,
                                 src_mobs, arrows, to_price, punch)))

        # app 案例文字帧
        q1 = cn("很多人做 app，第一反应是——设计页面。", size=34, color=C_TEXT)
        q2 = cn_bold("加氛围、加点击，到底是为了啥？", size=42, color=C_YELLOW)
        q3 = cn("先想清根本目的，再谈动作。", size=32, color=C_TEXT_DIM)
        grp = VGroup(q1, q2, q3).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(Write(q1))
        self.wait(0.4)
        self.play(Write(q2))
        self.play(Indicate(q2, color=C_YELLOW, scale_factor=1.06))
        self.play(fade_in_up(q3))
        self.wait(1.0)
        self.play(FadeOut(VGroup(head, grp)))

    # ---------- 3. Pillar Two · 角度 ----------
    def pillar_two_angle(self):
        chapter_card(self, "第二板斧", "不同角度", "身份 · 时代 · 抽象层次")

        tag = cn_bold("② 角度", size=34, color=C_BLUE)
        tag_box = highlight_box(tag, color=C_BLUE, opacity=0.22, pad=0.25)
        head = VGroup(tag_box, tag).to_edge(UP, buff=0.5)
        self.play(FadeIn(head))

        # 中央"问题"圈
        center = Circle(radius=0.7, color=C_TEXT, fill_opacity=0.1)
        center_lbl = cn_bold("问题", size=28, color=C_TEXT).move_to(center)
        problem = VGroup(center, center_lbl)
        self.play(Create(center), Write(center_lbl))

        # 三个角度放在三角位置
        angles = [
            ("身份角度", C_BLUE, np.array([-4.2, 1.1, 0]), "用户 / 供应商 / 平台"),
            ("时代角度", C_GREEN, np.array([4.2, 1.1, 0]), "卖方说 → 买方说"),
            ("抽象层次", C_PURPLE, np.array([0, -2.3, 0]), "具体 → 规律 → 规律的规律"),
        ]
        nodes = []
        for t, c, pos, sub in angles:
            box = RoundedRectangle(corner_radius=0.15, width=3.4, height=1.2,
                                   stroke_color=c, stroke_width=2.5,
                                   fill_color=c, fill_opacity=0.08).move_to(pos)
            name = cn_bold(t, size=28, color=c).move_to(box.get_top() + DOWN * 0.3)
            sub_t = cn(sub, size=20, color=C_TEXT_DIM).move_to(box.get_bottom() + UP * 0.3)
            node = VGroup(box, name, sub_t)
            nodes.append(node)

        for n in nodes:
            a = Arrow(problem.get_center(), n[0].get_center(),
                      buff=0.8, stroke_width=3, color=C_TEXT_DIM,
                      max_tip_length_to_length_ratio=0.08)
            self.play(GrowArrow(a), FadeIn(n), run_time=0.55)
        self.wait(0.8)

        # 时代角度动画：箭头反转
        era_note = cn("上个时代：卖家告诉买家「我有什么」", size=24, color=C_TEXT_DIM)
        era_note.to_edge(DOWN, buff=1.1)
        self.play(fade_in_up(era_note))
        self.wait(0.7)
        era_note2 = cn_bold("这个时代：买家先说「我要什么」", size=28, color=C_GREEN)
        era_note2.move_to(era_note)
        self.play(ReplacementTransform(era_note, era_note2))
        self.wait(0.9)
        self.play(FadeOut(era_note2))

        # 抽象层次动画：数据点 → 曲线 → 公式
        ax = Axes(x_range=[-1, 6, 1], y_range=[-1, 5, 1], x_length=4, y_length=2.8,
                  tips=False,
                  axis_config={"stroke_color": C_TEXT_DIM}).to_edge(DOWN, buff=0.8).shift(LEFT * 3)
        pts = VGroup(*[Dot(ax.c2p(x, 0.3 * x * x), color=C_YELLOW, radius=0.06)
                       for x in np.linspace(0.2, 5, 7)])
        curve = ax.plot(lambda x: 0.3 * x * x, x_range=[0, 5], color=C_YELLOW)
        eqn = cn_bold("y = a x²", size=36, color=C_YELLOW).next_to(ax, RIGHT, buff=1.2)
        self.play(Create(ax))
        self.play(AnimationGroup(*[FadeIn(p, scale=0.5) for p in pts], lag_ratio=0.1))
        self.play(Create(curve))
        self.play(fade_in_up(eqn))
        sub_ = cn("每升高一层抽象，变量越少、通用性越强。",
                  size=24, color=C_TEXT_DIM).to_edge(DOWN, buff=0.3)
        self.play(fade_in_up(sub_))
        self.wait(1.1)

        self.play(FadeOut(VGroup(head, problem, *nodes, ax, pts, curve, eqn, sub_)))

    # ---------- 4. Pillar Three · 结构化 ----------
    def pillar_three_structure(self):
        chapter_card(self, "第三板斧", "结构化拆解", "不重不漏，按维度切")

        tag = cn_bold("③ 结构化", size=34, color=C_GREEN)
        tag_box = highlight_box(tag, color=C_GREEN, opacity=0.22, pad=0.25)
        head = VGroup(tag_box, tag).to_edge(UP, buff=0.5)
        self.play(FadeIn(head))

        # 顶部"问题"
        root = RoundedRectangle(corner_radius=0.15, width=3.5, height=0.9,
                                stroke_color=C_TEXT, stroke_width=2,
                                fill_color=C_BLUE_DEEP, fill_opacity=0.15)
        root_lbl = cn_bold("打车 · 无结果", size=28, color=C_TEXT).move_to(root)
        top = VGroup(root, root_lbl).to_edge(UP, buff=1.8)
        self.play(FadeIn(top, shift=DOWN * 0.2))

        # 三个子维度
        dims = [("地点", "没运力", C_BLUE),
                ("用车时间", "高峰期", C_ORANGE),
                ("人不符", "被风控", C_RED)]
        children = VGroup()
        for name, sub, c in dims:
            box = RoundedRectangle(corner_radius=0.12, width=3.0, height=1.3,
                                   stroke_color=c, stroke_width=2.5,
                                   fill_color=c, fill_opacity=0.1)
            n = cn_bold(name, size=28, color=c).move_to(box.get_top() + DOWN * 0.35)
            s = cn(sub, size=22, color=C_TEXT_DIM).move_to(box.get_bottom() + UP * 0.3)
            children.add(VGroup(box, n, s))
        children.arrange(RIGHT, buff=0.6).next_to(top, DOWN, buff=1.3)

        lines = VGroup(*[
            Line(top.get_bottom(), child[0].get_top(),
                 stroke_color=C_TEXT_DIM, stroke_width=2)
            for child in children
        ])
        self.play(AnimationGroup(
            Create(lines, lag_ratio=0.2),
            AnimationGroup(*[fade_in_up(c) for c in children], lag_ratio=0.15),
        ), run_time=1.6)

        # MECE 提示
        mece = cn_bold("M E C E", size=28, color=C_GREEN)
        mece_sub = cn("不重叠 · 全覆盖", size=22, color=C_TEXT_DIM)
        g = VGroup(mece, mece_sub).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.7)
        self.play(Write(mece), fade_in_up(mece_sub))
        self.wait(1.1)

        # 根本 + 角度 → 才谈拆解
        punch = cn_bold("先根本，再角度，最后拆解。", size=38, color=C_YELLOW).move_to(ORIGIN)
        self.play(FadeOut(VGroup(top, children, lines, mece_sub, mece)))
        self.play(Write(punch))
        self.play(Indicate(punch, color=C_YELLOW))
        self.wait(1.0)
        self.play(FadeOut(VGroup(head, punch)))

    # ---------- 5. Synthesis ----------
    def synthesis(self):
        chapter_card(self, "综合演练", "回到开场那三题", "三板斧上场")

        rows = [
            ("先有鸡还是先有蛋？", "① 根本定义：你问的鸡是什么？", "基因突变体 ⇒ 先有蛋。", C_YELLOW),
            ("12 球找异常那一个？", "③ 结构化拆解：3³ = 27 > 12", "按三等分切，三次搞定。", C_GREEN),
            ("作文如何破题？", "② 角度：身份 / 时代 / 抽象", "选最能展开那个。", C_BLUE),
        ]
        row_mobjs = VGroup()
        for q, m, a, c in rows:
            tq = cn_bold(q, size=28, color=C_TEXT)
            tm = cn(m, size=24, color=c).next_to(tq, RIGHT, buff=0.4)
            ta = cn(a, size=24, color=C_TEXT_DIM).next_to(tm, RIGHT, buff=0.4)
            row_mobjs.add(VGroup(tq, tm, ta))
        row_mobjs.arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to(ORIGIN)

        for row in row_mobjs:
            self.play(fade_in_up(row), run_time=0.8)
            self.wait(0.6)

        self.wait(0.8)
        self.play(FadeOut(row_mobjs))

    # ---------- 6. Outro ----------
    def outro(self):
        t1 = cn("三板斧，记牢了：", size=36, color=C_TEXT_DIM)
        t2 = cn_bold("根本 → 角度 → 结构化拆解", size=52, color=C_YELLOW)
        t2.next_to(t1, DOWN, buff=0.4)
        grp = VGroup(t1, t2).move_to(ORIGIN + UP * 0.4)
        self.play(Write(t1))
        self.play(Write(t2))
        self.wait(1.2)

        teaser = cn("下集预告 · 自然启蒙：什么在变，什么不变？",
                    size=28, color=C_BLUE).next_to(grp, DOWN, buff=1.0)
        self.play(fade_in_up(teaser))
        self.wait(2.0)
        self.play(FadeOut(VGroup(grp, teaser)))
