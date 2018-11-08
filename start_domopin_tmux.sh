#!/bin/bash

SESSION=$USER

tmux -2 new-session -d -s $SESSION
# Setup a window for tailing log files
tmux new-window -t $SESSION:0 -n 'roscore'
tmux new-window -t $SESSION:1 -n 'central'
tmux new-window -t $SESSION:2 -n 'room'
tmux new-window -t $SESSION:3 -n 'rosbridge'
tmux new-window -t $SESSION:4 -n 'interface'


#tmux select-window -t $SESSION:0
#tmux split-window -v
#tmux select-pane -t 0
#tmux send-keys "roscore" C-m
#tmux resize-pane -U 30
#tmux select-pane -t 1
#tmux send-keys "htop" C-m

tmux select-window -t $SESSION:0
#tmux send-keys "roscore" Enter
tmux send-keys "roslaunch domopin_central multimaster.launch" Enter

tmux select-window -t $SESSION:1
#tmux send-keys "roscd roscd domopin_central" C-m
tmux send-keys "sleep 2; roslaunch domopin_central domopin.launch" Enter

tmux select-window -t $SESSION:2
#tmux send-keys "roscd roscd domopin_room" C-m
tmux send-keys " sleep 2; roslaunch domopin_room domopin_room.launch" Enter

tmux select-window -t $SESSION:3
tmux send-keys " sleep 4; roslaunch rosbridge_server rosbridge_websocket.launch" Enter

tmux select-window -t $SESSION:4
tmux send-keys "cd /home/robpin/catkin_ws/src/domopin/interface_touchscreen/www" C-m
tmux send-keys "python -m SimpleHTTPServer" Enter

# Set default window
tmux select-window -t $SESSION:1

# Attach to session
tmux -2 attach-session -t $SESSION

tmux setw -g mode-mouse off
