# these different interfaces are for the different roles a third party service
# can fulfill. implementing them adds some generic functionality to attempt to
# actually perform the role, but this will have to be overwritten in most cases.
# functionality is separated into different layers to allow partial override

# also yes, we're using singleton classes for the different providers
# pls don't sue me

import xml.etree.ElementTree as ElementTree
import json
import urllib.parse, urllib.request
import base64
import time
from doreah.logging import log
from threading import BoundedSemaphore

from ..pkg_global.conf import malojaconfig
from .. import database


services = {
	"proxyscrobble":[],
	"import":[],
	"metadata":[]
}



class InvalidResponse(Exception):
	"""Invalid Response from Third Party"""

class RateLimitExceeded(Exception):
	"""Rate Limit exceeded"""

# have a limited number of worker threads so we don't completely hog the cpu with
# these requests. they are mostly network bound, so python will happily open up 200 new
# requests and then when all the responses come in we suddenly can't load pages anymore
thirdpartylock = BoundedSemaphore(4)


def import_scrobbles(identifier):
	for service in services['import']:
		if service.identifier == identifier:
			return service.import_scrobbles()
	return False

def proxy_scrobble_all(artists,title,timestamp):
	for service in services["proxyscrobble"]:
		service.scrobble(artists,title,timestamp)

def get_image_track_all(track):
	with thirdpartylock:
		for service in services["metadata"]:
			try:
				res = service.get_image_track(track)
				if res:
					log("Got track image for " + str(track) + " from " + service.name)
					return res
				else:
					log(f"Could not get track image for {track} from {service.name}")
			except Exception as e:
				log(f"Error getting track image from {service.name}: {e.__doc__}")
def get_image_artist_all(artist):
	with thirdpartylock:
		for service in services["metadata"]:
			try:
				res = service.get_image_artist(artist)
				if res:
					log("Got artist image for " + str(artist) + " from " + service.name)
					return res
				else:
					log(f"Could not get artist image for {artist} from {service.name}")
			except Exception as e:
				log(f"Error getting artist image from {service.name}: {e.__doc__}")
def get_image_album_all(album):
	with thirdpartylock:
		for service in services["metadata"]:
			try:
				res = service.get_image_album(album)
				if res:
					log("Got album image for " + str(album) + " from " + service.name)
					return res
				else:
					log(f"Could not get album image for {album} from {service.name}")
			except Exception as e:
				log(f"Error getting album image from {service.name}: {e.__doc__}")


class GenericInterface:
	def active_proxyscrobble(self):
		return False
	def active_import(self):
		return False
	def active_metadata(self):
		return False

	settings = {}

	proxyscrobble = {}
	scrobbleimport = {}
	metadata = {}

	def __init__(self):
		# populate from settings file once on creation
		# avoid constant disk access, restart on adding services is acceptable
		for key in self.settings:
			self.settings[key] = malojaconfig[self.settings[key]]
		self.authorize()

	# this makes sure that of every class we define, we immediately create an
	# instance (de facto singleton). then each instance checks if the requirements
	# are met to use that service in each particular role and registers as such
	def __init_subclass__(cls,abstract=False):
		if not abstract:
			s = cls()
			if s.active_proxyscrobble():
				services["proxyscrobble"].append(s)
				#log(cls.name + " registered as proxy scrobble target")
			if s.active_import():
				services["import"].append(s)
				#log(cls.name + " registered as scrobble import source")
			if s.active_metadata():
				services["metadata"].append(s)
				#log(cls.name + " registered as metadata provider")

	def authorize(self):
		return True
		# per default. no authorization is necessary

	# wrapper method
	def request(self,url,data,responsetype):
		response = urllib.request.urlopen(
			url,
			data=utf(data)
		)
		responsedata = response.read()
		if responsetype == "xml":
			data = ElementTree.fromstring(responsedata)
			return data

# proxy scrobbler
class ProxyScrobbleInterface(GenericInterface,abstract=True):

	proxyscrobble = {
		"required_settings":[],
		"activated_setting":None
	}

	# service provides this role only if the setting is active AND all
	# necessary auth settings exist
	def active_proxyscrobble(self):
		return (
			all(self.settings[key] not in [None,"ASK",False] for key in self.proxyscrobble["required_settings"]) and
			malojaconfig[self.proxyscrobble["activated_setting"]]
		)

	def scrobble(self,artists,title,timestamp):
		response = urllib.request.urlopen(
			self.proxyscrobble["scrobbleurl"],
			data=utf(self.proxyscrobble_postdata(artists,title,timestamp)))
		responsedata = response.read()
		if self.proxyscrobble["response_type"] == "xml":
			data = ElementTree.fromstring(responsedata)
			return self.proxyscrobble_parse_response(data)

