import json
import pika
import time
import os
from datetime import datetime

# Connect to message queue
for _ in range(10):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="mq", heartbeat=0)
        )
    except pika.exceptions.AMQPConnectionError:
        time.sleep(1)

channel = connection.channel()
channel.queue_declare(queue="cv_to_od")
channel.queue_declare(queue="od_to_sockets")

# limit the number of cpus used by high performance libraries
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import sys
import numpy as np
from pathlib import Path
import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # yolov5 strongsort root directory
WEIGHTS = ROOT / "weights"

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if str(ROOT / "yolov5") not in sys.path:
    sys.path.append(str(ROOT / "yolov5"))  # add yolov5 ROOT to PATH
if str(ROOT / "strong_sort") not in sys.path:
    sys.path.append(str(ROOT / "strong_sort"))  # add strong_sort ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

import logging
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.dataloaders import VID_FORMATS, LoadImages, LoadStreams
from yolov5.utils.general import (
    LOGGER,
    check_img_size,
    non_max_suppression,
    scale_coords,
    cv2,
    xyxy2xywh,
    colorstr,
)
from yolov5.utils.torch_utils import select_device, time_sync
from yolov5.utils.plots import Annotator, colors, save_one_box
from strong_sort.utils.parser import get_config
from strong_sort.strong_sort import StrongSORT

# remove duplicated stream handler to avoid duplicated logging
logging.getLogger().removeHandler(logging.getLogger().handlers[0])


@torch.no_grad()
def run():
    yolo_weights = WEIGHTS / "yolov5s.pt"  # model.pt path(s),
    strong_sort_weights = WEIGHTS / "osnet_x0_25_msmt17.pt"  # model.pt path,
    config_strongsort = ROOT / "strong_sort/configs/strong_sort.yaml"
    imgsz = (640, 640)  # inference size (height, width)
    half = False  # use FP16 half-precision inference
    dnn = False  # use OpenCV DNN for ONNX inference

    save_dir = str(r"/output/")

    # Load model
    device = select_device("")
    model = DetectMultiBackend(
        yolo_weights, device=device, dnn=dnn, data=None, fp16=half
    )
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # initialize StrongSORT
    cfg = get_config()
    cfg.merge_from_file(config_strongsort)

    # Create as many strong sort instances as there are video sources
    strongsort_list = StrongSORT(
        strong_sort_weights,
        device,
        half,
        max_dist=cfg.STRONGSORT.MAX_DIST,
        max_iou_distance=cfg.STRONGSORT.MAX_IOU_DISTANCE,
        max_age=cfg.STRONGSORT.MAX_AGE,
        n_init=cfg.STRONGSORT.N_INIT,
        nn_budget=cfg.STRONGSORT.NN_BUDGET,
        mc_lambda=cfg.STRONGSORT.MC_LAMBDA,
        ema_alpha=cfg.STRONGSORT.EMA_ALPHA,
    )

    strongsort_list.model.warmup()

    def on_message(channel, method_frame, header_frame, body):
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        body = json.loads(body.decode("utf-8"))
        if body["type"] == "movement-stop":
            
            source_file = body["clip_url"]
            detect(
                source_file,
                save_dir,
                imgsz,
                stride,
                pt,
                model,
                device,
                half,
                cfg,
                strongsort_list,
                names,
                body
            )

    channel.basic_consume("cv_to_od", on_message)
    channel.start_consuming()


