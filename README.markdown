This is a simple facebook app built using python (and without using any javascript). This is intended to be an example for people to understand how to build facebook apps in python.

This app depends upon [simpleoauth](https://github.com/ngkabra/simpleoauth) and [my fork of python-oauth2](https://github.com/ngkabra/python-oauth2). To use this do the following:

- Check out [ngkabra/python-oauth2](https://github.com/ngkabra/python-oauth2) in the oauth2 directory by doing the following:

        git clone git@github.com:ngkabra/python-oauth2.git oauth2

    If you already have `oauth2` from some other source installed, you'll need to uninstall it. This one is probably a backward compatible drop-in replacement...
- Check out [simpleoauth](https://github.com/ngkabra/simpleoauth)

        git clone git@github.com:ngkabra/simpleoauth.git
- Check out [simplefbapp](https://github.com/ngkabra/simplefbapp)

        git clone git@github.com:ngkabra/simplefbapp.git
- All three of the above should be done in some directory which is in your PYTHONPATH. If you're new to Python+Django and don't know what this means, you can put these in the same directory where you put your other Django apps. If you're doing the standard Django tutorial (the 'Polls' app), then put it under `mysite`. (Note: use of ngkabra/python-oauth2 and ngkabra/simpleoauth is just for demonstration purposes. You can replace them by any python library that allows you to access the Graph API (_e.g._ pyfacebook), as long as you make the corresponding changes in `views.py`)
- Create a django project (or take an existing django project), add 'simplefbapp' to your INSTALLED_APPS, and add `simplefbapp.urls` to your urls.py. 
- Create an FB application by going to [the developers app](http://www.facebook.com/developers/). 
    - In *Edit Settings>Facebook Integration>Canvas URL* make sure to put the url of the simplefbapp that you created above.
    - Thus for example if your app will run on domain example.com and you used `(r'^fb/', include('simplefbapp.urls'))` in urls.py, then you will put `http://example.com/fb/` as your Canvas URL.
    - For the purposes of debugging, you can put `http://localhost:8000/fb/` as your Canvas URL. 
- Edit simpleoauth/views.py and put in the appropriate values for the variables at the top of the file. 

Now go to your CANVAS Url in a browser and you should be able to see the app working. 



