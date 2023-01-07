import collections

from Tweet import *
from colorama import Fore, init

init(autoreset=True)  # automatically auto-reset colorama text after print

Tweets_dict = {}  # {id: inst_tweet}
Users_dict = {}  # {id: inst_user}

system_info_header = ' SYSTEM INFO '
wtf_massage = ' WTFCK! '


class AuthenticationError(ValueError):
    pass


class NoUsersError(ValueError):
    pass


class NoTweetsError(ValueError):
    pass


# ______________________________DECORATORS BLOCK____________________________

# check If User logined
def check_login(func):
    def wrapper(*args, **kwargs):
        if user_session.current_user is None:
            print(Fore.RED + f'\n{wtf_massage:=^25}')
            print('| Please log in to perform the operation\n')
            return
        return func(*args, **kwargs)

    return wrapper


# decorator to check Tweet DB is empty
def check_Tweet_DB_empty(func):
    def wrapper(*args, **kwargs):
        if Tweets_dict == {}:
            print(Fore.RED + f'\n{wtf_massage:=^25}')
            print('| Tweets DB is empty\n')
            return
        return func(*args, **kwargs)

    return wrapper


# decorator to check Users DB is empty
def check_Users_DB_empty(func):
    def wrapper(*args, **kwargs):
        if Users_dict == {}:
            print(Fore.RED + f'\n{wtf_massage:=^25}')
            print('| Users DB is empty')
            return
        return func(*args, **kwargs)

    return wrapper


# __________________________________SYSTEM COMMANDS___________________________

class UserSession:
    current_user = None


user_session = UserSession()  # default state of User before registration


# 1 create user =======================================
def create_user(user: User):
    print(Fore.LIGHTYELLOW_EX + f'\n{" NEW USER CREATED ":=^25}')
    print(f'| User nickname: "{user}"\n'
          f'| User ID: ={user.user_id}=\n')
    Users_dict[user.user_id] = user
    return


# 2 login ============================================
def login(email, password):
    if len(Users_dict) == 0:
        raise NoUsersError("We can't check your credentials")

    for key, value in Users_dict.items():
        if value._email == email and value._psw == password:
            user_session.current_user = value
            print(Fore.LIGHTYELLOW_EX + f'\n{" USER LOGIN ":=^25}')
            print(f'| User {value} (id: ={key}=) logged in successfully\n')
            return
    raise AuthenticationError


# 3 create tweet ===================================
@check_login
def create_tweet(massage: str, parent_id):
    tweet = Tweet(massage=massage, user=user_session.current_user, parent_id=parent_id)
    Tweets_dict[tweet.tweet_id] = tweet
    Tweets_dict[tweet.tweet_id].parent_id = parent_id

    if parent_id is None:
        user_session.current_user.tweets_id.append(tweet.tweet_id)
        print(Fore.LIGHTYELLOW_EX + f'\n{" NEW TWEET ":=^25}')
        print(
            f'| Tw: "{tweet.massage}" [tweet ID: ={tweet.tweet_id}= | {tweet.author.nickname} | {tweet.time_of_tweet}]\n')
        return

# 4 create comment ==================================
    elif parent_id is not None:
        Tweets_dict[parent_id].comments.append(tweet)
        print(Fore.LIGHTYELLOW_EX + f'\n{" NEW COMMENT ":=^25}')
        print(
            f'| Tw: "{Tweets_dict[parent_id]}" [tweet ID: ={Tweets_dict[parent_id].tweet_id}= | {Tweets_dict[parent_id].author.nickname} | {Tweets_dict[parent_id].time_of_tweet}]'
            f'\n| Comment: "{tweet.massage}" [comment ID: ={tweet.tweet_id}= | {tweet.author.nickname} | {tweet.time_of_tweet}]\n')
        return


