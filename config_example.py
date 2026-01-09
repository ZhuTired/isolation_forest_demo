"""
风控系统配置示例
根据实际业务场景调整这些配置
"""

# ============================================================================
# 模型配置
# ============================================================================

MODEL_CONFIG = {
    # 孤立森林参数
    'isolation_forest': {
        'contamination': 0.05,      # 预期异常比例（5%）
        'n_estimators': 100,        # 树的数量
        'max_samples': 'auto',      # 每棵树的样本数
        'max_features': 1.0,        # 使用全部特征
        'random_state': 42,
        'n_jobs': -1                # 使用所有CPU核心
    },

    # 模型更新策略
    'update_policy': {
        'schedule': 'daily',        # 更新频率：daily/weekly/monthly
        'retrain_time': '03:00',    # 重训练时间（凌晨3点）
        'min_samples': 10000,       # 最小训练样本数
        'validation_split': 0.2     # 验证集比例
    }
}

# ============================================================================
# 风险等级阈值配置
# ============================================================================

RISK_THRESHOLDS = {
    'anomaly_score': {
        'low': -0.1,                # 低风险阈值
        'medium': -0.3,             # 中风险阈值
        'high': -0.5                # 高风险阈值
    },

    # 各特征的异常阈值（用于规则引擎兜底）
    'feature_thresholds': {
        'login_frequency_1h': 20,   # 1小时内登录超过20次
        'failed_attempts_1h': 10,   # 1小时内失败超过10次
        'device_change_7d': 5,      # 7天内更换设备超过5次
        'ip_risk_score': 80,        # IP风险评分超过80
        'geo_velocity': 500         # 地理速度超过500km/h
    }
}

# ============================================================================
# 风控策略配置
# ============================================================================

RISK_ACTIONS = {
    # 低风险：直接放行
    'low': {
        'action': 'pass',
        'log_level': 'info',
        'notify': False
    },

    # 中风险：人机验证
    'medium': {
        'action': 'challenge',
        'challenge_type': 'captcha',     # captcha/sms/email
        'max_attempts': 3,                # 最多尝试次数
        'log_level': 'warning',
        'notify': True,
        'notify_channels': ['slack']      # 通知渠道
    },

    # 高风险：强制验证或拦截
    'high': {
        'action': 'block',
        'challenge_type': 'sms',         # 短信验证
        'require_manual_review': True,   # 需要人工审核
        'log_level': 'error',
        'notify': True,
        'notify_channels': ['slack', 'email', 'pagerduty']
    }
}

# ============================================================================
# 特征工程配置
# ============================================================================

FEATURE_CONFIG = {
    # 时间窗口
    'time_windows': {
        'short': 3600,              # 1小时
        'medium': 21600,            # 6小时
        'long': 86400,              # 24小时
        'weekly': 604800            # 7天
    },

    # 需要计算的特征
    'features': [
        'login_hour',
        'login_frequency',
        'ip_risk_score',
        'device_change_freq',
        'login_duration',
        'failed_attempts',
        'geo_velocity',
        'unique_ips_24h',           # 24小时内不同IP数
        'unique_devices_7d',        # 7天内不同设备数
        'avg_session_duration',     # 平均会话时长
        'login_time_variance',      # 登录时间方差
        'is_new_device',            # 是否新设备
        'is_new_location',          # 是否新地点
        'time_since_last_login'     # 距上次登录时间
    ],

    # 特征缓存配置
    'cache': {
        'enabled': True,
        'ttl': 300,                 # 缓存5分钟
        'backend': 'redis'
    }
}

# ============================================================================
# 白名单/黑名单配置
# ============================================================================

WHITELIST_CONFIG = {
    # VIP用户白名单
    'vip_users': {
        'enabled': True,
        'min_level': 5,             # VIP等级>=5的用户
        'action': 'pass',           # 直接放行
        'log_only': True            # 仅记录日志
    },

    # 内部测试账号
    'internal_users': {
        'enabled': True,
        'user_ids': [],             # 从配置文件或数据库读取
        'action': 'pass'
    },

    # 可信IP白名单
    'trusted_ips': {
        'enabled': True,
        'ip_ranges': [
            '10.0.0.0/8',           # 内网IP
            '192.168.0.0/16'
        ]
    }
}

BLACKLIST_CONFIG = {
    # IP黑名单
    'blocked_ips': {
        'enabled': True,
        'source': 'database',       # database/redis/api
        'auto_block_threshold': 100, # 风险分超过100自动加入
        'ttl': 86400                # 24小时后自动解封
    },

    # 设备黑名单
    'blocked_devices': {
        'enabled': True,
        'source': 'database'
    },

    # 已知恶意用户
    'blocked_users': {
        'enabled': True,
        'source': 'database'
    }
}

# ============================================================================
# 性能配置
# ============================================================================

