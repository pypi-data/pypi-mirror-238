from .errors import Errors
from datetime import datetime


class EmbedField:
    def __init__(self, name: str=None, value: str=None, inline: bool=True):
        self.name=name
        self.value=value
        self.inline=inline


    @property
    def name(self):
        return self.name


    @property
    def value(self):
        return self.value


    @property
    def inline(self):
        return self.inline


    @property
    def _to_dict(self):
        return {"name": self.name, "valuel": self.value, "inline": self.inline}
        


class Embed:
    def __init__(self, title: str=None, description: str=None, colour: str=0xffffff, url: str=None, fields: list[EmbedField]=[], timestamp: datetime=None):
        self.title=title
        self.description=description
        self.colour=colour
        if url == None:
            self.url=url
        elif not url.startswith("https://"):
            raise Errors.URLError("This is not URL! Please check and change your URL!")
        else:
            self.url=url
        self.fields=fields
        self.timestamp=timestamp
        self._image={}
        self._thumbnail={}
        self._author={}
        self._footer={}


    def add_field(self, *fields: EmbedField):
        for field in fields:
            self.fields.append(field._to_dict)
        return self.field

    
    def remove_field(self, *fields: EmbedField):
        for field in fields:
            self.fields.remove(field._to_dict)
        return self.field


    def clear_field(self):
        self.field=[]
        return self.field


    @property
    def footer(self):
        return self._footer


    def set_footer(self, text: str=None, icon_url: str=None):
        if not icon_url.startswith("https://") and icon_url != None:
            raise Errors.URLError("This is not URL! Please check and change your URL!")
        self._footer={"text": text, "icon_url": icon_url}
        return self._footer


    def remove_footer(self):
        self._footer={}
        return self._footer


    @property
    def image(self):
        return self._image


    def set_image(self, url: str):
        if not url.startswith("https://"):
            raise Errors.URLError("This is not URL! Please check and change your URL!")
        self._image={"url": url}
        return self._image


    def remove_image(self):
        self._image={}
        return self._image


    @property
    def thumbnail(self):
        return self._thumbnail


    def set_thumbnail(self, url: str):
        if not url.startswith("https://"):
            raise Errors.URLError("This is not URL! Please check and change your URL!")
        self._thumbnail={"url": url}
        return self._thumbnail


    def remove_thumbnail(self):
        self._thumbnail={}
        return self._thumbnail


    @property
    def author(self):
        return self._author


    def set_author(self, name: str=None, url: str=None, icon_url: str=None):
        if not icon_url.startswith("https://") and icon_url != None:
            raise Errors.URLError("This is not URL! Please check and change your URL!")
        if not url.startswith("https://") and url != None:
            raise Errors.URLError("This is not URL! Please check and change your URL!")
        self._author={"name": name, "url": url, "icon_url": icon_url}
        return self._author


    def remove_author(self):
        self._author={}
        return self._author


    @property
    def _to_dict(self):
        return {"title": self.title, "description": self.description, "color": int(str(self.colour), 10), "fields": self.fields, "author": self._author, "footer": self._footer, "timestamp": self.timestamp, "image": self._image, "thumbnail": self._thumbnail}