def detect(
    source_file,
    save_dir,
    imgsz,
    stride,
    pt,
    model,
    device,
    half,
    cfg,
    strongsort_list,
    names,
    body
):
    # Config
    augment = False 

    conf_thres = 0.5
    iou_thres = 0.45

    classes = None
    agnostic_nms = False

    max_det = 1000

    try:
        os.mkdir(f"/output/{body['streamID']}")
    except FileExistsError:
        pass


    dest_file = f"/output{source_file}"

    source_file = f"/output/{source_file}"
    source_but_mp4 = os.path.splitext(source_file)[0] + ".mp4"

    # Pretend our .webm is a .mp4 so yolov5 can load it
    os.link(source_file, source_but_mp4)
    dataset = LoadImages(source_but_mp4, img_size=imgsz, stride=stride, auto=pt)
    os.unlink(source_but_mp4)

    # Run tracking
    objects, images = [], []
    model.warmup(imgsz=(1, 3, *imgsz))  # warmup
    dt, seen = [0.0, 0.0, 0.0, 0.0], 0
    curr_frames, prev_frames = np.array([0]), np.array([0])
    for frame_idx, (path, im, im0s, vid_cap, s) in enumerate(dataset):

        fps = vid_cap.get(cv2.CAP_PROP_FPS)
        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        t1 = time_sync()
        im = torch.from_numpy(im).to(device)
        im = im.half() if half else im.float()  # uint8 to fp16/32
        im /= 255.0  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        pred = model(im, augment=augment, visualize=False)
        t3 = time_sync()
        dt[1] += t3 - t2

        # Apply NMS
        pred = non_max_suppression(
            pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det
        )
        dt[2] += time_sync() - t3

        # Process detections
        det = pred[0]
        seen += 1
        p, im0, _ = path, im0s.copy(), getattr(dataset, "frame", 0)
        p = Path(p)  # to Path
        # video file

        curr_frames = im0

        s += "%gx%g " % im.shape[2:]  # print string

        annotator = Annotator(im0, line_width=2, pil=not ascii)
        if cfg.STRONGSORT.ECC:  # camera motion compensation
            strongsort_list.tracker.camera_update(prev_frames, curr_frames)

        if det is not None and len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

            # Print results
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class
                s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

            xywhs = xyxy2xywh(det[:, 0:4])
            confs = det[:, 4]
            clss = det[:, 5]

            # pass detections to strongsort
            t4 = time_sync()
            outputs = strongsort_list.update(xywhs.cpu(), confs.cpu(), clss.cpu(), im0)
            t5 = time_sync()
            dt[3] += t5 - t4

            # draw boxes for visualization
            if len(outputs) > 0:
                for j, (output, conf) in enumerate(zip(outputs, confs)):

                    bboxes = output[0:4]
                    id = int(output[4])
                    c = int(output[5])
                    conf = output[6]

                    # Corners of thresh boxes
                    bbox_left = output[0]
                    bbox_top = output[1]
                    bbox_w = output[2] - output[0]
                    bbox_h = output[3] - output[1]

                    detection = "{} (id: {})".format(names[c], id)

                    if detection not in objects:
                        objects.append(detection)

                    label = f"{id} {names[c]} {conf:.2f}"
                    annotator.box_label(bboxes, label, color=colors(c, True))

            LOGGER.info(f"{s}Done. YOLO:({t3 - t2:.3f}s), StrongSORT:({t5 - t4:.3f}s)")

        else:
            strongsort_list.increment_ages()
            LOGGER.info("No detections")

        # Stream results
        images.append(annotator.result())

        prev_frames = curr_frames

    if objects:
        vid_writer = cv2.VideoWriter(
            dest_file, cv2.VideoWriter_fourcc(*"VP90"), fps, (w, h)
        )
        for image in images:
            vid_writer.write(image)
        vid_writer.release()

        body = {**body, **{
            "type": "object",
            "detail": objects,
            "clip_url": dest_file.replace('/output', ''),
        }}

        channel.basic_publish(
            exchange="", routing_key="od_to_sockets", body=json.dumps(body)
        )

        # Print results
        t = tuple(x / seen * 1e3 for x in dt)  # speeds per image
        LOGGER.info(
            f"Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS, %.1fms strong sort update per image at shape {(1, 3, *imgsz)}"
            % t
        )
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")


if __name__ == "__main__":
    run()
