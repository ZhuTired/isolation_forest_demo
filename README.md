# 游戏登录异常检测 - 孤立森林算法Demo

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/ZhuTired/isolation_forest_demo?style=social)](https://github.com/ZhuTired/isolation_forest_demo)

## 项目简介

本项目演示如何使用**孤立森林(Isolation Forest)**算法检测游戏登录场景中的异常流量，帮助识别潜在的账号盗刷、机器人攻击、刷量等风控问题。

## 什么是孤立森林算法？

孤立森林是一种**无监督异常检测算法**，核心思想是：
- **异常数据更容易被孤立**：异常点的特征与正常数据差异大，在随机划分时更快被隔离
- **不需要标注数据**：算法自动学习数据分布，找出偏离正常模式的异常点
- **高效快速**：时间复杂度低，适合大规模数据处理

### 工作原理
1. 随机选择特征和分割值，构建多棵隔离树
2. 计算每个样本的平均路径长度（被隔离所需的分割次数）
3. 路径越短 = 越容易被孤立 = 越可能是异常

## 项目结构

```
isolation_forest_demo/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python依赖包
├── game_login_demo.py          # 核心演示代码
├── generate_sample_data.py     # 样本数据生成器
├── real_world_application.md   # 实际业务应用指南
└── data/                       # 数据目录
    └── game_login_data.csv     # 生成的样本数据
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 生成样本数据

```bash
python generate_sample_data.py
```

### 3. 运行异常检测

```bash
python game_login_demo.py
```

## 检测的异常类型

在游戏登录场景中，我们检测以下异常行为：

1. **异常登录频率**：短时间内大量登录尝试（暴力破解）
2. **异常登录时段**：非正常时间段的登录（如凌晨3点）
3. **异常IP地址**：来自高风险地区或频繁更换IP
4. **异常设备**：使用模拟器、多开软件等
5. **异常行为模式**：登录后立即进行交易、快速切换账号等

## 特征工程

本demo使用的核心特征：

| 特征名 | 说明 | 风控意义 |
|--------|------|----------|
| login_hour | 登录小时 | 识别异常时段登录 |
| login_frequency | 每小时登录次数 | 检测暴力破解 |
| ip_risk_score | IP风险评分 | 识别高风险IP |
| device_change_freq | 设备更换频率 | 检测设备异常 |
| login_duration | 登录时长 | 识别异常会话 |
| failed_attempts | 失败尝试次数 | 检测暴力破解 |
| geo_velocity | 地理位置变化速度 | 检测账号共享 |

## 输出结果

程序会生成：
- 异常检测结果的可视化图表
- 详细的异常用户列表
- 模型性能评估指标

## 实际应用

查看 [real_world_application.md](real_world_application.md) 了解如何将此算法应用到实际业务系统中。

## 技术栈

- Python 3.8+
- scikit-learn: 机器学习算法库
- pandas: 数据处理
- matplotlib/seaborn: 数据可视化
- numpy: 数值计算
