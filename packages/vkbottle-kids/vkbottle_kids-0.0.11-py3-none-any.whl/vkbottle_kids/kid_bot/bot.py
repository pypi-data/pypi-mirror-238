from vkbottle.bot import Bot, BotLabeler
from vkbottle import API

from vkbottle.dispatch.rules import ABCRule


class KidBot:

    def __init__(self, kid_keys: str, kid_labelers: list):

        self.kid_keys: str = kid_keys
        self.kid_labelers: list = kid_labelers
        self.run_bot()
        self.kid_labeler()

    def run_bot(self) -> Bot:

        if isinstance(self.kid_keys, str) and isinstance(self.kid_labelers, list):
            
            api = API(self.kid_keys)
            bot = Bot(api=api, labeler=BotLabeler())

            for kid_labeler in self.kid_labelers:
                bot.labeler.load(kid_labeler)

            bot.run_forever()
    
        elif isinstance(self.kid_keys, (int, float, tuple, dict, list)):

            raise ValueError(
                "Ты блядь неверно указал токен. Гуглить блядь научись"
            )
        
        else:

            raise TypeError(
                "Указал блядь неверный тип к kid_labeler. Укажи пустой список"
            )            


class KidLabeler(BotLabeler):

    def global_message(*rules: "ABCRule", **custom_rules):

        return BotLabeler.message(*rules, **custom_rules)