# scrobble import
class ImportInterface(GenericInterface,abstract=True):

	scrobbleimport = {
		"required_settings":[],
		"activated_setting":None
	}

	# service provides this role only if the setting is active AND all
	# necessary auth settings exist
	def active_import(self):
		return (
			all(self.settings[key] not in [None,"ASK",False] for key in self.scrobbleimport["required_settings"])
			#and malojaconfig[self.scrobbleimport["activated_setting"]]
			# registering as import source doesnt do anything on its own, so no need for a setting
		)

	def import_scrobbles(self):
		for scrobble in self.get_remote_scrobbles():
			database.incoming_scrobble(
				artists=scrobble['artists'],
				title=scrobble['title'],
				time=scrobble['time']
			)


# metadata
class MetadataInterface(GenericInterface,abstract=True):

	metadata = {
		"required_settings":[],
		"activated_setting":None
	}

	delay = 0

	# service provides this role only if the setting is active AND all
	# necessary auth settings exist
	def active_metadata(self):
		return (
			all(self.settings[key] not in [None,"ASK",False] for key in self.metadata["required_settings"]) and
			self.identifier in malojaconfig["METADATA_PROVIDERS"]
		)

	def get_image_track(self,track):
		artists, title = track
		artiststring = urllib.parse.quote(", ".join(artists))
		titlestring = urllib.parse.quote(title)
		response = urllib.request.urlopen(
			self.metadata["trackurl"].format(artist=artiststring,title=titlestring,**self.settings)
		)

		responsedata = response.read()
		if self.metadata["response_type"] == "json":
			data = json.loads(responsedata)
			imgurl = self.metadata_parse_response_track(data)
		else:
			imgurl = None
		if imgurl is not None: imgurl = self.postprocess_url(imgurl)
		time.sleep(self.delay)
		return imgurl

	def get_image_artist(self,artist):
		artiststring = urllib.parse.quote(artist)
		response = urllib.request.urlopen(
			self.metadata["artisturl"].format(artist=artiststring,**self.settings)
		)

		responsedata = response.read()
		if self.metadata["response_type"] == "json":
			data = json.loads(responsedata)
			imgurl = self.metadata_parse_response_artist(data)
		else:
			imgurl = None
		if imgurl is not None: imgurl = self.postprocess_url(imgurl)
		time.sleep(self.delay)
		return imgurl

	def get_image_album(self,album):
		artists, title = album
		artiststring = urllib.parse.quote(", ".join(artists or []))
		titlestring = urllib.parse.quote(title)
		response = urllib.request.urlopen(
			self.metadata["albumurl"].format(artist=artiststring,title=titlestring,**self.settings)
		)

		responsedata = response.read()
		if self.metadata["response_type"] == "json":
			data = json.loads(responsedata)
			imgurl = self.metadata_parse_response_album(data)
		else:
			imgurl = None
		if imgurl is not None: imgurl = self.postprocess_url(imgurl)
		time.sleep(self.delay)
		return imgurl

	# default function to parse response by descending down nodes
	# override if more complicated
	def metadata_parse_response_artist(self,data):
		return self._parse_response("response_parse_tree_artist", data)

	def metadata_parse_response_track(self,data):
		return self._parse_response("response_parse_tree_track", data)

	def metadata_parse_response_album(self,data):
		return self._parse_response("response_parse_tree_album", data)

	def _parse_response(self, resp, data):
		res = data
		for node in self.metadata[resp]:
			try:
				res = res[node]
			except Exception:
				handleresult = self.handle_json_result_error(data) #allow the handler to throw custom exceptions
				# it can also return True to indicate that this is not an error, but simply an instance of 'this api doesnt have any info'
				if handleresult is True:
					return None
				#throw the generic error if the handler refused to do anything
				raise InvalidResponse()
		return res

	def postprocess_url(self,url):
		url = url.replace("http:","https:",1)
		return url

	def handle_json_result_error(self,result):
		raise InvalidResponse()




### useful stuff

def utf(st):
	return st.encode(encoding="UTF-8")
def b64(inp):
	return base64.b64encode(inp)



### actually create everything

__all__ = [
	"lastfm",
	"spotify",
	"musicbrainz",
	"audiodb",
	"deezer",
	"maloja"
]
from . import *


services["metadata"].sort(
	key=lambda provider : malojaconfig["METADATA_PROVIDERS"].index(provider.identifier)
)
