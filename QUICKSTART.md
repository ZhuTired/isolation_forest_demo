# 快速入门指南

## 5分钟快速体验

### 步骤1: 安装依赖

```bash
cd isolation_forest_demo
pip install -r requirements.txt
```

### 步骤2: 生成样本数据

```bash
python generate_sample_data.py
```

这会生成1050条游戏登录记录（1000条正常 + 50条异常）

### 步骤3: 运行异常检测

```bash
python game_login_demo.py
```

程序会自动：
1. 训练孤立森林模型
2. 检测异常登录
3. 生成可视化报告
4. 保存检测结果

### 查看结果

运行完成后会生成：
- [data/anomaly_detection_results.png](data/anomaly_detection_results.png) - 可视化图表
- [data/detection_results.csv](data/detection_results.csv) - 完整检测结果

---

## 核心代码解读

### 1. 孤立森林是如何工作的？

```python
from sklearn.ensemble import IsolationForest

# 创建模型（预期5%的数据是异常）
model = IsolationForest(contamination=0.05)

# 训练（只需要数据，不需要标签！）
model.fit(training_data)

# 预测（返回 1=正常, -1=异常）
predictions = model.predict(test_data)

# 获取异常分数（越低越异常）
scores = model.score_samples(test_data)
```

### 2. 核心参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| contamination | 预期异常比例 | 0.01-0.1（1%-10%） |
| n_estimators | 树的数量 | 100-200 |
| max_samples | 每棵树的样本数 | 'auto' 或 256 |
| max_features | 使用的特征比例 | 1.0（使用全部） |

### 3. 关键特征

```python
features = [
    'login_hour',          # 登录时段（0-23）
    'login_frequency',     # 每小时登录次数
    'ip_risk_score',       # IP风险评分（0-100）
    'device_change_freq',  # 设备更换频率
    'login_duration',      # 登录时长（分钟）
    'failed_attempts',     # 失败尝试次数
    'geo_velocity'         # 地理位置变化速度（km/h）
]
```

---

## 常见问题

### Q: 为什么检测到的异常数量与实际不完全一致？

A: 孤立森林是**无监督算法**，它学习的是数据的分布模式，而不是依赖标签。检测结果与人工标注可能有差异，这是正常的。

### Q: 如何提高检测准确率？

A: 三个方向：
1. **优化特征**：增加更有区分度的特征
2. **调整参数**：调整contamination参数
3. **增加样本**：更多的训练数据能提升效果

### Q: 能否用于其他场景？

A: 完全可以！只需要：
1. 准备你的数据（CSV格式）
2. 修改特征列表
3. 调整contamination参数

---

## 下一步

- 查看 [README.md](README.md) 了解项目详情
- 查看 [real_world_application.md](real_world_application.md) 学习如何应用到实际业务
- 尝试修改参数，观察效果变化
- 使用自己的数据进行实验

---

## 实验建议

### 实验1: 调整异常比例

修改 [game_login_demo.py:31](game_login_demo.py#L31) 中的 contamination 参数：

```python
detector = GameLoginAnomalyDetector(contamination=0.1)  # 从5%改为10%
```

观察检测结果的变化。

### 实验2: 特征重要性分析

尝试去掉某个特征，看对检测效果的影响：

```python
# 在 generate_sample_data.py 中注释掉某个特征
# 例如：不使用 geo_velocity
```

### 实验3: 增加异常样本

修改 [generate_sample_data.py:223](generate_sample_data.py#L223)：

```python
anomaly_data = generate_anomaly_logins(100)  # 从50改为100
```

观察异常比例增加后的影响。

---

## 技术支持

如有问题，欢迎：
1. 查看代码注释（有详细说明）
2. 阅读 scikit-learn 官方文档
3. 参考 real_world_application.md 中的实战案例
