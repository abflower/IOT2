from datetime import *
from time import *
import json
import matplotlib.pyplot as plt
import requests
import time


# global variables

time_stamp = ''

curr_temp = 0.0
curr_humidity = 0

t_last_update = ''
h_last_update = ''

t_xs = []
t_ys = []

h_xs = []
h_ys = []


def gather_temp_humidity():
    # send request for temperature
    url = "http://192.168.0.25/temp"
    global curr_temp
    call = requests.get(url)

    # check that the status of the reponse is 200
    if '200' in str(call):
        curr_temp = float(call.content)

    else:
        curr_temp = None

    # send request for humidity
    url = "http://192.168.0.25/humidity"
    global curr_humidity
    call = requests.get(url)

    # check that the status of the reponse is 200
    if '200' in str(call):
        curr_humidity = int(requests.get(url).content)
    else:
        curr_humidity = None



def temp_check(check, t, arg2, function_name):
    if check == True:
        # check if the value of curr_temp is None, if so switches off
        if curr_temp == None:
            return function_mappings[function_name](False)

        # perform temperature check
        if curr_temp < float(t):
            print('temp check: Temp low')
            return function_mappings[function_name](True)
        if curr_temp >= float(t):
            print('temp check: Temp high')
            return function_mappings[function_name](False)
    else:
        return function_mappings[function_name](False)






def IFTTT(status):
    key = 'jTiMhMolHFo2ykbq64cxsbMi9rDDKGpvm0X80x-qloL'
    msg =''
    if status == True:
        msg = "low_temp"
        if events_list.get(name) == 0:
            del events_list[name]
            events_list[name] = 1
    if status == False:
        msg = "temp_ok"
        if events_list.get(name) == 1:
            del events_list[name]
            events_list[name] = 0
    print('IFTTT: ',msg)
    url = "https://maker.ifttt.com/trigger/%s/with/key/%s" % (msg, key)
    requests.post(url)


# this maps string to names of the corresponding function so that they can be called

function_mappings = {'temp_check': temp_check, 'IFTTT':IFTTT}


def check_time_and_execute(name, days, ora_ON, ora_OFF, function_name, arg1, arg2, function2_name):
    print(name, days, ora_ON, ora_OFF, function_name, arg1, arg2, function2_name)
    weekday = datetime.today().weekday()
    if str(weekday) in days:
        print('weekday test passed')
        now = strftime("%H:%M:%S")
        global time_stamp
        time_stamp = now
        now = datetime.strptime(now, "%H:%M:%S").time()
        if ora_ON < now < ora_OFF:
            if events_list.get(name) == 0:
                #del events_list[name]
                #print(events_list)
                #events_list[name] = 1
                #print(events_list)
                print('time test passed')
                return function_mappings[function_name](True, arg1, arg2, function2_name)
            else:
                pass

        else:
            print('time test not passed')
            if events_list.get(name) == 1:
                del events_list[name]
                #print(events_list)
                events_list[name] = 0
                #print(events_list)
                return function_mappings[function_name](False, arg1, arg2, function2_name)
            else:
                pass
    else:
        print('weekday test not passed')
        if events_list.get(name) == 1:
            del events_list[name]
            #print(events_list)
            events_list[name] = 0
            #print(events_list)
            return function_mappings[function_name](False, arg1, arg2, function2_name)
        else:
            pass



def decode_json_execute(e):
    global name
    name = e['name']
    days = e['days']
    ora_ON = e['time1']
    ora_ON = datetime.strptime(ora_ON, "%H:%M:%S").time()
    ora_OFF = e['time2']
    ora_OFF = datetime.strptime(ora_OFF, "%H:%M:%S").time()
    par1 = e['par1']
    par2 = e['par2']
    function = e['function']
    function2 = e['function2']
    check_time_and_execute(name, days, ora_ON, ora_OFF, function, par1, par2, function2)




# functions for the creation of graphs

def t_add_and_graph(value):

    global t_xs
    global t_ys

    # Add x and y to lists

    t_xs.append(datetime.now().strftime('%H:%M'))
    t_ys.append(value)

    # Limit x and y lists to 20 items
    t_xs = t_xs[-48:]
    t_ys = t_ys[-48:]



def t_draw(title):
    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # Draw plot
    ax.plot(t_xs, t_ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title(title)
    # plt.ylabel('Temperature (deg C)')

    # Draw the graph

    name = './static/images/' + title + '.png'
    plt.savefig(name, bbox_inches='tight')


def t_collect_graph_data(value, title):

    # check time from last addition

    now = time.time()

    global t_last_update

    if t_last_update == '':
        t_last_update = now
        t_add_and_graph(value)
        t_draw(title)

    elif (now - t_last_update) >= 1800:
        t_last_update = now
        t_add_and_graph(value)
        t_draw(title)
    else:
        pass



# humidity graph


def h_add_and_graph(value):

    global h_xs
    global h_ys

    # Add x and y to lists

    h_xs.append(datetime.now().strftime('%H:%M'))
    h_ys.append(value)

    # Limit x and y lists to 20 items
    h_xs = h_xs[-48:]
    h_ys = h_ys[-48:]



def h_draw(title):
    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # Draw plot
    ax.plot(h_xs, h_ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title(title)
    # plt.ylabel('Temperature (deg C)')

    # Draw the graph

    name = './static/images/'+title+'.png'
    plt.savefig(name, bbox_inches='tight')


def h_collect_graph_data(value, title):

    # check time from last addition

    now = time.time()

    global h_last_update

    if h_last_update == '':
        h_last_update = now
        h_add_and_graph(value)
        h_draw(title)

    elif (now - h_last_update) >= 1800:
        h_last_update = now
        h_add_and_graph(value)
        h_draw(title)
    else:
        pass

# ----- main body --------

with open('./files/auto_settings.json', 'r') as f:


        events_list = {}

        data = json.load(f)


        for e in data["events"]:
            events_list[e['name']] = 0

        while True:

            with open('./files/datatrasf.json', 'w') as trans:

                data_trans = {}
                gather_temp_humidity()

                data_trans["sensor"] = {"temp": curr_temp, "hum": curr_humidity}
                data_trans_event = []

                for e in data["events"]:
                    name = ''
                    decode_json_execute(e)
                    print('- - - - - -')
                for event in events_list:
                    if events_list[event] == 1:
                        data_trans_event.append(event)
                data_trans["automations"] = data_trans_event
                data_trans["check"] = time_stamp
                print(data_trans)
                json.dump(data_trans, trans)
                #t_collect_graph_data(curr_temp, 'Temperature')
                #h_collect_graph_data(curr_humidity, 'Humidity')
                trans.close()
                #print(events_list)
                print('++++++++++\n')



            time.sleep(300)

