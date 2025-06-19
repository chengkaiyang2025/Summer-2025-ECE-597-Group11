from models.spam_models import PredictLogisticRegression, PredictNaiveBayes

from response_generator import ResponseService, MODEL_LR, MODEL_NB
p1 = PredictLogisticRegression()
p_nb = PredictNaiveBayes()
spam_head_1 = 'UPDATE'
spam_content_1 = 'Notice: 💴💴💴💴 This message was sent from outside the University of Victoria email system. Please be cautious with links and sensitive information.\r\n\r\n\r\nHello\r\n\r\nYour Email account will be Deactivated shortly.\r\nTo stop De-activation CLICK HERE<https://edu-it-helpdesk-sys.weebly.com/> and log in\r\n\r\nThanks\r\n\r\n\r\nIT Help Desk\r\n'


def test_1(p1):
    result = p1.predict_email(spam_content_1,spam_head_1)

    print(result)
def test_nb():
    print("---------")
    result = p_nb.predict_email(spam_content_1,spam_head_1)
    print(result)

    print("---------")
    email_subject = "Important Update"
    email_body = "Click here to verify your account immediately."
    print(p_nb.predict_email(
        email_body,email_subject
    ))
# test_1(p1)
# test_1(p1)

def test_3():
    r1 = ResponseService()
    print(r1.predict(MODEL_LR,spam_head_1,spam_content_1))


    print(r1.predict(MODEL_NB, spam_head_1, spam_content_1))
# test_nb()
test_3()
