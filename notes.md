
# 5

## 5.1 简单决策原理


 - principle of simple decision
    - 分层处理
        - 底层行为如带球、传接球、射门等相对固定，易于代码化，也可用离线学习的方法来优化
        - 上层决策如跑位、技战术配合等由于场上形势的不确定性，很难明确给出，可以使用强化学 习之类的在线学习方法，来学习提高。
        - 另外，还可预先制定一些既定战术如中场开球、发角 球等以提高这些情况下的成功率。
    - 主要模块
        - 行为决策模块
            - 根据当前场上状态(包括实际感知和预测)，以及赛前制定的合作 协议，来决定当前的行为模式，并更新自身状态。
            - 行为决策模块将当前的行为模式以及该行 为附带的参数(如果需要的话)发送给动作解释及执行模块，作进一步分解。
        - 合作协议模块
            - 存储在赛前制定的合作协议。可以是特定的技战术配合如中场开球、 发角球等，还可以是比赛时的一些战术运用如交叉换位、下底传中等
 

### 5.1.1 决策系统

 - 行为树决策系统

![](https://raw.githubusercontent.com/mebusy/notes/master/imgs/robosoccer_5.1.1_behavior_tree.png)

> Fig 5.1

这种分层决策系统给出了一个比较简便易行的决策方法，根据环境变化可以比较快的做 出反应，产生相应的行为，具有比较好的实时要求，但涉及到机器人足球这样一个复杂的决 策环境，这种决策系统还有许多不足。

 - 首先，上面的结构是单向分层决策，高层决策无法了解下层决策的实际能力，只能按一 种预定模型来分析，不能实时调整，这就会导致上层决策与下层执行脱节，不能很好的完成 目标。
 - 其次，这种按照行为树的顺序决策方式不能很好地适应复杂的决策环境，实际上在这种 方式下每个行为都被赋予了一个优先级，高优先级的行为总是被优先考虑，好处很明显，高 优先级的行为总是被优先考虑执行
    - 现在大部分球队设计时都引入了决策论的思想，进行 全面的评估，不再是简单的按照行为树顺序决策。


 - 分层决策系统

一个三层决策系统模块，依次为:战略层，战术层和基本技能层。

![](https://raw.githubusercontent.com/mebusy/notes/master/imgs/robosoccer_5.1.1_layer_desicion_system.png)

> Fig 5.2

1) 战略层

在这层中智能体决定诸如决定自己的角色，判断自己是该进 攻还是该防守，要执行什么任务等问题，同时要明确当前达到的战略目标。

这层充分体现了 智能体的团队合作与规划行为. 目前很多智能体的战略决策还是基于 一些常规的分析法:

 - (1)判定是否它处于是某一合作协议中(例如中场开球、界外球、角球等)。
    - 如果是， 只需从合作协议库中提取出预先指定的计划，按角色来施行。
    - 虽说这些战术都是死的，但确 实是经常会出现的，使用这种方法往往会取得较好的效果。
    - 另外也可以引入比赛进行中的一 些合作协议配合。这属于动态的实时规划，难度较大。
 - (2)判断自己的角色和当前队阵型。由此来决定自己的任务(不同的角色在不同的阵 型下所要执行的任务自然也不尽相同)。
    - 战略层能根据当前的世界模型选择合适的阵型，确 定自己的角色。
 - (3)判断自己所处的行为模式(图 5.1)。 
    - 根据当前的世界模型、队阵型和智能体所处 的角色选择自己的行为模式，包括进攻模式、辅助进攻模式、防守模式、辅助防守模式、守 门员模式(由于守门员处理比较复杂，又很重要，所以单独处理)。

2) 战术层

在战略层确定行为模式后， 战术层要将这些行为模式具体化: 如果智能体在执行某个合作协议，只需从合 作协议库中提取出预先指定的计划，得到相应的执行命令。

一般地，智能体分析当前世界模 型，从对手模型中，把握对手的意图，依照行为树(图 5.1)来决定应采取的行为策略。包 括抢占有利的位置、使用越位陷井、抢球，拦截，带球，传球，射门，扑球(守门员)，盯 人，等等。

3) 底层技能层

底层技能层是决策系统层最低的，用以实现智能体的个人技能(如传球、带球等)，即 将这些具体的行为决策细化为比赛平台可以接受的执行指令。

实现时，一般只是给智能体一些基本的行为规则，如球来了要去接球(守门员要 去扑球)，对方控球要上去封堵，不能让它轻易射门得分，还有按照行为树(图 4.4.3)决 定自己的行为模式等等。

但是这些还远远不够，怎样接球不会丢，怎样封堵最有效，什么时 候处于进攻模式、什么时候处于防守模式，什么时候该传球等等都是无法直接给定的。

