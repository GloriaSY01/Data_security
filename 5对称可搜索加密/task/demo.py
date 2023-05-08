import Encrypt

test_strs = [
    'My name is Gloria',
    'Your name is data',
    'I learn 1 subject',]

seed = 1
Encrypt_mg = []  # 邮件信息，以及客户端生成的各种信息，多存了Ci，不用所以没事
Server_mg = []  # 服务端以密文形式存储的邮件[C1,C2,C3,……]
Decrypt_mg = []  # 解密 发回客户端邮件
DES_KEY = "1234567812345678"
HASH_KEY = "12345678"


class Encrypt_W:
    def __init__(self, Ci, Xi, Ki, Si):
        self.Ci = Ci
        self.Xi = Xi
        self.Ki = Ki
        self.Si = Si

    def getCi(self):
        if (self.Ci[0:2] == "0x"):
            return self.Ci[2:]
        return self.Ci

    def getXi(self):
        if (self.Xi[0:2] == '0x'):
            return self.Xi[2:]
        return self.Xi

    def getKi(self):
        if (self.Ki[0:2] == '0x'):
            return self.Ki[2:]
        return self.Ki

    def getSi(self):
        if (self.Si[0:2] == '0x'):
            return self.Si[2:]
        return self.Si

    def ew_print(self):
        print()
        print("[ENCRYPT_W] CI = ", self.Ci)
        print("[ENCRYPT_W] XI = ", self.Xi)
        print("[ENCRYPT_W] KI = ", self.Ki)
        print("[ENCRYPT_W] SI = ", self.Si)

class Server_W:
    def __init__(self, Ci):
        self.Ci = Ci

    def getCi(self):
        if (self.Ci[0:2] == "0x"):
            return self.Ci[2:]
        return self.Ci

    def sw_print(self):
        print("[SERVER_W] CI = ", self.Ci)
        print()

def print_Encrypt_Emails():
    count = 1
    for email in Encrypt_mg:
        print("No. %s  Client_msg" % str(count))
        # print()
        for ew in email:
            ew.ew_print()
        print()
        count += 1


def print_Server_Emails():
    count = 1
    for email in Server_mg:
        # print()
        print("No. %s  Server_msg" % str(count))
        for sw in email:
            sw.sw_print()
        print()
        count += 1


def Encrypt_email(ss):
    Encrypt_email = []
    Server_email = []
    words = Encrypt.split_str(ss)
    for word in words:
        Ci, Xi, Ki, Si = Encrypt.Encrypt_pipeline(word, seed, DES_KEY, HASH_KEY)
        ew = Encrypt_W(Ci, Xi, Ki, Si)
        Encrypt_email.append(ew)  # 加密文件的信息
        se = Server_W(Ci)
        Server_email.append(se)  # 发给客户端存储文件的信息

    Encrypt_mg.append(Encrypt_email)
    Server_mg.append(Server_email)


def Encrypt_emails():
    for email in test_strs:
        Encrypt_email(email)


def Search_msg(ss):
    # 直接检查所有的邮件列表里有没有这个词，有的话把对应位置的Encrypt_word对象取出来
    '''
    其实在这一步应该直接让用户输入对应的CI、XI、KI、SI
    但是就一个简单的demo而言还要用户交互几百个hex不太现实
    不如我直接在所有的已有的email里搜索
    '''
    index_i = -1
    index_j = -1

    for i in range(0, len(test_strs)):
        words = Encrypt.split_str(test_strs[i])
        for j in range(0, len(words)):
            if words[j] == ss:
                index_i = i
                index_j = j
                break
    if index_i == -1 & index_j == -1:
        print("[ERROR] : DO NOT HAVE THIS WORD")
        return None, None

    ee = Encrypt_mg[index_i][index_j]
    correct_emails = []
    for email in Server_mg:
        for sw in email:
            if Encrypt.Search_pipeline(sw.getCi(), ee.getXi(), ee.getKi(), HASH_KEY):
                correct_emails.append(email)

    return correct_emails, ee


def Decrypt_emails(ew):
    mails = []
    for mail in Decrypt_mg:
        temp_mail = []
        for sw in mail:
            temp_mail.append(Encrypt.Decrypt_pipeline(ew.getSi(), sw.getCi(), ew.getKi(), DES_KEY, HASH_KEY))
        mails.append(temp_mail)

    print()
    print("RESULT:")
    for email in mails:
        print("[msg]", end=' ')
        for word in email:
            print(word, end=' ')
        print()


if __name__ == '__main__':
    Encrypt_emails()
    print_Encrypt_Emails()
    print_Server_Emails()
    search_word = "name"
    Searched_emails, ew = Search_msg(search_word)

    if Searched_emails == None:
        print('error search_word')
        exit()

    Decrypt_mg = Searched_emails
    print('Searching', len(Searched_emails), 'eamil containing', search_word)
    Decrypt_emails(ew)


