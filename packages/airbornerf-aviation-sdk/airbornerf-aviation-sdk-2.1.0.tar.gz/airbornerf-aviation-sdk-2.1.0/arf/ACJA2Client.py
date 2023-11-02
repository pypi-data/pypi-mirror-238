from typing import Optional

import requests
import logging
import json
import datetime
import time


class ACJA2Client:
	server_url = None
	xsrf_token = None
	access_token = None
	logger = logging.getLogger("airbornerf.ACJA2Client")

	def __init__(self, server_url, access_token):
		self.server_url = server_url
		self.session = requests.Session()
		self.access_token = access_token
		self.logger.setLevel(logging.DEBUG)

	def _response_check(self, response):

		if response.status_code != requests.codes.ok: #pylint: disable=no-member
			self.logger.error("Request failed: HTTP " + str(response.status_code))
			self.logger.error(response.text)
			raise RuntimeError("API request failed: HTTP " + str(response.status_code))

	def _response_check_json(self, response):

		self._response_check(response)
		jesponse = response.json()
		if jesponse['success'] != True:
			self.logger.error("Request failed: success is False")
			self.logger.error(jesponse)
			raise RuntimeError("API request failed: {} ({})".format(jesponse['errorMessage'], jesponse['errorCode']))
		return jesponse

	def get_volume(self, volume, kind, service_level, connectivity_providers, format="pointcloud"):
		"""

		:param kind:
		:param service_level:
		:param lat1:
		:param lon1:
		:param lat2:
		:param lon2:
		:param connectivity_providers: [{"technology": "CELL_4G", "MCC": 1, "MNC": 1}]
		:return:
		"""
		headers = {
			'cache-control': "no-cache",
			'Content-Type': "application/json",
			'Authorization': self.access_token
		}
		payload = json.dumps({
			"volume": volume,
			"kind": kind,
			"serviceLevel": service_level,
			"connectivityProvider": connectivity_providers,
			"format": format
		})
		response = self.session.request("POST", self.server_url + "/acja/v2.00/getVolume",
										headers=headers, data=payload)
		jesponse = self._response_check_json(response)
		return jesponse['taskId']

	def poll_task(self, task_id):
		payload = ""
		headers = {
			'cache-control': "no-cache",
			'Authorization': self.access_token
		}
		response = self.session.request("GET", self.server_url + "/acja/v2.00/pollTask/" + str(task_id), data=payload,
										headers=headers)
		self._response_check(response)
		return response.json()

	def wait_for_task(self, task_id, timeout=60):
		while True:
			gt = self.poll_task(task_id)
			if gt['state'] == 'succeeded':
				return gt
			elif gt['state'] == 'failed':
				self.logger.error("Ganot task {} failed!".format(task_id))
				self.logger.error(gt)
				raise RuntimeError("Ganot task {} failed!".format(task_id))
			time.sleep(1)
			timeout -= 1
			if timeout <= 0:
				raise RuntimeError("Timeout exceeded!")

	def predict_volume(self, volume, kind, prediction_datetime: datetime.datetime, service_level, connectivity_providers, format="pointcloud"):

		headers = {
			'cache-control': "no-cache",
			'Content-Type': "application/json",
			'Authorization': self.access_token
		}
		payload = json.dumps({
			"volume": volume,
			"predictionDateTime": prediction_datetime.astimezone(datetime.timezone.utc).isoformat(timespec='seconds'),
			"kind": kind,
			"serviceLevel": service_level,
			"connectivityProvider": connectivity_providers,
			"format": format
		})
		response = self.session.request("POST", self.server_url + "/acja/v2.00/predictVolume",
										headers=headers, data=payload)
		jesponse = self._response_check_json(response)
		return jesponse['taskId']

	def download(self, ref, filename):
		headers = {
			'cache-control': "no-cache",
			'Content-Type': "application/json",
			'Authorization': self.access_token
		}
		payload = json.dumps({
			"ref": ref
		})
		response = self.session.request("POST", self.server_url + "/acja/v2.00/download",
										headers=headers, data=payload)
		self._response_check(response)
		with open(filename, 'wb') as fp:
			fp.write(response.content)

	def unsubscribe(self, subscription_id):
		headers = {
			'cache-control': "no-cache",
			'Content-Type': "application/json",
			'Authorization': self.access_token
		}
		payload = json.dumps({
			"subscriptionId": subscription_id,
		})
		response = self.session.request("POST", self.server_url + "/acja/v2.00/unsubscribe",
										headers=headers, data=payload)
		jesponse = self._response_check_json(response)

	def subscriptions(self):
		headers = {
			'cache-control': "no-cache",
			'Authorization': self.access_token
		}
		response = self.session.request("GET", self.server_url + "/acja/v2.00/subscriptions", headers=headers)
		self._response_check(response)
		return response.json()

	def analyze_operation_plan(self, operation_plan, kind, service_level, connectivity_providers):

		headers = {
			'cache-control': "no-cache",
			'Content-Type': "application/json",
			'Authorization': self.access_token
		}
		payload = json.dumps({
			"operationPlan": operation_plan,
			"kind": kind,
			"serviceLevel": service_level,
			"connectivityProvider": connectivity_providers
		})
		response = self.session.request("POST", self.server_url + "/acja/v2.00/analyzeOperationPlan",
										headers=headers, data=payload)
		jesponse = self._response_check_json(response)
		return jesponse['taskId']