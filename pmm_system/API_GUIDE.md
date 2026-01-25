# PMM System API Guide

本文档详细说明各功能的数据流、API 调用顺序、请求/响应示例及数据含义。

## 目录

1. [系统概览](#1-系统概览)
2. [核心监控流程](#2-核心监控流程)
3. [Dashboard 概览](#3-dashboard-概览)
4. [信号检测流程](#4-信号检测流程)
5. [趋势分析流程](#5-趋势分析流程)
6. [投诉跟踪流程](#6-投诉跟踪流程)
7. [性能监控流程](#7-性能监控流程)
8. [法规报告流程](#8-法规报告流程)

---

## 1. 系统概览

### 整体数据流

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PMM System Data Flow                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  AI System ──► Log Interaction ──► Extract Metrics ──► Check Thresholds    │
│                      │                    │                   │              │
│                      ▼                    ▼                   ▼              │
│               Store Data            Update Buffer      Generate Alerts      │
│                      │                    │                   │              │
│                      └────────────────────┼───────────────────┘              │
│                                           ▼                                  │
│                                    Signal Detection                          │
│                                           │                                  │
│                      ┌────────────────────┼────────────────────┐             │
│                      ▼                    ▼                    ▼             │
│               Trend Analysis      Anomaly Detection     Pattern Detection   │
│                      │                    │                    │             │
│                      └────────────────────┼────────────────────┘             │
│                                           ▼                                  │
│                                     Dashboard                                │
│                                           │                                  │
│                      ┌────────────────────┼────────────────────┐             │
│                      ▼                    ▼                    ▼             │
│                Complaints          Performance           Regulatory         │
│                 Tracking            Monitoring            Reporting         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 基础 URL

```
http://localhost:8000
```

### 通用响应格式

所有 API 响应都是 JSON 格式，包含以下通用字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `timestamp` | string | ISO 8601 格式的时间戳 |
| `status` | string | 操作状态 (如 "logged", "created", "completed") |

---

## 2. 核心监控流程

### 数据流

```
User/AI System ──► POST /interactions/log ──► Metrics Extraction
                                                      │
                         ┌────────────────────────────┼────────────────────────────┐
                         ▼                            ▼                            ▼
                  Store Interaction            Check Thresholds             Bias Monitoring
                         │                            │                            │
                         ▼                            ▼                            ▼
                   Update Metrics              Generate Alerts           Ethics Assessment
                         │                            │                            │
                         └────────────────────────────┼────────────────────────────┘
                                                      ▼
                                              Create Incidents
```

### Step 1: 记录 AI 交互

**请求**

```http
POST /api/v1/interactions/log
Content-Type: application/json
```

```json
{
    "interaction_id": "INT-20260124-001",
    "user_id": "user_123",
    "prompt": "What are the EU AI Act requirements for high-risk systems?",
    "response": "The EU AI Act requires high-risk AI systems to...",
    "response_time": 0.523,
    "model_version": "gpt-4-turbo",
    "metadata": {
        "temperature": 0.7,
        "max_tokens": 1000
    },
    "demographics": {
        "gender": "female",
        "age": "25-35",
        "region": "EU"
    }
}
```

**字段说明**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `interaction_id` | string | 是 | 交互唯一标识符 |
| `user_id` | string | 否 | 用户标识符 |
| `prompt` | string | 是 | 用户输入的提示 |
| `response` | string | 是 | AI 系统的响应 |
| `response_time` | float | 是 | 响应时间（秒） |
| `model_version` | string | 否 | AI 模型版本 |
| `metadata` | object | 否 | 额外元数据 |
| `demographics` | object | 否 | 用户人口统计信息（用于偏见监控） |

**响应**

```json
{
    "status": "logged",
    "interaction_id": "INT-20260124-001",
    "summary": {
        "interaction_id": "INT-20260124-001",
        "metrics_computed": 5,
        "alerts_triggered": 0,
        "bias_alerts": 0,
        "incidents_created": 0,
        "ethics_assessment": false,
        "timestamp": "2026-01-24T10:30:00+00:00"
    }
}
```

**响应字段说明**

| 字段 | 说明 |
|------|------|
| `metrics_computed` | 计算的指标数量 |
| `alerts_triggered` | 触发的告警数量 |
| `bias_alerts` | 偏见相关告警数量 |
| `incidents_created` | 创建的事件数量 |
| `ethics_assessment` | 是否触发伦理评估 |

### Step 2: 提交用户反馈

**请求**

```http
POST /api/v1/feedback/submit
Content-Type: application/json
```

```json
{
    "interaction_id": "INT-20260124-001",
    "user_id": "user_123",
    "rating": 4,
    "comment": "Good response but could be more detailed about Article 72.",
    "issues": ["incomplete_info"]
}
```

**字段说明**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `interaction_id` | string | 是 | 关联的交互 ID |
| `user_id` | string | 否 | 用户标识符 |
| `rating` | integer | 是 | 评分 (1-5) |
| `comment` | string | 否 | 用户评论 |
| `issues` | array | 否 | 问题标签列表 |

**响应**

```json
{
    "status": "received",
    "feedback_id": "FB-1706094600.123",
    "analysis": {
        "feedback_id": "FB-1706094600.123",
        "sentiment": "positive",
        "categories": ["high_satisfaction", "accuracy_issue"],
        "requires_action": false
    }
}
```

**响应字段说明**

| 字段 | 说明 |
|------|------|
| `sentiment` | 情感分析结果: positive/neutral/negative |
| `categories` | 自动分类标签 |
| `requires_action` | 是否需要采取行动（rating <= 2 时为 true） |

### Step 3: 查询指标

**请求**

```http
POST /api/v1/metrics/query
Content-Type: application/json
```

```json
{
    "metric_names": ["response_accuracy", "hallucination_rate", "user_satisfaction"],
    "hours": 24
}
```

**响应**

```json
{
    "metrics": {
        "response_accuracy": {
            "average": 0.932,
            "count": 150,
            "target": 0.95,
            "status": "✓ OK",
            "trend": "stable"
        },
        "hallucination_rate": {
            "average": 0.048,
            "count": 150,
            "target": 0.05,
            "status": "✓ OK",
            "trend": "improving"
        },
        "user_satisfaction": {
            "average": 4.2,
            "count": 45,
            "target": 4.0,
            "status": "✓ OK",
            "trend": "stable"
        }
    },
    "period_hours": 24,
    "timestamp": "2026-01-24T10:35:00+00:00"
}
```

**指标状态说明**

| 状态 | 说明 |
|------|------|
| `✓ OK` | 指标在目标范围内 |
| `✗ ALERT` | 指标超出告警阈值 |

**趋势说明**

| 趋势 | 说明 |
|------|------|
| `improving` | 指标正在改善 |
| `stable` | 指标保持稳定 |
| `declining` | 指标正在下降 |

### Step 4: 查看告警

**请求**

```http
GET /api/v1/alerts/active
```

**响应**

```json
{
    "alerts": [
        {
            "alert_id": "ALT-1706094650.789",
            "timestamp": "2026-01-24T09:15:00+00:00",
            "severity": "high",
            "alert_type": "response_accuracy_threshold_violation",
            "metric_name": "response_accuracy",
            "current_value": 0.872,
            "threshold": 0.90
        }
    ],
    "count": 1
}
```

**告警严重程度**

| 级别 | 说明 |
|------|------|
| `critical` | 临界告警，需立即处理 |
| `high` | 高优先级告警 |
| `medium` | 中等优先级 |
| `low` | 低优先级 |

---

## 3. Dashboard 概览

### 数据流

```
Dashboard Request ──► Aggregate Data ──► Calculate Health Score ──► Return Overview
                            │
           ┌────────────────┼────────────────┐
           ▼                ▼                ▼
      Active Signals   Active Alerts   Open Complaints
           │                │                │
           └────────────────┼────────────────┘
                            ▼
                     Trends Summary
```

### 获取仪表板概览

**请求**

```http
GET /api/v1/dashboard/overview
```

**响应**

```json
{
    "timestamp": "2026-01-24T10:40:00+00:00",
    "health_score": 85,
    "health_status": "warning",
    "active_signals": 2,
    "active_alerts": 1,
    "open_complaints": 3,
    "feedback_today": 12,
    "metrics_tracked": 5,
    "trends_summary": {
        "response_accuracy": {
            "direction": "stable",
            "current": 0.932
        },
        "hallucination_rate": {
            "direction": "improving",
            "current": 0.048
        },
        "user_satisfaction": {
            "direction": "stable",
            "current": 4.2
        }
    },
    "compliance_status": "compliant",
    "last_report": "REG-20260123-0001"
}
```

**字段说明**

| 字段 | 类型 | 说明 |
|------|------|------|
| `health_score` | integer | 系统健康分数 (0-100) |
| `health_status` | string | 健康状态: healthy/warning/degraded/critical |
| `active_signals` | integer | 活跃的检测信号数量 |
| `active_alerts` | integer | 活跃的告警数量 |
| `open_complaints` | integer | 未解决的投诉数量 |
| `feedback_today` | integer | 今日收到的反馈数量 |
| `metrics_tracked` | integer | 跟踪的指标数量 |
| `trends_summary` | object | 各指标的趋势摘要 |
| `compliance_status` | string | EU AI Act 合规状态 |
| `last_report` | string | 最近一次法规报告 ID |

**健康分数计算规则**

| 条件 | 扣分 |
|------|------|
| 每个 CRITICAL 信号 | -15 |
| 每个 HIGH 信号 | -10 |
| 每个 MEDIUM 信号 | -5 |
| 每个 CRITICAL 告警 | -20 |
| 每个 HIGH 告警 | -10 |

### 获取 KPI

**请求**

```http
GET /api/v1/dashboard/kpis
```

**响应**

```json
{
    "timestamp": "2026-01-24T10:45:00+00:00",
    "interactions": {
        "last_24h": 156,
        "last_7d": 1023,
        "avg_per_day": 146.14
    },
    "feedback": {
        "count_7d": 89,
        "avg_rating": 4.15,
        "satisfaction_rate": 78.5
    },
    "metrics": {
        "response_accuracy": 0.932,
        "hallucination_rate": 0.048,
        "user_satisfaction": 4.2
    },
    "alerts": {
        "active": 1,
        "last_24h": 3
    },
    "signals": {
        "active": 2,
        "detected_7d": 8
    }
}
```

**字段说明**

| 字段 | 说明 |
|------|------|
| `interactions.last_24h` | 过去 24 小时的交互数量 |
| `interactions.last_7d` | 过去 7 天的交互数量 |
| `feedback.satisfaction_rate` | 满意率百分比 (rating >= 4 的比例) |
| `signals.detected_7d` | 过去 7 天检测到的信号总数 |

---

## 4. 信号检测流程

### 数据流

```
Trigger Detection ──► Analyze Metrics Buffer ──► Run Detection Algorithms
                                                          │
                             ┌────────────────────────────┼────────────────────────────┐
                             ▼                            ▼                            ▼
                      Anomaly Detection           Trend Change Detection        Pattern Detection
                      (Z-score based)             (Compare half periods)        (Consecutive drops)
                             │                            │                            │
                             └────────────────────────────┼────────────────────────────┘
                                                          ▼
                                                   Store Signals
                                                          │
                                                          ▼
                                                   Return Results
```

### Step 1: 运行信号检测

**请求**

```http
GET /api/v1/signals/detect
```

**响应**

```json
{
    "status": "completed",
    "signals_detected": 2,
    "signals": [
        {
            "signal_id": "SIG-20260124103000-0001",
            "type": "anomaly",
            "severity": "high",
            "metric": "response_accuracy",
            "description": "Anomaly detected: response_accuracy = 0.8150 (expected ~0.9320, z-score: 2.45)"
        },
        {
            "signal_id": "SIG-20260124103000-0002",
            "type": "trend_change",
            "severity": "medium",
            "metric": "hallucination_rate",
            "description": "Trend change detected: hallucination_rate is increasing (+18.5% change)"
        }
    ],
    "timestamp": "2026-01-24T10:30:00+00:00"
}
```

**信号类型说明**

| 类型 | 说明 | 检测方法 |
|------|------|----------|
| `anomaly` | 异常值 | Z-score > 2.0 标准差 |
| `trend_change` | 趋势变化 | 前后半段均值变化 > 15% |
| `pattern_detected` | 模式检测 | 连续 4 次或以上下降 |
| `threshold_breach` | 阈值突破 | 超过预设阈值 |
| `drift_detected` | 数据漂移 | 分布偏移检测 |

### Step 2: 查看信号历史

**请求**

```http
GET /api/v1/signals/history?status=active&hours=24
```

**参数说明**

| 参数 | 类型 | 说明 |
|------|------|------|
| `status` | string | 过滤状态: active/acknowledged/resolved/false_positive |
| `hours` | integer | 时间范围（小时） |

**响应**

```json
{
    "signals": [
        {
            "signal_id": "SIG-20260124103000-0001",
            "timestamp": "2026-01-24T10:30:00+00:00",
            "type": "anomaly",
            "severity": "high",
            "metric_name": "response_accuracy",
            "detected_value": 0.815,
            "expected_value": 0.932,
            "deviation": -12.55,
            "confidence": 0.89,
            "description": "Anomaly detected: response_accuracy = 0.8150...",
            "status": "active"
        }
    ],
    "count": 1,
    "period_hours": 24
}
```

**字段说明**

| 字段 | 说明 |
|------|------|
| `detected_value` | 检测到的实际值 |
| `expected_value` | 期望值（历史均值） |
| `deviation` | 偏差百分比 |
| `confidence` | 检测置信度 (0-1) |

### Step 3: 确认信号

**请求**

```http
POST /api/v1/signals/SIG-20260124103000-0001/acknowledge
Content-Type: application/json
```

```json
{
    "acknowledged_by": "admin@company.com"
}
```

**响应**

```json
{
    "status": "acknowledged",
    "signal_id": "SIG-20260124103000-0001",
    "acknowledged_by": "admin@company.com",
    "timestamp": "2026-01-24T10:35:00+00:00"
}
```

---

## 5. 趋势分析流程

### 数据流

```
Request Trends ──► Fetch Metrics Data ──► Calculate Statistics ──► Determine Trend Direction
                                                                            │
                                                                            ▼
                                                                    Generate Forecast
                                                                            │
                                                                            ▼
                                                                     Return Analysis
```

### Step 1: 获取所有指标趋势

**请求**

```http
GET /api/v1/trends/metrics?hours=24
```

**响应**

```json
{
    "trends": {
        "response_accuracy": {
            "metric_name": "response_accuracy",
            "current_value": 0.932,
            "mean": 0.928,
            "std": 0.015,
            "min": 0.895,
            "max": 0.965,
            "trend_direction": "stable",
            "trend_strength": 0.0,
            "data_points": 150,
            "forecast": {
                "next_value": 0.934,
                "next_3": 0.938,
                "confidence": 0.7
            },
            "analysis_time": "2026-01-24T10:50:00+00:00"
        },
        "hallucination_rate": {
            "metric_name": "hallucination_rate",
            "current_value": 0.048,
            "mean": 0.052,
            "std": 0.008,
            "min": 0.035,
            "max": 0.072,
            "trend_direction": "improving",
            "trend_strength": 0.15,
            "data_points": 150,
            "forecast": {
                "next_value": 0.045,
                "next_3": 0.039,
                "confidence": 0.65
            },
            "analysis_time": "2026-01-24T10:50:00+00:00"
        }
    },
    "period_hours": 24,
    "timestamp": "2026-01-24T10:50:00+00:00"
}
```

**字段说明**

| 字段 | 说明 |
|------|------|
| `mean` | 期间内的平均值 |
| `std` | 标准差 |
| `min` / `max` | 最小值 / 最大值 |
| `trend_direction` | 趋势方向: increasing/stable/decreasing |
| `trend_strength` | 趋势强度 (0-1) |
| `forecast.next_value` | 预测的下一个值 |
| `forecast.next_3` | 预测 3 个周期后的值 |
| `forecast.confidence` | 预测置信度 |

### Step 2: 获取特定指标预测

**请求**

```http
GET /api/v1/trends/forecast?metric_name=response_accuracy&hours=48
```

**响应**

```json
{
    "metric_name": "response_accuracy",
    "analysis": {
        "metric_name": "response_accuracy",
        "current_value": 0.932,
        "mean": 0.925,
        "std": 0.018,
        "min": 0.885,
        "max": 0.968,
        "trend_direction": "stable",
        "trend_strength": 0.05,
        "data_points": 280,
        "forecast": {
            "next_value": 0.933,
            "next_3": 0.935,
            "confidence": 0.72
        },
        "analysis_time": "2026-01-24T10:55:00+00:00"
    },
    "period_hours": 48,
    "timestamp": "2026-01-24T10:55:00+00:00"
}
```

---

## 6. 投诉跟踪流程

### 数据流

```
Create Complaint ──► Assign Priority ──► Store Complaint
                                               │
                                               ▼
                                        Track Updates
                                               │
        ┌──────────────────────────────────────┼──────────────────────────────────────┐
        ▼                                      ▼                                      ▼
  Update Status                          Assign Owner                         Add Resolution
        │                                      │                                      │
        └──────────────────────────────────────┼──────────────────────────────────────┘
                                               ▼
                                         Close Complaint
                                               │
                                               ▼
                                        Update Analytics
```

### Step 1: 创建投诉

**请求**

```http
POST /api/v1/complaints
Content-Type: application/json
```

```json
{
    "user_id": "user_456",
    "category": "accuracy",
    "subject": "Incorrect information about EU AI Act Article 72",
    "description": "The AI system provided outdated information about the post-market monitoring requirements. The response mentioned requirements that have been amended in the latest version of the regulation.",
    "priority": "high",
    "related_interaction_id": "INT-20260124-001",
    "tags": ["accuracy", "eu-ai-act", "legal"]
}
```

**字段说明**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | 否 | 投诉用户 ID |
| `category` | string | 是 | 投诉类别 |
| `subject` | string | 是 | 投诉主题 |
| `description` | string | 是 | 详细描述 |
| `priority` | string | 否 | 优先级: critical/high/medium/low |
| `related_interaction_id` | string | 否 | 关联的交互 ID |
| `tags` | array | 否 | 标签列表 |

**投诉类别**

| 类别 | 说明 |
|------|------|
| `accuracy` | 准确性问题 |
| `bias` | 偏见问题 |
| `privacy` | 隐私问题 |
| `performance` | 性能问题 |
| `safety` | 安全问题 |
| `other` | 其他 |

**响应**

```json
{
    "status": "created",
    "complaint_id": "CMP-20260124-0001",
    "timestamp": "2026-01-24T11:00:00+00:00"
}
```

### Step 2: 获取投诉列表

**请求**

```http
GET /api/v1/complaints?status=open&priority=high&days=30
```

**参数说明**

| 参数 | 类型 | 说明 |
|------|------|------|
| `status` | string | 状态过滤: open/in_progress/under_review/resolved/closed |
| `priority` | string | 优先级过滤: critical/high/medium/low |
| `days` | integer | 时间范围（天） |

**响应**

```json
{
    "complaints": [
        {
            "complaint_id": "CMP-20260124-0001",
            "created_at": "2026-01-24T11:00:00+00:00",
            "user_id": "user_456",
            "category": "accuracy",
            "subject": "Incorrect information about EU AI Act Article 72",
            "priority": "high",
            "status": "open",
            "assigned_to": null,
            "tags": ["accuracy", "eu-ai-act", "legal"]
        }
    ],
    "count": 1,
    "period_days": 30
}
```

### Step 3: 获取投诉详情

**请求**

```http
GET /api/v1/complaints/CMP-20260124-0001
```

**响应**

```json
{
    "complaint_id": "CMP-20260124-0001",
    "created_at": "2026-01-24T11:00:00+00:00",
    "user_id": "user_456",
    "category": "accuracy",
    "subject": "Incorrect information about EU AI Act Article 72",
    "description": "The AI system provided outdated information...",
    "priority": "high",
    "status": "in_progress",
    "assigned_to": "support@company.com",
    "related_interaction_id": "INT-20260124-001",
    "resolution": null,
    "resolved_at": null,
    "tags": ["accuracy", "eu-ai-act", "legal"],
    "updates": [
        {
            "timestamp": "2026-01-24T11:30:00+00:00",
            "changes": {
                "status": "in_progress",
                "assigned_to": "support@company.com"
            }
        }
    ]
}
```

### Step 4: 更新投诉

**请求**

```http
PUT /api/v1/complaints/CMP-20260124-0001
Content-Type: application/json
```

```json
{
    "status": "resolved",
    "resolution": "Updated the knowledge base with correct Article 72 information. Retrained the model with the latest EU AI Act amendments."
}
```

**响应**

```json
{
    "status": "updated",
    "complaint_id": "CMP-20260124-0001",
    "updates": {
        "status": "resolved",
        "resolution": "Updated the knowledge base..."
    },
    "timestamp": "2026-01-24T12:00:00+00:00"
}
```

### Step 5: 获取投诉分析

**请求**

```http
GET /api/v1/complaints/analytics?days=30
```

**响应**

```json
{
    "analytics": {
        "total": 25,
        "period_days": 30,
        "by_status": {
            "open": 5,
            "in_progress": 8,
            "resolved": 10,
            "closed": 2
        },
        "by_priority": {
            "critical": 2,
            "high": 8,
            "medium": 10,
            "low": 5
        },
        "by_category": {
            "accuracy": 12,
            "performance": 6,
            "bias": 4,
            "privacy": 2,
            "other": 1
        },
        "resolution_stats": {
            "resolved_count": 12,
            "avg_resolution_hours": 18.5,
            "min_resolution_hours": 2.0,
            "max_resolution_hours": 72.0
        },
        "open_count": 13
    },
    "timestamp": "2026-01-24T12:05:00+00:00"
}
```

**字段说明**

| 字段 | 说明 |
|------|------|
| `resolution_stats.avg_resolution_hours` | 平均解决时间（小时） |
| `open_count` | 当前未解决的投诉数量 |

---

## 7. 性能监控流程

### 数据流

```
Request Performance ──► Capture Snapshot ──► Calculate Metrics ──► Check SLA
                                                    │
                           ┌────────────────────────┼────────────────────────┐
                           ▼                        ▼                        ▼
                    Response Time              Throughput               Error Rate
                           │                        │                        │
                           └────────────────────────┼────────────────────────┘
                                                    ▼
                                             Store Snapshot
                                                    │
                                                    ▼
                                             Return Metrics
```

### Step 1: 获取实时性能

**请求**

```http
GET /api/v1/performance/realtime
```

**响应**

```json
{
    "timestamp": "2026-01-24T12:10:00+00:00",
    "response_time": {
        "avg_ms": 185.32,
        "p95_ms": 456.78,
        "sla_status": "ok"
    },
    "throughput": {
        "requests_per_sec": 112.5,
        "sla_status": "ok"
    },
    "availability": {
        "percentage": 99.95,
        "sla_status": "ok"
    },
    "error_rate": {
        "percentage": 0.45,
        "sla_status": "ok"
    },
    "active_users": 127,
    "system": {
        "cpu_usage": 45.2,
        "memory_usage": 62.8,
        "request_queue": 12
    }
}
```

**字段说明**

| 字段 | 说明 |
|------|------|
| `response_time.avg_ms` | 平均响应时间（毫秒） |
| `response_time.p95_ms` | P95 响应时间（毫秒） |
| `throughput.requests_per_sec` | 每秒请求数 |
| `availability.percentage` | 可用性百分比 |
| `error_rate.percentage` | 错误率百分比 |
| `sla_status` | SLA 状态: ok/breach |
| `system.cpu_usage` | CPU 使用率 |
| `system.memory_usage` | 内存使用率 |
| `system.request_queue` | 请求队列长度 |

### Step 2: 获取性能历史

**请求**

```http
GET /api/v1/performance/history?hours=24
```

**响应**

```json
{
    "snapshots": [
        {
            "timestamp": "2026-01-24T11:00:00+00:00",
            "response_time_avg": 178.5,
            "response_time_p95": 432.1,
            "throughput": 108.2,
            "error_rate": 0.32,
            "availability": 99.98,
            "active_users": 95
        },
        {
            "timestamp": "2026-01-24T12:00:00+00:00",
            "response_time_avg": 185.3,
            "response_time_p95": 456.8,
            "throughput": 112.5,
            "error_rate": 0.45,
            "availability": 99.95,
            "active_users": 127
        }
    ],
    "count": 2,
    "period_hours": 24
}
```

### Step 3: 获取 SLA 状态

**请求**

```http
GET /api/v1/performance/sla
```

**响应**

```json
{
    "status": "compliant",
    "period": "24h",
    "metrics": {
        "response_time_avg": {
            "value": 182.45,
            "target": 200,
            "compliant": true
        },
        "availability": {
            "value": 99.96,
            "target": 99.9,
            "compliant": true
        },
        "error_rate": {
            "value": 0.38,
            "target": 1.0,
            "compliant": true
        }
    },
    "breaches": [],
    "samples": 24
}
```

**SLA 目标值**

| 指标 | 目标 | 单位 |
|------|------|------|
| `response_time_avg` | < 200 | ms |
| `response_time_p95` | < 500 | ms |
| `availability` | >= 99.9 | % |
| `error_rate` | <= 1.0 | % |
| `throughput` | >= 100 | req/s |

---

## 8. 法规报告流程

### 数据流

```
Generate Report ──► Gather Metrics ──► Gather Incidents ──► Check Compliance
                                                                    │
                           ┌────────────────────────────────────────┼────────────────────────────────────────┐
                           ▼                                        ▼                                        ▼
                    Metrics Summary                         Incidents Summary                         Compliance Status
                           │                                        │                                        │
                           └────────────────────────────────────────┼────────────────────────────────────────┘
                                                                    ▼
                                                            Generate Summary
                                                                    │
                                                                    ▼
                                                         Generate Recommendations
                                                                    │
                                                                    ▼
                                                             Store Report
```

### Step 1: 获取合规状态

**请求**

```http
GET /api/v1/regulatory/compliance-status
```

**响应**

```json
{
    "framework": "EU AI Act",
    "articles_covered": ["Article 72"],
    "status": {
        "overall_status": "compliant",
        "articles": {
            "article_72_1": {
                "requirement": "Post-market monitoring system established",
                "status": "compliant",
                "last_verified": "2026-01-24T12:00:00+00:00"
            },
            "article_72_2": {
                "requirement": "Data collection and analysis procedures defined",
                "status": "compliant",
                "last_verified": "2026-01-24T12:00:00+00:00"
            },
            "article_72_3": {
                "requirement": "Serious incident reporting mechanism in place",
                "status": "compliant",
                "last_verified": "2026-01-24T12:00:00+00:00"
            },
            "article_72_4": {
                "requirement": "Corrective action procedures established",
                "status": "compliant",
                "last_verified": "2026-01-24T12:00:00+00:00"
            },
            "article_72_5": {
                "requirement": "Documentation maintained and updated",
                "status": "compliant",
                "last_verified": "2026-01-24T12:00:00+00:00"
            }
        },
        "next_audit_due": "2026-04-24T12:00:00+00:00"
    },
    "last_updated": "2026-01-24T12:15:00+00:00",
    "system_classification": "High-Risk AI System",
    "monitoring_status": "Active"
}
```

**EU AI Act Article 72 要求**

| 条款 | 要求 |
|------|------|
| Article 72.1 | 建立上市后监控系统 |
| Article 72.2 | 定义数据收集和分析程序 |
| Article 72.3 | 建立严重事件报告机制 |
| Article 72.4 | 建立纠正措施程序 |
| Article 72.5 | 维护和更新文档 |

### Step 2: 生成法规报告

**请求**

```http
POST /api/v1/regulatory/reports/generate
Content-Type: application/json
```

```json
{
    "report_type": "periodic",
    "period_days": 30
}
```

**报告类型**

| 类型 | 说明 |
|------|------|
| `periodic` | 定期报告 |
| `incident` | 事件报告 |
| `compliance` | 合规报告 |
| `audit` | 审计报告 |

**响应**

```json
{
    "status": "generated",
    "report_id": "REG-20260124-0001",
    "title": "EU AI Act Article 72 Compliance Report - January 2026",
    "summary": "This report summarizes post-market monitoring activities \nin accordance with EU AI Act Article 72 requirements.\n\nMetrics tracked: 5\nTotal alerts: 8\nCritical incidents: 1\n\nThe AI system continues to operate within defined safety parameters.",
    "metrics_summary": {
        "response_accuracy": {
            "count": 450,
            "avg": 0.928,
            "min": 0.815,
            "max": 0.968,
            "std": 0.022
        },
        "hallucination_rate": {
            "count": 450,
            "avg": 0.052,
            "min": 0.028,
            "max": 0.095,
            "std": 0.012
        }
    },
    "incidents_summary": {
        "total_alerts": 8,
        "by_severity": {
            "critical": 1,
            "high": 3,
            "medium": 4
        },
        "by_type": {
            "response_accuracy_threshold_violation": 2,
            "hallucination_rate_threshold_violation": 1,
            "bias_alert": 5
        },
        "critical_count": 1,
        "high_count": 3
    },
    "compliance_status": {
        "overall_status": "compliant",
        "articles": {
            "article_72_1": {
                "requirement": "Post-market monitoring system established",
                "status": "compliant",
                "last_verified": "2026-01-24T12:20:00+00:00"
            }
        },
        "next_audit_due": "2026-04-24T12:20:00+00:00"
    },
    "recommendations": [
        "Review and address root causes of critical incidents",
        "Continue regular monitoring and documentation updates"
    ],
    "timestamp": "2026-01-24T12:20:00+00:00"
}
```

### Step 3: 获取报告列表

**请求**

```http
GET /api/v1/regulatory/reports?report_type=periodic&status=approved
```

**参数说明**

| 参数 | 类型 | 说明 |
|------|------|------|
| `report_type` | string | 报告类型过滤 |
| `status` | string | 状态过滤: draft/pending_review/approved/submitted |

**响应**

```json
{
    "reports": [
        {
            "report_id": "REG-20260124-0001",
            "created_at": "2026-01-24T12:20:00+00:00",
            "report_type": "periodic",
            "period_start": "2025-12-25T12:20:00+00:00",
            "period_end": "2026-01-24T12:20:00+00:00",
            "status": "draft",
            "title": "EU AI Act Article 72 Compliance Report - January 2026"
        }
    ],
    "count": 1
}
```

### Step 4: 获取报告详情

**请求**

```http
GET /api/v1/regulatory/reports/REG-20260124-0001
```

**响应**

```json
{
    "report_id": "REG-20260124-0001",
    "created_at": "2026-01-24T12:20:00+00:00",
    "report_type": "periodic",
    "period_start": "2025-12-25T12:20:00+00:00",
    "period_end": "2026-01-24T12:20:00+00:00",
    "status": "draft",
    "title": "EU AI Act Article 72 Compliance Report - January 2026",
    "summary": "This report summarizes post-market monitoring activities...",
    "metrics_summary": {
        "response_accuracy": {
            "count": 450,
            "avg": 0.928,
            "min": 0.815,
            "max": 0.968,
            "std": 0.022
        }
    },
    "incidents_summary": {
        "total_alerts": 8,
        "by_severity": {
            "critical": 1,
            "high": 3,
            "medium": 4
        },
        "critical_count": 1,
        "high_count": 3
    },
    "compliance_status": {
        "overall_status": "compliant"
    },
    "recommendations": [
        "Review and address root causes of critical incidents",
        "Continue regular monitoring and documentation updates"
    ],
    "submitted_at": null,
    "submitted_to": null
}
```

---

## 附录

### A. 完整 API 端点列表

| 模块 | 端点 | 方法 | 说明 |
|------|------|------|------|
| Core | `/health` | GET | 健康检查 |
| Core | `/api/v1/interactions/log` | POST | 记录交互 |
| Core | `/api/v1/feedback/submit` | POST | 提交反馈 |
| Core | `/api/v1/metrics/query` | POST | 查询指标 |
| Core | `/api/v1/metrics/current` | GET | 当前指标 |
| Core | `/api/v1/alerts/active` | GET | 活跃告警 |
| Core | `/api/v1/incidents/active` | GET | 活跃事件 |
| Core | `/api/v1/reports/summary` | GET | 摘要报告 |
| Core | `/api/v1/reports/bias` | GET | 偏见报告 |
| Core | `/api/v1/stats` | GET | 系统统计 |
| Dashboard | `/api/v1/dashboard/overview` | GET | 仪表板概览 |
| Dashboard | `/api/v1/dashboard/kpis` | GET | KPI 指标 |
| Signal | `/api/v1/signals/detect` | GET | 信号检测 |
| Signal | `/api/v1/signals/history` | GET | 信号历史 |
| Signal | `/api/v1/signals/{id}/acknowledge` | POST | 确认信号 |
| Trend | `/api/v1/trends/metrics` | GET | 指标趋势 |
| Trend | `/api/v1/trends/forecast` | GET | 预测分析 |
| Complaint | `/api/v1/complaints` | GET | 投诉列表 |
| Complaint | `/api/v1/complaints` | POST | 创建投诉 |
| Complaint | `/api/v1/complaints/{id}` | GET | 投诉详情 |
| Complaint | `/api/v1/complaints/{id}` | PUT | 更新投诉 |
| Complaint | `/api/v1/complaints/analytics` | GET | 投诉分析 |
| Performance | `/api/v1/performance/realtime` | GET | 实时性能 |
| Performance | `/api/v1/performance/history` | GET | 性能历史 |
| Performance | `/api/v1/performance/sla` | GET | SLA 状态 |
| Regulatory | `/api/v1/regulatory/compliance-status` | GET | 合规状态 |
| Regulatory | `/api/v1/regulatory/reports` | GET | 报告列表 |
| Regulatory | `/api/v1/regulatory/reports/generate` | POST | 生成报告 |
| Regulatory | `/api/v1/regulatory/reports/{id}` | GET | 报告详情 |

### B. 错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 资源未找到 |
| 500 | 服务器内部错误 |

### C. 典型使用场景

#### 场景 1: 日常监控

```
1. GET /api/v1/dashboard/overview          # 查看整体状态
2. GET /api/v1/signals/detect              # 运行信号检测
3. GET /api/v1/alerts/active               # 查看活跃告警
4. GET /api/v1/performance/realtime        # 查看实时性能
```

#### 场景 2: 问题调查

```
1. GET /api/v1/signals/history?hours=24    # 查看最近信号
2. GET /api/v1/trends/metrics?hours=48     # 分析趋势
3. GET /api/v1/complaints?status=open      # 查看未解决投诉
4. POST /api/v1/complaints                 # 创建新投诉
```

#### 场景 3: 合规审计

```
1. GET /api/v1/regulatory/compliance-status     # 检查合规状态
2. POST /api/v1/regulatory/reports/generate     # 生成报告
3. GET /api/v1/regulatory/reports/{id}          # 查看报告详情
4. GET /api/v1/performance/sla                  # 检查 SLA 状态
```

---

**Version**: 2.0.0
**Last Updated**: 2026-01-24
