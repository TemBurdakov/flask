from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
from langchain_core.messages import SystemMessage, HumanMessage


class Question:
    pass

def open_file(filepath):
    if filepath != "":
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
            print("Проверка1")
            return text


def chat_questions(user_input, chat):
    messages = [SystemMessage(
        content='Ты преподаватель, твоя цель сгенерировать 5 - 6 вопросов по тексту, который ведёт пользователь, так чтобы проверить его знания по этому тексту, например: текст:{Меня зовут Алёна , мне 32 года}, твой вопрос:{Как тебя зовут?}')
        , HumanMessage(content=user_input)]
    res = chat(messages)
    messages.append(res)

    return res.content


def chat_answer(questions, chat):
    messages = [SystemMessage(
        content='Тебе надо сгенерировать ответы на вопросы по тексту, который тебе пришлёт пользователь'),
        HumanMessage(content=questions)]
    res = chat(messages)
    messages.append(res)
    return res.content


def generate_questions(user_input):
    questions = chat_questions(user_input, chat=GigaChat(
        credentials="MDQ0MzhkMTYtZTQ0NS00M2M0LWI5OGItNmRmZDdkYTNkZmFmOjA0MDliNzIzLTU0YjYtNDY3OC1iMjVjLTY4MjczYjExOWU3Yg==",
        verify_ssl_certs=False))
    return questions

def generate_answer(user_input):
    answers = chat_answer(user_input, chat=GigaChat(
        credentials="MDQ0MzhkMTYtZTQ0NS00M2M0LWI5OGItNmRmZDdkYTNkZmFmOjA0MDliNzIzLTU0YjYtNDY3OC1iMjVjLTY4MjczYjExOWU3Yg==",
        verify_ssl_certs=False))
    return answers


'''def get_text_by_url():
    url = url_entry.get()
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    print(root)
    paragraphs = root.find_all('p')
    text_for_viewing = ""
    for p in paragraphs:
        text_for_viewing += p.text
    text_editor.delete("1.0", END)
    text_editor.insert("1.0", text_for_viewing)'''







