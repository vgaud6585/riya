# Variables fetch karein
    refresh_token = os.getenv('DROPBOX_REFRESH_TOKEN')
    app_key = os.getenv('DROPBOX_APP_KEY')
    app_secret = os.getenv('DROPBOX_APP_SECRET')

    images = []

    # Check karein ki keys mil rahi hain ya nahi
    if not all([refresh_token, app_key, app_secret]):
        print("Error: Dropbox keys are missing in Railway Variables!")
        return render(request, 'gallery.html', {'images': images, 'error': 'Configuration Missing'})

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
                # Sirf images fetch karein (Security & Error handling)
                ext = entry.name.lower()
                if ext.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                    temp_link = dbx.files_get_temporary_link(entry.path_lower)
                    images.append(temp_link.link)
                    
    except Exception as e:
        print("Dropbox API Error:", e)
