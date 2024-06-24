import cv2
import numpy as np
import yaml
import matplotlib.pyplot as plt
import os

def non_max_suppression(boxes, overlap_thresh=0.5):
    if len(boxes) == 0:
        return []
    
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
    
    pick = []
    
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]
    
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)
    
    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        
        overlap = (w * h) / area[idxs[:last]]
        
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlap_thresh)[0])))
    
    return boxes[pick].astype("int")

def generate_hsv_label(cfg_file, image_file, label_file):
    with open(cfg_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    image = cv2.imread(image_file)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv_image = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2HSV)
    height, width, _ = image.shape
    
    plt.imshow(hsv_image)
    plt.show()

    with open(label_file, 'w') as f:
        for entry in config['classes']:
            class_id = entry['class_id']
            hsv_lower = np.array([
                entry['H']['start'],
                entry['S']['start'],
                entry['V']['start']
            ])
            hsv_upper = np.array([
                entry['H']['stop'],
                entry['S']['stop'],
                entry['V']['stop']
            ])
            
            mask = cv2.inRange(hsv_image, hsv_lower, hsv_upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            boxes = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                if w > 10 and h > 10:  # Exclude very small bounding boxes
                    boxes.append([x, y, x + w, y + h])
            
            boxes = np.array(boxes)
            boxes = non_max_suppression(boxes)
            
            for box in boxes:
                x1, y1, x2, y2 = box
                x_center = (x1 + (x2 - x1) / 2) / width
                y_center = (y1 + (y2 - y1) / 2) / height
                w_norm = (x2 - x1) / width
                h_norm = (y2 - y1) / height
                
                f.write(f'{class_id} {x_center} {y_center} {w_norm} {h_norm}\n')

if __name__ == "__main__":
    import glob
    
    cfg_file = 'HSV_Thresholds.cfg.yaml'  # Replace with your actual config file name
    images_dir = 'dataset/images/'        # Replace with your actual images directory
    labels_dir = 'dataset/gen_labels/'    # Replace with your actual labels directory
    
    for subdir in ['train']:
        images_subdir = os.path.join(images_dir, subdir)
        labels_subdir = os.path.join(labels_dir, subdir)
        os.makedirs(labels_subdir, exist_ok=True)
        
        print(f'Processing images in directory: {images_subdir}')
        
        for image_file in glob.glob(os.path.join(images_subdir, '*.jpg')):
            base_name = os.path.basename(image_file)
            label_file = os.path.join(labels_subdir, os.path.splitext(base_name)[0] + '.txt')
            
            generate_hsv_label(cfg_file, image_file, label_file)
            print(f'Generated label for {image_file} at {label_file}')

