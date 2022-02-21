# código para comentar en los grupos de la clase
# de acuerdo al patrón trabajado

import serial
import cv2,    numpy as np

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
ser.write(b'\r\na \r\n')     
img = np.zeros((512,512,3), np.uint8)
position = (30, 30)
text = "Some text including newline \n characters."
font_scale = 0.75
color = (255, 0, 0)
thickness = 3
font = cv2.FONT_HERSHEY_SIMPLEX
line_type = cv2.LINE_AA

text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
line_height = text_size[1] + 5
x, y0 = position
rep=1
while rep:
    n=ser.in_waiting
    for i, line in enumerate(text.split("\n")):
        y = y0 + i * line_height
        cv2.putText(img,
                    line,
                    (x, y),
                    font,
                    font_scale,
                    color,
                    thickness,
                    line_type)
    cv2.imshow('image',img)

    letra_serial = ser.read(n).decode()
    if letra_serial == '\r':
        letra_serial = '\r\n'
    text += letra_serial
        
    letra_teclado = cv2.waitKey(20) 
    if letra_teclado == 27:
        break
    elif letra_teclado > 0:
        if letra_teclado == 13:
            ser.write(b'\r\n')  
        else:
            ser.write(chr(letra_teclado).encode('ascii'))  
        
        
cv2.destroyAllWindows()
ser.close()   

