''' code to make the POMDP file for assignment ''' 

NO_OF_AGENT_POSITIONS = 8
NO_OF_TARGET_POSITIONS = 8
NO_OF_CALL_STATES = 2
GRID_HEIGHT = 2
GRID_WIDTH = 4
TOTAL_NO_OF_STATES = NO_OF_AGENT_POSITIONS*NO_OF_TARGET_POSITIONS*NO_OF_CALL_STATES
NO_OF_OBSERVATIONS = 6
DISCOUNT = 0.5
ROLL_NUMBER = 2019111020
p_x = 1-(((ROLL_NUMBER%10000)%30 + 1)/100)
REWARD = (ROLL_NUMBER)%90 + 10
STEP_COST = -1

QUESTION_NUMBER = 1

''' function to convert (x,y) denoting grid position to an integer ''' 
def hash(x,y):
    return y*4 + x

''' function to undo the hash.Given z return (x,y) such that hash(x,y) = z '''
def reverse_hash(z):
    return (z % 4, z // 4)


''' a variable given a state (position_of_agent,position_of_target,call on/off) return a integer representing id ''' 
state_identity = [[[0 for i in range(NO_OF_CALL_STATES)] for j in range(NO_OF_TARGET_POSITIONS)] for k in range(NO_OF_AGENT_POSITIONS)]

''' a variable given a id return the state '''

get_state = []

''' create the state_identity and get state '''
def generate():
    cnt = 0
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            for k in range(GRID_HEIGHT):
                for l in range(GRID_WIDTH):
                    for m in range(NO_OF_CALL_STATES):
                        agent_pos = hash(j,i)
                        target_pos = hash(l,k)
                        state_identity[agent_pos][target_pos][m] = cnt 
                        get_state.append((agent_pos,target_pos,m))
                        cnt += 1

''' given the position of the agent ,returns the distribution of the next position of the agent when the action is "STAY"'''
def stay_agent(pos_id): 
    distribution = [0.0 for i in range(NO_OF_AGENT_POSITIONS)]
    distribution[pos_id] = 1
    return distribution

''' given the position of the agent ,returns the distribution of the next position of the agent when the action is "UP" '''
def up_agent(pos_id): 
    distribution = [0.0 for i in range(NO_OF_AGENT_POSITIONS)]
    (x,y) = reverse_hash(pos_id)
    #succesfull
    distribution[hash(x,max(y-1,0))] = p_x
    #unsuccesfull
    distribution[hash(x,min(y+1,GRID_HEIGHT - 1))] = 1-p_x
    return distribution

''' given the position of the agent ,returns the distribution of the next position of the agent when the action is "DOWN" '''
def down_agent(pos_id): 
    distribution = [0.0 for i in range(NO_OF_AGENT_POSITIONS)]
    (x,y) = reverse_hash(pos_id)
    #succesfull
    distribution[hash(x,min(y+1,GRID_HEIGHT - 1))] = p_x
    #unsuccesfull
    distribution[hash(x,max(y-1,0))] = 1 - p_x
    return distribution

''' given the position of the agent ,returns the distribution of the next position of the agent when the action is "LEFT" '''
def left_agent(pos_id): 
    distribution = [0.0 for i in range(NO_OF_AGENT_POSITIONS)]
    (x,y) = reverse_hash(pos_id)
    #succesfull
    distribution[hash(max(x-1,0),y)] = p_x
    #unsuccesfull
    distribution[hash(min(x+1,GRID_WIDTH - 1),y)] = 1 - p_x
    return distribution

''' given the position of the agent ,returns the distribution of the next position of the agent when the action is "RIGHT" '''
def right_agent(pos_id): 
    distribution = [0.0 for i in range(NO_OF_AGENT_POSITIONS)]
    (x,y) = reverse_hash(pos_id)
    #unsuccesfull
    distribution[hash(max(x-1,0),y)] = 1 - p_x
    #succesfull
    distribution[hash(min(x+1,GRID_WIDTH - 1),y)] = p_x
    return distribution

''' given position of the the target returns the distribution of next position of target ''' 
def move_target(pos_id):
    distribution = [0.0 for i in range(NO_OF_TARGET_POSITIONS)]
    distribution[pos_id] += 0.6
    (x,y) = reverse_hash(pos_id)
    #up
    distribution[hash(x,max(y-1,0))] += 0.1
    #down
    distribution[hash(x,min(GRID_HEIGHT-1,y+1))] += 0.1
    #left
    distribution[hash(max(0,x-1),y)] += 0.1
    #right
    distribution[hash(min(GRID_WIDTH-1,x+1),y)] += 0.1
    return distribution
    



'''List of Actions '''
ACTIONS = ["STAY","UP","DOWN","LEFT","RIGHT"]

ACTION_CODE = { 
    'STAY' : 0,
    "UP" : 1,
    "DOWN" : 2,
    "LEFT" : 3,
    "RIGHT" : 4
    }

ACTION_FUNCTIONS = {
    'STAY': stay_agent,
    'UP': up_agent,
    'DOWN': down_agent,
    'LEFT': left_agent,
    'RIGHT': right_agent
}

OBERVATIONS = [i+1 for i in range(NO_OF_OBSERVATIONS)]

def create_transition_table_alt():
    transition_table = [[[] for j in range(len(ACTIONS))] for i  in range(TOTAL_NO_OF_STATES)]
    
    for s in range(TOTAL_NO_OF_STATES):
        (current_agent,current_target,call) = get_state[s]
        target_distribution = move_target(current_target)

        caught = False
        if call == 1 and current_agent == current_target:
            caught = True
        
        for a in ACTIONS:
            distribution = [0.0 for i  in range(TOTAL_NO_OF_STATES)]
            agent_distribution = ACTION_FUNCTIONS[a](current_agent)
            for a_p in range(len(agent_distribution)):
                for t_p in range(len(target_distribution)):
                    p1 = agent_distribution[a_p]
                    p2 = target_distribution[t_p]
                    if caught:
                        next_state_id = state_identity[a_p][t_p][0]
                        distribution[next_state_id] = p1*p2
                    else:
                        if call == 1:
                            #if call changes to 0
                            next_state_id = state_identity[a_p][t_p][0]
                            distribution[next_state_id] += p1*p2*0.1
                            #if call remains 1
                            next_state_id = state_identity[a_p][t_p][1]
                            distribution[next_state_id] += p1*p2*0.9
                        elif call == 0:
                            #if call changes to  1
                            next_state_id = state_identity[a_p][t_p][1]
                            distribution[next_state_id] += p1*p2*0.5
                            #if call remains 0
                            next_state_id = state_identity[a_p][t_p][0]
                            distribution[next_state_id] += p1*p2*0.5
            
            transition_table[s][ACTION_CODE[a]] = distribution
    
    return transition_table

''' TRANSITION TABLE CREATION , T[s][a][s'] denotes the probability of reaching state s' after taking action a from current state s '''

''' function to generate the transition table '''
def create_transition_table():
    transition_table = [[[] for j in range(len(ACTIONS))] for i  in range(TOTAL_NO_OF_STATES)]
    for s in range(TOTAL_NO_OF_STATES):
        for a in ACTIONS:
            (current_agent,current_target,call) = get_state[s]
            distribution = [0.0 for i  in range(TOTAL_NO_OF_STATES)]
            target_distribution = move_target(current_target)


            if(a == "STAY"):
                agent_distribution = stay_agent(current_agent)
                if(call == 1):
                    for a_p in range(len(agent_distribution)):
                        for t_p in range(len(target_distribution)):
                            p1 = agent_distribution[a_p]
                            p2 = target_distribution[t_p]
                            #agent and target reaches same positon
                            if(a_p == t_p):
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2
                            else:
                                #if call changes to  0
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2*0.1
                                #if call remains 1
                                next_state_id = state_identity[a_p][t_p][1]
                                distribution[next_state_id] += p1*p2*0.9

                if(call == 0):
                    for a_p in range(len(agent_distribution)):
                        for t_p in range(len(target_distribution)):
                            p1 = agent_distribution[a_p]
                            p2 = target_distribution[t_p]
                            #agent and target reaches same positon
                            if(a_p == t_p):
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2
                            else:
                                #if call changes to  1
                                next_state_id = state_identity[a_p][t_p][1]
                                distribution[next_state_id] += p1*p2*0.5
                                #if call remains 0
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2*0.5

            
            
            if(a == "DOWN"):
                agent_distribution = down_agent(current_agent)
                if(call == 1):
                    for a_p in range(len(agent_distribution)):
                        for t_p in range(len(target_distribution)):
                            p1 = agent_distribution[a_p]
                            p2 = target_distribution[t_p]
                            #agent and target reaches same positon
                            if(a_p == t_p):
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2
                            else:
                                #if call changes to  0
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2*0.1
                                #if call remains 1
                                next_state_id = state_identity[a_p][t_p][1]
                                distribution[next_state_id] += p1*p2*0.9

                if(call == 0):
                    for a_p in range(len(agent_distribution)):
                        for t_p in range(len(target_distribution)):
                            p1 = agent_distribution[a_p]
                            p2 = target_distribution[t_p]
                            #agent and target reaches same positon
                            if(a_p == t_p):
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2
                            else:
                                #if call changes to  1
                                next_state_id = state_identity[a_p][t_p][1]
                                distribution[next_state_id] += p1*p2*0.5
                                #if call remains 0
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2*0.5
            
            if(a == "LEFT"):
                agent_distribution = left_agent(current_agent)
                if(call == 1):
                    for a_p in range(len(agent_distribution)):
                        for t_p in range(len(target_distribution)):
                            p1 = agent_distribution[a_p]
                            p2 = target_distribution[t_p]
                            #agent and target reaches same positon
                            if(a_p == t_p):
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2
                            else:
                                #if call changes to  0
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2*0.1
                                #if call remains 1
                                next_state_id = state_identity[a_p][t_p][1]
                                distribution[next_state_id] += p1*p2*0.9

                if(call == 0):
                    for a_p in range(len(agent_distribution)):
                        for t_p in range(len(target_distribution)):
                            p1 = agent_distribution[a_p]
                            p2 = target_distribution[t_p]
                            #agent and target reaches same positon
                            if(a_p == t_p):
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2
                            else:
                                #if call changes to  1
                                next_state_id = state_identity[a_p][t_p][1]
                                distribution[next_state_id] += p1*p2*0.5
                                #if call remains 0
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2*0.5    

            if(a == "RIGHT"):
                agent_distribution = right_agent(current_agent)
                if(call == 1):
                    for a_p in range(len(agent_distribution)):
                        for t_p in range(len(target_distribution)):
                            p1 = agent_distribution[a_p]
                            p2 = target_distribution[t_p]
                            #agent and target reaches same positon
                            if(a_p == t_p):
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2
                            else:
                                #if call changes to  0
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2*0.1
                                #if call remains 1
                                next_state_id = state_identity[a_p][t_p][1]
                                distribution[next_state_id] += p1*p2*0.9

                if(call == 0):
                    for a_p in range(len(agent_distribution)):
                        for t_p in range(len(target_distribution)):
                            p1 = agent_distribution[a_p]
                            p2 = target_distribution[t_p]
                            #agent and target reaches same positon
                            if(a_p == t_p):
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2
                            else:
                                #if call changes to  1
                                next_state_id = state_identity[a_p][t_p][1]
                                distribution[next_state_id] += p1*p2*0.5
                                #if call remains 0
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2*0.5    


            if(a == "UP"):
                agent_distribution = up_agent(current_agent)
                if(call == 1):
                    for a_p in range(len(agent_distribution)):
                        for t_p in range(len(target_distribution)):
                            p1 = agent_distribution[a_p]
                            p2 = target_distribution[t_p]
                            #agent and target reaches same positon
                            if(a_p == t_p):
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2
                            else:
                                #if call changes to  0
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2*0.1
                                #if call remains 1
                                next_state_id = state_identity[a_p][t_p][1]
                                distribution[next_state_id] += p1*p2*0.9

                if(call == 0):
                    for a_p in range(len(agent_distribution)):
                        for t_p in range(len(target_distribution)):
                            p1 = agent_distribution[a_p]
                            p2 = target_distribution[t_p]
                            #agent and target reaches same positon
                            if(a_p == t_p):
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2
                            else:
                                #if call changes to  1
                                next_state_id = state_identity[a_p][t_p][1]
                                distribution[next_state_id] += p1*p2*0.5
                                #if call remains 0
                                next_state_id = state_identity[a_p][t_p][0]
                                distribution[next_state_id] += p1*p2*0.5
            transition_table[s][ACTION_CODE[a]] = distribution                    
    return transition_table


'''function returns a observation table. For every action and end state it returns a list of 6 tuple giving the probability of observation '''
def generate_observations():
    observation_table = [[[] for i in range(len(ACTIONS))] for j in range(TOTAL_NO_OF_STATES)]
    for s in range(TOTAL_NO_OF_STATES):
        for a in range(len(ACTIONS)):
            (agent_pos,target_pos,call) = get_state[s]
            distribution = [0.0 for i in range(NO_OF_OBSERVATIONS)]
            (a_x,a_y) = reverse_hash(agent_pos)
            (t_x,t_y) = reverse_hash(target_pos)

            #observation o1
            if(a_x == t_x and a_y == t_y):
                distribution[0] += 1.00
            #observation o2
            elif((a_x + 1) == t_x and a_y == t_y):
                distribution[1] += 1.00
            #observation o3
            elif(a_x == t_x and (a_y + 1) == t_y):
                distribution[2] += 1.00
            #observation o4
            elif(a_x == (t_x + 1) and a_y == t_y):
                distribution[3] += 1.00
            #observation o5
            elif(a_x == t_x and (a_y - 1) == t_y):
                distribution[4] += 1.00
            #observatio o6
            else:
                distribution[5] += 1.00
            observation_table[s][a] = distribution
    return observation_table

''' Generates observation_table such that observation_table[i] gives a 6-tuple giving the probability of observtions in the ith state '''
def generate_observations_alt():
    observation_table = []
    for s in range(TOTAL_NO_OF_STATES):
        distribution = [0.0 for i in range(NO_OF_OBSERVATIONS)]
        agent_pos, target_pos, call = get_state[s]
        (a_x,a_y) = reverse_hash(agent_pos)
        (t_x,t_y) = reverse_hash(target_pos)
        #observation o1
        if(a_x == t_x and a_y == t_y):
            distribution[0] += 1.00
        #observation o2
        elif((a_x + 1) == t_x and a_y == t_y):
            distribution[1] += 1.00
        #observation o3
        elif(a_x == t_x and (a_y + 1) == t_y):
            distribution[2] += 1.00
        #observation o4
        elif(a_x == (t_x + 1) and a_y == t_y):
            distribution[3] += 1.00
        #observation o5
        elif(a_x == t_x and (a_y - 1) == t_y):
            distribution[4] += 1.00
        #observatio o6
        else:
            distribution[5] += 1.00
        observation_table.append(distribution)
    return observation_table


''' function which generates a reward table. For every (s,a,s') where s= start state,a = action and final state = s' return reward'''
def generate_rewards():
    rewards_table = [[[0 for i in range(TOTAL_NO_OF_STATES)] for j in range(len(ACTIONS))] for k in range(TOTAL_NO_OF_STATES)]
    for s in range(TOTAL_NO_OF_STATES):
        for a in range(len(ACTIONS)):
            for z in range(TOTAL_NO_OF_STATES):
                (final_agent,final_target,final_call) = get_state[z]
                if(final_agent == final_target and final_call == 0):
                    (start_agent,start_target,start_call) = get_state[s]
                    if(start_agent == start_target and start_call == 1):
                        rewards_table[s][a][z] = REWARD
                    else:
                        rewards_table[s][a][z] = STEP_COST
                else:
                    rewards_table[s][a][z] = STEP_COST
    return rewards_table

''' Generates rewards with just action and final state as initial state is not required'''
def generate_rewards_alt():
    rewards_table = [[0.0 for a in range(len(ACTIONS))] for s in range(TOTAL_NO_OF_STATES)]
    for s in range(TOTAL_NO_OF_STATES):
        (agent_pos, target_pos, call) = get_state[s]
        for a in range(len(ACTIONS)):
            if ACTIONS[a] != 'STAY':
                rewards_table[s][a] += STEP_COST
            if agent_pos == target_pos and call == 1:
                rewards_table[s][a] += REWARD
    return rewards_table


def generate_start_belief(question=1):
    belief = []
    if question == 1:
        for s in range(TOTAL_NO_OF_STATES):
            (agent_pos, target_pos, call) = get_state[s]
            tx_ty = reverse_hash(target_pos)
            ax_ay = reverse_hash(agent_pos)
            if tx_ty != (0,1):
                belief.append(0.0)
            elif ax_ay in [(0,0), (0,1), (1,1)]:
                belief.append(0.0)
            else:
                belief.append(0.1)
        return belief
    elif question == 2:
        for s in range(TOTAL_NO_OF_STATES):
            (agent_pos, target_pos, call) = get_state[s]
            ax_ay = reverse_hash(agent_pos)
            tx_ty = reverse_hash(target_pos)
            if ax_ay != (1,1) or call != 0:
                belief.append(0.0)
            elif tx_ty not in [(0,1), (1,0), (1,1), (2,1)]:
                belief.append(0.0)
            else:
                belief.append(1/4) 
        return belief
    elif question == 5:
        for s in range(TOTAL_NO_OF_STATES):
            (agent_pos, target_pos, call) = get_state[s]
            ax_ay = reverse_hash(agent_pos)
            tx_ty = reverse_hash(target_pos)
            if (ax_ay not in [(0,0), (3,1)]) or (tx_ty not in [(1,0), (2,0), (1,1), (2,1)]):
                belief.append(0.0)
            elif ax_ay == (0,0):
                belief.append(0.4 * 0.25 * 0.5)
            elif ax_ay == (3,1):
                belief.append(0.6 * 0.25 * 0.5)
        return belief                


''' creates the POMDP file . PIPE the output to the desired file'''
def generate_POMDP_file():
    print("discount : {0}".format(DISCOUNT))
    print("values : reward")
    print("states : {0}".format(TOTAL_NO_OF_STATES))
    print("actions : {0}".format(len(ACTIONS)))
    print("observations : {0}".format(NO_OF_OBSERVATIONS))
    
    #initialisation
    generate()

    #I am skipping the initial belief state for now 
    start_beliefs = generate_start_belief(QUESTION_NUMBER)
    print("start: ", end="")
    for prob in start_beliefs:
        print(prob, end=" ")
    print("")

    #now the transition table
    transition_table = create_transition_table_alt()
    #transition_table = create_transition_table()
    for l in range(len(transition_table)):
        for a in range(len(transition_table[l])):
            print("T : {0} : {1}".format(a,l))
            for r in transition_table[l][a]:
                print(r,end = " ")
            print("")

    '''
    #now the observation table
    observation_table = generate_observations()
    for l in range(len(observation_table)):
        for a in range(len(observation_table[l])):
            print("O : {0} : {1}".format(a,l))
            for r in observation_table[l][a]:
                print(r,end = " ")
            print("")
    '''

    # Alternate method for observation table
    observation_table = generate_observations_alt()
    for s in range(len(observation_table)):
        distribution = observation_table[s]
        print("O: * : {0}".format(s))
        for prob in distribution:
            print(prob, end=" ")
        print("")
    
    '''
    #now the rewards table
    rewards_table = generate_rewards()
    for s in range(len(rewards_table)):
        for a in range(len(rewards_table[l])):
            for z in range(len(rewards_table[l][a])):
                for o in range(NO_OF_OBSERVATIONS):
                    print("R : {0} : {1} : {2} : {3} {4}".format(a,s,z,o,rewards_table[l][a][z]))
    '''

    # Alternate method for rewards table
    rewards_table = generate_rewards_alt()
    for s in range(TOTAL_NO_OF_STATES):
        for a in range(len(ACTIONS)):
            print("R : {0} : * : {1} : * {2}".format(a, s, rewards_table[s][a]))
    

if __name__ == '__main__':
    generate_POMDP_file()