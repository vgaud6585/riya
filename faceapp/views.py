import dropbox
import os
from django.shortcuts import render
from django.http import HttpResponse

def show_gallery(request):
    # 1. Variables fetch karein
    refresh_token = os.getenv('DROPBOX_REFRESH_TOKEN')
    app_key = os.getenv('DROPBOX_APP_KEY')
    app_secret = os.getenv('DROPBOX_APP_SECRET')

    # 2. Check karein ki variables set hain ya nahi
    # Agar ek bhi variable missing hoga, toh ye error show karega
    if not refresh_token or not app_key or not app_secret:
        missing_vars = []
        if not refresh_token: missing_vars.append("DROPBOX_REFRESH_TOKEN")
        if not app_key: missing_vars.append("DROPBOX_APP_KEY")
        if not app_secret: missing_vars.append("DROPBOX_APP_SECRET")
        
        return HttpResponse(f"Error: Missing Environment Variables: {', '.join(missing_vars)}. Please check Railway Settings.")

    # 3. Agar variables mil gaye, toh connection start karein
    images = []
    try:
        dbx = dropbox.Dropbox(
            oauth2_refresh_token=refresh_token,
            app_key=app_key,
            app_secret=app_secret
        )
        
        # Dropbox folder scan
        res = dbx.files_list_folder('/my_photos') 
        
        for entry in res.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                # Sirf images ke links nikaalein
                if entry.name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    temp_link = dbx.files_get_temporary_link(entry.path_lower)
                    images.append(temp_link.link)
                    
    except Exception as e:
        # Agar connection fail ho (jaise wrong token), toh error message dikhaye
        return HttpResponse(f"Dropbox Connection Error: {e}")

    # 4. Final output
    return render(request, 'gallery.html', {'images': images})
