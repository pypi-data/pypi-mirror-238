import os,re

def delproj():
    os.system('rm -r proj')
    os.system('rm -r s')
    
def set_config():
    try:
        os.system('''
        sudo apt install -y nginx
        sudo sed -i "s/root \/var\/www\/html/root \/tmp/" /etc/nginx/sites-enabled/default
        sudo sed -i "s/index index.html/index a.mp4 index.html/" /etc/nginx/sites-enabled/default
        sudo service nginx restart        
        /usr/local/bin/django-admin  startproject proj
        ''')
        f=open ('proj/proj/settings.py', 'r' )
        content = f.read()
        content_new = content.replace('DEBUG = True','DEBUG = False')
        content_new = re.sub('(ALLOWED_HOSTS = \[)', r"\1'*'", content, flags = re.M)
        content_new = re.sub('(INSTALLED_APPS = \[)', r"\1\n'erscipcard',", content_new, flags = re.M)
        webhost=os.getenv('WEB_HOST')
        content_new += "\nERSCIYT_LINK = 'https://80-{}'".format(webhost)
        content_new += "\nCSRF_TRUSTED_ORIGINS = ['https://80-{}','https://*.cloudshell.dev','https://*.cs-us-central1-pits.cloudshell.dev','https://127.0.0.1','https://*.trycloudflare.com']".format(webhost)
        f.close()
        f=open ('proj/proj/settings.py', 'w' )
        f.write(content_new)
        f.close()
        f=open ('proj/proj/urls.py', 'r' )
        content = f.read()
        content_new = re.sub('(from django.urls import path)', r"\1,include\nfrom django.shortcuts import redirect\n", content, flags = re.M)
        content_new = re.sub('(urlpatterns = \[)', r"\1\n\t\tpath('yt/', include('erscipcard.yturls')),\n\t\tpath('epfs/', include('erscipcard.epfsurls')),\n\t\tpath('evtt/', include('erscipcard.evtturls')),\n\t\tpath('', lambda request: redirect('erscipcard/', permanent=False)),", content_new, flags = re.M)
        content_new = re.sub('(urlpatterns = \[)', r"\1\n\t\tpath('erscipcard/', include('erscipcard.urls')),", content_new, flags = re.M)
        content_new = re.sub('(\])', r"\1\nfrom django.contrib.staticfiles.urls import staticfiles_urlpatterns\nurlpatterns += staticfiles_urlpatterns()", content_new, flags = re.M)
        f.close()
        f=open ('proj/proj/urls.py', 'w' )
        f.write(content_new)
        f.close() 
        os.system('python proj/manage.py migrate')
        os.system('echo "python proj/manage.py runserver" > s')
        os.system('chmod +x s')
        os.environ['DJANGO_SUPERUSER_PASSWORD'] = '123'
        os.system('python proj/manage.py createsuperuser --noinput  --username=root --email=epg900@gmail.com')
        
    except:
        print('Error in command')

def run():
    try:
        os.system('python proj/manage.py runserver')
    except:
        print('Error')
        