但采取每个行为都有个成功率的概念，智能体 可以在实践中评价每个行为，修正每个行为在确定形势下的成功率，选取成功率高的行为， 即可达到相对较好的效果。

成功率的设置，一方面可根据规则，如球不在能踢的区域内 (kickable_area 由 Server 给出)就不能踢球;一方面可根据常识经验，如在有守门员的情况 下，离球门 25 米以外很难射门得分;另外还可以通过使用机器学习(包括离线的和在线的) 来调整各行为的成功率。如在实现一些基本行为决策(如传球、射门)时可以采用一些离线 学习方法如 C4.5 决策树方法来提高行为的成功率，在可使用一些强化学习方法，来提高决 策的智能度，以获得较好的效果。

### 5.1.2 决策模块分析

1) 进攻决策模块

目前更多球队采用的都是类似于决 策论的方法[Yang et al. 2002]，在给定的形势下分析各种可能行为(包括传球、射门、带球 等)的成功率 p，同时也给出执行该行为的收益 u，然后通过计算得到执行一个行为的综合 评价 b，选择评价最高的执行即可

由于比赛环境是动态不确定的，所以无法准确预知其他球员的行为，这里无论是成功率 p 还是收益 u 的计算，都是一种基于期望的预测(EBP)[Yang et al. 2002]。我们在计算时实 际已经假定所有队员都是按照程序里的“最优”决策方式进行，当然也可以根据球队的风格 “高估”或“低估”对手。

助攻队员跑位点的选择以及对时机的把握都会对结果产生很大影响。助攻队员如果善于 发现对方防守空档并选择合适的时机跑位，就能够配合控球队员出色地完成进攻任务。

对于跑位点的选择以及时机的把握都需要与控球队员协同。由于比赛环境限制，完全依 靠通讯来协同是很困难的。很多队都是事先制定了战术，这样只要在比赛中由控球者选择合 适的战术，然后通知参与者来实现协同。比较典型的如清华队的“scheme”机制[Jinyi Yao et al. 2003]，荷兰 UvA 队的协调图方法(CG)[Kok et al. 2003]。这些球队都给出了一种描述 战术的方法，实现了队员间的一些配合。

这些战术由于都是事先制定的，所以并不总能够适用于所有的情况，队员还需有其他方 法来适应场上多变的环境。

一种简单的方法 是 根据自 己的决策算法预测控球队员可能采取的行为。由于是同一球队通常采用同一种算法，这种方 法大多时候都比较准，除非两人获得的关键信息有较大差异。由于这种预测是近似算法，所 以在实际使用时对算出的结果还要作些修正。另外要注意的是这种方法实际是根据当前状况 查找可行的机会，我们更多的需要是无球队员能通过跑位来创造机会，这方面还需要通过战 术或其他方式来帮助无球队员实现。


2) 防守决策模块

针对防守对象和场景的不同，防守行为可以简单分为抢球、封堵、盯人三种。

 - 抢球是在对方没有完全控制住球，双方处于拼抢状态时采取的行为。
 - 但由于对方处于主 动，如果判断有误，很容易被对方晃过，所以安全的防守行为是封堵，虽然拿不到球，但也 不让对手带球前进或轻易转移;
 - 盯人一般是指对无球进攻队员的盯防，破坏其可能的配合。


类似的，葡萄牙队将防守行为细分为[Reis and Lau 2000]

 - 拦截球 -- 以最快的速度抢到球
 - 被动拦截球 -- 根据场上形势，在尽可能占优的位置拦截球，不保证最快
 - 封堵传球路线 -- 盯住对方控球队员的可能传球路线，防止其通过传球突破防守   
 - 封堵对手 -- 盯住对方控球队员，防止他带球前进
 - 逼近球 -- 即使不能抢到球，也要逼近对方控球队员，减少他的选择机会
 - 盯防路线 -- 选择合适的防守位置处于对手和我方球门之间

中国清华队还引入了两人协防概念，实现更有效的防守[Cai et al. 2002]。

守门员与普通球员不同，他的主要职责就是坚守球门，另外守门员专用的扑球指令使其 比其他球员更容易抢到球，所以防守策略与一般球员也有所不同。

由于比赛环境是 2 维的，守门员防守相对容易一些。根据比赛平台模型，只要守门员发 送扑球指令及时，球是不可能穿越守门员的。

所以守门员的防守策略可以简单分为站位和出 击。合理的站位可以使守门员覆盖尽可能大的球门区域，将对手射门机会降至最低;及时的 出击扑球才能彻底瓦解对手的进攻。

合理的站位点原则上是在球到球门连线上，要保证无论球以多大速度射向球门任何位 置，守门员都可以及时拦截到;同时考虑有威胁的对方助攻球员，站位点可以适当偏移。

