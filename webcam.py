import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

def crop_center_zoom(frame, zoom_factor=5.0):
    h, w = frame.shape[:2]
    new_w, new_h = int(w / zoom_factor), int(h / zoom_factor)
    x1 = (w - new_w) // 2
    y1 = (h - new_h) // 2
    cropped = frame[y1:y1 + new_h, x1:x1 + new_w]
    return cv2.resize(cropped, (w, h))

colors_hsv = {
    'Red': [
        ([0, 120, 70], [10, 255, 255]),
        ([160, 120, 70], [179, 255, 255])
    ],
    'Green': [
        ([40, 40, 40], [80, 255, 255])
    ],
    'White': [
        ([0, 0, 200], [180, 30, 255])
    ]
}

box_colors = {
    'Red': (0, 0, 255),
    'Green': (0, 255, 0),
    'White': (255, 255, 255)
}
kernel = np.ones((5, 5), np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = crop_center_zoom(frame, zoom_factor=2.0)

    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    for color_name, ranges in colors_hsv.items():
        mask = None
        for lower, upper in ranges:
            lower_np = np.array(lower)
            upper_np = np.array(upper)
            current_mask = cv2.inRange(hsv, lower_np, upper_np)
            mask = current_mask if mask is None else cv2.bitwise_or(mask, current_mask)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 300:
                x, y, w, h = cv2.boundingRect(cnt)
                aspect_ratio = h / float(w)

                if 1.3 < aspect_ratio < 4.5 and h > 30:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), box_colors[color_name], 2)
                    cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_colors[color_name], 2)

    cv2.imshow("Pin Color Detection (Improved)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
