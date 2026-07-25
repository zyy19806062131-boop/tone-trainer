# 交接单 · 音调训练器 HSK1 重做（2026-07-21）

## 1. 目标
把音调训练器（仓库 `zyy19806062131-boop/tone-trainer`，Render 部署，赛博朋克风单页 + Python 后端 + 口令门禁）里**脑补编造、无出处的 HSK 例句**，全部替换成《HSK标准教程》**课文对话原文**。
用户拍板（2026-07-20）：①**只换内容·保留 App**；②**课文对话/短文为主**；③**先只做 HSK1 验证**，满意再铺 2–4 级。

## 2. 现状
- **HSK1 全 15 课 156 句已完成并本地验证通过**（渲染正确、声调/变调/轻声/儿化对齐 0 错）。
- 所有改动**在本地、未提交、未推送**。`git status`：`data/*.private.json` 已改，新增 `.claude/`、`data-source/`、`HANDOFF_HSK1.md`。
- 音频**未重生成**，现走浏览器 TTS 兜底（发音正常，省 TTS 额度）。
- 旧数据（含 hsk2/hsk3 假句 + 内嵌音频）仍在 git 历史 commit `99d8d05`，需要可 `git show 99d8d05:data/trainer_data.private.json` 取回。

## 3. 已完成
- 从《HSK标准教程1》PDF（`/Volumes/My PSSD/课件和教材/1.HSK/HSK 1/HSK标准教程1.pdf`，**扫描版无文字层**，靠逐页渲染成图**看图转录**）抠出 15 课课文原文。
- 声调/拼音**取自教材**（权威）：变调 bú/yí/yì、电话号 yāo、轻声 sheng/you/zi/hou 等，逐字校验 0 错。
- 逐字对齐：儿化"儿"单列 `er`/轻声(0)/weak；`zh` 存**纯汉字（去标点）**匹配 App 逐字映射契约；标点保留在 `spokenZh` 供 TTS。
- 修正旧数据错误课名（旧"2 我叫李文"→真实"2 谢谢你"，"3 我是中国人"→"3 你叫什么名字"等）。
- 可复现管线落盘 `data-source/`（见第 5 项）。

## 4. 待办（按优先级）
1. **用户验收 HSK1**（本地服务器验收；等用户反馈要不要调）。
2. **音频**：批准后用 `scripts/build_project_audio.py --deck hsk1` 给新句生成女/男声（**要花 TTS 额度**，先小样）。注意旧内嵌音频按旧句 id，新句 id=`lesson-XX-NN`，对不上，需重生成。
3. **铺 HSK2–4**：照 HSK1 同法（HSK 2/3/4 PDF 都在 `1.HSK/` 下；**5、6 级无 PDF，取不到原文**）。复用 `data-source/build_hsk1.py` 的编译逻辑。
4. **部署**：线上是 Render + **Postgres**（`DATABASE_URL`），本地 JSON 只是种子。要把新数据推到线上库才生效——查 server.py 的 `apply_data_migrations` 迁移逻辑，或走 admin 接口/直接改库。
5. **可选**：让显示保留标点（现为零改动兼容，句子不显示 ？！。）。需小改 `public/tone_trainer-ponk.html` 的 `drawContour`（Array.from(zh) 改成只取汉字）+ server.py `validate_sentence` 第 391 行 `len(clean_syl)!=len(zh)` 改成按汉字计数。

## 5. 关键路径 / 命令 / 文件
- 仓库本地：`/Users/a1/Claude/repos/tone-trainer`
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