出击关键是时机的把握，相对于普通球员，守门员的拦截行为更强调成功率。所以，守 门员出击的判断一定要尽可能准确。这就使得很多时候守门员并不是选最快拦截点扑球，而 是成功率相对比较高的位置扑球。当然如果情况危急，守门员也不得不冒险。

3) 一般跑位模块

一般跑位是指场上队员在没有明确进攻或防守任务的情况下，所遵循的一种移动原则。

很多球队学习了人类足球比赛的经验，开始引入“阵型”的 概念.

如 1998、1999 两届世界冠军卡耐基梅隆大学仿真足球队设计了一种方式，即给每个 队员划定一块“责任区”[Stone and Veloso 1999]，限制队员的活动范围，在没有任务时就在 活动中心待命

![](https://raw.githubusercontent.com/mebusy/notes/master/imgs/robosoccer_f5.3.png)

> Fig 5.3

这种设计的问题也很明显，就是球员站位过死，不能适应场上多变的形势，一旦比赛节奏加快， 球员之间就会产生脱节，让对方有机可乘。

终于 2000 年世界冠军葡萄牙队提出了一个新的、更加合理的跑位模型——“基于形势 的战略跑位 SBSP” [Reis and Lau 2000]，这个跑位模型将队员的跑位与场上的形势紧密的 联系到一起。

在计算每个时刻的跑位点时，球员要分析目前正采用哪种战术和阵型，并根据 自己的角色计算出一个基本跑位点，然后再根据场上各种不同的形势，如球的位置、速度等 信息，是进攻还是防守，还有比分等信息，以及角色的特点调整得到最终的战略跑位点。

角 色的特点包括对球变化的敏感程度、特殊的区域限制(如守门员不能出禁区)、保持在球之 后(如后卫)等。这些都使得这种战略跑位更加灵活多变。

这种跑位系统使得球队的移动更像一个真实的足球队，球员保持这种场上分布可以比较 好的覆盖球的移动，不至于产生大的漏洞。后来被各球队广泛采用。

## 5.2 简单团队合作实现

### 5.2.1 自发的团队合作

团队合作可以是自发的，也可以是有规划的。

前者主要是当智能体在掌握了一定的基本 技能(如能较准确的将球踢到指定点)、能够进行一些简 单的反应式行为决策(如抢球、简单传球、跑位等)之后， 在某种情况下就会产生自发的团队合作如二过一配合:

 - 控球队员 A 控制球在前进过程中被对方阻挡，此时另一名队 员 B 处于一个无人防守的位置，队员 A 发现队员 B 位置比 较安全，就会将球传给他，这时防守队员就会继续去抢队 员 B 的球，队员 A 就可摆脱防守队员迅速前进，然后队员 B 再把球传回给队员 A，从而过掉防守队员，形成二过一 的配合.

![](https://raw.githubusercontent.com/mebusy/notes/master/imgs/robosoccer_2on1.png)

### 5.2.2 有规划的团队合作

自发合作虽然也有它的不足，它只能完成短期的、局部的、比较明确的目标，而对于长 期的、全局的目标就很难胜任了，这就需要规划。

没有规划，可以说团队合作就不完整，顶 多也只能算是一支“业余球队”。

全局规划使全队上下有了一个共同的目标，所有的行为都 将为这个目标而服务。全局规划又可划分为一些子规划，以几个队员为一个单元，制定局部 的子目标，做一些局部合作。

这样逐步细化最终可使每个队员的行为都明确化，这样就使智 能体的行为决策更明确、更有效。

这种有规划的合作实现也有两种情况，

 - 一种是预先建立一些合作协议，如我方中场开球，当某一特定的条件满足时，如比赛模式(Play_Mode)为我 方中场开球(My_Kick_Off)，即按照该协议执行。

此方法在条件比较明确时常常采用，在 比赛中由行为决策模块来引用合作协议，作为智能体之间合作的规范，效果还比较好。但是， 由于它是相对比较固定，容易让对手找到对付的办法，所以不易过多采用; 

 - 另外，场上环境 的复杂性和实时性，使得有许多情况，是很难确定其触发条件的，这就需要把球队看成一个 多智能体系统，建立全局的规划。所有队员有一个一致的长期目标，再向下细分为若干个子 目标，将智能体分组划分为几个单元来完成这些子目标，以实现小范围的团队合作，使问题 简化。逐步实现最终目标。 

这种规划实现起来比较困难，其根本原因是当前的智能体体系 结构中缺少了团队合作的理论，也不能适应实时性的需要[Kitano et al. 1997]。可以考虑选择 一些比较好的智能体体系结构如 BDI 模型，在其上来实现规划。

### 5.2.3 团队合作的一些结构表示

为了实现团队合作，就需要有些合适的结构单元来表示。

美国卡耐基梅隆大学球队 CMU98 最早提出了一个团队合作结构，称为更衣室协定[Stone and Veloso 1999]，主要由三 部分组成:

 - 可以根据协定灵活多变(包括互换)的角色(Role)
 - 由角色组成的阵型(Formation)
 - 和在特点场景执行多步、多球员的合作协议(Set-Play)

决策系统的决策依靠世界状态模 型和这些结构。

**角色**

就是一个球员在比赛中承担的责任，包含一个球员所应执行的内部和外部行为的 规范，任何行为的执行条件和相关参数都依赖于球员当前的角色。

在机器人足球领域中，所有智能体都有一些特定的相对独立的职责，每个角色记录都包 括了这个角色的活动区域，初始位置等，当然，不同角色的活动区域可以互相重叠。每个角 色有不同的行为模式，这主要是通过行为树中的条件来体现的;当执行一些合作 协议时，有时也会需要它们的位置、任务发生一些变动。

**阵型** 

通过引入阵型可以实现球员智能体之间的合作。

一个阵型是由定义了一组特定角 色集合的任务空间组成。阵型包括了和球队球员数相同数目的角色，这样每个角色都对应由 一个球员充当。如 433 阵型就是 1 个守门员、4 个后卫、3 个前卫和 3 个前锋的集合，每条 线上又可以细分为左、中、右等，总共 11 个不同的角色。

另外，还可以定义子阵型，或称 为单元，不包括整个球队。

一个单元包括从阵型中抽取的角色子集，一个队长和在角色中的单元内部交互。

略...

一个单独的角色可以是任何数量的单元和阵型的一部分。


单元是用于出来解决局部问题的。与其要考虑整个队来处理一个局部问题，不如针对它 由相关角色组成一个局部单元来处理。队长是一个拥有特权的单元成员，它可以指挥其他单 元程序行动。


在球员智能体实现中，角色和阵型的引入是独立的。更衣室协定定义了一个初始阵型， 一个初始的球员到角色的映射，以及为了能动态变换阵型而设的实时的触发器。

任何给定 的时间，每个球员智能体都明确知道当前球队所使用的阵型。智能体在当前阵型中保持着从 队员到角色的映射 A->R 。所有这些团队合作的结构信息都存储在智能体的内部状态中。它 可以通过智能体的内部行为转换。

由于球员智能体都是全自主的，加上环境的限制(信息局部性、通讯受限)，使得无法 保证每个队员都清楚无误的知道自己当前的角色，自然也不清楚准确的映射关系 A->R。事 实上，球员智能体唯一需要准确知道的是自己当前的角色。因此，在实际实现时可以进行简 化，一般不需要每周期都更新维护场上所有队友的角色分配信息。合理利用有限的通讯，可 以逐步的互相通告协调各自的角色信息，直到所有的角色达成一致。

另外考虑到球场上瞬息万变的情况。可以设计几套不同的阵型以应付各种不同的情况和 不同的对手。每个阵型都明确指定场上所有角色和球员的映射关系，当场上的情况满足预定 的阵型变化触发条件时(如比分、球的位置、比赛状态等比较明显的客观信息)，整个球队 就会自动转换阵型，以适应新的情况。


**合作协议**

作为更衣室协定的一部分，球队可以定义多步、多球员的计划在合适的时机 执行。

特别是如果存在总是重复发生的特定状态时，球队在这些状态发生之前制定的计划就 显得十分有意义。合作协议中存储了各角色站位、任务安排(例如发中场球、角球、任意球、 球门球等)，一个完整的合作协议主要由以下几个部分组成:

 - 一个触发条件指明激活一个合作协议所处的状态集
 - 合作协议的角色集 定义了合作协议中参与者要采取的行 为。每个合作协议角色 sprᵢ 包括:
    - 一个要执行的合作协议行为;
    - 一个终止条件指明一个球员智能体应该终止充当合作协议角色恢复它的正常 行为所处的状态集。

一个合作协议不需 要涵盖整个球队:m≤n. 决策系统的战略层将主要运用这些结构来表示、实现高层的规划。具体的决策依据是用 行为树来表示的每个叶结点表示最终在战术层中贯彻执行行为决策。

而中间节点 则是对场上形势的分析。当然，目前的合作还很低级，必须选择一些比较好的智能体体系结构如 BDI 模型，建立完整团队合作的理论，能把新的精神状态作为团队合作的基础，如团 队目标、团队规划、共有信念和联合承诺等[Kitano et al. 1997]，才能实现更高层次的团队合 作。

---















 





