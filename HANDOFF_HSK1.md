# 交接单 · 音调训练器 HSK1 重做（2026-07-21）

> **姊妹文档：[`HANDOFF_HSK2.md`](HANDOFF_HSK2.md)（2026-08-05，新版 HSK2 全 15 课 348 句已做完，待部署）。**
> 铺 HSK3/4 之前**必须先读那份的第 5 节「坑」**：HSK2 起句子变长、一个气泡含多句，
> 本册用的「静音切段数 == 句数就按位对应」在那边会**静默错位**，已证明只有 ASR 内容校验靠得住。

## 1. 目标
把音调训练器（仓库 `zyy19806062131-boop/tone-trainer`，Render 部署，赛博朋克风单页 + Python 后端 + 口令门禁）里**脑补编造、无出处的 HSK 例句**，全部替换成《HSK标准教程》**课文对话原文**。
用户拍板（2026-07-20）：①**只换内容·保留 App**；②**课文对话/短文为主**；③**先只做 HSK1 验证**，满意再铺 2–4 级。

## 2. 现状（2026-08-03 第二次更正——第一次更正把「两版教材」误判成「新旧数据」，已被老师当场纠正）
- **HSK1 其实有两版教材，两版都已做完并各自配好真音频**：`hsk1` deck＝**旧版《HSK标准教程1》**（第2课「谢谢你」，153 句，153 条内嵌音频）；`nhsk1` deck＝**新版《新HSK教程1》/HSK3.0**（第2课「我叫李文」，15 课，200 条内嵌音频）。**两个课名都是对的，各属各的教材，不是谁在纠正谁**——上一版把「我叫李文」当成待替换的旧占位句，是我没查证「是否真有两版教材」就下的结论，老师 2026-08-03 当场指出。核实来源：新版第2课＝`My PSSD/教材库/01_成套教材/xin-hsk-jiaocheng/新HSK1PPT/…第2课.pptx`（英文标题 "Lesson 2 My name is Li Wen"）；旧版第2课＝本仓库 `data-source/hsk1_kewen_source.py`（转录自 `HSK标准教程1.pdf`）。
- **仓库代码本体干净、与 origin/main 一致**，`git status` 无待提交项。
- **`data/*.private.json`（真实访问码与训练数据）已于 07-25 有意移出版本控制**（公开仓库不能带真访问码，见 commit `922adc5`），此后**永远不会再进 git**——这不是「还没提交」，是设计如此，往后也不用等它被提交。
- **部署风险已排除**：本会话原本担心 `nhsk1` 这个新 deck id 不在 `server.py:172-196` 的自动迁移函数 `apply_data_migrations()` 处理范围内，线上可能没有新版内容——**老师 2026-08-03 确认线上已经能看到「新HSK1」入口，之前就看过**。所以这条不是理论推测的风险，是已经上线过的事实，具体是走 admin 接口手动推的还是别的路径，没细问，不影响结论。**留一句给以后**：`apply_data_migrations()` 代码本身没变，仍然不认识新 deck id——以后再往 `hsk1`/`nhsk1` 加新内容，**改完重启不会自动同步到线上**，这条经验还成立，只是这次的内容已经用某种方式弄上去了。
- 每个 deck 的音频已是**真人声 TTS 批量生成后内嵌**（base64 embedded in `audio` 字段），不是本条原先写的"未重生成、走浏览器 TTS 兜底"——那句是 07-21 写交接单当时的状态，后续会话已经把两版的音频都补上了，只是这份交接单没跟着更新。
- 旧的占位/测试数据（hsk2/hsk3 假句、scene-speaking 等其他项目早期 deck）仍在 git 历史 commit `99d8d05`，需要可 `git show 99d8d05:data/trainer_data.private.json` 取回，与本条两版 HSK1 教材无关，另案处理。

