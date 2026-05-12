# 第 04 集 · 分镜脚本 · 打磨版

> 时长：约 12 分钟 | 面向观众：对"为什么社会是这样"好奇的人
> 一句话价值：**社会秩序不是被设计出来的——它是个体、交互、激励叠加后的自发涌现。**

---

## 一、节拍表

| # | 时间 | 旁白主题 | 画面关键帧 | ManimCE Scene |
|:-:|:----:|---------|-----------|:-------------:|
| 0 | 0:00–0:50 | 冷开场：十字路口 / 排队 / 点赞爆款 → "秩序从何来" | 三意象 + 亚当·斯密引言 | `ColdOpen` |
| 1 | 0:50–3:10 | 第一支柱：个体 + 正态分布 + 中心极限定理 | 点云 → 正态曲线覆盖 | `IndividualDistribution` |
| 2 | 3:10–5:40 | 第二支柱：博弈 + 囚徒困境 + 重复博弈 | 2×2 收益矩阵 + Tit-for-Tat | `InteractionsGame` |
| 3 | 5:40–8:00 | 第三支柱：激励 + 激励相容 + 机制设计 | 双曲线对比 + 赫维茨引言 | `IncentivesMatter` |
| 4 | 8:00–10:20 | 第四支柱：涌现 + 生命游戏演示 | 18×10 网格演化 5 代 | `Emergence` |
| 5 | 10:20–11:30 | 四集串联 + 预告下季 | 四行卡 + 循环链 + 留问 | `Closing` |

---

## 二、分镜要点

### Beat 1 · IndividualDistribution
- **Phase A**：140 个蓝色 Dot 随机撒在 Axes 区域（看起来无序）。
- **Phase B**：Dot 按 x 坐标"落"到对应 pdf(x) 的高度——形成正态轮廓。
- **Phase C**：一条黄色正态曲线覆盖上去 + MathTex 公式。
- 结论帧："大量独立因素叠加 → 正态分布是数学必然。"

### Beat 2 · InteractionsGame
- 2×2 收益矩阵格子动画：逐格 fade_in，颜色区分合作(绿)/背叛(红)。
- 高亮 (背叛,背叛) 格子 → Flash + "纳什均衡"大字。
- 新增：右侧画"重复博弈"时间轴——箭头从 "一次" 延伸到 "∞次"。
  - 出现 Tit-for-Tat 策略图示：先合作 → 镜像对方 → 稳定合作。
  - 条件："有信任 · 有反馈 · 有未来"三字竖排。

### Beat 3 · IncentivesMatter
- Axes 画时间 vs 产出：
  - 红色低斜线："按工时"。
  - 绿色高斜线："按成果"。
  - 蓝色更高线（新增）："计件 + 质检" → 最优。
- 曼昆引言灰色置底。
- 激励地图：中央"目标"→ 向左"参与者 A 的最优"→ 向右"参与者 B 的最优"。
  - 箭头对齐 = 激励相容（绿色）。
  - 箭头相反 = 冲突（红色）。

### Beat 4 · Emergence
- 18×10 网格初始随机状态。
- 演化 5 步（Game of Life 规则），每步 Transform。
- 新增：在网格右侧放一根"活细胞数量"折线，随代数更新。
- 结论帧："简单规则 + 大量交互 + 时间 = 复杂秩序。"

### Beat 5 · Closing
- 四行卡片（如何思考 / 自然 / 数学 / 社会）。
- 四张卡用箭头连成一条链——最后首尾相连成环。
- 留问："既然社会靠涌现运行——你怎么找到自己的位置？"
- 下季标题："知识 · 组织 · 成长"。

---

## 三、学术引用备忘

| 出处 | 用途 |
| --- | --- |
| Adam Smith, *The Wealth of Nations* (1776) | 冷开场："看不见的手" |
| Central Limit Theorem (Laplace, 1810) | 个体板块：为什么正态分布如此常见 |
| John von Neumann & Morgenstern, *Theory of Games* (1944) | 博弈板块 |
| John Nash, "Equilibrium Points in N-Person Games" (1950) | 纳什均衡 |
| Robert Axelrod, *The Evolution of Cooperation* (1984) | 重复博弈 + Tit-for-Tat |
| N. Gregory Mankiw, *Principles of Economics* Ch.1 | "People respond to incentives" |
| Leonid Hurwicz, Mechanism Design (Nobel 2007) | 激励相容 |
| John Conway, Game of Life (1970) | 涌现 |
| Philip Anderson, "More Is Different" (1972) | 涌现哲学：多不仅仅是多 |

---

## 四、视觉规范

| 主题 | 主色 |
|------|------|
| 个体 / 正态 | `C_BLUE` → `C_YELLOW` (曲线) |
| 博弈 / 合作 | `C_GREEN` |
| 博弈 / 背叛 | `C_RED` |
| 激励 / 制度 | `C_ORANGE` |
| 涌现 / 活细胞 | `C_YELLOW` |
| 引言 | `C_TEXT_DIM` |
