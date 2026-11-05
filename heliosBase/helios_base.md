# RoboCup Soccer 2D 与 HELIOS Base 学习笔记

本文整理了关于 player agent、librcsc、HELIOS Base 及 HELIOS2018 论文的讨论。比赛服务器、客户端基础库、示例队伍是不同层次；论文中的技术与公开示例代码也不能直接画等号。

## 1. 如何制作 player agent

[`rcssserver`](https://github.com/rcsoccersim/rcssserver) 是比赛服务器，不是球员策略框架。每个球员是独立运行的客户端，通过 UDP 接收服务器观测，维护自身对场上局面的估计，并逐周期提交动作。同一队的 11 个客户端使用相同队名。

典型处理链如下：

```text
UDP 收发 -> 解析 see / sense_body / hear -> 定位与世界状态估计
         -> 比赛状态及角色决策 -> 基础动作控制 -> 发送命令
```

主要设计工作包括：

- **观测与时间管理**：视觉只有视野内的相对信息，且存在噪声、延迟和缺项；需要记录周期号及观测新鲜度，不能把旧球位当作当前真值。
- **运动与动作控制**：将“移动到某位置”“射向某目标”落实为当前周期的 `turn`、`dash`、`kick` 等动作；同一周期只能执行一个身体动作，`turn_neck` 可以独立使用。
- **比赛状态与战术**：处理开球前、比赛中、定位球等不同状态；确定争球队员、阵型位置、接应、防守、射门与传球选择。
- **守门员与协作**：守门员注册时指定 `(goalie)` 并设计专属行为；队友可通过受限的 `say`/`hear` 交换信息。
- **验证**：先让一个球员稳定完成找球、追球、踢球，再扩展到整队；比较多场比赛的胜率、净胜球、体力消耗和动作执行情况。

入门时可以用服务器自带的 `rcssclient` 手动试协议：向默认 UDP 6000 端口发送 `(init MyTeam (version N))`，在开赛前用 `(move -10 0)` 摆位。初始化成功后，客户端发送后续命令时应使用服务器响应报文的来源端口，而非始终使用 6000。协议版本应明确指定，并与服务器及所选客户端库兼容。`rcssclient` 只是手动收发协议的样例，不是完整智能球员。

如果目标是尽快制作可比赛队伍，优先从 librcsc 和 HELIOS Base 入手；如果目标是研究协议与定位，则可自行编写 UDP 客户端。参考：[官方 Soccer Client 指南](https://rcsoccersim.readthedocs.io/en/latest/soccerclient.html)、[传感器与动作模型](https://rcsoccersim.readthedocs.io/en/latest/soccerserver.html)、[安装指南](https://rcsoccersim.readthedocs.io/en/latest/gettingstarted.html)。

## 2. librcsc 做了什么

[`librcsc`](https://github.com/helios-base/librcsc) 是 C++ 客户端基础库，不是比赛服务器，也不是安装后自动参赛的队伍。以下模块名称依据其 `develop` 分支源码。

| 层次 | 主要组件 | 作用 |
| --- | --- | --- |
| 客户端运行 | [`PlayerAgent`](https://github.com/helios-base/librcsc/blob/develop/rcsc/player/player_agent.h)、[`OnlineClient`](https://github.com/helios-base/librcsc/blob/develop/rcsc/common/online_client.cpp)、`net` | UDP 收发、消息处理、周期调度、动作提交；通过继承 `PlayerAgent` 实现 `actionImpl()` 等决策入口。 |
| 观测解析 | [`VisualSensor`](https://github.com/helios-base/librcsc/blob/develop/rcsc/player/visual_sensor.h)、`BodySensor`、`AudioSensor` | 将视觉、身体及听觉协议消息解析为结构化数据；区分已知和未知身份球员。 |
| 定位与状态 | [`LocalizationDefault`](https://github.com/helios-base/librcsc/blob/develop/rcsc/player/localization_default.cpp)、[`WorldModel`](https://github.com/helios-base/librcsc/blob/develop/rcsc/player/world_model.h) | 依据旗标、边线等观测估计自身位置及朝向，更新球、队友、对手、比赛模式及状态可信度。 |
| 参数与预测 | `ServerParam`、`PlayerParam`、`PlayerType`、[`InterceptTable`](https://github.com/helios-base/librcsc/blob/develop/rcsc/player/intercept_table.h) | 使用服务器参数与球员类型估计运动、体力和各方到球所需周期。 |
| 动作执行 | [`ActionEffector`](https://github.com/helios-base/librcsc/blob/develop/rcsc/player/action_effector.h)、[`rcsc/action`](https://github.com/helios-base/librcsc/tree/develop/rcsc/action) | 管理命令并提供去目标点、截球、踢球、带球、控球、扫描等可组合基础行为。 |
| 阵型与通信 | [`rcsc/formation`](https://github.com/helios-base/librcsc/tree/develop/rcsc/formation)、`audio_codec` 等 | 静态或动态阵型的位置计算；短消息编码、解析及听觉记忆。 |
| 其他工具 | `coach`、`trainer`、`rcg`、`geom`、日志及调试模块 | 支持教练、训练、比赛日志分析和几何计算。 |

例如 `InterceptTable::selfStep()`、`teammateStep()` 和 `opponentStep()` 提供各方预计截球周期。库解决的是“谁可能先到球”的预测，是否抢球仍由队伍决定。`Body_GoToPoint` 解决“如何走到目标点”，而“由谁去、去哪里、何时去”属于战术。`FormationDT` 利用 Delaunay 三角剖分和线性插值，从阵型样本及参考点计算目标站位，但阵型数据和使用规则仍需设计。

`WorldModel` 是球员基于局部观测建立的估计，并非服务器真值。库虽然包含 `FullstateSensor`，并不表示普通比赛球员默认可获得全状态。librcsc 也提供通信组件，但不会自动制定有效的团队交流协议。其 README 写明 C++17 依赖，并称程序可与 `rcssserver-18` 工作；使用其他版本时应实测兼容性。

## 3. librcsc 与 HELIOS Base 的分工

[`HELIOS Base`](https://github.com/helios-base/helios-base) 是使用 librcsc 的可运行示例队伍。它提供角色、战术决策、定位球、守门员行为、阵型数据和启动脚本，而 librcsc 主要提供可复用的客户端与足球仿真组件。

源码中，[`SamplePlayer`](https://github.com/helios-base/helios-base/blob/develop/src/player/sample_player.h) 继承 `rcsc::PlayerAgent`。示例队伍的 [`Bhv_BasicMove`](https://github.com/helios-base/helios-base/blob/develop/src/player/bhv_basic_move.cpp) 读取库的截球预测，自行决定截球还是回到策略给定的阵型位置，再使用基础移动行为执行。这是“库提供能力、队伍制定选择”的直观例子。

想研究比赛策略，适合先看示例队伍的 `src/player/sample_player.cpp`、`strategy.cpp`、角色与定位球逻辑；想研究协议、定位或预测，再深入 librcsc。HELIOS Base 的 README 称它为 *sample team*，并写明可用于 `rcssserver-16`。它与 librcsc README 提到的服务器版本不同，组合新版本时需要实测。

## 4. HELIOS Base 原版大概是什么水平

它是工程较完整、能踢完整比赛的研究基线，通常明显强于“所有人追球”或随机传球等教学级策略，但**不能把公开示例队伍直接当成 HELIOS2018 冠军正式参赛版本**，也不能仅凭源码给出当代赛事排名。

其决策主要表现为模型预测、树搜索和人工设计的规则及评价函数，而非端到端训练出的单一神经网络：

- 无球移动会比较自己、队友和对手的预计截球周期，决定是否追球，否则返回阵型目标位置。
- 有球角色尝试执行规划动作，必要时保持控球；项目包含传球、射门、守门员、定位球和通信逻辑。
- [`SampleFieldEvaluator`](https://github.com/helios-base/helios-base/blob/develop/src/player/sample_field_evaluator.cpp) 根据进球、出界、推进位置及射门机会等对预测局面评分。这是启发式评价，不是精确的比赛胜率预测。

README 引用 HELIOS2012 和 HELIOS2018 冠军等论文，说明技术背景，**不等于公开示例代码拥有冠军队相同的实力**。要判断具体强度，应在固定服务器版本和相同赛制下，与目标对手多次比赛、交换左右半场，记录胜率、净胜球和进失球方式。作为开发基线，它尤其适合用来衡量新策略是否真正带来提升。

## 5. HELIOS2018 论文要点与证据边界

冠军论文是 [《HELIOS2018: RoboCup 2018 Soccer Simulation 2D League Champion》](https://doi.org/10.1007/978-3-030-27544-0_37)，发表于 *RoboCup 2018: Robot World Cup XXII*，第 450–461 页。讨论中未能打开 Springer 的冠军论文全文；下面的具体技术与实验数字来自另一份已阅读全文的 [《HELIOS2018: Team Description Paper》](https://tdpsearch.com/paper/soccer_simulation_2d__2018__HELIOS)（[原始 PDF](https://wrighteagle2d.github.io/robocup/2018/HELIOS_SS2D_RC2018_TDP.pdf)），**不能冒充冠军论文全文结论**。

### 问题与方法

团队先前具备动态阵型，以及持球者的行动序列树搜索：持球者生成传球、带球等候选动作，评估当前及后续局面，通过 best-first search 选择较好的序列。例如计划“传给 A，再由 A 传给 B”。问题在于无球者未必知道持球者规划的后续动作，因此没有提前接应，计划经常在执行中断裂。

该团队描述论文着重研究 *knowledge sharing*：无球者尽量观察持球者周围的信息，运行相近的行动序列规划，以**推断**持球者可能选择的计划，再相应调整自己的行动。这里的“共享”不等于持球者向全队广播完整计划；它要求队友的观测与规划结果足够接近。

### 实验结果及局限

- 实验使用基于 `agent2d` 的 **opuSCOM** 队伍，而非直接用表格证明冠军队的整体胜率。
- 为便于评估，只考察深度不超过 2、且动作均为传球的规划序列；没有在该实验中完整覆盖带球等行为。
- 论文称针对各对手进行了 300 场比赛。表 1 的计划共享成功率约为 **87%–92%**。
- 表 2 的两步计划执行成功率在所列对手上均有提升：对 `agent2d` 从 **42.12%** 增至 **47.15%**；对 `opuSCOM` 从 **41.04%** 增至 **47.14%**。论文称新旧版本的差异通过 5% 显著性水平的统计检验。
- 上述百分比是计划推断或**两步行动序列的执行率**，不是比赛胜率、进球率，也不能单独证明该机制导致夺冠。

对 agent 设计最有启发的结论是：当策略依赖多步协作时，提高持球者规划质量还不够；必须考虑队友如何知道或推断意图、如何提前跑位，以及如何测量计划在比赛中是否真的完成。