# 5 like tweet =====================================
@check_login
@check_Tweet_DB_empty
def like(massage_id: int):
    author_of_like = user_session.current_user
    if massage_id not in Tweets_dict:
        print(Fore.RED + f'\n{wtf_massage:=^25}')
        print(f'| There is no Tweet/Comment with ID ={massage_id}=\n')
        return

    if Tweets_dict[massage_id].parent_id is None:
        if author_of_like in Tweets_dict[massage_id].likes_of_tweet:
            print(Fore.RED + f'\n{wtf_massage:=^25}')
            print(f'| U already performed LIKE to this tweet. U can not do it twice\n')
        else:
            print(Fore.LIGHTYELLOW_EX + f'\n{" LIKE ":=^25}')
            Tweets_dict[massage_id].likes_of_tweet.append(author_of_like)
            print(f'| Tweet "{Tweets_dict[massage_id].massage}" was liked by {author_of_like.nickname}\n')

    elif Tweets_dict[massage_id].parent_id is not None:
        if author_of_like in Tweets_dict[massage_id].likes_of_tweet:
            print(Fore.RED + f'\n{wtf_massage:=^25}')
            print(f'| U already performed LIKE to this comment. U can not do it twice\n')
        else:
            Tweets_dict[massage_id].likes_of_tweet.append(author_of_like)
            print(Fore.LIGHTYELLOW_EX + f'\n{" LIKE ":=^25}')
            print(f'| Comment "{Tweets_dict[massage_id].massage}" was liked by {author_of_like.nickname}\n')
    return


# 6 unlike tweet ===================================
@check_login
@check_Tweet_DB_empty
def unlike(massage_id: int):
    author_of_unlike = user_session.current_user
    if massage_id not in Tweets_dict:
        print(Fore.RED + f'\n{wtf_massage:=^25}')
        print(f'| There is no Tweet/Comment with ID ={massage_id}=\n')
        return
    if Tweets_dict[massage_id].parent_id is None and author_of_unlike in Tweets_dict[
        massage_id].likes_of_tweet:
        Tweets_dict[massage_id].likes_of_tweet.remove(author_of_unlike)
        print(Fore.LIGHTYELLOW_EX + f'\n{" UNLIKE ":=^25}')
        print(f'| Tweet "{Tweets_dict[massage_id].massage}" was unliked by {author_of_unlike.nickname}\n')
    elif Tweets_dict[massage_id].parent_id is not None and author_of_unlike in Tweets_dict[
        massage_id].likes_of_tweet:
        Tweets_dict[massage_id].likes_of_tweet.remove(author_of_unlike)
        print(Fore.LIGHTYELLOW_EX + f'\n{" UNLIKE ":=^25}')
        print(f'| Comment "{Tweets_dict[massage_id].massage}" was unliked by {author_of_unlike.nickname}\n')
    else:
        print(Fore.RED + f'\n{wtf_massage:=^25}')
        print(
            f"| {author_of_unlike.nickname} can't unlike massage with ID {massage_id} "
            f"because he didn't make like for it\n")
    return


# 7 retweet ========================================
@check_login
@check_Tweet_DB_empty
def retweet(massage_id: int):
    author_of_retweet = user_session.current_user

    if massage_id not in Tweets_dict:
        print(Fore.RED + f'\n{wtf_massage:=^25}')
        print(f'| There is no Tweet/Comment with ID ={massage_id}=\n')
        return

    print(Fore.LIGHTYELLOW_EX + f'\n{" RETWEET ":=^25}')
    if Tweets_dict[massage_id].parent_id is None:
        Tweets_dict[massage_id].retweets_of_tweet.append(author_of_retweet)
        print(f'| Tweet "{Tweets_dict[massage_id].massage}" was retweeted by {author_of_retweet.nickname}\n')
    elif Tweets_dict[massage_id].parent_id is not None:
        Tweets_dict[massage_id].retweets_of_tweet.append(author_of_retweet)
        print(f'| Comment "{Tweets_dict[massage_id].massage}" was retweeted by {author_of_retweet.nickname}\n')
    return


