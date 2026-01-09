"""
游戏登录数据生成器
生成包含正常登录和异常登录的模拟数据
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# 设置随机种子，保证结果可复现
np.random.seed(42)
random.seed(42)


def generate_normal_logins(n_samples=1000):
    """
    生成正常的游戏登录数据

    正常用户特征：
    - 登录时间集中在8:00-23:00
    - 每小时登录频率较低（1-3次）
    - IP风险评分低
    - 设备稳定
    - 登录时长合理
    - 很少失败尝试
    """
    data = []

    for i in range(n_samples):
        # 正常登录时间：主要在白天和晚上
        login_hour = np.random.choice(
            range(24),
            p=[0.01, 0.01, 0.01, 0.01, 0.01, 0.02,  # 0-5点 (低概率)
               0.03, 0.05, 0.06, 0.07, 0.08, 0.08,  # 6-11点 (逐渐增加)
               0.07, 0.06, 0.05, 0.05, 0.05, 0.06,  # 12-17点 (平稳)
               0.08, 0.10, 0.09, 0.08, 0.05, 0.02]  # 18-23点 (高峰后下降)
        )

        # 正常登录频率：每小时1-3次
        login_frequency = np.random.randint(1, 4)

        # IP风险评分：0-30（低风险）
        ip_risk_score = np.random.uniform(0, 30)

        # 设备更换频率：很低，大多数用户使用固定设备
        device_change_freq = np.random.choice([0, 1, 2], p=[0.7, 0.25, 0.05])

        # 登录时长：30-180分钟（正常游戏时长）
        login_duration = np.random.uniform(30, 180)

        # 失败尝试次数：0-2次（偶尔输错密码）
        failed_attempts = np.random.choice([0, 1, 2], p=[0.85, 0.12, 0.03])

        # 地理位置变化速度：km/h，正常用户很少快速移动
        geo_velocity = np.random.uniform(0, 50)

        data.append({
            'user_id': f'user_{i}',
            'login_hour': login_hour,
            'login_frequency': login_frequency,
            'ip_risk_score': ip_risk_score,
            'device_change_freq': device_change_freq,
            'login_duration': login_duration,
            'failed_attempts': failed_attempts,
            'geo_velocity': geo_velocity,
            'is_anomaly': 0  # 正常用户标记为0
        })

    return data


def generate_anomaly_logins(n_samples=50):
    """
    生成异常的游戏登录数据

    异常用户特征：
    - 凌晨时段登录
    - 高频登录（暴力破解、刷量）
    - 高风险IP
    - 频繁更换设备
    - 异常登录时长（过短或过长）
    - 大量失败尝试
    - 快速地理位置变化
    """
    data = []

    for i in range(n_samples):
        anomaly_type = np.random.choice(['brute_force', 'bot', 'account_sharing', 'suspicious_time'])

        if anomaly_type == 'brute_force':
            # 暴力破解：高频登录 + 大量失败
            login_hour = np.random.randint(0, 24)
            login_frequency = np.random.randint(20, 100)  # 异常高频
            ip_risk_score = np.random.uniform(60, 100)
            device_change_freq = np.random.randint(0, 3)
            login_duration = np.random.uniform(1, 10)  # 很短
            failed_attempts = np.random.randint(10, 50)  # 大量失败
            geo_velocity = np.random.uniform(0, 100)

        elif anomaly_type == 'bot':
            # 机器人：规律性强 + 异常时段 + 高频
            login_hour = np.random.choice([2, 3, 4, 5])  # 凌晨
            login_frequency = np.random.randint(30, 80)
            ip_risk_score = np.random.uniform(70, 100)
            device_change_freq = np.random.randint(5, 15)  # 频繁换设备
            login_duration = np.random.uniform(200, 500)  # 异常长
            failed_attempts = np.random.randint(0, 3)
            geo_velocity = np.random.uniform(0, 50)

        elif anomaly_type == 'account_sharing':
            # 账号共享：快速地理位置变化 + 频繁换设备
            login_hour = np.random.randint(0, 24)
            login_frequency = np.random.randint(5, 15)
            ip_risk_score = np.random.uniform(40, 80)
            device_change_freq = np.random.randint(10, 30)  # 非常频繁
            login_duration = np.random.uniform(20, 150)
            failed_attempts = np.random.randint(0, 5)
            geo_velocity = np.random.uniform(500, 2000)  # 不可能的速度

        else:  # suspicious_time
            # 可疑时段：凌晨 + 异常行为
            login_hour = np.random.choice([1, 2, 3, 4])
            login_frequency = np.random.randint(15, 40)
            ip_risk_score = np.random.uniform(50, 90)
            device_change_freq = np.random.randint(3, 10)
            login_duration = np.random.uniform(5, 30)  # 短时间
            failed_attempts = np.random.randint(3, 15)
            geo_velocity = np.random.uniform(100, 800)

        data.append({
            'user_id': f'anomaly_{i}',
            'login_hour': login_hour,
            'login_frequency': login_frequency,
            'ip_risk_score': ip_risk_score,
            'device_change_freq': device_change_freq,
            'login_duration': login_duration,
            'failed_attempts': failed_attempts,
            'geo_velocity': geo_velocity,
            'is_anomaly': 1  # 异常用户标记为1
        })

    return data


def main():
    """主函数：生成并保存数据"""
    print("=" * 60)
    print("开始生成游戏登录样本数据...")
    print("=" * 60)

    # 生成正常和异常数据
    print("\n1. 生成正常登录数据（1000条）...")
    normal_data = generate_normal_logins(1000)

    print("2. 生成异常登录数据（50条，约5%异常率）...")
    anomaly_data = generate_anomaly_logins(50)

    # 合并数据
    all_data = normal_data + anomaly_data
    df = pd.DataFrame(all_data)

    # 打乱数据顺序
    df = df.sample(frac=1).reset_index(drop=True)

    # 保存到CSV
    output_path = 'data/game_login_data.csv'
    df.to_csv(output_path, index=False)

    print(f"\n3. 数据已保存到: {output_path}")

    # 显示统计信息
    print("\n" + "=" * 60)
    print("数据统计信息")
    print("=" * 60)
    print(f"总样本数: {len(df)}")
    print(f"正常样本: {len(df[df['is_anomaly'] == 0])} ({len(df[df['is_anomaly'] == 0])/len(df)*100:.1f}%)")
    print(f"异常样本: {len(df[df['is_anomaly'] == 1])} ({len(df[df['is_anomaly'] == 1])/len(df)*100:.1f}%)")

    print("\n正常样本特征统计:")
    print(df[df['is_anomaly'] == 0].describe())

    print("\n异常样本特征统计:")
    print(df[df['is_anomaly'] == 1].describe())

    print("\n" + "=" * 60)
    print("数据生成完成！可以运行 game_login_demo.py 进行异常检测")
    print("=" * 60)


if __name__ == '__main__':
    main()
