import requests
import os

                    
class Notification: 

    def send_lotto_buying_message(self, body: dict, webhook_url: str) -> None:
        assert type(webhook_url) == str

        result = body.get("result", {})
        if result.get("resultMsg", "FAILURE").upper() != "SUCCESS":  
            return

        lotto_number_str = self.make_lotto_number_message(result["arrGameChoiceNum"])
        message = f"{result['buyRound']}회 로또 구매 완료 :moneybag: 남은잔액 : {body['balance']}\n```{lotto_number_str}```"
        self._send_discord_webhook(webhook_url, message)
        self._send_slack_webhook(webhook_url, message)

    def make_lotto_number_message(self, lotto_number: list) -> str:
        assert type(lotto_number) == list

        # parse list without last number 3
        lotto_number = [x[:-1] for x in lotto_number]
        
        # remove alphabet and | replace white space  from lotto_number
        lotto_number = [x.replace("|", " ") for x in lotto_number]
        
        # lotto_number to string 
        lotto_number = '\n'.join(x for x in lotto_number)
        
        return lotto_number

    def send_win720_buying_message(self, body: dict, webhook_url: str) -> None:
        assert type(webhook_url) == str
        
        if body.get("resultCode") != '100':  
            return       

        win720_round = body.get("resultMsg").split("|")[3]

        win720_number_str = self.make_win720_number_message(body.get("saleTicket"))
        message = f"{win720_round}회 연금복권 구매 완료 :moneybag: 남은잔액 : {body['balance']}\n```{win720_number_str}```"

    def make_win720_number_message(self, win720_number: str) -> str:
        return "\n".join(win720_number.split(","))

    def send_lotto_winning_message(self, winning: dict, webhook_url: str) -> None: 
        assert type(winning) == dict
        assert type(webhook_url) == str

        try: 
            round = winning["round"]
            money = winning["money"]
            message = f"로또 *{winning['round']}회* - *{winning['money']}* 당첨 되었습니다 :tada:"
            self._send_discord_webhook(webhook_url, message)
        except KeyError:
            return

    def send_win720_winning_message(self, winning: dict, webhook_url: str) -> None: 
        assert type(winning) == dict
        assert type(webhook_url) == str

        try: 
            round = winning["round"]
            money = winning["money"]
            message = f"연금복권 *{winning['round']}회* - *{winning['money']}* 당첨 되었습니다 :tada:"
            self._send_discord_webhook(webhook_url, message)
        except KeyError:
            return

    def _send_discord_webhook(self, webhook_url: str, message: str) -> None:        
        payload = { "content": message }
        requests.post(webhook_url, json=payload)

    def _send_slack_webhook(self, webhook_url: str, message: str) -> None:        
        payload = { "content": message }
        try:
            url = webhook_url
            header = {'Content-type': 'application/json'}
            icon_emoji = ":slack:"
            username = "TEST"
            attachments = [{
                "color": "good",
                "text": message
            }]

            data = {"username": username, "attachments": attachments, "icon_emoji": icon_emoji}
            print(data)

            # 메세지 전송
            return requests.post(url, headers=header, json=data)
            
        except Exception as e:
            print.error("Slack Message 전송에 실패했습니다.")
            print.error("에러 내용 : " + e)

            exit(0)