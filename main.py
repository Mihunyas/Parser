import requests
import time
import json
from tqdm import tqdm

quest_url = "https://api.stackexchange.com/2.3/questions"
ans_url = "https://api.stackexchange.com/2.3/questions/{question_id}/answers"

def fetch_stackexchange_questions(site = "stackoverflow", page = 1, pagesize = 100):
    params = {
        "order" : "desc",
        "sort" : "activity",
        "site" : site,
        "pagesize" : pagesize,
        "page" : page,
        "filter" : "withbody"
    }
    response = requests.get(quest_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Я ошибся{response.status_code}")
        return None
    
def fetch_answer_for_question(question_id, site = "stackoverflow"):
    params = {
        "order" : "desc",
        "sort" : "activity",
        "site" : site,
        "filter" : "withbody"
    }
    response = requests.get(ans_url.format(question_id=question_id), params=params)
    if response.status_code == 200:
        return response.json
    else:
        print(f"Я ошибся {question_id} : {response.status_code}")
        return None
    
def parse_qustions_with_answer(data, site = "stackoverflow"):
    parsed_data = []
    if "items" in data:
        for item in tqdm(data["items"], desc="Parsing qustions and answer"):
            qustion = {
                "qustion_id" : item.get("qustion_id"),
                "title" : item.get("title"),
                "body" : item.get("body"),
                "tags" : item.get("tags"),
                "link" : item.get("link"),
                "creation_date" : time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(item.get("creation_date"))),
                "score" : item.get("score"),
                "answer" : []
            }
        answers_data = fetch_answer_for_question(item.get("qustion_id"), site)
        if answers_data and "items" in answers_data:
            for answer in answers_data["items"]:
                answer_info = {
                    "answer_id" : answer.get("answer_id"),
                    "body" : answer.get("body"),
                    "creation_date" : time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(answer.get("creation_date"))),
                    "score" : answer.get("score"),
                    "is_accepted" : answer.get("is_accepted")                                      
                }
                qustion["answers"].append(answer_info)
        parsed_data.append(qustion)
    return parsed_data

def save_to_json(data, filename="stackexchange_data_with_answer.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Данные сохранены в {filename}")

if __name__ == "__main__":
    site = "stackoverflow"
    page = 1
    pagesize = 100
    questions_data = fetch_stackexchange_questions(site=site, page=page, pagesize=pagesize)
    if questions_data:
        parsed_qustions = parse_qustions_with_answer(questions_data, site)
        save_to_json(parsed_qustions), f"{site}_qustions_with_answer.json"
