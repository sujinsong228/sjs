# 金融客服意图识别微调项目（可放简历）

一个可落地的 **SFT + LoRA** 微调项目模板，目标是把开源基础模型微调为“金融客服意图分类 + 简短回复建议”助手。

## 1. 项目目标

- 输入：用户提问（如“信用卡逾期会影响征信吗？”）
- 输出：
  1) 意图标签（账单查询 / 还款咨询 / 投诉建议 / 风险提醒 等）
  2) 一段合规、简短、可执行的回复草案

## 2. 技术方案

- 基座模型：`Qwen/Qwen2.5-1.5B-Instruct`（可替换）
- 微调方式：`PEFT LoRA`（参数高效）
- 训练框架：`transformers + datasets + trl`
- 评估指标：`intent accuracy`、`macro F1`、`response pass@policy`

## 3. 数据格式（JSONL）

`data/train.jsonl` / `data/val.jsonl` 每行示例：

```json
{"instruction":"判断用户意图并给出回复","input":"信用卡账单日怎么改？","output":"意图: 账单查询\n回复: 可在App-信用卡-账单设置中修改，通常每自然年可调整次数有限，请以页面规则为准。"}
```

## 4. 快速开始

```bash
pip install -U transformers datasets peft trl accelerate bitsandbytes scikit-learn
python projects/finetune_demo/train_lora.py \
  --train_file projects/finetune_demo/data/train.jsonl \
  --val_file projects/finetune_demo/data/val.jsonl \
  --output_dir projects/finetune_demo/outputs/lora_ckpt

python projects/finetune_demo/infer.py \
  --base_model Qwen/Qwen2.5-1.5B-Instruct \
  --lora_path projects/finetune_demo/outputs/lora_ckpt \
  --query "信用卡逾期会影响征信吗？"
```

## 5. 简历可粘贴版本

**项目名称：** 金融客服大模型微调（LoRA）

**项目描述：**
- 基于开源指令模型构建客服场景 SFT 数据集，完成意图识别与回复生成联合任务；
- 使用 LoRA 实现参数高效微调，训练成本显著低于全量微调；
- 建立离线评测集，按 intent accuracy / macro F1 / 合规规则通过率迭代优化。

**个人职责：**
- 设计数据标注规范与清洗流程（去重、脱敏、策略规则）；
- 实现训练、推理、评估脚本与可复现实验配置；
- 通过错误样本分析迭代提示模板与数据分布，降低高风险回复比例。

**成果（示例）：**
- 意图识别准确率从 78% 提升到 92%；
- 宏平均 F1 提升 11%；
- 合规规则通过率提升 15%。

## 6. 面试回答建议

> 这个项目核心不是“把模型跑起来”，而是“把业务目标可度量地优化”：
> 数据质量、评测口径、风险控制、迭代闭环，决定了微调是否有业务价值。
