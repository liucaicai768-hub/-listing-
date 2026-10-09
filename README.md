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