## 3. 已完成
- 从《HSK标准教程1》PDF（`/Volumes/My PSSD/教材库/01_成套教材/hsk-biaozhun-jiaocheng/HSK1/HSK标准教程1.pdf`，**扫描版无文字层**，靠逐页渲染成图**看图转录**）抠出 15 课课文原文。
- 声调/拼音**取自教材**（权威）：变调 bú/yí/yì、电话号 yāo、轻声 sheng/you/zi/hou 等，逐字校验 0 错。
- 逐字对齐：儿化"儿"单列 `er`/轻声(0)/weak；`zh` 存**纯汉字（去标点）**匹配 App 逐字映射契约；标点保留在 `spokenZh` 供 TTS。
- **⚠️ 这条本条已更正**：原文写「修正旧数据错误课名（旧"2 我叫李文"→真实"2 谢谢你"）」，措辞不准——「我叫李文」不是错误课名，是**新版教材**（HSK3.0）的真实课名，两版并存于 `hsk1`（旧版）+`nhsk1`（新版）两个 deck，不是谁替换谁。当时做的实际工作是「给旧版《HSK标准教程1》补一份独立的课文重写」，不是「纠正新版的错误」。
- 可复现管线落盘 `data-source/`（见第 5 项）。

## 4. 待办（按优先级）
1. **用户验收 HSK1**（线上或本地均可看；**两版都要看**：`hsk1`=旧版标准教程、`nhsk1`=新版HSK3.0）。**部署已确认在线上**（见第 2 节，老师 08-03 已看到「新HSK1」入口），这条现在缺的是「逐句听过、内容满意」这层真验收，还是只是「看到入口存在」——待老师明确。
2. **音频**：两版音频已在本地生成并内嵌（`hsk1` 153 条／`nhsk1` 200 条，见第 2 节），**这条基本已完成**，除非验收后要调整个别句子/重录音色。
3. **铺 HSK2–4**：照 HSK1 同法（HSK 2/3/4 PDF 都在 `1.HSK/` 下；**5、6 级无 PDF，取不到原文**；若新旧两版都要铺，参照 `1.新HSK/` 目录下的新版 PDF/PPT）。复用 `data-source/build_hsk1.py` 的编译逻辑。
4. **部署**：线上是 Render + **Postgres**（`DATABASE_URL`），**新HSK1 已确认在线上**（08-03 老师确认）。以后再更新内容时记得：`init_db()`/`apply_data_migrations()` 都只认已知 deck id（`server.py:172-196`），**改完重启不会自动同步**，得走 admin 接口（`/api/admin/deck`、`/api/admin/sentence` 等）或直接接 `DATABASE_URL` 改库。
5. **可选**：让显示保留标点（现为零改动兼容，句子不显示 ？！。）。需小改 `public/tone_trainer-ponk.html` 的 `drawContour`（Array.from(zh) 改成只取汉字）+ server.py `validate_sentence` 第 391 行 `len(clean_syl)!=len(zh)` 改成按汉字计数。

## 5. 关键路径 / 命令 / 文件
- 仓库本地：`~/Claude/repos/tone-trainer`
- **课文原文源**（人工转录的真源，改内容从这里改）：`data-source/hsk1_kewen_source.py`
- **编译脚本**（源 → deck JSON，含拼音拆分/对齐/变调逻辑）：`data-source/build_hsk1.py`
  - 跑法：`python3 data-source/build_hsk1.py` → 输出 `scratchpad/hsk1_deck.json`（脚本内路径写死在 scratchpad，铺量前改成写进仓库）
- 数据文件（App 实际读）：`data/trainer_data.private.json`（已是新 HSK1）、`data/access_codes.private.json`
- 本地口令：**（见 `~/Claude/私密/` 下的密码记录，不写进仓库）**（decks=all）；admin 口令（同上，见私密目录）
- 本地起服务器：`cd repos/tone-trainer && PORT=8765 python3 server.py`，页面 `http://127.0.0.1:8765/tone_trainer-ponk.html`
- 依赖：pypinyin、PyMuPDF(fitz)、tesseract(chi_sim) 均已装（转码/定位课文页用）

## 6. 坑与决策
- **绝不凭记忆编课文**：PDF 是扫描图，必须渲染成图看图转录（出处可查），这是本次重做的红线依据。
- **拼音源用教材不用 pypinyin**：pypinyin 默认读音有多音字/变调差异（谁 shuí≠shéi、一不变调、ü 归一），教材才权威；pypinyin 只用来定"每字几字母"的边界。
- **对齐契约**：App 用 `Array.from(zh)[i]` 映射 `syl[i]`，不跳标点 → 所以 `zh` 必须纯汉字、音节数==汉字数（server `validate_sentence` 也强制此约束）。
- **数字用汉字**：教材"50/28/9月"等，为逐字对齐一律写成汉字（五十/二十八/九月）。
- **审美无上限**：验收后按用户意见迭代，别停在"能用"。