# 8 get tweet ======================================
@check_login
@check_Tweet_DB_empty
def get_tweet_info(tweet_id: int):
    if tweet_id not in Tweets_dict:
        print(Fore.RED + f'\n{wtf_massage:=^25}')
        print(f'| There is no Tweet/Comment with ID ={tweet_id}=\n')
        return
    print(Fore.LIGHTYELLOW_EX + f'\n{" TWEET INFO ":=^25}')
    print(
        f'\n| Tweet: "{Tweets_dict[tweet_id].massage}"'
        f'\n| Tweet ID: ={tweet_id}='
        f'\n| Author: {Tweets_dict[tweet_id].author.nickname}'
        f'\n| Posted: {Tweets_dict[tweet_id].time_of_tweet}'
        f'\n| Likes: {len(Tweets_dict[tweet_id].likes_of_tweet)}')

    if len(Tweets_dict[tweet_id].likes_of_tweet):
        print(f'| Liked by: {Tweets_dict[tweet_id].likes_of_tweet}')

    print(f'| Retweets: {len(Tweets_dict[tweet_id].retweets_of_tweet)}')
    if len(Tweets_dict[tweet_id].retweets_of_tweet):
        print(f'| Retweeted by: {Tweets_dict[tweet_id].retweets_of_tweet}')

    print(f'| Comments: {len(Tweets_dict[tweet_id].comments)}')

    devider = 1
    for key, value in Tweets_dict.items():
        if value.parent_id == tweet_id:
            print(f'{"|" * devider} Comment: "{value.massage}" [Author: {value.author} | Posted: {value.time_of_tweet} | Likes: {len(value.likes_of_tweet)} | Reposts: {len(value.retweets_of_tweet)} | Comments: {len(value.comments)} | comment_id: ={key}=]')
    print()
    return


# 9 get user tweets ================================
@check_Tweet_DB_empty
def get_user_tweets(user_id: int):
    if user_id not in Users_dict:
        print(Fore.RED + f'\n{wtf_massage:=^25}')
        print(f'| There is no User with ID ={user_id}=\n')
        return

    if not Users_dict[user_id].tweets_id:
        print(Fore.LIGHTYELLOW_EX + f'\n{" USERS TWEETS ":=^25}')
        print(f'| User with ID ={user_id}= did not make any tweet yet\n')
        return

    print(Fore.LIGHTYELLOW_EX + f'\n{" USERS TWEETS ":=^25}')
    print(f'| Author: {Users_dict[user_id]}')
    for key, value in Tweets_dict.items():
        if value.parent_id is None:
            if value.author.user_id == user_id:
                print(
                    f'| "{value}" [tweet ID: ={key}= | created: {value.time_of_tweet} | likes: {len(value.likes_of_tweet)} | retweets: {len(value.retweets_of_tweet)} | comments: {len(value.comments)}]')
    print()
    return


# 10 get all Tweets DB ==============================
@check_Tweet_DB_empty
def get_all_tweet_database():
    print(Fore.LIGHTYELLOW_EX + f'\n{" TWEETS DATABASE ":=^25}')
    for key, value in Tweets_dict.items():
        if value.parent_id is None:
            print(f'| ID ={key}= : "{value}" | [Original Tweet] | {value.time_of_tweet}')
        elif value.parent_id is not None:
            print(f'| ID ={key}= : "{value}" | [Comment] | {value.time_of_tweet} | Parent Tweet ID: ={value.parent_id}=')
    print()
    return


