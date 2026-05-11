# MainmCE · 启蒙思考频道

一个模仿 **3Blue1Brown** 的中文知识视频项目，聚焦于**方法论与思考**。
全部动画使用 [Manim Community Edition](https://www.manim.community/) 制作。

## 系列规划

| 系列 | 主题 | 核心问题 |
| --- | --- | --- |
| 如何思考 | 方法论 | 上学/工作中遇到相同知识，为什么有人能做题、有人做不了？ |
| 自然启蒙 | 物理/生物/化学 | 世界上什么在变，什么不变？变与不变之下的恒量。 |
| 数学启蒙 | 描述世界的语言 | 数学怎样成为描述规律的通用工具？ |
| 社会启蒙 | 社会/价值观 | 个体的价值观如何涌现为群体秩序？ |

每集 ≈ 10 分钟，自洽独立，但互相呼应。

## 方法论三板斧（贯穿全频道）

1. **根本** — 根本定义 / 根本目的 / 根本原因
2. **不同角度** — 身份角度 / 时代角度 / 抽象层次角度
3. **结构化拆解** — 在 1 和 2 的基础上，按任意维度切得干净

## 仓库结构

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── theme.py                    # 统一配色、字体、转场、Logo
├── ep01_how_to_think/
│   ├── script.md               # 分镜脚本（画面 + 节拍）
│   ├── narration.md            # 中文旁白（可直接对着念）
│   └── scene.py                # ManimCE 代码
├── ep02_nature/
├── ep03_math/
└── ep04_society/
```

## 本地运行

```bash
pip install -r requirements.txt
# 预览：
manim -pql ep01_how_to_think/scene.py HowToThink
# 高清出片：
manim -qh ep01_how_to_think/scene.py HowToThink
```

## 字体

脚本默认使用 `Source Han Sans CN` / `Noto Sans CJK SC`。若本机没装，
请在 `theme.py` 里改 `CJK_FONT` 为你已安装的中文字体。

## 许可

内容（脚本/旁白）CC BY-NC-SA 4.0，代码 MIT。
