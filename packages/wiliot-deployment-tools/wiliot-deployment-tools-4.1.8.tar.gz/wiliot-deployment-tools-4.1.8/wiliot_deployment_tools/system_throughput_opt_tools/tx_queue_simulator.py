import random
from collections import deque
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

# repetition algo global vars:
last_rep_check_for_inc_time_ms = 0
last_rep_check_for_dec_time_ms = 0
last_lower_ss_cross_time_ms = 0
last_change_dir = 'dec'
rep_dec_step_cnt = 1
rep_inc_step_cnt = 1
low_traffic_duration_ms = 300000 #5 min

# PacerInterval global vars:
last_pi_check_for_inc_time_ms = 0
last_pi_check_for_dec_time_ms = 0
pi0_first_call = 1

def new_pi_algo(TxRepetitions,queue_size, queue_limit,PacerInterval,InternalPacerInterval,curr_time_ms,pi_inc_window_rxtx,pi_dec_window_sec):
    '''
    this algo is tcp based:
    Increase: every X cycles
    Decrease: every cycle
    Addaptive ss_th
    '''
    tx_q_upper_th = round(queue_limit * (2/3))
    tx_q_lower_th = round(queue_limit / 3)
    global last_pi_check_for_inc_time_ms
    global last_pi_check_for_dec_time_ms
    global pi0_first_call
    if pi0_first_call and PacerInterval == 0:
        pi0_first_call = 0
        return 50
    #reset time count if th is crossed
    if queue_size > tx_q_lower_th:
        last_pi_check_for_dec_time_ms = curr_time_ms
    if queue_size < tx_q_upper_th:
        last_pi_check_for_inc_time_ms = curr_time_ms

    if queue_size > tx_q_upper_th and (curr_time_ms - last_pi_check_for_inc_time_ms) > pi_inc_window_rxtx*RxTxPeriodMs and TxRepetitions==1:
        last_pi_check_for_inc_time_ms = curr_time_ms
        return InternalPacerInterval + 1
    if queue_size < tx_q_lower_th and (curr_time_ms - last_pi_check_for_dec_time_ms) > pi_dec_window_sec*1000:
        last_pi_check_for_dec_time_ms = curr_time_ms
        if PacerInterval == 0:
            PacerInterval = 1
        return max(InternalPacerInterval - 1,PacerInterval)
    else:
        return InternalPacerInterval

def new_rep0_algo(TxRepetitions,queue_size, queue_limit,RxTxPeriodMs,rep_change_window_rxtx,curr_time_ms,queue_limit_top):
    '''
    this algo is tcp based:
    Increase: every X cycles
    Decrease: every cycle
    Addaptive ss_th
    '''
    tx_q_upper_th = round(queue_limit * (2/3))
    tx_q_lower_th = round(queue_limit / 3)

    global last_rep_check_for_inc_time_ms
    global last_rep_check_for_dec_time_ms
    global last_lower_ss_cross_time_ms
    global last_change_dir
    global rep_dec_step_cnt
    global rep_inc_step_cnt
    global low_traffic_duration_ms

    if queue_size >= tx_q_lower_th:
        last_rep_check_for_inc_time_ms = curr_time_ms
    if queue_size <= tx_q_upper_th:
        last_rep_check_for_dec_time_ms = curr_time_ms    
    '''
    handle tags amount changing by setting defults value to weights:
    queue_size > 100 is for *overflow*
    (curr_time_ms - last_lower_ss_cross_time_ms) > low_traffic_duration if for *underflow*
    reset last_lower_ss_cross_time_ms every time that queue_size > tx_q_lower_th
    '''
    if queue_size > queue_limit_top or (curr_time_ms - last_lower_ss_cross_time_ms) > low_traffic_duration_ms:
        rep_dec_step_cnt = 1
        rep_inc_step_cnt = 1
        if queue_size > queue_limit_top: #tx queue overflow 
            return 1
        else:
            last_lower_ss_cross_time_ms = curr_time_ms #undeflow
            return TxRepetitions + 1    
    if queue_size > tx_q_lower_th:
        last_lower_ss_cross_time_ms = curr_time_ms
    
    # set weight to 1 for first decrease in current direction
    if last_change_dir == 'inc': 
        rep_dec_step_cnt_curr = 1
    else:
        rep_dec_step_cnt_curr = rep_dec_step_cnt
    # set weight to 1 for first increase in current direction
    if last_change_dir == 'dec':
        rep_inc_step_cnt_curr = 1
    else:
        rep_inc_step_cnt_curr = rep_inc_step_cnt

    # check if need to decrease repetition:
    if queue_size > tx_q_upper_th and (curr_time_ms - last_rep_check_for_dec_time_ms) > rep_change_window_rxtx*RxTxPeriodMs*rep_dec_step_cnt_curr:
        if last_change_dir == 'inc': #first decrease - raise the timer for next decrease
            rep_dec_step_cnt = rep_dec_step_cnt
        else:
            rep_dec_step_cnt = min(rep_dec_step_cnt + 1,30)
        last_rep_check_for_dec_time_ms = curr_time_ms
        last_change_dir = 'dec'
        return [max(1,TxRepetitions - 1),rep_inc_step_cnt_curr,rep_dec_step_cnt_curr]
    
    # check if need to increase repetition:    
    if queue_size < tx_q_lower_th and (curr_time_ms - last_rep_check_for_inc_time_ms) > rep_change_window_rxtx*rep_inc_step_cnt_curr*RxTxPeriodMs:
        if last_change_dir == 'dec': #first decrease - raise the timer for next decrease
            rep_inc_step_cnt = rep_inc_step_cnt
        else:
            rep_inc_step_cnt = min(rep_inc_step_cnt+1,30)
        last_rep_check_for_inc_time_ms = curr_time_ms
        last_change_dir = 'inc'
        return [min(TxRepetitions + 1,5),rep_inc_step_cnt_curr,rep_dec_step_cnt_curr]
    else:
        return [TxRepetitions,rep_inc_step_cnt_curr,rep_dec_step_cnt_curr]


