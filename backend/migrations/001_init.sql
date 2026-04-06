-- M4 工作坊：notify_channel_configs + notify_rules（对齐 spec/09 DTO）

CREATE TABLE IF NOT EXISTS notify_channel_configs (
  channel_id TEXT PRIMARY KEY,
  channel_type TEXT NOT NULL DEFAULT 'dingtalk',
  enabled INTEGER NOT NULL DEFAULT 1,
  secret_ref TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notify_rules (
  rule_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  enabled INTEGER NOT NULL DEFAULT 1,
  trigger_type TEXT NOT NULL DEFAULT 'manual',
  schedule_cron TEXT,
  condition_json TEXT NOT NULL DEFAULT '{}',
  template_id TEXT,
  channel_ids_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

-- 演示用：一条已启用渠道，供规则 channelIds 引用（与 spec/09 示例 UUID 一致）
INSERT OR IGNORE INTO notify_channel_configs (channel_id, channel_type, enabled, secret_ref, created_at, updated_at)
VALUES (
  '550e8400-e29b-41d4-a716-446655440000',
  'dingtalk',
  1,
  'sandbox-ref-demo',
  '2026-04-06T00:00:00+00:00',
  '2026-04-06T00:00:00+00:00'
);
