# ENPM673 Project 4 Charles Nguyen

## Github Repo Link
- https://github.com/cnguye21-umd/ENPM661/tree/main/Project%202
## Libraries Used
- docker
- moveit
- ros2
## How to run code
1. Download the package and place it in a workspace
2. Make sure to include moveit2_tutorials base package as well as that has the mtc_demo.launch.py file required to launch the robot used in this pick and place
3. colcon build in your workspace
4. source install/setup.bash
5. In Terminal 1 run: ros2 launch moveit2_tutorial mtc_demo.launch.py
6. In Terminal 2 run: ros2 launch package_116924733 proj4.launch.py