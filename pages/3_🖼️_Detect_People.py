import cv2
import streamlit as st
from ultralytics import YOLO
import tempfile
from deep_sort_realtime.deepsort_tracker import DeepSort

st.title("People Detection")


vid = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
model = YOLO("people_detector.pt")
if vid is not None:

    video = tempfile.NamedTemporaryFile(delete=False)
    video.write(vid.read())
    st.video(vid)

    cap = cv2.VideoCapture(video.name)

    stframe = st.empty()
    counter = st.empty()

    detect_button = st.button("Detect People")
    if detect_button:
        tracker = DeepSort(max_age=30)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (640, 360))

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            detections = model(frame)
            det = detections[0]
            boxes = det.boxes.xyxy.cpu().numpy()

            tracker = DeepSort(max_age=30) 
            ids_detections = [
                [[float(x1), float(y1), float(x2), float(y2)], float(conf), int(class_id)] 
                for (x1, y1, x2, y2), conf, class_id in zip(boxes, det.boxes.conf.cpu().numpy(), det.boxes.cls.cpu().numpy())
                if int(class_id) == 0  # only person class
            ]
            tracks = tracker.update_tracks(ids_detections, frame=frame) 
            
            seen_ids = set() 
            for track in tracks:
                if not track.is_confirmed(): 
                    continue
                track_id = track.track_id 
                if track_id not in seen_ids: 
                    seen_ids.add(track_id)

            for detection in detections:
                for box in detection.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = box.conf[0]  
                    cls = int(box.cls[0])  
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)


                    label = f"{model.names[cls]} {conf:.2f}"

                    text_x, text_y = x2 + 10, y1 - 10
                    cv2.line(frame, (x2, y1), (text_x, text_y), (0, 255, 0), 2)

                    text_box_w, text_box_h = 150, 30
                    cv2.rectangle(frame, (text_x, text_y - 20), (text_x + text_box_w, text_y + text_box_h), (0, 255, 0), -1)

                    cv2.putText(frame, label, (text_x + 5, text_y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    stframe.image(frame)
            
                    counter.write(f"Detected people: {len(seen_ids)}")

        cap.release()
    