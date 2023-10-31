import requests
import time
import threading
from urllib.parse import quote_plus
from tqdm import tqdm

"""
Status reporting of collection auto tagging through getting constant updates from DB collection until the request is timied out.
"""

"""
Sending the main request to invokde flask app endpoint and start autotagging on the server side. 
@param url:url which the request is sent : {self.automatic_analysis_url} in automatic_analysis_interface.py
@param payload:payload of the request sent
@param headers: headers of the reqeust sent
""" 
def send_request(url, payload, headers):
    try:
        response = requests.post(url=f"{url}/dataIn_embedding", json=payload, headers=headers, timeout=30)
        #print(response.json())
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
def get_status(url,unique_id,task,headers):
    flag, print_status_flag, initialize_progress_bar, progress_bar_end ,inference_flag, initialize_upload_progress_bar, start_upload = True, True, True, False, True, True, False
    status_message = "Started Embedding Generation"
    dot_count = 0
    state_start_end_flags=[[True,True],[True,True],[True,True],[True,True]]
    while flag:
        payload = {
        "unique_id":unique_id,
        "Task" : task
        }
        response = requests.post(f'{url}/get_status',json=payload,headers=headers)
        document = response.json()['status']
        #print(document)
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
            if len(document['collection_name_registered'])==1:
                print("Error occured while trying to find layernext annotationproject details")
                print(document['collection_name_registered'][0])
                print_status_flag = False
                flag=False
            if len(document['end_point_initialization'])==1:
                new_status_message="Inference EndPoint Creating.. Stay Tuned"    
            if len(document['logs'])==0:
                if len(document['end_point_initialization'])==2:
                    if document['end_point_initialization'][1]=='Ended':
                        if state_start_end_flags[3][1]:
                            print("Inference EndPoint Created!!!")
                            state_start_end_flags[3][1]=False
                        if state_start_end_flags[0][0]:
                            print("Started Downloading the Collection")
                            state_start_end_flags[0][0]=False
                        new_status_message="Downloading the Collection"
                    else:
                        print("Error occured while creating the inference endpoint")
                        print(document['end_point_initialization'][1])
                        print_status_flag = False
                        flag=False
            if len(document['logs'])>0 and inference_flag:
                print_status_flag = False
                if state_start_end_flags[0][1]:
                    print("Collection Download Complete !!!")
                    state_start_end_flags[0][1]=False
                if state_start_end_flags[1][0]:
                    print("Started Embedding Generation Process")
                    state_start_end_flags[1][0]=False
                if document['logs'][0][:4]=='INFO':  
                    if initialize_progress_bar:
                        constraint = document['number_of_files']
                        pbar = tqdm(total=constraint, desc="Embedding Generation in progress ", ncols=100, unit="item") 
                        initialize_progress_bar = False
                    if len(document['inferenced_files'])>0 and not start_upload:
                        if len(document['inferenced_files'])<constraint:     
                            second_len = len(document['inferenced_files'])
                            difference=second_len - pbar.n
                            pbar.update(difference)
                        else:
                            second_len = len(document['inferenced_files'])
                            difference=second_len - pbar.n
                            pbar.update(difference)
                            pbar.close()
                            start_upload=True
                            progress_bar_end=True
                            
            if len(document['predictor_invoke'])==1:
                print("Error occured while invoking inference endpoint")
                print(document['predictor_invoke'][0])
                pbar.close()
                print_status_flag = False
                flag=False
            if len(document['logs'])==2 and progress_bar_end:
                print_status_flag=True
                collection_name = document['collection_name']
                if document['logs'][1][:4]=='INFO':
                    print_status_flag=False
                    new_status_message=""
                    print(f"Completed Embedding Generation for the Collection : {collection_name}")
                    print("Successfully Completed the Process \u2714 \u2714 \u2714")
                    flag=False
                else:  
                    print("Error Occured while Generating Embeddings") 
                    flag=False
            # if len(document['logs'])>2 and progress_bar_end:
            #     if document['logs'][2][:4]=='INFO':
            #         print("Uploading Annotations is Complete!!!")
            #         print("Successfully Completed the Process \u2714 \u2714 \u2714")
            #         operation_id=document["operation_id"]
            #         print('')
            #         print(f"Annotation Operation ID of the process :{operation_id}")
            #         flag=False
            #     else:
            #         print("Error occured while updating Annotations")
            #         flag=False

        if new_status_message != status_message:
            status_message = new_status_message
            dot_count = 0
        dots = '.' * (dot_count % 4) 
        padded_message = f'{status_message} {dots}'.ljust(100)
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
def main_embedding(url,payload,headers,unique_id,task): 
    request_thread = threading.Thread(target=send_request, args=(url, payload, headers))
    status_thread = threading.Thread(target=get_status, args=(url,unique_id,task,headers))
    request_thread.start()
    status_thread.start()

    request_thread.join()
    #print("request thread finished")
    status_thread.join()
    #print("status thread finished")