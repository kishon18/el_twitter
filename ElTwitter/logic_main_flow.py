import sys
import TwitterSystem
from art import tprint
from logic_registration_and_login import field_cant_be_blank, registration_nickname, registration_email, \
    registration_psw
from TwitterSystem import create_user, wtf_massage, NoUsersError, AuthenticationError, login
from colorama import Fore
from User import *

##############################################
# Creating User

# stepan_user = User(first_name='Stepan', second_name='Bandera', email='a', psw='a')
# create_user(stepan_user)
#
# peter_crouch = User(first_name='Peter', second_name='Crouch', email='qwe', psw='qwe')
# create_user(peter_crouch)


##############################################

def begin_program_flow():
    while True:
        begin = input(
            '- CREATE ACCOUNT (input: "crACC")\n'
            '- LOGIN ACCOUNT (input: "login")\n'
            '- QUIT (input "Q")\n'
            'Input command: '
        )

        match begin.strip().upper():
            case 'CRACC':
                result_nickname = registration_nickname()
                user_instance = User(
                    first_name=result_nickname[0],
                    second_name=result_nickname[1],
                    email=registration_email(),
                    psw=registration_psw()
                )

                create_user(user=user_instance)

            case 'LOGIN':
                do_login()

            case 'Q':
                print(Fore.LIGHTYELLOW_EX + f'\n{" EL TWITTER ":=^25}')
                print('| Bye, see U next time\n')
                tprint('EL TWITTER', font='bulbhead')
                break

            case _:
                print(Fore.RED + f'\n{wtf_massage:=^25}')
                print('| Incorrect command, try one more time\n')


def do_login():
    while True:
        email = field_cant_be_blank(input('Input your e-mail: '))
        psw = input('Input your password: ')

        try:
            login(
                email=email,
                password=psw
            )
            break
        except NoUsersError:
            print(Fore.RED + f'\n{wtf_massage:=^25}')
            print("| DB is empty")
            return
        except AuthenticationError:
            print(Fore.RED + f'\n{wtf_massage:=^25}')
            print("| Wrong email or password\n")

    main_flow_from_console()


########################################################################################


# ______________________________________ Validation _________________________________

# main flow
def try_parse_int(val) -> (bool, int):
    try:
        return True, int(val)
    except:
        return False, None


# checking for INT type of input data
def check_int_type(tweet_id_str):
    ok, tweet_id = try_parse_int(tweet_id_str)
    if not ok:
        print(Fore.RED + f'\n{TwitterSystem.wtf_massage:=^25}')
        print("| Please enter valid INT as tweet id\n")
        return main_flow_from_console()
    else:
        return tweet_id


# ____________________________________ Main flow _______________________________________

