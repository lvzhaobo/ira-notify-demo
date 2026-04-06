# 09 — API 接口规格（工作稿）

> **Base**：`/api/v1`。本稿已补齐 US-M4-001 的 rules CRUD 明细，并与当前后端实现对齐。

## 约定

- **Base path**：`/api/v1`
- **统一错误体**：`{ "error": { "code": "string", "message": "string" }, "traceId": "string" }`
- **业务错误码前缀**：`M4_`

### 错误码（US-001）

| HTTP | `code` | 说明 |
|------|--------|------|
| 400 | `M4_VALIDATION_ERROR` | 参数非法、`channelIds` 无效或未启用、JSON 非法 |
| 404 | `M4_RULE_NOT_FOUND` | 规则不存在 |
| 409 | `M4_RULE_DISABLED` | （预留）禁用规则触发真发 |

---

## 2. DTO

### 2.1 `NotifyRule`

| 字段 | 类型 | 说明 |
|------|------|------|
| `ruleId` | string (UUID) | 服务端生成 |
| `name` | string | 规则名 |
| `enabled` | boolean | 是否启用 |
| `triggerType` | string | `manual` / `schedule` / `event` |
| `scheduleCron` | string \| null | cron，可空 |
| `condition` | object | 结构化条件 |
| `templateId` | string \| null | 模板 ID |
| `channelIds` | string[] | 必须引用已存在且启用的渠道配置 |
| `createdAt` | string | ISO8601 |
| `updatedAt` | string | ISO8601 |

---

## 3. 端点明细

### 3.1 `GET /notify/health`

- `200`：`{ "status": "ok", "module": "M4" }`

### 3.2 `GET /notify/rules`

**Query**：`limit`（默认 20，范围 1~100）、`enabledOnly`（可选，`true/1/yes`）

**响应** `200`：

```json
{
  "items": [
    {
      "ruleId": "550e8400-e29b-41d4-a716-446655440001",
      "name": "早间摘要",
      "enabled": true,
      "triggerType": "manual",
      "scheduleCron": null,
      "condition": { "keywords": ["加息"] },
      "templateId": null,
      "channelIds": ["550e8400-e29b-41d4-a716-446655440000"],
      "createdAt": "2026-04-06T08:00:00+00:00",
      "updatedAt": "2026-04-06T08:00:00+00:00"
    }
  ],
  "nextCursor": null,
  "hasMore": false
}
```

### 3.3 `POST /notify/rules`

**Body**：`NotifyRule` 创建子集（不含 `ruleId`、`createdAt`、`updatedAt`）

```json
{
  "name": "早间摘要",
  "enabled": true,
  "triggerType": "manual",
  "scheduleCron": null,
  "condition": { "keywords": ["加息"] },
  "templateId": null,
  "channelIds": ["550e8400-e29b-41d4-a716-446655440000"]
}
```

**校验**：`channelIds` 任一不存在或未启用 -> `400 M4_VALIDATION_ERROR`

**响应** `201`：`{ "rule": NotifyRule }`

### 3.4 `GET /notify/rules/{ruleId}`

- **成功**：`200`，`{ "rule": NotifyRule }`
- **失败**：`404 M4_RULE_NOT_FOUND`

### 3.5 `PATCH /notify/rules/{ruleId}`

- 支持部分更新字段：`name`、`enabled`、`triggerType`、`scheduleCron`、`condition`、`templateId`、`channelIds`
- `channelIds` 若存在，校验规则同创建

**请求示例**：

```json
{
  "enabled": false,
  "name": "改名后的规则"
}
```

- **成功**：`200`，`{ "rule": NotifyRule }`
- **失败**：
  - `400 M4_VALIDATION_ERROR`
  - `404 M4_RULE_NOT_FOUND`

### 3.6 `DELETE /notify/rules/{ruleId}`

- **成功**：`204`（空响应）
- **失败**：`404 M4_RULE_NOT_FOUND`

---

## 4. 其余 P0 端点（后续 US）

| Method | Path | 对应 US |
|--------|------|---------|
| POST | `/notify/dispatch` | US-M4-002 |
| GET | `/notify/deliveries` | US-M4-002 |
| POST | `/notify/channels/{type}/test` | US-M4-003 |
