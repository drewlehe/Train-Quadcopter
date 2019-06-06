{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'physics_sim'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "\u001b[1;32mcell_name\u001b[0m in \u001b[0;36masync-def-wrapper\u001b[1;34m()\u001b[0m\n",
      "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'physics_sim'"
     ]
    }
   ],
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
    "        reward = 1.-.3*(abs(self.sim.pose[:3] - self.target_pos)).sum()\n",
    "        return reward\n",
    "\n",
    "    def step(self, rotor_speeds):\n",
    "        \"\"\"Uses action to obtain next state, reward, done.\"\"\"\n",
    "        reward = 0\n",
    "        pose_all = []\n",
    "        for _ in range(self.action_repeat):\n",
    "            done = self.sim.next_timestep(rotor_speeds) # update the sim pose and velocities\n",
    "            reward += self.get_reward() \n",
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
  },
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
    "    def __init__(self, init_pose=None, init_velocities=None,\n",
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
    "        self.sim = PhysicsSim(init_pose, init_velocities, init_angle_velocities, runtime)\n",
    "        self.start_pos = self.sim.pose[:3]\n",
    "        self.action_repeat = 3\n",
    "\n",
    "        # state made of current position, velocity and angular velocity\n",
    "        self.state_size = self.action_repeat * (6 + 3 + 3)\n",
    "        self.action_low = 0\n",
    "        self.action_high = 900\n",
    "        self.action_size = 4\n",
    "\n",
    "        # Goal\n",
    "        self.target_pos = target_pos if target_pos is not None else np.array([0., 0., 10.])\n",
    "\n",
    "    def get_reward(self):\n",
    "        \"\"\"Uses current pose of sim to return reward.\"\"\"\n",
    "        reward = 0\n",
    "        penalty = 0\n",
    "        current_position = self.sim.pose[:3]\n",
    "        # penalty for euler angles, we want the takeoff to be stable\n",
    "        penalty += abs(self.sim.pose[3:6]).sum()\n",
    "        # penalty for distance from target\n",
    "        penalty += abs(current_position[0]-self.target_pos[0])**2\n",
    "        penalty += abs(current_position[1]-self.target_pos[1])**2\n",
    "        penalty += 10*abs(current_position[2]-self.target_pos[2])**2\n",
    "\n",
    "        # link velocity to residual distance\n",
    "        penalty += abs(abs(current_position-self.target_pos).sum() - abs(self.sim.v).sum())\n",
    "\n",
    "        distance = np.sqrt((current_position[0]-self.target_pos[0])**2 + (current_position[1]-self.target_pos[1])**2 + (current_position[2]-self.target_pos[2])**2)\n",
    "        # extra reward for flying near the target\n",
    "        if distance < 10:\n",
    "            reward += 1000\n",
    "        # constant reward for flying\n",
    "        reward += 100\n",
    "        return reward - penalty*0.0002\n",
    "\n",
    "\n",
    "    def step(self, rotor_speeds):\n",
    "        \"\"\"Uses action to obtain next state, reward, done.\"\"\"\n",
    "        reward = 0\n",
    "        pose_all = []\n",
    "        for _ in range(self.action_repeat):\n",
    "            done = self.sim.next_timestep(rotor_speeds) # update the sim pose and velocities\n",
    "            reward += self.get_reward()\n",
    "            state = self.current_state()\n",
    "            pose_all.append(self.current_state())\n",
    "        next_state = np.concatenate(pose_all)\n",
    "        return next_state, reward, done\n",
    "\n",
    "    def current_state(self):\n",
    "        \"\"\"The state contains information about current position, velocity and angular velocity\"\"\"\n",
    "        state = np.concatenate([np.array(self.sim.pose), np.array(self.sim.v), np.array(self.sim.angular_v)])\n",
    "        return state\n",
    "\n",
    "    def reset(self):\n",
    "        \"\"\"Reset the sim to start a new episode.\"\"\"\n",
    "        self.sim.reset()\n",
    "        state = np.concatenate([self.current_state()] * self.action_repeat)\n",
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