PERFORMANCE_CONFIG = {
    # API配置
    'api': {
        'timeout': 1.0,             # 超时时间（秒）
        'max_workers': 20,          # 最大并发数
        'queue_size': 1000,         # 请求队列大小
        'rate_limit': {
            'enabled': True,
            'max_requests': 1000,   # 每秒最大请求数
            'per': 'second'
        }
    },

    # 批处理配置
    'batch': {
        'enabled': True,
        'batch_size': 100,          # 批处理大小
        'max_wait_time': 0.1        # 最大等待时间（秒）
    },

    # 缓存配置
    'cache': {
        'redis': {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'max_connections': 50
        }
    }
}

# ============================================================================
# 监控告警配置
# ============================================================================

MONITORING_CONFIG = {
    # 性能监控
    'performance': {
        'enabled': True,
        'metrics': [
            'requests_per_second',
            'avg_latency',
            'p95_latency',
            'p99_latency',
            'error_rate'
        ],
        'alert_thresholds': {
            'p99_latency': 100,     # P99延迟超过100ms告警
            'error_rate': 0.01      # 错误率超过1%告警
        }
    },

    # 业务指标监控
    'business': {
        'enabled': True,
        'metrics': [
            'anomaly_detection_rate',
            'false_positive_rate',
            'block_rate',
            'challenge_rate'
        ],
        'alert_thresholds': {
            'anomaly_detection_rate': (0.01, 0.2),  # 异常率在1%-20%之间
            'block_rate': 0.05      # 拦截率超过5%告警
        }
    },

    # 告警通知
    'alerting': {
        'channels': {
            'slack': {
                'enabled': True,
                'webhook_url': 'https://hooks.slack.com/xxx'
            },
            'email': {
                'enabled': True,
                'recipients': ['security@company.com']
            },
            'pagerduty': {
                'enabled': False,
                'api_key': 'xxx'
            }
        }
    }
}

# ============================================================================
# 日志配置
# ============================================================================

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'json': {
            'format': '{"time":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'json',
            'filename': 'logs/risk_control.log',
            'maxBytes': 10485760,   # 10MB
            'backupCount': 10
        }
    },
    'loggers': {
        'risk_control': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }
}

# ============================================================================
# 数据库配置
# ============================================================================

DATABASE_CONFIG = {
    # 主数据库（MySQL/PostgreSQL）
    'main': {
        'engine': 'postgresql',
        'host': 'localhost',
        'port': 5432,
        'database': 'risk_control',
        'user': 'risk_user',
        'password': 'xxx',
        'pool_size': 20
    },

    # Redis（缓存和队列）
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None
    },

    # 数据仓库（用于离线分析）
    'warehouse': {
        'type': 'hive',             # hive/clickhouse/bigquery
        'connection': 'hive://xxx'
    }
}

# ============================================================================
# 实验配置（A/B测试）
# ============================================================================

EXPERIMENT_CONFIG = {
    'enabled': True,

    # 实验1: 测试新的contamination参数
    'exp_contamination': {
        'enabled': True,
        'traffic_split': 0.1,       # 10%流量
        'variants': {
            'control': {'contamination': 0.05},
            'treatment': {'contamination': 0.03}
        },
        'metrics': ['precision', 'recall', 'f1', 'user_complaint_rate']
    },

    # 实验2: 测试新特征
    'exp_new_features': {
        'enabled': False,
        'traffic_split': 0.05,
        'additional_features': ['user_behavior_score', 'social_network_risk']
    }
}

# ============================================================================
# 合规配置
# ============================================================================

COMPLIANCE_CONFIG = {
    # 数据保留策略
    'data_retention': {
        'raw_logs': 90,             # 原始日志保留90天
        'detection_results': 180,   # 检测结果保留180天
        'user_profiles': 365        # 用户画像保留1年
    },

    # 隐私保护
    'privacy': {
        'anonymize_logs': True,     # 日志匿名化
        'encrypt_sensitive_data': True,
        'gdpr_compliant': True      # 符合GDPR要求
    }
}

# ============================================================================
# 应用示例
# ============================================================================

if __name__ == '__main__':
    """配置验证和使用示例"""

    # 1. 检查配置完整性
    required_configs = [
        'MODEL_CONFIG',
        'RISK_THRESHOLDS',
        'RISK_ACTIONS',
        'FEATURE_CONFIG'
    ]

    for config_name in required_configs:
        if config_name not in globals():
            raise ValueError(f"缺少必需配置: {config_name}")

    # 2. 使用配置创建检测器
    from sklearn.ensemble import IsolationForest

    model = IsolationForest(**MODEL_CONFIG['isolation_forest'])
    print("模型配置:")
    print(f"  - Contamination: {MODEL_CONFIG['isolation_forest']['contamination']}")
    print(f"  - N Estimators: {MODEL_CONFIG['isolation_forest']['n_estimators']}")

    # 3. 打印风控策略
    print("\n风控策略:")
    for risk_level, action in RISK_ACTIONS.items():
        print(f"  {risk_level.upper()}: {action['action']}")
        if 'challenge_type' in action:
            print(f"    验证方式: {action['challenge_type']}")

    # 4. 打印特征列表
    print("\n使用特征:")
    for i, feature in enumerate(FEATURE_CONFIG['features'], 1):
        print(f"  {i}. {feature}")

    print("\n配置加载完成！")
