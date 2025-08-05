import requests
def sendMsg():
    TOKEN = "7996574904:AAEtvpuxFx859QUQ70BbENDrLT9oydtU358"
    chat_id = "6644289057"
    message = "There is a fire breaking out, help!\nMy address is blk123, unit 01-234"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json())
    return True