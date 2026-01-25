# Post-Market Monitoring (PMM) System

符合 EU AI Act Article 72 的 AI 系统监控平台，具有 AI 驱动信号检测的警戒仪表板。

## 功能特性

### 核心功能

**Functionality 1**: Post-Market Monitoring Plan
- 自动化监控计划创建
- 基于风险级别的指标配置
- 符合 EU AI Act Article 72

**Functionality 2**: Performance Metrics Tracking
- 6 个核心指标追踪：response_accuracy, hallucination_rate, privacy_incidents, user_satisfaction, prompt_injection_attempts, citation_accuracy
- 实时阈值检查和告警
- 趋势分析和预测

**Functionality 3**: User Feedback Collection and Analysis
- 自动情感分析
- 智能分类
- 趋势检测

### Post-Market Monitoring Dashboard

**Signal Detection** - AI 驱动的信号检测
- 异常检测 (Z-score based anomaly detection)
- 趋势变化检测 (Trend change detection)
- 模式识别 (Pattern detection)

**Trend Analysis** - 趋势分析
- 指标趋势分析
- 预测分析
- 历史数据对比

**Complaint Tracking** - 投诉跟踪
- 投诉创建和管理
- 状态跟踪和更新
- 投诉分析统计

**Performance Monitoring** - 性能监控
- 实时性能指标
- SLA 合规状态
- 历史性能数据

**Regulatory Reporting** - 法规报告
- EU AI Act Article 72 合规状态
- 自动报告生成
- 合规性审计

## 集成模块

- **ai-safety-planning**: 安全指标和阈值配置
- **ai-ethics-advisor**: 偏见监控和伦理评估
- **incident-responder**: 事件响应和管理

## 快速开始

### 1. 安装依赖

```bash
cd pmm_system
pip install -r pmm_system/requirements.txt
```

### 2. 启动 API

```bash
python -m uvicorn pmm_agent.main:app --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档

### 3. 测试 API

```bash
python scripts/test_client.py
```

### 4. 运行演示

```bash
python scripts/demo.py
```

## 项目结构

```
pmm_system/
├── pmm_agent/                    # 核心代码
│   ├── core/                     # 核心模块
│   │   ├── pmm_core.py           # PMM 核心代理
│   │   └── dashboard.py          # Dashboard 核心（信号检测、趋势分析等）
│   ├── integrations/             # 集成模块
│   │   ├── safety_provider.py    # ai-safety-planning 集成
│   │   ├── ethics_bridge.py      # ai-ethics-advisor 集成
│   │   └── incident_trigger.py   # incident-responder 集成
│   ├── data/                     # 数据模型和存储
│   │   ├── models.py             # 数据模型
│   │   └── storage.py            # 存储层
│   ├── api/                      # API 端点
│   └── main.py                   # FastAPI 应用
├── scripts/                      # 脚本
│   ├── demo.py                   # 演示脚本
│   └── test_client.py            # API 测试客户端
├── tests/                        # 测试
│   └── test_basic.py             # 基本测试
├── pmm_data/                     # 数据存储目录
├── pmm_system/
│   └── requirements.txt          # 依赖
├── RUN_GUIDE.md                  # 运行指南
└── README.md                     # 本文件
```

## API 端点

### 核心 PMM API

| 端点 | 方法 | 功能 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/api/v1/interactions/log` | POST | 记录 AI 交互 |
| `/api/v1/feedback/submit` | POST | 提交用户反馈 |
| `/api/v1/metrics/query` | POST | 查询指标 |
| `/api/v1/metrics/current` | GET | 获取当前指标 |
| `/api/v1/alerts/active` | GET | 获取活跃告警 |
| `/api/v1/incidents/active` | GET | 获取活跃事件 |
| `/api/v1/reports/summary` | GET | 综合报告 |
| `/api/v1/reports/bias` | GET | 偏见报告 |
| `/api/v1/stats` | GET | 系统统计 |

### Dashboard API

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/v1/dashboard/overview` | GET | 仪表板概览 |
| `/api/v1/dashboard/kpis` | GET | 关键性能指标 |

### Signal Detection API

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/v1/signals/detect` | GET | 运行 AI 信号检测 |
| `/api/v1/signals/history` | GET | 历史信号记录 |
| `/api/v1/signals/{id}/acknowledge` | POST | 确认信号 |

### Trend Analysis API

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/v1/trends/metrics` | GET | 指标趋势分析 |
| `/api/v1/trends/forecast` | GET | 预测分析 |

### Complaint Tracking API

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/v1/complaints` | GET | 获取投诉列表 |
| `/api/v1/complaints` | POST | 创建投诉 |
| `/api/v1/complaints/{id}` | GET | 获取投诉详情 |
| `/api/v1/complaints/{id}` | PUT | 更新投诉 |
| `/api/v1/complaints/analytics` | GET | 投诉分析统计 |

### Performance Monitoring API

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/v1/performance/realtime` | GET | 实时性能数据 |
| `/api/v1/performance/history` | GET | 历史性能数据 |
| `/api/v1/performance/sla` | GET | SLA 合规状态 |

### Regulatory Reporting API

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/v1/regulatory/compliance-status` | GET | EU AI Act 合规状态 |
| `/api/v1/regulatory/reports` | GET | 报告列表 |
| `/api/v1/regulatory/reports/generate` | POST | 生成法规报告 |
| `/api/v1/regulatory/reports/{id}` | GET | 报告详情 |

## 监控指标

| 指标 | 目标 | 告警阈值 | 临界阈值 |
|------|------|---------|---------|
| response_accuracy | >95% | <90% | <85% |
| hallucination_rate | <5% | >10% | >15% |
| user_satisfaction | >4.0 | <3.5 | <3.0 |
| citation_accuracy | >99% | <95% | <90% |
| privacy_incidents | 0 | >1 | >3 |

## EU AI Act 合规

本系统符合 EU AI Act Article 72 的以下要求：

- **Article 72.1**: Post-market monitoring system established
- **Article 72.2**: Data collection and analysis procedures defined
- **Article 72.3**: Serious incident reporting mechanism in place
- **Article 72.4**: Corrective action procedures established
- **Article 72.5**: Documentation maintained and updated

## 测试

```bash
# 运行基本测试
pytest tests/test_basic.py -v

# 运行所有测试
pytest tests/ -v

# 运行 API 测试（需要先启动服务器）
python scripts/test_client.py
```

## 技术栈

- **框架**: FastAPI
- **语言**: Python 3.10+
- **数据**: JSON (文件存储)
- **测试**: pytest

## 文档

- **[RUN_GUIDE.md](./RUN_GUIDE.md)** - 详细运行和测试指南
- **[POST_MARKET_MONITORING_DESIGN.md](./POST_MARKET_MONITORING_DESIGN.md)** - 系统设计文档
- **[QUICK_START_GUIDE.md](./QUICK_START_GUIDE.md)** - 快速入门指南
- **[INTEGRATION_EXAMPLE.py](./INTEGRATION_EXAMPLE.py)** - 集成示例代码

## 许可

遵循项目整体许可协议

---

**Version**: 2.0.0
**Status**: MVP - Ready for Testing
**Last Updated**: 2026-01-24