# 11 subscribe ======================================
@check_login
def subscribe(target_id: int):
    if target_id not in Users_dict:
        print(Fore.RED + f'\n{wtf_massage:=^25}')
        print(f'| There is no User with ID ={target_id}=\n')
        return
    if target_id == user_session.current_user.user_id:
        print(Fore.RED + f'\n{wtf_massage:=^25}')
        print(f'| U trying to subscribe to yourself. Only stupid russian pig can think of such a thing\n')
        return
    if user_session.current_user in Users_dict[target_id].followers:
        print(Fore.RED + f'\n{wtf_massage:=^25}')
        answer = input(f'| U already subscribed to {Users_dict[target_id]}. Do U want to Unsubscribe?: y/N \n')
        if answer.upper() == 'Y':
            Users_dict[target_id].followers.remove(user_session.current_user)
            user_session.current_user.subscribes.remove(Users_dict[target_id])
            print(Fore.LIGHTYELLOW_EX + f'\n{" UNSUBSCRIBE ":=^25}')
            print(f'| U unsubscribed from User {Users_dict[target_id].nickname}\n')
        elif answer.upper() == 'N':
            pass
        else:
            print(Fore.RED + f'\n{wtf_massage:=^25}')
            return print('| Incorrect input, try one more time\n')
        return

    user_session.current_user.subscribes.append(Users_dict[target_id])
    Users_dict[target_id].followers.append(user_session.current_user)
    print(Fore.LIGHTYELLOW_EX + f'\n{" SUBSCRIBE ":=^25}')
    print(f'| {user_session.current_user} subscribed to {Users_dict[target_id]}\n')
    return Users_dict[target_id].nickname


# 12 get my profile =================================
@check_login
def get_my_profile():
    print(Fore.LIGHTYELLOW_EX + f'\n{" YOUR PROFILE ":=^25}')
    print(f'| ID: ={user_session.current_user.user_id}='
          f'\n| First name: {user_session.current_user.first_name}'
          f'\n| Second name: {user_session.current_user.second_name}'
          f'\n| Nickname: {user_session.current_user.nickname}'
          f'\n| Registration time: {user_session.current_user.registration_time}'
          f'\n| Subscribes: {len(user_session.current_user.subscribes)}'
          f'\n| Followers: {len(user_session.current_user.followers)}'
          f'\n| Tweets: {len(user_session.current_user.tweets_id)}')
    print()
    return


# 13 get my subscribes =================================
@check_login
def my_subscribes():
    print(Fore.LIGHTYELLOW_EX + f'\n{" YOUR SUBSCRIBES ":=^25}')
    if not Users_dict[user_session.current_user.user_id].subscribes:
        print('| Ooops... You have no subscribes\n')
        return
    for subsc in Users_dict[user_session.current_user.user_id].subscribes:
        print(f'| {subsc.nickname} [user ID: ={subsc.user_id}= ]')
    print()
    return


# 14 get my followers =================================
@check_login
def my_followers():
    print(Fore.LIGHTYELLOW_EX + f'\n{" YOUR FOLLOWERS ":=^25}')
    if not Users_dict[user_session.current_user.user_id].followers:
        print('| Ooops... You have no followers\n')
        return
    for follower in Users_dict[user_session.current_user.user_id].followers:
        print(f'| {follower.nickname} [user ID: ={follower.user_id}= ]')
    print()
    return


# 15 get my tweets =================================
@check_login
@check_Tweet_DB_empty
def my_tweets():
    print(Fore.LIGHTYELLOW_EX + f'\n{" YOUR TWEET ":=^25}')
    if not user_session.current_user.tweets_id:
        print('| You did not create any tweet. Try it')
        return
    for tweet_id in user_session.current_user.tweets_id:
        for key, value in Tweets_dict.items():
            if key == tweet_id:
                print(f'| "{value}" [tweet ID ={key}= | {value.time_of_tweet} | likes: {len(value.likes_of_tweet)} | retweets: {len(value.retweets_of_tweet)} | comments: {len(value.comments)}]')
    print()
    return


# 16 edit my profile ================================
@check_login
def edit_my_profile(new_name, new_second_name, new_email):
    print(Fore.LIGHTYELLOW_EX + f'\n{" EDIT PROFILE ":=^25}')
    User._edit_user_profile(
        self=user_session.current_user,
        new_name=new_name,
        new_second_name=new_second_name,
        new_email=new_email
    )
    return


