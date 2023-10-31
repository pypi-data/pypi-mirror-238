import requests
import time
import threading
from urllib.parse import quote_plus
from tqdm import tqdm


"""
Status reporting of metalake population auto tagging through getting constant updates from DB collection until the request is timied out.
"""

"""
Sending the main request to invokde flask app endpoint and start autotagging on the server side. 
@param url:url which the request is sent : {self.automatic_analysis_url} in automatic_analysis_interface.py
@param payload:payload of the request sent
@param headers: headers of the reqeust sent
""" 
def send_request(url, payload, headers):
    try:
        response = requests.post(url=f"{url}/dataIn", json=payload, headers=headers, timeout=30)
        print(response.json())
    except requests.exceptions.Timeout:
        #print("The request timed out")
        pass
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
"""
Sending and receving the get status reqeust periodically to return the current status reagarding the autotagging process happening 
and reporting status to the SDK terminal
@param url:url which the request is sent : {self.automatic_analysis_url} in automatic_analysis_interface.py
@param unique_id: a unique id generated to identify which autotagging process to refer. 
@param headers: headers of the reqeust sent
""" 
def get_status(url,unique_id,headers):
    flag, print_status_flag, new_bar_flag,endpoint_created= True, True,True,False
    status_message = "Started Autotagging"
    dot_count, page_count,position = 0, 0, 0 
    state_start_end_flags=[[True,True],[True,True],[True,True],[True,True]]
    flag=True
    while flag:
        payload = {
        "unique_id":unique_id,
        "Task" : "auto_tagging"
        }
        response = requests.post(f'{url}/get_status',json=payload,headers=headers)
        document = response.json()['status']
        new_status_message = status_message
        if document=='NotFound':
            new_status_message = status_message
        else:
            if state_start_end_flags[3][0]:
                print("Started Creating Inference EndPoint")
                state_start_end_flags[3][0]=False 
            if len(document['model_name_registered'])==1:
                print("Error occured while creating the inference endpoint")
                print(document['model_name_registered'][0])
                print_status_flag = False
                flag=False
            if len(document['end_point_initialization'])==1:
                new_status_message="Inference EndPoint Creating.. Stay Tuned"    
            if len(document['end_point_initialization'])==2:
                if document['end_point_initialization'][1]=='Ended':
                    if state_start_end_flags[3][1]:
                        print("Inference EndPoint Created!!!")
                        print_status_flag = False
                        state_start_end_flags[3][1]=False
                        endpoint_created=True
                else:
                    print("Error occured while creating the inference endpoint")
                    print(document['end_point_initialization'][1])
                    print_status_flag = False
                    flag=False
            if  len(document['metalake_tagging'])==1:
                if document['page_start']==page_count:
                    if len(document['inferenced_files'])==0:
                        print_status_flag = True
                        new_status_message="page "+str(page_count)+" downloading"
                    else:
                        new_status_message="page "+str(page_count)+" autotagging | stay tuned"
                    #     if position==0:
                    #         if new_bar_flag:
                    #             pbar = tqdm(total=10, desc="Auto Tagging in progress ", ncols=100, unit="item", position=position)
                    #             new_bar_flag=False 
                    #     else:                           
                    #         if new_bar_flag and pbar.n==0:
                    #             pbar = tqdm(total=10, desc="Auto Tagging in progress ", ncols=100, unit="item", position=position)
                    #             new_bar_flag=False
                    #     print_status_flag = False
                    #     new_status_message="page "+str(page_count)+" tags generating"
                    #     if len(document['inferenced_files'])<10:     
                    #         second_len = len(document['inferenced_files'])
                    #         difference=second_len - pbar.n
                    #         pbar.update(difference)
                    #     else:
                    #         second_len = len(document['inferenced_files'])
                    #         difference=second_len - pbar.n
                    #         pbar.update(difference)
                    #         pbar.close()
                    #         new_bar_flag=True
                else:    
                    print(f"page {page_count} autotagging complete!!!")
                    page_count+=1
                    position += 1
            elif len(document['metalake_tagging'])==2:
                print_status_flag = False
                print("")
                print("Successfully Completed the Process \u2714 \u2714 \u2714")
                flag=False
        if new_status_message != status_message:
            status_message = new_status_message
            dot_count = 0
        dots = '.' * (dot_count % 4) 
        padded_message = f'{status_message} {dots}'.ljust(120)
        if print_status_flag:
            print(f'{padded_message}', end='\r', flush=True)
            
        dot_count += 1

        time.sleep(1)
"""
combining about two processes as two threads to run them parallely
@param url:url which the request is sent : {self.automatic_analysis_url} in automatic_analysis_interface.py
@param payload:payload of the request sent
@param headers: headers of the reqeust sent
@param unique_id: a unique id generated to identify which autotagging process to refer. 
"""  
def main_population(url,payload,headers,unique_id): 
    request_thread = threading.Thread(target=send_request, args=(url, payload, headers))
    status_thread = threading.Thread(target=get_status, args=(url,unique_id,headers))
    request_thread.start()
    status_thread.start()

    request_thread.join()
    #print("request thread finished")
    status_thread.join()
    #print("status thread finished")