def main_flow_from_console():
    while True:
        main_command = field_cant_be_blank(input(
            """SO, THERE ARE OPTIONS U CAN DO:
    
= ABOUT TWEETS =
Create Tweet (input: crTW)
Like Tweet/Comment (input: like)
Unlike Tweet/Comment (input: unlike)
Retweet Tweet/Comment (input: retweet)
Get all info about Tweet (input: getTw)
Get all User"s tweets (input: getUserTw)

= ABOUT COMMENTS =
Create Comment to exact Tweet (input: crCM)

= ABOUT USERS =
Subscribe/Unsubscribe to someone: (input: subscribe)
Watch a list of Subscribes: (input: mySub)
Watch a list of Your followers: (input: myFollowers)
Watch all your Tweets: (input: myTweets)
Watch your profile: (input: getMyProfile)
Edit your profile (input: editMyProfile)
Delete your profile (input: delMyProfile)
Get all info about exact User (input: getUserInfo)
Get exact User's tweets: (input: getUserTw)

= FEED =
To observe your feed - your tweets and tweets of your subscribes: (input: feed)

Logout from the System: (input: logout) 
U always can Quit: (input: Q)

Choose command: """))

        match main_command.upper():

            # 3 create tweet ===================================
            case 'CRTW':
                massage = input('Write tweet massage: ')
                TwitterSystem.create_tweet(massage=field_cant_be_blank(massage), parent_id=None)

            # 4 create comment ==================================
            case 'CRCM':
                tweet_id_str = input('Input Tweet/Comment ID U want to comment: ')

                '''Check if input is INT type and empty input'''
                tweet_id_valid = check_int_type(tweet_id_str=field_cant_be_blank(tweet_id_str))

                '''Check if Tweet exists'''
                if tweet_id_valid not in TwitterSystem.Tweets_dict:
                    print(Fore.RED + f'\n{TwitterSystem.wtf_massage:=^25}')
                    print(f'| There is no Tweet/Comment with ID ={tweet_id_valid}=')
                    print()

                else:
                    text_of_comment = input('Input text of comment: ')

                    '''Call Method'''
                    TwitterSystem.create_tweet(massage=text_of_comment, parent_id=tweet_id_valid)

            # 5 like tweet =====================================
            case 'LIKE':
                tweet_id_str = input('Input Tweet ID U want to like: ')

                '''Check if input is INT type and empty input'''
                tweet_id_valid = check_int_type(tweet_id_str=field_cant_be_blank(tweet_id_str))

                '''Call Method'''
                TwitterSystem.like(massage_id=tweet_id_valid)

            # 6 unlike tweet ===================================
            case 'UNLIKE':
                tweet_id_str = input('Input Tweet ID U want to unlike: ')

                '''Check if input is INT type and empty input'''
                tweet_id_valid = check_int_type(tweet_id_str=field_cant_be_blank(tweet_id_str))

                '''Call Method'''
                TwitterSystem.unlike(massage_id=tweet_id_valid)

            # 7 retweet ========================================
            case 'RETWEET':
                tweet_id_str = input('Input Tweet ID U want to retweet: ')

                '''Check if input is INT type and empty input'''
                tweet_id_valid = check_int_type(tweet_id_str=field_cant_be_blank(tweet_id_str))

                '''Call Method'''
                TwitterSystem.retweet(massage_id=tweet_id_valid)

            # 8 get tweet ======================================
            case 'GETTW':
                tweet_id_str = input('Input Tweet ID about which tweet U want to get the info: ')

                '''Check if input is INT type and empty input'''
                tweet_id_valid = check_int_type(tweet_id_str=field_cant_be_blank(tweet_id_str))

                '''Call Method'''
                TwitterSystem.get_tweet_info(tweet_id=tweet_id_valid)

            # 9 get user tweets ================================
            case 'GETUSERTW':
                target_id = input('Input User ID U want to get all tweets: ')

                '''Check if input is INT type and empty input'''
                user_id_valid = check_int_type(tweet_id_str=field_cant_be_blank(target_id))

                '''Call Method'''
                TwitterSystem.get_user_tweets(user_id=user_id_valid)

            # 21 feed ==========================================
            case 'FEED':
                TwitterSystem.feed()

            # 22 feed fool ======================================
            # case 'FEEDFOOL':
            #     TwitterSystem.feed_fool()

            # 10 get all Tweets DB ==============================
            case 'GETALLTWEETSDATABASE':
                TwitterSystem.get_all_tweet_database()

            # 11 subscribe ======================================
            case 'SUBSCRIBE':
                target_id = input('Input User ID U want to subscribe: ')

                '''Check if input is INT type and empty input'''
                user_id_valid = check_int_type(tweet_id_str=field_cant_be_blank(target_id))

                '''Call Method'''
                TwitterSystem.subscribe(target_id=user_id_valid)

            # 12 get my profile =================================
            case 'GETMYPROFILE':
                TwitterSystem.get_my_profile()
                return main_flow_from_console()

            # 13 get my subscribes ==============================
            case 'MYSUB':
                TwitterSystem.my_subscribes()

            # 14 get my followers ===============================
            case 'MYFOLLOWERS':
                TwitterSystem.my_followers()

            # 15 get my tweets ==================================
            case 'MYTWEETS':
                TwitterSystem.my_tweets()

            # 16 edit my profile ================================
            case 'EDITMYPROFILE':
                new_first_name = field_cant_be_blank(input('Input new first name: '))
                new_second_name = field_cant_be_blank(input('Input new second name: '))
                new_email = field_cant_be_blank(input('Input new e-mail: '))

                '''Call Method'''
                TwitterSystem.edit_my_profile(new_name=new_first_name,
                                              new_second_name=new_second_name,
                                              new_email=new_email)

            # 17 delete my profile ===============================
            case 'DELMYPROFILE':

                '''Call Method'''
                TwitterSystem.delete_my_profile()
                tprint('EL TWITTER', font='bulbhead')
                sys.exit()

            # 18 get user info ===================================
            case 'GETUSERINFO':
                user_id = input('Input User ID U want to know about: ')

                '''Check if input is INT type and empty input'''
                user_id_valid = check_int_type(tweet_id_str=field_cant_be_blank(user_id))

                '''Call Method'''
                TwitterSystem.get_user_info(user_id=user_id_valid)

            # 19 get all Users DB ================================
            case 'GETALLUSERSDATABASE':

                '''Call Method'''
                TwitterSystem.get_all_users_database()

            # 20 Quit ============================================
            case 'Q':
                print(TwitterSystem.Fore.LIGHTYELLOW_EX + f'\n{" EL TWITTER ":=^25}')
                print('| Bye, see U next time\n')
                tprint('EL TWITTER', font='bulbhead')
                sys.exit()

            case 'LOGOUT':
                print(TwitterSystem.Fore.LIGHTYELLOW_EX + f'\n{" LOGOUT ":=^25}')
                print('| Go to main page\n')
                return begin_program_flow()

            case _:
                print(TwitterSystem.Fore.RED + f'\n{TwitterSystem.wtf_massage:=^25}')
                print('| Incorrect command, try one more time\n')


if __name__ == '__main__':
    tprint('EL TWITTER', font='bulbhead')

    print(Fore.LIGHTYELLOW_EX + 'Hello my friend, welcome to EL TWITTER created by Ihor Zabudskyi')
    print()
    print('First of all U need to CREATE ACCOUNT or LOGIN to your ACCOUNT')

    begin_program_flow()
