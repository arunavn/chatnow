from wtforms import Form, StringField, IntegerField, BooleanField, RadioField, FileField, TextAreaField, PasswordField,validators
from wtforms.fields.html5 import EmailField
from wtforms.fields.html5 import TelField
from chatnow.utilities.auth import user_api_utils
def userid_validation(existence=True):  
    message1= 'User Id does not exists'
    message2= 'User Id already exists'
    def _userid_validation(form, field):
        response= user_api_utils.api_search_user(field.data, token= False)
        userid= []
        if response is not None:
            userid.append(response['userid'])
        if field.data not in userid and existence:
            raise validators.ValidationError(message1)
        elif field.data in userid and not(existence):
            raise validators.ValidationError(message2)

    return _userid_validation

def email_validation(existence= True):
    message1= 'Email id is not registered'
    message2= 'Email id already registered'
    def _email_validation(form, field):
        u= user_api_utils.api_search_user(field.data, 'email', token= False)
        if u is None and existence:
             raise validators.ValidationError(message1)
        elif u is not None and not(existence):
            raise validators.ValidationError(message2)
    return _email_validation

    

def validate_login(form, field):
    message= 'Incorrect password'
    login_status= user_api_utils.api_login(form.userid.data, field.data)
    if not login_status:
        raise validators.ValidationError(message)

def validate_password(form, field):
    if len(field.data) < 3:
        raise validators.ValidationError("Password should be atleast 3 characters long ")

def validate_cnfPassword(form, field):
    if field.data != form.password.data:
        raise validators.ValidationError("Passwords do not match ")
            


class RegisterForm(Form):
    userid= StringField('User Id', [validators.DataRequired(), userid_validation(existence=False)])
    email= EmailField('Email Id', [validators.DataRequired(), email_validation(existence= False)])
    name= StringField('Name', [validators.DataRequired(), validators.length(min=2, max=80, message= "Name length should be between 2 and 80")])
    #password= PasswordField('Password',[validators.DataRequired(), validate_password])
    #cnfPassword= PasswordField('Confirm Password',[validators.DataRequired(), validate_cnfPassword])
    phone= StringField('Phone', [validators.length(min=10, max=10, message= "Phone number should 10 digits long")])
    profilePic= FileField('Profile Picture')
    about= TextAreaField('About')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    def validate_userid(self, field):
        if len(field.data)<3 or len(field.data)>15:
            raise validators.ValidationError("User Id length should be between 3 and 15")
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in field.data:
            if char in excluded_chars:
                raise validators.ValidationError(
                    f"Character {char} is not allowed in username.")
    def validate_email(self, field):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in field.data:
            if char in excluded_chars:
                raise validators.ValidationError(
                    f"Character {char} is not allowed in email.")
    

class LoginForm(Form):
    userid= StringField('User Id', [validators.DataRequired(), userid_validation(existence=True)])
    password= PasswordField('Password', [validators.DataRequired(), validate_login])


class TroubleInLogin(Form):
    email= StringField('Enter Your Email Id', [validators.DataRequired(), email_validation(existence= True)])
    trouble= RadioField('', choices=[('U','Get User Id'),('P','Reset password')], default='U' )


class UpdatePersonalDetails(Form):
    name= StringField('Name', [validators.DataRequired(), validators.length(min=2, max=80, message= "Name length should be between 2 and 80")])
    phone= StringField('Phone', [validators.length(min=10, max=10, message= "Phone number should 10 digits long")])
    about= TextAreaField('About')

class UpdatePassword(Form):
    password= PasswordField('Password',[validators.DataRequired()])
    newpassword= PasswordField('New password',[validators.DataRequired(), validate_password])
    cnfpassword= PasswordField('Confirm password',[validators.DataRequired(), validate_cnfPassword])

class UpdateEmail(Form):
    password= PasswordField('Password',[validators.DataRequired()])
    email= EmailField('Email Id', [validators.DataRequired(), email_validation(existence= False)])
