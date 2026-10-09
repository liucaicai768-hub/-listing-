# Amazon US 定制产品 Listing Skill

将 `listing规范输出.xlsx` 整理为可复用的 AI skill，用于生成和审核美国站定制商品文案。

入口：[SKILL.md](skills/amazon-us-custom-listing/SKILL.md)。包含字段规则、原始表格和无需第三方依赖的检查脚本。

## 使用

将 `skills/amazon-us-custom-listing` 目录放入所用工具支持的 skills 目录。支持 Codex 的环境可将该目录安装到 `~/.agents/skills/`，然后使用 `$amazon-us-custom-listing` 调用。

提供真实产品资料（类别、材质、尺寸、定制选项、卖点和关键词），例如：

> 使用 $amazon-us-custom-listing，根据以下资料生成 Amazon US listing，并给出合规检查：……

## 检查

```bash
python3 skills/amazon-us-custom-listing/scripts/validate_listing.py /path/to/listing.json
```

JSON 字段：`item_name`、`item_highlight`、`bullet_points`（五个字符串）、`product_description`、`generic_keyword`。

返回码 0 表示机械检查通过，1 表示文案检查失败，2 表示输入或文件错误。语义重复、事实真实性、竞品品牌及当前平台政策需要人工复核。规则来源是用户表格，并非实时官方政策。原文冲突和操作解释见 [规则说明](skills/amazon-us-custom-listing/references/listing-rules.md)。

---

## 亚马逊关键词词库 Skill

根据《关键词 SOP》整理的可复用 Skill，帮助将 ABA、竞品反查、搜索下拉词和拓词数据整理成可审计的多 Sheet Excel 词库。

入口：[skills/amazon-keyword-library/SKILL.md](skills/amazon-keyword-library/SKILL.md)

## 使用

将 `skills/amazon-keyword-library` 整个目录复制到你的 Skill 工具支持的目录。例如 Codex 可使用 `~/.agents/skills/amazon-keyword-library`。重新加载后，以 `$amazon-keyword-library` 调用。

先填写 [项目输入卡](skills/amazon-keyword-library/assets/project-input.md)，再提供原始关键词文件。例如：

> 使用 $amazon-keyword-library，按项目输入卡整理这些 ABA 和竞品反查文件。先合并去重并检查来源，再按产品边界分类，缺失指标留空，输出待人工审核的多 Sheet Excel。

Skill 包含完整操作流程、审核要求、项目输入模板和工作簿规范。它不会自动接入不存在的数据工具，也不会自动投放广告或发布 Listing。Python/openpyxl 是生成 Excel 时的可选实现方式；不需要独立服务或 API 密钥才能读取 Skill。

原始 SOP 中的露营灯仅作为判断示例；每个产品都需要独立的产品边界和人工审核。本仓库不包含原始 Excel 或其中的工具截图。
