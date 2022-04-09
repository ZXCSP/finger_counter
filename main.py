import cv2
import mediapipe as mp
cap = cv2.VideoCapture(0)  # Подключение к веб-камере.
mp_Hands = mp.solutions.hands  #Говорим что хотим распознать руки.
hands = mp_Hands.Hands(max_num_hands = 2)  #Характеристики для распознования.
mpDraw = mp.solutions.drawing_utils  #Инициализация утилит рисования.

fingers_coord = [(8, 6), (12, 10), (16, 14), (20,18),]  #Координаты ключевых точек на руке, кроме большого пальца.
thumb_coord = (4, 2) #Координаты ключевых точек для большого пальца.
while cap.isOpened():  #Пока камера работает.
    success, image = cap.read()  #Получаем кадр с камеры.
    if not success:  #Если не удалось получить кадр с камеры    
        print("Не удалось получит кадр с веб-камеры")
        continue  #Переход к ближайшему циклу (while).
    image = cv2.flip(image, 1) #Зеркально отражаем изображение.
    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  #BGR -> RGB 
    results = hands.process(RGB_image) #Ищем руки на изоброжении
    multiLandMarks = results.multi_hand_landmarks #Извлекаем список найденных
    print (multiLandMarks)
    if multiLandMarks: #Если руки найдены
        upCount = 0
        for idx, handLms in enumerate(multiLandMarks):#Перебираем найденные руки.
            lbl = results.multi_handedness[idx].classification[0].label
            print(lbl)

            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
            fingersList = []

            for idx, im in enumerate(handLms):#Перебираем ключевые точки на руке.
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h) 
                fingersList.append((cx, cy))
            for coordinate in fingers_coord:
                if fingersList[coordinate[0]][1] < fingersList[coordinate[1]][1]:
                    upCount += 1
        print(upCount)
    if multiLandMarks:
        print("Руки есть в кадре")
    else:
        print('Рук в кадре нет')
    cv2.imshow("web-cam", image)
    if cv2.waitKey(1) & 0xFF == 27: #Ожидаем нажатия клавиши ESC
        break
cap.release()