# 17 delete my profile ===============================
@check_login
def delete_my_profile():
    print(Fore.LIGHTYELLOW_EX + f'\n{" USER DElETE ":=^25}')
    print(f'| User {user_session.current_user} made a suicide\n')
    user_session.current_user._psw = user_session.current_user._psw + '_deleted_'
    user_session.current_user = None
    return


# 18 get user info ===================================
@check_login
def get_user_info(user_id):
    if user_id not in Users_dict:
        print(Fore.RED + f'\n{wtf_massage:=^25}')
        print(f'There is no User with ID ={user_id}=\n')
        return
    print(Fore.LIGHTYELLOW_EX + f'\n{" USER INFO ":=^25}')
    print(f'| User ID: ={user_id}=\n'
          f'| Nickname: {Users_dict[user_id].nickname}\n'
          f'| Registered: {Users_dict[user_id].registration_time}')

    if len(Users_dict[user_id].tweets_id) != 0:
        print(f'| Tweets: {len(Users_dict[user_id].tweets_id)}')
    else:
        print(f'| Tweets: 0')

    if len(Users_dict[user_id].subscribes) != 0:
        print(f'| Subscribes: {Users_dict[user_id].subscribes}')
    else:
        print(f'| Subscribes: 0')

    if len(Users_dict[user_id].followers) != 0:
        print(f'| Followers: {Users_dict[user_id].followers}\n')
    else:
        print(f'| Followers: 0\n')
    return


# 19 get all Users DB ================================
@check_Users_DB_empty
def get_all_users_database():
    print(Fore.LIGHTYELLOW_EX + f'\n=== EL TWITTER {" USERS DATABASE ":=^25}')
    for key, value in Users_dict.items():
        print(f'| User ID ={key}= : "{value}" | Registered {value.registration_time}')
    print()
    return


# 21 feed ===========================================
@check_login
@check_Tweet_DB_empty
def feed():
    print(Fore.LIGHTYELLOW_EX + f'\n{" YOUR FEED ":=^25}')

    authors = set(user_session.current_user.subscribes)
    authors.add(user_session.current_user)
    feed_list = []
    number_of_items_in_feed = 3

    all_tweets = list(Tweets_dict.values())

    for tweet in all_tweets[::-1]:
        if tweet.parent_id:
            continue

        if tweet.author in authors or user_session.current_user in tweet.retweets_of_tweet:
            feed_list.append(tweet)
            if len(feed_list) == number_of_items_in_feed:
                break

    if not feed_list:
        print('| Your feed is empty. Try Tweet something or Subscribe to somebody')

    for tweet in sorted(feed_list, key=lambda item: item.time_of_tweet, reverse=True):

        if tweet.parent_id is None:
            print(f'| Tweet: "{tweet.massage}" | Author: {tweet.author.nickname} | Tweet ID: {tweet.tweet_id} | {tweet.time_of_tweet}')

            if len(tweet.comments) != 0:
                for each_comment in tweet.comments:
                    print(f'|| Comment: "{each_comment.massage}" | Author: {each_comment.author.nickname} | Comment ID: {each_comment.tweet_id} | Parent Tweet ID: {each_comment.parent_id} | {each_comment.time_of_tweet}')

                    if len(each_comment.comments) != 0:
                        for comment_of_comment in each_comment.comments:
                            print(
                                f'||| Comment to Comment: "{comment_of_comment.massage}" | Author: {comment_of_comment.author.nickname} | Comment ID: {comment_of_comment.tweet_id} | Parent Tweet ID: {comment_of_comment.parent_id} | {comment_of_comment.time_of_tweet}')

        if user_session.current_user in tweet.retweets_of_tweet:
            print(f'|||| ^^^ Retweet: "{tweet.massage}" | Author: {tweet.author.nickname} | Tweet ID: {tweet.tweet_id} | {tweet.time_of_tweet}')

    return print()

