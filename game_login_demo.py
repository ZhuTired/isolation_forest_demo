"""
游戏登录异常检测 - 孤立森林算法演示

本脚本演示如何使用孤立森林算法检测游戏登录中的异常行为
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import warnings

warnings.filterwarnings('ignore')

# 设置中文字体（macOS）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class GameLoginAnomalyDetector:
    """游戏登录异常检测器"""

    def __init__(self, contamination=0.05):
        """
        初始化检测器

        参数:
            contamination: 预期异常比例（默认5%），这是一个重要的超参数
                         - 设置过高：会把正常用户误判为异常
                         - 设置过低：会遗漏真实的异常
        """
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100,  # 树的数量，越多越稳定但计算越慢
            max_samples='auto',  # 每棵树的样本数
            max_features=1.0,  # 每棵树使用的特征比例
            bootstrap=False,
            n_jobs=-1  # 使用所有CPU核心
        )
        self.scaler = StandardScaler()
        self.feature_names = None

    def prepare_features(self, df):
        """
        准备特征数据

        特征工程说明：
        - 只选择数值型特征用于模型训练
        - 需要对特征进行标准化，因为不同特征的量纲差异大
        """
        # 选择用于训练的特征（排除user_id和标签）
        feature_cols = [col for col in df.columns if col not in ['user_id', 'is_anomaly']]
        self.feature_names = feature_cols

        X = df[feature_cols].values
        return X

    def train(self, df):
        """
        训练孤立森林模型

        注意：孤立森林是无监督算法，不需要标签
        但我们这里保留标签用于后续评估模型效果
        """
        print("=" * 60)
        print("开始训练孤立森林模型...")
        print("=" * 60)

        X = self.prepare_features(df)

        # 标准化特征
        print("\n1. 特征标准化...")
        X_scaled = self.scaler.fit_transform(X)

        # 训练模型
        print("2. 训练孤立森林模型（100棵树）...")
        self.model.fit(X_scaled)

        print("3. 模型训练完成！")

    def predict(self, df):
        """
        预测异常

        返回值说明：
        - 1: 正常样本
        - -1: 异常样本（孤立森林的输出是-1表示异常）
        """
        X = self.prepare_features(df)
        X_scaled = self.scaler.transform(X)

        # 预测
        predictions = self.model.predict(X_scaled)

        # 获取异常分数（分数越低越异常，负值表示异常）
        anomaly_scores = self.model.score_samples(X_scaled)

        return predictions, anomaly_scores

    def evaluate(self, df, predictions):
        """
        评估模型效果

        因为我们有真实标签，可以计算精确率、召回率等指标
        在实际业务中，通常没有标签，需要通过人工审核来验证
        """
        print("\n" + "=" * 60)
        print("模型评估结果")
        print("=" * 60)

        # 转换预测结果：-1(异常) -> 1, 1(正常) -> 0
        y_pred = np.where(predictions == -1, 1, 0)
        y_true = df['is_anomaly'].values

        # 分类报告
        print("\n1. 分类性能指标:")
        print(classification_report(y_true, y_pred,
                                    target_names=['正常', '异常'],
                                    digits=3))

        # 混淆矩阵
        cm = confusion_matrix(y_true, y_pred)
        print("2. 混淆矩阵:")
        print(f"   真正常/预测正常(TN): {cm[0, 0]}")
        print(f"   真正常/预测异常(FP): {cm[0, 1]} <- 误报")
        print(f"   真异常/预测正常(FN): {cm[1, 0]} <- 漏报")
        print(f"   真异常/预测异常(TP): {cm[1, 1]}")

        # 关键指标解释
        precision = cm[1, 1] / (cm[1, 1] + cm[0, 1]) if (cm[1, 1] + cm[0, 1]) > 0 else 0
        recall = cm[1, 1] / (cm[1, 1] + cm[1, 0]) if (cm[1, 1] + cm[1, 0]) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        print("\n3. 关键指标解释:")
        print(f"   精确率(Precision): {precision:.3f} - 在所有预测为异常的样本中，真正异常的比例")
        print(f"   召回率(Recall): {recall:.3f} - 在所有真实异常的样本中，被成功检出的比例")
        print(f"   F1分数: {f1:.3f} - 精确率和召回率的调和平均")

        print("\n4. 业务解读:")
        print(f"   - 共检测出 {cm[1, 1] + cm[0, 1]} 个异常登录")
        print(f"   - 其中 {cm[1, 1]} 个确实是异常（成功拦截）")
        print(f"   - 误报了 {cm[0, 1]} 个正常用户（需要优化）")
        print(f"   - 漏报了 {cm[1, 0]} 个真实异常（有风险）")

    def analyze_anomalies(self, df, predictions, anomaly_scores, top_n=20):
        """
        详细分析检测到的异常样本
        """
        print("\n" + "=" * 60)
        print(f"Top {top_n} 异常样本详细分析")
        print("=" * 60)

        # 创建结果DataFrame
        result_df = df.copy()
        result_df['predicted_anomaly'] = np.where(predictions == -1, 1, 0)
        result_df['anomaly_score'] = anomaly_scores

        # 获取最异常的样本（分数最低的）
        top_anomalies = result_df.nsmallest(top_n, 'anomaly_score')

        print("\n最可疑的登录行为（按异常分数排序）:\n")
        print(f"{'用户ID':<15} {'异常分数':<10} {'登录时段':<10} {'登录频率':<10} "
              f"{'IP风险':<10} {'失败次数':<10} {'真实标签':<10}")
        print("-" * 85)

        for idx, row in top_anomalies.iterrows():
            print(f"{row['user_id']:<15} {row['anomaly_score']:<10.3f} "
                  f"{row['login_hour']:<10.0f} {row['login_frequency']:<10.0f} "
                  f"{row['ip_risk_score']:<10.1f} {row['failed_attempts']:<10.0f} "
                  f"{'异常' if row['is_anomaly']==1 else '正常':<10}")

        # 分析异常特征的重要性
        print("\n" + "=" * 60)
        print("异常用户与正常用户的特征对比")
        print("=" * 60)

        anomaly_users = result_df[result_df['predicted_anomaly'] == 1]
        normal_users = result_df[result_df['predicted_anomaly'] == 0]

        for feature in self.feature_names:
            anomaly_mean = anomaly_users[feature].mean()
            normal_mean = normal_users[feature].mean()
            diff_pct = (anomaly_mean - normal_mean) / normal_mean * 100 if normal_mean != 0 else 0

            print(f"\n{feature}:")
            print(f"  正常用户均值: {normal_mean:.2f}")
            print(f"  异常用户均值: {anomaly_mean:.2f}")
            print(f"  差异: {diff_pct:+.1f}%")

        return result_df

    def visualize_results(self, result_df):
        """
        可视化异常检测结果
        """
        print("\n" + "=" * 60)
        print("生成可视化图表...")
        print("=" * 60)

        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('游戏登录异常检测可视化分析', fontsize=16, y=1.00)

        # 1. 异常分数分布
        ax1 = axes[0, 0]
        ax1.hist(result_df[result_df['is_anomaly'] == 0]['anomaly_score'],
                 bins=50, alpha=0.6, label='正常用户', color='green')
        ax1.hist(result_df[result_df['is_anomaly'] == 1]['anomaly_score'],
                 bins=50, alpha=0.6, label='异常用户', color='red')
        ax1.set_xlabel('异常分数（越低越异常）')
        ax1.set_ylabel('数量')
        ax1.set_title('异常分数分布')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. 登录时段分布
        ax2 = axes[0, 1]
        normal_hours = result_df[result_df['predicted_anomaly'] == 0]['login_hour']
        anomaly_hours = result_df[result_df['predicted_anomaly'] == 1]['login_hour']
        ax2.hist(normal_hours, bins=24, alpha=0.6, label='正常', color='green', range=(0, 24))
        ax2.hist(anomaly_hours, bins=24, alpha=0.6, label='异常', color='red', range=(0, 24))
        ax2.set_xlabel('登录时段（小时）')
        ax2.set_ylabel('数量')
        ax2.set_title('登录时段分布')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # 3. 登录频率 vs IP风险
        ax3 = axes[0, 2]
        normal = result_df[result_df['predicted_anomaly'] == 0]
        anomaly = result_df[result_df['predicted_anomaly'] == 1]
        ax3.scatter(normal['login_frequency'], normal['ip_risk_score'],
                   alpha=0.5, s=30, c='green', label='正常')
        ax3.scatter(anomaly['login_frequency'], anomaly['ip_risk_score'],
                   alpha=0.7, s=50, c='red', label='异常', marker='^')
        ax3.set_xlabel('登录频率')
        ax3.set_ylabel('IP风险评分')
        ax3.set_title('登录频率 vs IP风险评分')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # 4. 设备更换频率 vs 地理速度
        ax4 = axes[1, 0]
        ax4.scatter(normal['device_change_freq'], normal['geo_velocity'],
                   alpha=0.5, s=30, c='green', label='正常')
        ax4.scatter(anomaly['device_change_freq'], anomaly['geo_velocity'],
                   alpha=0.7, s=50, c='red', label='异常', marker='^')
        ax4.set_xlabel('设备更换频率')
        ax4.set_ylabel('地理位置变化速度 (km/h)')
        ax4.set_title('设备更换 vs 地理速度')
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        # 5. 失败尝试次数分布
        ax5 = axes[1, 1]
        ax5.hist(normal['failed_attempts'], bins=20, alpha=0.6, label='正常', color='green')
        ax5.hist(anomaly['failed_attempts'], bins=20, alpha=0.6, label='异常', color='red')
        ax5.set_xlabel('失败尝试次数')
        ax5.set_ylabel('数量')
        ax5.set_title('登录失败尝试次数分布')
        ax5.legend()
        ax5.grid(True, alpha=0.3)

        # 6. 混淆矩阵热力图
        ax6 = axes[1, 2]
        from sklearn.metrics import confusion_matrix
        y_pred = result_df['predicted_anomaly'].values
        y_true = result_df['is_anomaly'].values
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax6,
                   xticklabels=['预测正常', '预测异常'],
                   yticklabels=['真实正常', '真实异常'])
        ax6.set_title('混淆矩阵')
        ax6.set_ylabel('真实标签')
        ax6.set_xlabel('预测标签')

        plt.tight_layout()
        plt.savefig('data/anomaly_detection_results.png', dpi=300, bbox_inches='tight')
        print("图表已保存到: data/anomaly_detection_results.png")
        plt.show()


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("游戏登录异常检测系统 - 基于孤立森林算法")
    print("=" * 60)

    # 1. 加载数据
    print("\n步骤1: 加载游戏登录数据...")
    try:
        df = pd.read_csv('data/game_login_data.csv')
        print(f"成功加载 {len(df)} 条登录记录")
    except FileNotFoundError:
        print("错误: 找不到数据文件！")
        print("请先运行 python generate_sample_data.py 生成数据")
        return

    # 2. 创建检测器
    print("\n步骤2: 初始化异常检测器...")
    detector = GameLoginAnomalyDetector(contamination=0.05)
    print("参数设置: 预期异常比例 = 5%")

    # 3. 训练模型
    print("\n步骤3: 训练模型...")
    detector.train(df)

    # 4. 预测异常
    print("\n步骤4: 检测异常登录...")
    predictions, anomaly_scores = detector.predict(df)
    detected_anomalies = np.sum(predictions == -1)
    print(f"检测到 {detected_anomalies} 个异常登录 "
          f"(占比 {detected_anomalies/len(df)*100:.1f}%)")

    # 5. 评估模型
    print("\n步骤5: 评估模型性能...")
    detector.evaluate(df, predictions)

    # 6. 详细分析异常
    print("\n步骤6: 分析异常样本...")
    result_df = detector.analyze_anomalies(df, predictions, anomaly_scores, top_n=20)

    # 7. 可视化
    print("\n步骤7: 生成可视化报告...")
    detector.visualize_results(result_df)

    # 8. 保存结果
    print("\n步骤8: 保存检测结果...")
    result_df.to_csv('data/detection_results.csv', index=False)
    print("完整结果已保存到: data/detection_results.csv")

    print("\n" + "=" * 60)
    print("异常检测完成！")
    print("=" * 60)
    print("\n关键发现:")
    print(f"1. 总共分析了 {len(df)} 条登录记录")
    print(f"2. 检测出 {detected_anomalies} 个可疑登录")
    print(f"3. 真实异常数量: {df['is_anomaly'].sum()}")
    print(f"4. 检测准确率: 请查看上方的评估指标")
    print(f"\n建议:")
    print("- 对检测出的异常用户进行二次验证（短信验证、人机验证等）")
    print("- 持续监控这些账号的后续行为")
    print("- 定期重新训练模型，适应新的攻击模式")


if __name__ == '__main__':
    main()
