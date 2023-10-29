from .errors import Errors
from .embed import Embed
import requests


class Webhook:
    def __init__(self, weburl: str, name: str=None, avatar_url: str=None):
        if not weburl.startswith("https://discord.com/api/webhooks/"):
            raise Errors.WebhookURLError("This is not Discord Webhook URL! Please check your URL and change the URL to the correct URL!")
        response=requests.get(weburl).json()
        if avatar_url == None:
            self.avatar_url=avatar_url
        elif not avatar_url.startswith("https://"):
            raise Errors.URLError("This is not URL! Please check and change your URL!")
        else:
            self.avatar_url=avatar_url
        self.weburl=weburl
        if name == None:
            self.name=response["name"]
        else:
            self.name=name
        self.id=response["id"]
        self.mention=f"<@{self.id}>"
        self.token=response["token"]
        if response["application_id"] == None:
            self.application_id=0
        else:
            self.application_id=response["application_id"]
        self.channel_id=response["channel_id"]
        self.guild_id=response["guild_id"]
        self.json=response


    @property
    def url(self):
        return self.weburl


    async def edit(self, channel_id: int, name: str, avatar_url: str=None):
        if not avatar_url.startswith("https!//") and avatar_url != None:
            raise Errors.URLError("This is not URL! Please check and change your URL!")
        _jdata={"name": name, "channel_id": channel_id, "avatar": avatar_url}
        return requests.patch(self.weburl, data=_jdata)


    def get_message(self, message_id: int):
        from .message import Message
        return Message(self, message_id)

    
    async def send_message(self, content: str=None, embeds: list[Embed]=[]):
        _embeds=[]
        for embed in embeds:
            _embeds.append(embed._to_dict)
        if content == None:
            _content=""
        else:
            _content=content
        _jdata={"content": _content, "embeds": _embeds, "username": self.name, "avatar_url": self.avatar_url}
        response=requests.post(self.weburl, data=_jdata)
        if response.status_code == 304:
            raise Errors.APIError("The entity was not modified (no action was taken).")
        elif response.status_code == 429:
            raise Errors.APIError("You are being rate limited, see https://discord.com/developers/docs/topics/rate-limits.")
        elif response.status_code == 400:
            raise Errors.APIError("The request was improperly formatted, or the server couldn't understand it.")
        elif response.status_code == 401:
            raise Errors.APIError("The Authorization header was missing or invalid.")
        elif response.status_code == 403:
            raise Errors.APIError("The Authorization token you passed did not have permission to the resource")
        elif response.status_code == 404:
            raise Errors.APIError("The resource at the location specified doesn't exist.")
        elif response.status_code == 405:
            raise Errors.APIError("The HTTP method used is not valid for the location specified.")
        elif response.status_code == 502:
            raise Errors.APIError("There was not a gateway available to process your request. Wait a bit and retry.")
        else:
            return response