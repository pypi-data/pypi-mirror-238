import os
import nbformat
import requests
import json


def get_ipynb_directory_and_index():
    current_directory = os.getcwd()
    notebook_files = [file for file in os.listdir(current_directory) if file.endswith('.ipynb')]
    matching_cell_index = None
    current_input = In[-1]
    for notebook_file in notebook_files:
        with open(os.path.join(current_directory, notebook_file), 'r', encoding='utf-8') as file:
            try:
                notebook_content = nbformat.read(file, as_version=4)
                for idx, cell in enumerate(notebook_content.cells):
                    now_ipynb_file=notebook_file
                    if cell.cell_type == 'code' and cell.source.strip() == current_input.strip():
                        matching_cell_index = idx
                        
                        break
            except Exception as e:
                # print(f"Error reading {notebook_file}: {e}")
                continue
        if matching_cell_index is not None:
            break
            
    return (current_directory+"\\"+now_ipynb_file, matching_cell_index)

# print(get_ipynb_directory_and_index())


# n 번째 셀의 입력과 출력을 반환

def extract_cell(notebook_path,target_cell_index):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = f.read()
    notebook = nbformat.reads(notebook_content, as_version=4)

    second_cell_input = None
    second_cell_output = None
    target_cell_index =target_cell_index
    if len(notebook.cells) >= 2 and notebook.cells[target_cell_index].cell_type == 'code':
        second_cell_input = notebook.cells[target_cell_index].source
        second_cell_output = notebook.cells[target_cell_index].outputs

    return {'input': second_cell_input, 'output': second_cell_output}

####### 삽입
import mysql.connector
import json

def get_before_sell_data():
    data = get_ipynb_directory_and_index()
    path, index = data[0],data[1]
    cell_data = extract_cell(path, index-1)
    return cell_data

def call_api(endpoint,data):
    url = f"http://localhost:8000/{endpoint}"
    response = requests.post(url, json=data)
    # 응답 확인
    if response.status_code == 200:
        # 성공적으로 요청이 처리됨
        response_data = response.json()
        print(f"Response from server/{endpoint}:", response_data)
    else:
        # 요청이 실패한 경우 오류 코드 출력
        print(f"Request failed with status code/{endpoint}:", response.status_code)

def professor_sign_in(name, university, pwd, ph_num, e_mail, ip):
    data_to_send = {
    "NAME": f"{name}",
    "UNIVERSITY": f"{university}",
    "PWD" : f"{pwd}",
    "PHONE_NUM" : f"{ph_num}",
    "E_MAIL" : f"{e_mail}",
    "IP" : f"{ip}"     
    }
    call_api('pro_sign_in',data_to_send)


def send(pro_id, stu_name): #교수 id와 학생 이름만 입력하도록
    data_to_send = {
        "PRO_NO" : f"{pro_id}",
        "STU_NAME" : f"{stu_name}", 
    }
    cd = get_before_sell_data() # 셀데이터 추가
    data_to_send.update(cd)
    call_api('inNout', data_to_send)

def pro_sing_in():
    print("todo")


def q_db(stu_name): # 보류
    result = {}
    data = get_before_sell_data()
    input = data['input']
    output = json.dumps(data['output'])  # 출력을 JSON 형태로 변환
    
    # 연결 정보 설정
    host = "34.64.61.73"
    user = "jeong"
    password = "wjdghdus1!"
    database = "main"
    connection = None  # connection 객체를 미리 정의

    try:
        # MySQL 데이터베이스에 연결
        connection = mysql.connector.connect(host=host, user=user, database=database, password=password)
        
        if connection.is_connected():
            cursor = connection.cursor()

            # 새로운 레코드 추가
            query = "INSERT INTO pro1 (stu_name, input, `output`) VALUES (%s, %s, %s)"
            values = (stu_name, input, output)
            cursor.execute(query, values)

            connection.commit()  # 변경사항을 커밋하여 데이터베이스에 반영
            
            result['success'] = "레코드가 성공적으로 추가되었습니다."
            
    except mysql.connector.Error as error:
        result['err'] = ("오류 발생:", error)
        
    finally:
        # 연결 닫기 (오류 발생 여부와 상관없이 항상 연결을 닫아야 합니다.)
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
            result['result'] = "MySQL 연결이 닫혔습니다."
        return result
# q_db(stu_name='jhy')
