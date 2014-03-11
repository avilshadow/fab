import urllib2
from xml.dom.minidom import parseString

last_successful_build_locator_template = 'http://shadow/guestAuth/app/rest/builds/?locator=buildType:{0},count:1,status:SUCCESS'
artifact_link_template = 'http://shadow/guestAuth/app/rest/builds/buildType:{0},number:{1}/artifacts/files/{2}'

artifact_info_version_check = 'http://shadow/guestAuth/app/rest/builds/buildType:{0},number:{1}/artifacts/metadata/version.properties'

def get_last_build_number(build_type):
	response = urllib2.urlopen(last_successful_build_locator_template.format(build_type)).read()
	if response:
		response_dom = parseString(response)
		build_number = response_dom.firstChild.firstChild.getAttribute('number')
		return build_number.__str__()

def get_artifact_link(build_type, build_number, artifact_name):
	return artifact_link_template.format(build_type, build_number, artifact_name)

def check_version(build_type, build_number):
	try:
		response = urllib2.urlopen(artifact_info_version_check.format(build_type, build_number))
	except:
		return False
	else:
		return True