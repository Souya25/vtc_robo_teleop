# vtc_teleop
トピック/cmd_vel にキーボードをつかって速度指令を与えるパッケージ　

## インストールと使い方
```
cd ~/catkin_ws/src
git clone https://github.com/Souya25/vtc_robo_teleop.git
cd ~/catkin_ws
catkin_make

(別のターミナルで)roscore
rosrun vtc_teleop vtc_teleop.py
```

https://github.com/ROBOTIS-GIT/turtlebot3/blob/master/turtlebot3_teleop/nodes/turtlebot3_teleop_key
を基に作成
変更点
  ・最大速度を変更
