# 09 — API 接口规格（工作稿）

> **工作坊提示**：以下为 **P0 路径清单 + 约束**；请求/响应 JSON 请小组补全并与前端联调。前缀与 `backend` 注册一致：`/api/v1`。讨论用模板：`docs/spec/templates/09-API接口规格-模板.md`。

## 约定

- **Base path**：`/api/v1`
- **错误体**（建议）：`{ "error": { "code": "string", "message": "string" }, "traceId": "string" }`
- **提示**：先定错误码枚举，再写实现，避免前后端各写一套字符串。

## P0 端点（须与实现一致）

| Method | Path | 说明 |
|--------|------|------|
| GET | `/notify/health` | 存活探测（**工作坊骨架已实现**） |
| POST | `/notify/rules` | 创建规则 |
| GET | `/notify/rules` | 列表 |
| GET | `/notify/rules/{id}` | 详情（若 P0 需要） |
| PATCH | `/notify/rules/{id}` | 更新 |
| DELETE | `/notify/rules/{id}` | 删除 |
| POST | `/notify/dispatch` | 试发 |
| GET | `/notify/deliveries` | 投递历史 |
| POST | `/notify/channels/{type}/test` | 渠道连通性测试 |

## 请求/响应示例（TODO）

> 提示：在 PR 中补充 JSON 示例（至少各 1 个成功 + 1 个 4xx）。

（小组在此追加章节：§3.2 …）
