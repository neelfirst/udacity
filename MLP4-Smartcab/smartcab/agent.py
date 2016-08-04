import random
import numpy as np
import pandas as pd
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

ALPHA = 0.5
GAMMA = 0.25
MAX_EPSILON = 0.25
EP_DECAY_RATE = 100.0

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""
    Q = pd.DataFrame()
    alpha = ALPHA
    gamma = GAMMA
    epsilon = MAX_EPSILON
    ep_decay_rate = EP_DECAY_RATE
#    rolling_reward = 0.0
    penalties = 0
    moves = 0

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
	states = []
	actions = [None,"forward","left","right"]
	for l in ['r','g']:
	    for w in ['f','r','l']:
		for O in ['N','f','r','l']:
		    for R in ['N','f','r','l']:
			for L in ['N','f','r','l']:
			    key = l + w + O + R + L
			    states.append(key)
	self.Q = pd.DataFrame(np.zeros((len(states),len(actions))),index=states,columns=actions)

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
	inputs = self.env.sense(self)
	self.state = self.get_state_key(inputs, self.planner.next_waypoint())
	self.epsilon = MAX_EPSILON
#	self.rolling_reward = 0.0
	self.penalties = 0
	self.moves = 0

    def get_penalty_rate(self):
	return (self.penalties + 0.0)

    def get_move_count(self):
	return (self.moves + 0.0)

    def update(self, t):
        # Gather inputs
	listOfActions=[None,"forward","right","left"]
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
	self.state = self.get_state_key(inputs, self.next_waypoint)
#	print state

#	# Deadline-informed epsilon: Explore less as deadline approaches
	self.epsilon = min(MAX_EPSILON, deadline / self.ep_decay_rate)
        
        # TODO: Select action according to your policy
#       action = random.choice(listOfActions)
#	action = self.next_waypoint
	if np.random.rand() > self.epsilon:
	    action = np.argmax(self.Q.loc[self.state])
	else:
	    action = random.choice(listOfActions)

        # Execute action and get reward
        reward = self.env.act(self, action)
	self.moves += 1
	if (reward < 0):
	    self.penalties += 1

	if (reward < 5):
	    new_inputs = self.env.sense(self)
	    new_waypoint = self.planner.next_waypoint()
	    new_state = self.get_state_key(new_inputs, new_waypoint)
        # TODO: Learn policy based on state, action, reward
	    temp = self.Q.loc[self.state,action]
	    max_Qprime = max(self.Q.loc[new_state])
	    self.Q.loc[self.state,action] = (1.0-self.alpha)*temp + self.alpha*(reward+self.gamma*max_Qprime)
	else:
	    temp = self.Q.loc[self.state,action]
	    self.Q.loc[self.state,action] = (1.0-self.alpha)*temp + self.alpha*reward
	    print "num moves = {}".format(self.moves)
	# if/else hack to ensure reward for completion processed quickly and properly
	# for some reason LearningAgent.update() does not print upon successful end state; we cannot guarantee Q has been updated

#	print "LA.update(): t = {}, s-->s' = {}-->{}, r = {}, net r = {}, a = {}".format(deadline, self.state, new_state, reward, self.rolling_reward, action)
#	print "LearningAgent.update(): deadline = {}, state = {}, action = {}, reward = {}, new_state = {}".format(deadline, self.state, action, reward, new_state)
#        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
#        print "LearningAgent.update(): inputs = {}, action = {}, reward = {}, state = {}".format(inputs, action, reward, self.state)  # [debug]

    def get_state_key(self, inputs, waypoint):
	key = inputs['light'][0] + waypoint[0]
	key += 'N' if inputs['oncoming'] == None else inputs['oncoming'][0]
	key += 'N' if inputs['right'] == None else inputs['right'][0]
	key += 'N' if inputs['left'] == None else inputs['left'][0]
	return key

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.1, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=1000)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
