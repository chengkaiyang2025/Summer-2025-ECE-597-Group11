from models.model_loader import p1


def test_1(p1):
    spam_head_1 = 'UPDATE'
    spam_content_1 = 'Notice: 💴💴💴💴 This message was sent from outside the University of Victoria email system. Please be cautious with links and sensitive information.\r\n\r\n\r\nHello\r\n\r\nYour Email account will be Deactivated shortly.\r\nTo stop De-activation CLICK HERE<https://edu-it-helpdesk-sys.weebly.com/> and log in\r\n\r\nThanks\r\n\r\n\r\nIT Help Desk\r\n'
    result = p1.predict_with_logistic_regression(spam_content_1,spam_head_1)

    print(result.conclusion)

test_1(p1)
# test_1(p1)
