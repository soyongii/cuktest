from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

#레벤슈타인 계산 함수  
def levenshtein_distance(s1, s2):
    # 긴 문자열이 s1에 오도록 재정렬
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    # s2가 비어 있다면 s1의 길이를 반환
    if len(s2) == 0:
        return len(s1)

    # 행렬을 초기화
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]

        # 삽입, 삭제, 변경 비용을 비교
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 문자를 s1에 삽입
            deletions = current_row[j] + 1       # j 문자를 s1에서 삭제
            substitutions = previous_row[j] + (c1 != c2) # s1의 j 문자를 변경
            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]


# 챗봇 클래스를 정의
class SimpleChatBot:
    # 챗봇 객체를 초기화하는 메서드, 초기화 시에는 입력된 데이터 파일을 로드하고, TfidfVectorizer를 사용해 질문 데이터를 벡터화함
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    # CSV 파일로부터 질문과 답변 데이터를 불러오는 메서드
    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()
        answers = data['A'].tolist()
        return questions, answers

    # 입력 문장에 가장 잘 맞는 답변을 찾는 함수
    def find_best_answer(self, input_sentence):
        # 각 질문과의 레벤슈타인 거리를 계산합니다.
        distances = [levenshtein_distance(input_sentence, question) for question in self.questions]
        # 가장 거리가 짧은 질문을 찾습니다.
        best_match_index = distances.index(min(distances))
        # 해당 질문의 답변을 반환합니다.
        return self.answers[best_match_index]
        

# 데이터 파일의 경로를 지정합니다.
filepath = '/content/drive/MyDrive/ChatbotData.csv'

# 챗봇 객체를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 입력이 나올 때까지 사용자의 입력에 따라 챗봇의 응답을 출력하는 무한 루프를 실행합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)
