import os
import random
import shutil

def split_dataset(input_dir, output_dir, train_ratio=0.8):
    """
    将子文件夹中的图片分为训练集和验证集。
    :param input_dir: 输入文件夹，包含子文件夹和图片
    :param output_dir: 输出文件夹，将生成 train 和 val 子文件夹
    :param train_ratio: 训练集比例（默认 80%）
    """
    # 确保输出文件夹存在
    os.makedirs(output_dir, exist_ok=True)
    train_dir = os.path.join(output_dir, 'train')
    val_dir = os.path.join(output_dir, 'val')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    for subfolder in os.listdir(input_dir):
        subfolder_path = os.path.join(input_dir, subfolder)
        if not os.path.isdir(subfolder_path):
            continue  # 跳过非文件夹

        # 创建类别文件夹
        train_subfolder = os.path.join(train_dir, subfolder)
        val_subfolder = os.path.join(val_dir, subfolder)
        os.makedirs(train_subfolder, exist_ok=True)
        os.makedirs(val_subfolder, exist_ok=True)

        # 获取图片文件列表
        images = [img for img in os.listdir(subfolder_path) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
        random.shuffle(images)  # 随机打乱文件顺序

        # 计算分割点
        train_count = int(len(images) * train_ratio)
        train_images = images[:train_count]
        val_images = images[train_count:]

        # 将图片分别移动到 train 和 val 文件夹
        for img in train_images:
            shutil.copy(os.path.join(subfolder_path, img), os.path.join(train_subfolder, img))
        for img in val_images:
            shutil.copy(os.path.join(subfolder_path, img), os.path.join(val_subfolder, img))

    print("数据集划分完成！")

# 使用示例
input_dir = "./datasets/wafer_map"
output_dir = "./datasets/wafer_map"
split_dataset(input_dir, output_dir, train_ratio=0.8)
