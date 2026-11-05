## User

rcssserver v18 -> v19 修改了哪些内容，有没有 changelist ？

## Assistant

有，而且有官方 changelog。rcssserver 19.0.0 相比 18.0.0，最重要的变化不是简单的协议升级，而是引入了新的双足运动模型（Bipedal Dash Model）和高斯视觉噪声模型（Gaussian See）。

官方发布记录：

- [rcssserver GitHub Releases](https://github.com/rcsoccersim/rcssserver/releases?utm_source=chatgpt.com)
- [18.0.0 → 19.0.0 GitHub Commit Diff](https://github.com/rcsoccersim/rcssserver/compare/rcssserver-18.0.0...rcssserver-19.0.0?utm_source=chatgpt.com)

## 1. 18 → 19 的主要变化

| 变化 | 18.0.0 | 19.0.0 |
| --- | --- | --- |
| C++ 标准 | C++17 | 仍为 C++17 |
| Dash 模型 | 原有 dash | 新增双腿独立 dash |
| 视觉噪声 | 量化噪声模型 | 新增 Gaussian See |
| 视觉噪声参数 | 原有参数 | 新增 4 个噪声参数 |
| JSON Game Log | JSON 格式改进 | 进一步调整格式，纯 JSON 文件 |

### ① 双足运动模型（重要）

19.0.0 新增命令：

Plain text`(dash (l POWER DIR) (r POWER DIR))`

以前的命令：

Plain text`(dash POWER)`

新命令允许左右腿分别施加加速度，因此可以同时控制：

- 左腿加速度
- 右腿加速度
- 两条腿各自的方向

这意味着球员的运动模型可以表现出更细致的双足动作。

值得注意的是，官方说明所有版本的球员都可以使用新命令，但是否接受仍由服务器的动作处理逻辑决定。GitHub+1

### ② Gaussian See 视觉噪声模型

19.0.0 新增命令：

Plain text`(gaussian_see)`

发送后，服务器返回：

Plain text`(ok gaussian_see)`

它用高斯分布代替之前的量化视觉噪声模型。

距离噪声的标准差：

σ=actual_dist⋅noise_rate+focus_dist⋅focus_noise_rate\sigma = actual\_dist \cdot noise\_rate
+ focus\_dist \cdot focus\_noise\_rateσ=actual_dist⋅noise_rate+focus_dist⋅focus_noise_rate

观测距离：

noised_dist=max⁡(0,N(actual_dist,σ))noised\_dist =
\max(0,\mathcal{N}(actual\_dist,\sigma))noised_dist=max(0,N(actual_dist,σ))

也就是说，视觉距离不再只是简单地按照固定精度量化，而是引入了随机误差。

这对 Agent 的视觉处理、定位和预测算法都有影响。GitHub

### ③ 新增四个服务器参数

| 参数 | 默认值 | 作用 |
| --- | --- | --- |
| server::dist_noise_rate | 0.0125 | 球和球员距离噪声 |
| server::focus_dist_noise_rate | 0.0125 | 与 focus point 距离相关的噪声 |
| server::land_dist_noise_rate | 0.00125 | 地标距离噪声 |
| server::land_focus_dist_noise_rate | 0.00125 | 地标与 focus point 相关的噪声 |

这些参数可以用来调整不同类型视觉对象的噪声程度。

### ④ JSON Game Log 改进

19.0.0 对 JSON 游戏日志格式进行了整理：

- 调整每条记录的数据结构，使其更容易解析。
- JSON 格式的 RCG 日志现在记录为纯 JSON 文件。
- 解析库被整合进 `rcssmonitor`。

如果你自己编写比赛日志分析器，这部分需要特别注意，不能假设 18 和 19 的 JSON 日志结构完全一致。GitHub

## 2. 不要忽略 18.x 的中间版本变化

18.0.0 到 19.0.0 之间还有几个小版本：

| 版本 | 变化 |
| --- | --- |
| 18.0.0 | C++17、change_focus、新视觉模型 |
| 18.1.0 | 恢复 17.0.1 的视觉消息频率和噪声模型 |
| 18.1.1 | 修复 focus point 偶尔不更新的问题 |
| 18.1.2 | 修复视觉距离量化精度问题 |
| 18.1.3 | 后续维护版本 |

所以，如果你从 18.1.3 升级到 19.0.0，实际需要关注的变化和直接从 18.0.0 升级并不完全一样。GitHub+1

## 3. 如何查看完整源代码变更？

官方 GitHub 提供了两个版本之间的完整代码比较：

[GitHub：18.0.0 → 19.0.0 完整代码 Diff](https://github.com/rcsoccersim/rcssserver/compare/rcssserver-18.0.0...rcssserver-19.0.0?utm_source=chatgpt.com)

也可以在本地执行：

Bash

```
git clone https://github.com/rcsoccersim/rcssserver.git
cd rcssserver

git fetch --tags

# 查看两个版本之间的提交
git log --oneline rcssserver-18.0.0..rcssserver-19.0.0

# 查看所有文件的变更统计
git diff --stat rcssserver-18.0.0 rcssserver-19.0.0

# 查看完整代码差异
git diff rcssserver-18.0.0 rcssserver-19.0.0
```

## 4. 对 HELIOS Base / librcsc 的影响

结合你现在的目标——在 Mac 上用 HELIOS Base 学习和开发 Agent，我建议优先检查以下几个地方：

| 模块 | 检查重点 | 优先级 |
| --- | --- | --- |
| Action | 新的双腿 dash 命令 | 高 |
| See Parser | Gaussian See 下的视觉数据 | 高 |
| Player Model | 运动预测与服务器模型是否一致 | 高 |
| Localization | 新视觉噪声对定位的影响 | 高 |
| Game Log Parser | JSON 日志格式 | 中 |
| Server Parameters | 新增四个噪声参数 | 中 |

我的建议：不要一开始就修改 HELIOS Base 的所有代码。 先用原版 HELIOS Base 连接 rcssserver 19.0.0，验证基本比赛能否运行，再逐步测试 Gaussian See 和新 dash。

这样可以区分两类问题：一类是 19.0.0 的兼容性问题，另一类是 Agent 尚未利用新功能的问题。

如果你愿意，我可以进一步帮你做一份 rcssserver 19.0.0 对 HELIOS Base / librcsc 的源码级兼容性检查清单，具体定位需要检查的类、函数和协议解析代码。

## User

v19 server 能兼容 v18 player 吗？

## Assistant

可以。rcssserver 19.0.0 官方明确考虑了旧版本 Player 的兼容性。 一般来说，v18 Player 可以直接连接 v19 Server，不需要为了连接而升级 Player。

不过，要区分「能够连接并正常比赛」和「能够使用 v19 的新功能」。

### 1. 兼容性情况

| 功能 | v18 Player + v19 Server |
| --- | --- |
| Init / Connect | 兼容 |
| Move / Turn / Dash | 兼容 |
| Kick / Catch / Tackle | 兼容 |
| Say / Hear | 兼容 |
| v18 See 协议 | 兼容 |
| 双足 Dash | 需要主动使用新命令 |
| Gaussian See | 需要主动启用 |

依据是 v19 官方 NEWS 明确写道：

- 新的双足 Dash 命令适用于所有版本的 Player。
- `gaussian_see` 命令也适用于所有版本的 Player。GitHub+1

### 2. 为什么旧 Player 可以兼容？

RoboCup Soccer Simulator 有协议版本控制机制。

Player 在初始化时声明协议版本，例如：

Plain text`(init HELIOS (version 18))`

Server 根据 Player 声明的版本选择相应的消息序列化格式。

因此，v19 Server 不会简单地强制所有 Player 使用 v19 协议。官方手册也明确说明了这一向后兼容机制。GitHub

### 3. 需要注意一个重要区别

虽然 v18 Player 可以正常连接，但 v19 Server 引入了新的物理模型。

例如旧命令：

Plain text`(dash 100)`

仍然可以使用。

新命令：

Plain text`(dash (l 100 0) (r 100 0))`

可以分别控制左右腿。

旧 Player 如果不发送新命令，就不会主动利用双足运动能力。

另外，Gaussian See 也不是自动对所有旧 Player 生效，而是需要发送：

Plain text`(gaussian_see)`

才能启用。

### 4. 对你当前 HELIOS Base 项目的建议

我建议采用下面的升级路线：

1. 第一阶段：原版 HELIOS Base + v19 Server

不修改 librcsc，先验证连接、比赛、See、Dash、Kick 等基本功能。
2. 第二阶段：测试 v19 新视觉模型

在 Player 初始化后发送 `gaussian_see`，观察视觉数据解析和定位效果。
3. 第三阶段：扩展 librcsc

增加双足 Dash Action，以及对应的运动预测模型。
4. 第四阶段：优化 Agent

研究双足运动对转向、加速、体力消耗和路径规划的影响。

我的结论：没有必要因为 rcssserver 升级到 v19，就立即放弃 HELIOS Base。 先用原版 v18 Player 在 v19 Server 上跑起来，是非常合理的路线。

官方参考：

- [rcssserver NEWS（版本变更记录）](https://github.com/rcsoccersim/rcssserver/blob/master/NEWS?utm_source=chatgpt.com)
- [Soccer Simulator Player Protocol Version Control](https://github.com/rcsoccersim/manual/blob/master/source/soccerclient.rst?utm_source=chatgpt.com)
- [RoboCup Soccer Simulator Users Manual](https://rcsoccersim.readthedocs.io/_/downloads/en/latest/pdf/?utm_source=chatgpt.com)


