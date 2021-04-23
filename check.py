''' code to make the POMDP file for assignment ''' 

NO_OF_AGENT_POSITIONS = 8
NO_OF_TARGET_POSITIONS = 8
NO_OF_CALL_STATES = 2
GRID_HEIGHT = 2
GRID_WIDTH = 4
TOTAL_NO_OF_STATES = NO_OF_AGENT_POSITIONS*NO_OF_TARGET_POSITIONS*NO_OF_CALL_STATES
NO_OF_OBSERVATIONS = 6

ROLL_NUMBER = 2019111020
p_x = 1-(1020%30 + 1)/100

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
    #unsuccesfull
    distribution[hash(x,max(y-1,0))] = 1 - p_x
    #unsuccesfull
    distribution[hash(x,min(y+1,GRID_HEIGHT - 1))] = p_x
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

OBERVATIONS = [i+1 for i in range(NO_OF_OBSERVATIONS)]

''' TRANSITION TABLE CREATION , T[s][a][s'] denotes the probability of reaching state s' after taking action a from current state s '''

''' function to generate the transition table '''
def create_transition_table():
    transition_table = [[[] for i in range(len(ACTIONS))] for i  in range(TOTAL_NO_OF_STATES)]
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


generate()
transition_table = create_transition_table()
for l in range(len(transition_table)):
    for a in range(len(transition_table[l])):
        print("state : {0} ,action : {1} size of distribution : {2} sum : {3}".format(l,a,len(transition_table[l][a]),sum(transition_table[l][a])))
        if(abs(sum(transition_table[l][a]) - 1.00) > 0.00001):
            print("WRONG")
