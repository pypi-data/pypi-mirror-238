# Quick Start
----------------
**Step 1:**
> Install [Discohooker](https://pypi.org/project/discohooker/) in Shell.
> 
> ```pip install discohooker```
----------------
**Step 2:**
> Get your Webhook link in [Discord](https://discord.com/channels/@me).
---------------
**Step 3:**
> Import Discohooker.
>
> ```py
> import discohooker
> ```
-------------
**Step 4:**
> Setup [Webhook](https://discord.com/developers/docs/resources/webhook).
>
> ```py
> webhook=discohooker.Webhook(
>     weburl="YOUR DISCORD WEBHOOK URL",
>     name="DISCORD WEBHOOK NAME(IF YOU HAVE SET IN DISCORD ALREADY, YOU MUST NOT ENTER.)",
>     avatar_url="DISCORD WEBHOOK AVATAR URL(IF YOU HAVE SET IN DISCORD ALREADY, YOU MUST NOT ENTER.)"
> )
> ```
------------
**Step 5:**
> Send [Message](https://discord.com/developers/docs/resources/channel#message-object).
>
> ```py
> @discohooker.Tasks.worker
> async def run():
>     await webhook.send_message("I am made by Discohooker!")
> ```
--------------
DONE! Do you feel very easy? 