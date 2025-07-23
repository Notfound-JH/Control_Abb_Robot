import pyrealsense2 as rs
import numpy as np
import cv2

def main():
    # 配置深度和彩色流
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # 启动相机
    pipeline.start(config)

    # 创建对齐对象，将深度帧对齐到彩色帧
    align_to = rs.stream.color
    align = rs.align(align_to)

    # 提前创建窗口，避免循环内重复创建
    cv2.namedWindow('RGB和深度图像实时显示', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('RGB和深度图像实时显示', 1280, 480)

    try:
        while True:
            # 等待获取下一组帧
            frames = pipeline.wait_for_frames()
            
            # 对齐深度帧到彩色帧
            aligned_frames = align.process(frames)
            
            # 获取对齐后的深度帧和彩色帧
            aligned_depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            
            # 验证两个帧都有效
            if not aligned_depth_frame or not color_frame:
                continue
            
            # 将图像转换为numpy数组
            depth_image = np.asanyarray(aligned_depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            
            # 应用深度色映射
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            
            # 创建一个大窗口，水平拼接RGB和深度图像
            combined_image = np.hstack((color_image, depth_colormap))
            
            # 显示组合图像
            cv2.imshow('RGB和深度图像实时显示', combined_image)
            
            # 按ESC或q退出循环
            key = cv2.waitKey(1)
            if key & 0xFF == 27 or key == ord('q'):
                break

    finally:
        # 停止相机并释放资源
        cv2.destroyAllWindows()
        pipeline.stop()

if __name__ == "__main__":
    main()    