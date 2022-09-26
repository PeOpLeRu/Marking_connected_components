import matplotlib.pyplot as plt
import numpy as np

def check(B, y, x):
    if not 0 <= y < B.shape[0]:
        return False
    if not 0 <= x < B.shape[1]:
        return False
    if B[y, x] != 0:
        return True
    return False

def neighbors2(B, y, x):
    left = y, x-1
    top = y - 1, x
    if not check(B, *left):
        left = None
    if not check(B, *top):
        top = None
    return left, top

def exists(neighbors):
    return not all([n is None for n in neighbors])

def find(label, linked):
    j = label
    while linked[j] != 0:
        j = linked[j]
    return j

def union(label1, label2, linked):
    j = find(label1, linked)
    k = find(label2, linked)
    if j != k:
        linked[k] = j

def two_pass_labeling(B):
    B = (B.copy() * - 1).astype("int")
    linked = np.zeros(len(B), dtype="uint")
    labels = np.zeros_like(B)
    print(labels)
    label = 1
    for row in range(B.shape[0]):
        for col in range(B.shape[1]):
            if B[row, col] != 0:
                n = neighbors2(B, row, col)
                if not exists(n):
                    m = label
                    label += 1
                else:
                    lbs = [labels[i] for i in n if i is not None]
                    m = min(lbs)
                labels[row, col] = m
                for i in n:
                    if i is not None:
                        lb = labels[i]
                        if lb != m:
                            union(m, lb, linked)
                
            #print(f"({row}, {col})   " + str(linked))

    ref_label = [0] * label # Здесь будут хранится новые значения маркера <---> ref_label[текущий номер маркера] = будущий номер маркера
    counter = 1

    # Назначаем номер нессылающимся маркерам
    # Обновляем номер у ссылающихся маркеров
    # Обновляем маркер

    for i in range(1, label):
        if linked[i] == 0: # Если этот объект никуда не ссылается даем ему порядковый номер марки
            ref_label[i] = counter
            counter += 1

    for i in range(1, label):
        if linked[i] != 0:
            ref_label[i] = ref_label[linked[i]] # Объекты, которые ссылаются на другие маркеры, получают маркеры целевыъ объектов (которые уже размечены)

    for row in range(B.shape[0]):
        for col in range(B.shape[1]):
            if B[row, col] != 0:
               labels[row, col] = ref_label[labels[row][col]] # Переназначаем объекту номер маркера

    return labels

if __name__ == "__main__":
    image = np.zeros((20, 20), dtype='int32')
    
    image[1:-1, -2] = 1
    
    image[1, 1:5] = 1
    image[1, 7:12] = 1
    image[2, 1:3] = 1
    image[2, 6:8] = 1
    image[3:4, 1:7] = 1
    
    image[7:11, 11] = 1
    image[7:11, 14] = 1
    image[10:15, 10:15] = 1
    
    image[5:10, 5] = 1
    image[5:10, 6] = 1

    labeled_image = two_pass_labeling(image)
    
    plt.figure(figsize=(12, 5))
    plt.subplot(121)
    plt.imshow(image)
    plt.subplot(122)
    plt.imshow(labeled_image.astype("uint8"))
    plt.show()