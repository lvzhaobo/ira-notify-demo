# M4 Notify Workshop（小组 Fork 用）

本仓库为 **工作坊专用骨架**：**Spec 模板 + 可运行的最小工程 + 业务刻意未实现**。  
目标：练习 **契约先行、分支协作、PR、联调**；P0 功能需小组基于定稿 Spec **自行补全**。

**无 Docker 环境**：不必安装容器；**只按下方「快速开始（本地）」** 即可跑通前后端，工作坊与 Spec 流程 **不依赖** Dockerfile / `docker-compose.yml`（二者仅为可选）。

## 设计说明：不是「空壳 vs 成品」二选一

| 形态 | 本仓库采用 |
|------|------------|
| 几乎空壳 | 仅保留目录与依赖，学员从零写路由。 |
| 能跑的成品 | 功能全好，学员只剩改样式。 |
| **第三路径（本仓库）** | **Flask + React 能启动**；**健康检查可用**；**业务 API 统一返回未实现**；**数据库迁移文件仅有注释提示**；学员按 `09`/`10` 补表、补逻辑、补页面。 |

这样既避免 **环境装三天**，又保证 **有足够代码量与决策点**。

## 仓库里有什么

| 路径 | 说明 |
|------|------|
| `docs/spec/templates/` | **讨论用模板**：`{编号}-{主题}-模板.md`，与 `spec/` 同编号对齐 |
| `spec/` | **工作稿**：`03`/`05`/`09`/`10`/`14`，含少量 **提示**，定稿后应与实现一致 |
| `backend/` | Flask：`/api/v1/notify/health` 可用；其余 notify 端点为 **501 stub** |
| `frontend/` | React：路由与占位页；调用 API 后可见「未实现」或仅 health 成功 |
| `backend/migrations/001_init.sql` | **无有效 CREATE**（仅注释提示），表结构由小组补充 |
| `backend/Dockerfile` / `frontend/Dockerfile` | **可选**：容器化运行（见下节） |
| `docker-compose.yml` | **可选**：`profile=app` 起 API+Web；`profile=full` 起 Postgres+Mailhog |

## Docker（可选）

工作坊 **默认仍推荐本机 `python` + `npm`**，便于热重载。Docker 适合 **统一演示环境** 或学员本机不便装依赖时使用。

```bash
# 后端 + 前端：浏览器打开 http://localhost:8080 （Nginx 将 /api 反代到 api:5000）
docker compose --profile app up --build

# 仅基础设施（PostgreSQL + Mailhog；后端仍须本机或自行接线）
docker compose --profile full up -d
```

说明：`api` 服务通过卷 `ira_notify_sqlite` 持久化 `M4_DATABASE_PATH=/data/notify.db`；与 `compose` 中的 `postgres` **无自动连线**，接 PostgreSQL 需在代码中读取 `DATABASE_URL` 后自行实现（进阶）。

## 快速开始（本地）

**推荐路径**：日常开发与课程练习以本节为准（热重载、排障简单）。未使用 Docker 的学员可跳过上一节「Docker（可选）」。

```bash
# 后端
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt
set FLASK_APP=app.py
flask run --port 5000
# 访问 http://127.0.0.1:5000/api/v1/notify/health

# 前端（新终端）
cd frontend
npm install
npm start
```

**说明**：未配置数据库时，stub 路由不依赖表；一旦开始实现 CRUD，需先补 `migrations` 与 `db.py` 初始化逻辑。

## Spec 与代码的关系

1. 小组复制 **`docs/spec/templates/*-模板.md`** 讨论填空，再合并入 **`spec/`** 对应 **`03`/`05`/`09`/`10`/`14`** 工作稿并提 PR。  
2. **契约变更**：先合并 `09`/`10` 相关段落，再改 `backend/`。  
3. 以 **`spec/09`**、**`spec/10`** 已合并版本为唯一契约来源（与课程 `AGENTS.md` 一致）。

## 与参考实现对比

讲师可另提供 **`solution` 分支** 或独立 **参考答案仓库** 供 diff；本 **`main`** 保持骨架，避免学员直接抄成品。

## 许可

教学用途；请勿提交真实 Webhook 与密钥。
