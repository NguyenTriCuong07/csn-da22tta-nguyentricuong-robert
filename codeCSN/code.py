import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def roberts_cross_edge_detection_manual(image):
    # Chuyển ảnh sang dạng numpy array
    image = np.array(image, dtype=float)

    # Bộ lọc Roberts
    roberts_cross_v = np.array([[1, 0], [0, -1]])  # Roberts filter theo hướng dọc
    roberts_cross_h = np.array([[0, 1], [-1, 0]])  # Roberts filter theo hướng ngang

    # Kích thước ảnh
    rows, cols = image.shape

    # Tạo mảng kết quả
    vertical_edges = np.zeros((rows - 1, cols - 1))
    horizontal_edges = np.zeros((rows - 1, cols - 1))

    # Áp dụng bộ lọc thủ công
    for i in range(rows - 1):
        for j in range(cols - 1):
            # Lọc dọc
            vertical_edges[i, j] = (
                roberts_cross_v[0, 0] * image[i, j] +
                roberts_cross_v[0, 1] * image[i, j + 1] +
                roberts_cross_v[1, 0] * image[i + 1, j] +
                roberts_cross_v[1, 1] * image[i + 1, j + 1]
            )

            # Lọc ngang
            horizontal_edges[i, j] = (
                roberts_cross_h[0, 0] * image[i, j] +
                roberts_cross_h[0, 1] * image[i, j + 1] +
                roberts_cross_h[1, 0] * image[i + 1, j] +
                roberts_cross_h[1, 1] * image[i + 1, j + 1]
            )

    # Kết hợp các cạnh dọc và ngang
    edges = np.sqrt(np.square(vertical_edges) + np.square(horizontal_edges))
    edges = (edges / edges.max()) * 255  # Chuẩn hóa về [0, 255]

    return edges.astype(np.uint8)

# Đọc ảnh đầu vào
input_image = Image.open('hoa-hau-dong-bang-song-cuu-long-17348923470501543287600.webp').convert('L')  # Chuyển sang ảnh xám

# Phát hiện cạnh bằng kỹ thuật Roberts thủ công
edges = roberts_cross_edge_detection_manual(input_image)

# Hiển thị ảnh gốc và ảnh sau khi phát hiện cạnh
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Ảnh gốc")
plt.imshow(input_image, cmap='gray')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Cạnh phát hiện bằng Roberts (Thủ công)")
plt.imshow(edges, cmap='gray')
plt.axis('off')

plt.show()
