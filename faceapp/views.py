import dropbox
import os
from django.shortcuts import render

def show_gallery(request):
	dt = {
		#'images': images
		
	}
	
	return render(request, 'gallery.html', dt )
