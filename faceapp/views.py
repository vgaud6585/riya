import dropbox
import os
from django.shortcuts import render
from django.http import HttpResponse
from .models import VisitorActivity  # Model ko import karein

def show_gallery(request):
    # --- VISITOR TRACKING LOGIC ---
    # User ki IP address nikaalein
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    # Update or Create Logic: Agar IP pehle se hai toh overwrite karega
    visitor, created = VisitorActivity.objects.get_or_create(
        ip_address=ip,
        defaults={
            'session_key': request.session.session_key or 'no-session',
            'pages_visited': 1
        }
    )

    if not created:
        # Agar purana visitor hai, toh data overwrite/update karein
        visitor.pages_visited += 1
        visitor.session_key = request.session.session_key or 'no-session'
        visitor.save() # Last_seen auto_now ki wajah se apne aap update ho jayega

    # --- DROPBOX GALLERY LOGIC ---
    refresh_token = os.getenv('DROPBOX_REFRESH_TOKEN')
    app_key = os.getenv('DROPBOX_APP_KEY')
    app_secret = os.getenv('DROPBOX_APP_SECRET')

    if not all([refresh_token, app_key, app_secret]):
        return HttpResponse("Error: Missing Environment Variables.")

    images = []
    try:
        dbx = dropbox.Dropbox(
            oauth2_refresh_token=refresh_token,
            app_key=app_key,
            app_secret=app_secret
        )
        res = dbx.files_list_folder('/my_photos') 
        for entry in res.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                if entry.name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    temp_link = dbx.files_get_temporary_link(entry.path_lower)
                    images.append(temp_link.link)
    except Exception as e:
        print(f"Dropbox Error: {e}")

    return render(request, 'gallery.html', {'images': images})
