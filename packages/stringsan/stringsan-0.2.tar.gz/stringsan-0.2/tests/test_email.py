from stringsan.email import is_email, domainname, username

VALID_EMAIL = "ilikemails@email.gg"
INVALID_EMAIL = "idontlikemails$iprefercalls.com"

def test_is_email():
    assert is_email(VALID_EMAIL) == True 
    assert is_email(INVALID_EMAIL) == False 

def test_username():
    assert username(VALID_EMAIL) == "ilikemails"
    assert username(INVALID_EMAIL) == None 

def test_domainname():
    assert domainname(VALID_EMAIL) == "email.gg"
    assert domainname(INVALID_EMAIL) == None
