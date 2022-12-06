import glob 
import cv2
import math


# ------------- Implementação do algoritmo apresentado por (PREMAL, 2014) ----------------------
imagens = [cv2.imread(file) for file in glob.glob("dataset/*.jpg")]

for i in imagens:
    # convertendo BGR -> YCbCr
    bgr_imagem = i
    ycc_imagem = cv2.cvtColor(bgr_imagem, cv2.COLOR_BGR2YCrCb)
    cv2.imshow("Imagem de Entrada", bgr_imagem)
    (m, n, z) = ycc_imagem.shape

    # calculado a dimensao da imagem
    print(f"M = {m}")
    print(f"N = {n}")
    print(f"Z = {z}")

    # calculando Y_mean, Cb_mean e Cr_mean
    y_soma = 0
    cb_soma = 0
    cr_soma = 0
    for i in range(m):
        for j in range(n):
            y_soma += ycc_imagem[i, j, 0]
            cb_soma += ycc_imagem[i, j, 2]
            cr_soma += ycc_imagem[i, j, 1]

    dimensao = m * n
    y_media = y_soma / dimensao
    cb_media = cb_soma / dimensao
    cr_media = cr_soma / dimensao

    print(f"y_media = {y_media}")
    print(f"cb_media = {cb_media}")
    print(f"cr_media = {cr_media}")

    # calculando desvio padrão de Cr
    cr_std_soma = 0
    for i in range(m):
        for j in range(n):
            cr_std_soma += ((ycc_imagem[i, j, 1] - cr_media) ** 2)

    cr_std_media = cr_std_soma / dimensao
    cr_std = math.sqrt(cr_std_media)

    print(f"Desvio padrão Cr = {cr_std}")

    regra1_imagem = bgr_imagem.copy()
    regra2_imagem = bgr_imagem.copy()
    regra3_imagem = bgr_imagem.copy()
    regra4_imagem = bgr_imagem.copy()

    for i in range(m):
        for j in range(n):
            if ycc_imagem[i][j][0] > ycc_imagem[i][j][2]:
                regra1_imagem[i][j] = bgr_imagem[i][j]
            else:
                regra1_imagem[i][j] = 0 

    for i in range(m):
        for j in range(n):
            if ycc_imagem[i][j][0] > y_media and ycc_imagem[i][j][1] > cr_media:
                regra2_imagem[i][j] = regra1_imagem[i][j]
            else:
                regra2_imagem[i][j] = 0

    for i in range(m):
        for j in range(n):
            if ycc_imagem[i][j][2] >= ycc_imagem[i][j][0] and ycc_imagem[i][j][0] > ycc_imagem[i][j][1]:
                regra3_imagem[i][j] = bgr_imagem[i][j]
            else:
                regra3_imagem[i][j] = 0

    for i in range(m):
        for j in range(n):
            if ycc_imagem[i][j][1] < (7.4 * cr_std):
                regra4_imagem[i][j] = regra3_imagem[i][j]
            else:
                regra4_imagem[i][j] = 0

    # cv2.imshow("Regra 1", regra1_imagem)
    # cv2.imshow("Regra 2", regra2_imagem)
    # cv2.imshow("Regra 3", regra3_imagem)
    # cv2.imshow("Regra 4", regra4_imagem)

    comb_12 = cv2.addWeighted(regra1_imagem, 1, regra2_imagem, 1, 0)
    comb_34 = cv2.addWeighted(regra3_imagem, 1, regra4_imagem, 1, 0)

    comb = cv2.addWeighted(comb_12, 1, comb_34, 1, 0)
    cv2.imshow("Regiao de Fogo Segmentada", comb)

    # cv2.imwrite("r12.jpg", comb_12)
    # cv2.imwrite("r34.jpg", comb_34)
    # cv2.imwrite("rule1.jpg", regra1_imagem)
    # cv2.imwrite("rule2.jpg", regra2_imagem)
    # cv2.imwrite("resultado.jpg", comb)

    cv2.waitKey(0)
cv2.destroyAllWindows()
