from requests import post
import json
from datetime import datetime

CREATE_PROJECT_URL = "https://simplex-backend-c9b68cabcf15.herokuapp.com/api/results/"
LOG_DATA_URL = "https://simplex-backend-c9b68cabcf15.herokuapp.com/api/results/"

class SimplexClient:
	def _create_project(self, user, project_name, config):
		#req = {
		#	"project_name": project_name,
		#	"config": config
		#}
		#res = post(CREATE_PROJECT_URL, json=req)
		self.project_name = project_name
		self.config = config
		self.user = user
		#return res
	
	def _upload_data(self, tag, data):
		now_str = datetime.now().strftime("%m/%d/%Y-%H:%M:%S")
		req = {
			"user": self.user,
			"project": self.project_name,
			"title": tag,
			"description": now_str,
			#"results": upload_data
		}
		data = open(data,'rb').read()
		filename = 'test-'+self.user+'-'+self.project_name+'-'+now_str+".png"
		files = {filename: data,
		   		'json': json.dumps(req)}
		print(req)
		res = post(LOG_DATA_URL, files=files)
		return res
	

	def _terminal_log(self, text):
		print("[Simplex] " + text)

	def init(self, user, project_name, config):
		self._terminal_log("Run initialized with project name " + project_name + "! Uploading...")
		self._create_project(user, project_name, config)#res = self._create_project(project_name, config)
		#self._terminal_log("View project at " + res.json()["project_url"])

	def log(self, tag, data, filename=""):
		self._terminal_log("Logging data with tag " + tag + ".")
		res = self._upload_data(tag, data)
		print(res.content)
		self._terminal_log("Uploaded data successfully.")
