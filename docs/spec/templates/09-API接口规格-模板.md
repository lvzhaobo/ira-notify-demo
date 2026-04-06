# 09 — API 接口规格（模板）

> **提示**：路径前缀建议与实现一致（如 `/api/v1`）；错误体建议统一 `{ "error": { "code", "message" }, "traceId" }`。定稿后合并到 **`spec/09-API接口规格.md`**。

## P0 端点清单

| Method | Path | 说明 |
|--------|------|------|
| GET | `/notify/health` | 健康检查 |
| POST | `/notify/rules` | 创建规则 |
| GET | `/notify/rules` | 列表 |
| PATCH | `/notify/rules/{id}` | 更新 |
| DELETE | `/notify/rules/{id}` | 删除 |
| POST | `/notify/dispatch` | 试发 |
| GET | `/notify/deliveries` | 历史 |
| POST | `/notify/channels/{type}/test` | 渠道测试 |

## 错误码（示例）

| HTTP | code | 场景 |
|------|------|------|
| 400 | M4_VALIDATION | channelIds 非法 |
| 429 | M4_RATE_LIMIT | 频控 |

（继续补充）