def current_rep0_algo(TxRepetitions,NumOfTags,RxTxPeriodMs,PacerInterval,queue_size, queue_limit):
    tx_slots_per_sec = 1000 / RxTxPeriodMs
    tx_demand_per_sec = NumOfTags / PacerInterval
    threshold_value = (TxRepetitions * NumOfTags * 2 * RxTxPeriodMs) / 1000
    if (tx_slots_per_sec / 2) < tx_demand_per_sec or queue_size >= (queue_limit / 2):
         return 1 # minimum value
    if ((tx_slots_per_sec / 2) > tx_demand_per_sec * 2):
        return 3 # maximum value
    else:
        return 2 #mid value
    
def tx_queue_simulator(NumOfTags, PacerInterval, RxTxPeriodMs, TxRepetitions, 
                      max_cycle_rate, TTFP,SimDurPI,queue_limit,queue_limit_top,rand_change_tag_num = False,
                      new_rep0_algo_enable=False,old_rep0_algo_enable=False,new_pi_algo_enable=False,
                      rep_change_window_rxtx=60,pi_inc_window_rxtx=2,pi_dec_window_sec=30,tags_pace = 0.5,is_production_line_sim = False):
    tx_queue = deque()  # Initialize the queue
    queue_size_vec = []  
    lost_packets_graph = []
    tags_amount_graph = []
    repetitions_graph = []
    pacerinterval_graph = []
    lost_packets_cnt = 0
    sent_packets_cnt = 0
    time_ms = 0  # Time counter
    time_sec = 0
    orig_NumOfTags = NumOfTags
    InternalPacerInterval = PacerInterval
    start_times = [random.uniform(3, 2*TTFP) for _ in range(NumOfTags)]  # Random start times for each client
    rand_time_vec = [random.uniform(0.01,max_cycle_rate) for _ in range(NumOfTags* 100)]
    random_tags_addition = [round(random.uniform(-5,5)) for _ in range(SimDurPI*1000*PacerInterval+1)]
    counters = [0] * NumOfTags
    inc_weight_graph = []
    dec_weight_graph = []
    inc_weight = 1
    dec_weight = 1
    counter_ms = 0 #for production line simulation only
    if is_production_line_sim:
        NumOfTags = 0
    while True:
        if new_pi_algo_enable:
            InternalPacerInterval = new_pi_algo(TxRepetitions,len(tx_queue), queue_limit,PacerInterval,InternalPacerInterval,time_ms,pi_inc_window_rxtx,pi_dec_window_sec)
        #add HB every 30 seconds:
        if time_sec % 30 == 0 and time_ms % 1000 == 0 and len(tx_queue) < queue_limit_top:
            tx_queue.appendleft(['mgmt',6])
            sent_packets_cnt += 1
        #add 2 CFG evert 60 seconds
        if time_sec % 60 == 0 and time_ms % 1000 == 0 and len(tx_queue) < queue_limit_top:
            tx_queue.appendleft(['cfg',6])
            tx_queue.appendleft(['cfg',6])
            sent_packets_cnt += 2
        #add new packet to tx_queue if received  
        if is_production_line_sim:
                if counter_ms >= 1000*tags_pace:
                    counter_ms = 0
                    # Add new messages to the tx_queue for the client
                    if len(tx_queue) < queue_limit - 2:
                        tx_queue.append(['tag', -1])
                        start_times.append(time_sec)
                        NumOfTags +=1
                        sent_packets_cnt += 1
                    else:
                        lost_packets_cnt = lost_packets_cnt + 1
                counter_ms += 1
        else: #non production line sim case  
            for tag in range(NumOfTags):
                #randome packet receiving time 
                rand_time = rand_time_vec[(tag+1) % (orig_NumOfTags*100) -1]
                rand_time_to_rec = 1000 * InternalPacerInterval + 10000 * rand_time
                if time_sec >= start_times[tag] and counters[tag] >= rand_time_to_rec:
                    counters[tag] = 0
                    # add new packet to the tx_queue for the tag
                    if len(tx_queue) < queue_limit_top - 2:
                        tx_queue.append(['tag', -1])
                        sent_packets_cnt += 1
                    else:
                        lost_packets_cnt = lost_packets_cnt + 1
                counters[tag] += 1
        
        if time_ms % RxTxPeriodMs == 0:
            # sample values for graph creating
            queue_size_vec.append(len(tx_queue))
            lost_packets_graph.append(lost_packets_cnt)
            tags_amount_graph.append(NumOfTags)
            repetitions_graph.append(TxRepetitions)
            inc_weight_graph.append(inc_weight)
            dec_weight_graph.append(dec_weight)
            pacerinterval_graph.append(InternalPacerInterval)           
            #calculate repetition:
            if old_rep0_algo_enable:
                TxRepetitions = current_rep0_algo(TxRepetitions,NumOfTags,RxTxPeriodMs,PacerInterval,len(tx_queue), queue_limit)
            if new_rep0_algo_enable and PacerInterval == InternalPacerInterval:
                new_rep0_algo_res = new_rep0_algo(TxRepetitions,len(tx_queue), queue_limit,RxTxPeriodMs,rep_change_window_rxtx,time_ms,queue_limit_top)
                TxRepetitions = new_rep0_algo_res[0]
                inc_weight = new_rep0_algo_res[1]
                dec_weight = new_rep0_algo_res[2]
            #update repetition for packet:
            if len(tx_queue) > 0:
                msg_curr = tx_queue.popleft()
                curr_tag_repetition = msg_curr[1]
                if msg_curr[0] != 'tag':
                    if not curr_tag_repetition:
                        tx_queue.appendleft([msg_curr[0],curr_tag_repetition - 1])
                else:
                    if curr_tag_repetition == -1: #first rxtxperiod for current packet 
                        tx_queue.appendleft(['tag',TxRepetitions*2 - 1])
                    elif curr_tag_repetition > 0:
                        tx_queue.appendleft(['tag',curr_tag_repetition-1])

        if rand_change_tag_num or is_production_line_sim:
            # handle aging
            for tag in range(NumOfTags):
                if time_sec - start_times[tag] > InternalPacerInterval+100:
                    if not is_production_line_sim:
                        del counters[tag]
                    del start_times[tag]
                    NumOfTags -= 1 
                    break
            if not is_production_line_sim:
                # random add or remove tags in random time periods
                if time_sec > 1.5*InternalPacerInterval and time_ms % (1000 * (1+abs(random_tags_addition[time_sec]))) == 0:
                    tags_change = random_tags_addition[time_sec]
                    if tags_change > 0 and NumOfTags > 3 * orig_NumOfTags:
                        tags_change = tags_change * -1
                    if tags_change < 0 and NumOfTags > -1 * tags_change:
                        for tag in range(-1 * tags_change):
                            NumOfTags = NumOfTags - 1
                            del counters[NumOfTags]
                            del start_times[NumOfTags]
                    if tags_change > 0:
                        for tag in range(tags_change):
                            NumOfTags = NumOfTags + 1
                            counters.append(0)
                            start_times.append(time_sec)
        
        if time_sec > SimDurPI * InternalPacerInterval: # Exit the loop after SimDurPI PIs 
            break       

        time_ms += 1  # add 1 ms
        if time_ms % 1000 == 0 and time_ms:
            time_sec += 1

    return [queue_size_vec,lost_packets_graph,repetitions_graph,pacerinterval_graph,tags_amount_graph,inc_weight_graph,dec_weight_graph]
