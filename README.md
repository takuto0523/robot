# robot
```
ros2 run apriltag_ros apriltag_node --ros-args -r image_rect:=/image_raw -r camera_info:=/camera_info --params-file /home/takuto/ros2_ws/src/apriltag_ros/cfg/tags_36h11.yaml
```
```
ros2 run usb_cam usb_cam_node_exe --ros-args --params-file /home/takuto/ros2_ws/src/usb_cam/config/params_2.yaml
```
```
ros2 run image_proc rectify_node --ros-args -r image:=/image_raw -r image_rect:=/image_rect --params-file /home/takuto/ros2_ws/src/usb_cam/config/rectify_params.yaml
```
