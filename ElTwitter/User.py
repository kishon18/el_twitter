from datetime import datetime


class User:
    default_user_id = 0

    def __init__(self, first_name: str, second_name: str, email: str, psw: str):
        self.first_name = first_name.capitalize()
        self.second_name = second_name.capitalize()
        self._email = email
        self._psw = psw

        self.registration_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.nickname = f'@{self.first_name.strip().capitalize()}{self.second_name.strip().capitalize()}'
        self.subscribes = []
        self.followers = []
        self.tweets_id = []

        User.default_user_id += 1
        self.user_id = User.default_user_id

    def __repr__(self):
        return f'{self.nickname}'

    def _edit_user_profile(self, new_name: str, new_second_name: str, new_email: str):
        print(f'| Say BYE to your previous name "{self.first_name} {self.second_name}"')
        self.first_name = new_name
        self.second_name = new_second_name
        self.email = new_email
        self.nickname = f'@{new_name.strip().capitalize()}{new_second_name.strip().capitalize()}'
        print(f'| Now your new name is: "{self.first_name} {self.second_name}"\n'
              f'| Also U have new nickname: {self.nickname}\n'
              f'| And your e-mail: {self.email}\n'
              f'| Your ID still ={self.user_id}=\n')