'''
For production line case configure just the folowing:
PacerInterval, RxTxPeriodMs, TxRepetitions, tags_pace, SimDurPI, queue_limit,queue_limit_top
'''
PacerInterval = 1 # Pacing interval (in seconds)
RxTxPeriodMs = 150  # Rx/Tx period (in ms)
TxRepetitions = 1  # Number of repetitions for every message
tags_pace = 0.5 # for productionline simulation only
SimDurPI = 180  # Simulation duration in PacerIntervals
queue_limit = 60  # Effective q limit
queue_limit_top = 100 # actual q limit

NumOfTags = 45  # Number of clients
max_cycle_rate = 1.25  # Rate at which the cycle varies (larger values mean more variation)
TTFP = 10  # Time to first packet (larger values mean larger delays before clients start adding messages)
pi_dec_window_sec = 10 # time period (in sec) that the q zise must be below lower_th to increse rep by 1
pi_inc_window_rxtx = 10 # time period (in rxtxperiod) that must pass between decresing rep by 1
rep_change_window_rxtx = 30 # time period (in rxtxperiod) that the q zise must be below lower_th to increse rep by 1

rand_change_tags_amount = False
new_rep0_algo_enable    = True
old_rep0_algo_enable    = False
new_pi_algo_enable      = False

is_production_line_sim = True

