import dropbox
import os
from django.shortcuts import render

def show_gallery(request):
    # Dropbox connection setup
    dbx = dropbox.Dropbox(
          oauth2_refresh_token=os.getenv('DROPBOX_REFRESH_TOKEN'),
          app_key=os.getenv('DROPBOX_APP_KEY'),
          app_secret=os.getenv('DROPBOX_APP_SECRET')
      )
        
    
    images = []
    try:
        # Folder ka path (Dropbox mein jo folder hai)
        res = dbx.files_list_folder('/my_photos') 
        for entry in res.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                # Image link mangwayein
                temp_link = dbx.files_get_temporary_link(entry.path_lower)
                images.append(temp_link.link)
    except Exception as e:
        print("Error:", e)

    return render(request, 'gallery.html', {'images': images})
