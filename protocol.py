# REQUEST and RESPONSE TYPE
REG_NICKNAME_TYPE = "REG_NICKNAME"
WAITING_ROOM_TYPE = "WAITING_ROOM"
QUESTION_TYPE = "QUESTION"
ANSWER_TYPE = "ANSWER"
CLOSE_TYPE = "CLOSE"


# RESPONSE DATA
REG_COMPLETE_RESPONSE = "Registration Completed Successfully"
REG_EXIST_RESPONSE = "Existing or Invalid Name! Try Another Name"


# JSON REQUEST
## Register Nickname
# {
#     "protocol": "REQUEST",
#     "type": "REG_NICKNAME",
#     "data": "Viet"
# }
## 

# JSON REG NAME RESPONSE
# {
#     "protocol": "RESPONSE",
#     "type": WAITING_ROOM_TYPE,
#     "data": ['...', '...']
# }

# JSON WAITING ROOM RESPONSE
# {
#     "protocol": "RESPONSE",
#     "type": "REG_NICKNAME",
#     "data": "Registration Completed Successfully"
# }

# JSON QUESTION RESPONSE
# {
#     "protocol": "RESPONSE",
#     "type": "QUESTION",
#     "data": {
#         "nickname": "Viet"
#         "num_players": 10,
#         "current_order": 1,
#         "your_order": 1,
#         "num_questions": 10,
#         "current_question": 0
#         "time": 40,
#         "question": {
#             "question": "What is the capital of France?",
#             "answer": ["Paris", "London", "Rome", "Berlin"],
#             "correct_answer": 0
#         }
#     }
# }