tx_queue_simulator_res = tx_queue_simulator(NumOfTags, PacerInterval, RxTxPeriodMs, TxRepetitions,
                                                max_cycle_rate, TTFP, SimDurPI, queue_limit,queue_limit_top,rand_change_tags_amount,
                                                new_rep0_algo_enable,old_rep0_algo_enable,new_pi_algo_enable,
                                                rep_change_window_rxtx,pi_inc_window_rxtx,pi_dec_window_sec,tags_pace,is_production_line_sim)

# Extract the results for plotting
queue_size_graph              = tx_queue_simulator_res[0]
lost_packets_graph            = tx_queue_simulator_res[1]
repetitions_graph             = tx_queue_simulator_res[2]
pacerinterval_graph           = tx_queue_simulator_res[3]
tags_amount_graph             = tx_queue_simulator_res[4]
inc_weight_graph              = tx_queue_simulator_res[5]
dec_weight_graph              = tx_queue_simulator_res[6]
tx_q_upper_th = round(queue_limit * (2/3))
tx_q_lower_th = round(queue_limit / 3)

# Customizing the x-axis tick labels to show time in seconds
def format_time(x, pos):
    return f'{round((x*RxTxPeriodMs) / 1000):.1f}'
    
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(queue_size_graph, label=f'current queue size')
ax.plot(lost_packets_graph, label=f'total lost packets')
ax.plot(repetitions_graph, label=f'repetitions')
if new_pi_algo:
    ax.plot(pacerinterval_graph,label=f'PacerInterval')
ax.axhline(tx_q_upper_th, color='red', linestyle='--', label=f'upper queue size th')
ax.axhline(tx_q_lower_th, color='red', linestyle='--', label=f'lower queue size th')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
ax.set_xlabel('Time [Sec]')
ax.set_ylabel('Number of Packets in Queue')
ax.set_title(f'TX Queue Size With New Rep0 algorithm')
ax.legend()

fig, ay = plt.subplots(figsize=(10, 6))
ay.plot(repetitions_graph, label=f'Repetitions')
ay.plot(pacerinterval_graph, label=f'PacerInterval')
ay.plot(tags_amount_graph, label=f'NumOfTags')
ay.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
ay.set_xlabel('Time [Sec]')
ay.legend()
if not is_production_line_sim and new_rep0_algo_enable:
    fig, az = plt.subplots(figsize=(10, 6))
    az.set_title(f'Repetitions value With New Rep0 algorithm')
    az.plot(repetitions_graph, label=f'Repetitions')
    az.plot(inc_weight_graph,color='green', label=f'Increasing adaptive weight')
    az.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
    az.set_xlabel('Time [Sec]')
    az.legend()

    fig, bx = plt.subplots(figsize=(10, 6))
    bx.set_title(f'Repetitions value With New Rep0 algorithm')
    bx.plot(repetitions_graph, label=f'Repetitions')
    bx.plot(dec_weight_graph,color='red', label=f'Decreasing adaptive weight')
    bx.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
    bx.set_xlabel('Time [Sec]')
    bx.legend()


plt.grid(True)
plt.tight_layout()
plt.show()