from .errors import Errors
from .embed import Embed
from .webhook import Webhook
import requests


class Message:
    def __init__(self, webhook: Webhook, message_id: int):
        self.webhook=webhook
        response=requests.get(f"{self.webhook.weburl}/messages/{message_id}").json()
        try:
            response["code"]
        except:
            pass
        else:
            raise Errors.MessageNotFound("This message is not sent by webhook so you cannot get this message!")
        self.id=response["id"]
        self.content=response["content"]
        self.is_pinned=response["pinned"]
        self.embeds=[]
        for embed in response["embeds"]:
            _embed=Embed()
            _embed._to_dict=embed
            self.embeds.appead(_embed)
        self.timestamp=response["timestamp"]
        self.mentions_id=[]
        for user in response["mentions"]:
            self.memtions_id.appead(user["id"])
        self.channel_id=response["channel_id"]

    
    async def edit(self, content: str=None, embeds: list[Embed]=[]):
        message_id=self.id
        _embeds=[]
        for embed in embeds:
            _embeds.append(embed._to_dict)
        if content == None:
            _content=""
        else:
            _content=content
        _jdata={"content": _content, "embeds": _embeds}
        response=requests.patch(f"{self.webhook.weburl}/messages/{message_id}", data=_jdata)
        if response.status_code == 304:
            raise Errors.APIError("The entity was not modified (no action was taken).")
        elif response.status_code == 429:
            raise Errors.APIError("You are being rate limited, see https://discord.com/developers/docs/topics/rate-limits.")
        elif response.status_code == 400:
            raise Errors.APIError("The request was improperly formatted, or the server couldn't understand it.(Bad Request)")
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


    async def delete(self):
        message_id=self.id
        response=requests.delete(f"{self.webhook.weburl}/messages/{message_id}")
        if response.status_code != 204:
            raise Errors.MessageNotFound("This message was not sent by this Webhook! Please make sure your message id is correct!")
        else:
            return response