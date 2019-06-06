{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "from physics_sim import PhysicsSim\n",
    "\n",
    "class Task():\n",
    "    \"\"\"Task (environment) that defines the goal and provides feedback to the agent.\"\"\"\n",
    "    def __init__(self, init_pose=None, init_velocities=None, \n",
    "        init_angle_velocities=None, runtime=5., target_pos=None):\n",
    "        \"\"\"Initialize a Task object.\n",
    "        Params\n",
    "        ======\n",
    "            init_pose: initial position of the quadcopter in (x,y,z) dimensions and the Euler angles\n",
    "            init_velocities: initial velocity of the quadcopter in (x,y,z) dimensions\n",
    "            init_angle_velocities: initial radians/second for each of the three Euler angles\n",
    "            runtime: time limit for each episode\n",
    "            target_pos: target/goal (x,y,z) position for the agent\n",
    "        \"\"\"\n",
    "        # Simulation\n",
    "        self.sim = PhysicsSim(init_pose, init_velocities, init_angle_velocities, runtime) \n",
    "        self.action_repeat = 3\n",
    "\n",
    "        self.state_size = self.action_repeat * 6\n",
    "        self.action_low = 0\n",
    "        self.action_high = 900\n",
    "        self.action_size = 4\n",
    "\n",
    "        # Goal\n",
    "        self.target_pos = target_pos if target_pos is not None else np.array([0., 0., 10.]) \n",
    "\n",
    "    def get_reward(self):\n",
    "        \"\"\"Uses current pose of sim to return reward.\"\"\"\n",
    "        #reward = 1-(0.3*(abs(self.sim.pose[:3] - self.target_pos))).sum()\n",
    "        #reward = np.tanh(reward)\n",
    "        reward = np.tanh(1 - 0.0005*(abs(self.sim.pose[:3] - self.target_pos)).sum())\n",
    "        return reward\n",
    "\n",
    "    def step(self, rotor_speeds):\n",
    "        \"\"\"Uses action to obtain next state, reward, done.\"\"\"\n",
    "        reward = 0\n",
    "        pose_all = []\n",
    "        for _ in range(self.action_repeat):\n",
    "            done = self.sim.next_timestep(rotor_speeds) # update the sim pose and velocities\n",
    "            reward += (self.get_reward()/2)\n",
    "            #if reward > 1: reward = 1\n",
    "            #if reward < -1: reward = -1\n",
    "            #reward = np.tanh(0.5*reward)\n",
    "            pose_all.append(self.sim.pose)\n",
    "        next_state = np.concatenate(pose_all)\n",
    "        return next_state, reward, done\n",
    "\n",
    "    def reset(self):\n",
    "        \"\"\"Reset the sim to start a new episode.\"\"\"\n",
    "        self.sim.reset()\n",
    "        state = np.concatenate([self.sim.pose] * self.action_repeat) \n",
    "return state"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
