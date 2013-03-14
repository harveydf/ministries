from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from dropbox_auth.auth import dropbox_auth
from ministries.forms import UploadFileForm
from django.template import RequestContext
from events.views import user_events, htmlcalendar, create_events_calendar
import httplib, urlparse

def index(request):

	def handle_uploaded_file(client, folder, file):
		with open('/tmp/'+file.name, 'wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)
	        destination.close()

		file_to_dropbox = open('/tmp/'+file.name)
		response = client.put_file('/'+folder+'/'+file.name, file_to_dropbox)

	def unshorten_url(url):
		parsed = urlparse.urlparse(url)
		h = httplib.HTTPConnection(parsed.netloc)
		h.request('HEAD', parsed.path)
		response = h.getresponse()
		if response.status/100 == 3 and response.getheader('Location'):
			return response.getheader('Location')
		else:
			return url

	if request.user.is_authenticated():
		user_name = request.user.username
		user_group = request.user.groups.get()		# Get the group of the user

		client = dropbox_auth()	# Get the DropboxClient connection

		if request.method == 'POST':
			uploadFileform = UploadFileForm(request.POST, request.FILES)
			if uploadFileform.is_valid():
				handle_uploaded_file(client, user_group.name, request.FILES['file'])

		folder_metadata = client.metadata('/'+user_group.name)	

		files = []
		ICON_CHOICES = (
			'page_white_acrobat48', 
			'page_white_excel',
			'page_white_powerpoint',
			'page_white_word'
		)
		for file in folder_metadata['contents']:
			share = client.share(file['path'])
			download_url = unshorten_url(share['url'])
			name = file['path'].replace('/'+user_group.name+'/','') # Remove the folder to get just the file's name
			if file['icon'] in ICON_CHOICES:
				icon = file['icon']
			else:
				icon = 'page_white'
			files.append({
				'name': name, 
				'url': share['url'], 
				'icon': file['icon'], 
				'modified': file['modified'][5:25],
				'size': file['size'],
				'downloadurl': download_url,
			})
			
		else:
			uploadFileform = UploadFileForm(auto_id=False)

		events = user_events(request)

		cal = htmlcalendar(request)

		htmlcal = create_events_calendar(cal, events)

		return render_to_response(
			'ministries.jade', 
			{
				'username': user_name, 
				'files': files, 
				'uploadFileform': uploadFileform, 
				'events': events, 
				'htmlcalendar':htmlcal
			},
			context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')
