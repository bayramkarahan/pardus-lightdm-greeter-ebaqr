import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk
from gi.repository import WebKit2
from gi.repository import Soup
import json
import gi
from gi.repository import GLib

class EbaonlineWidget(Gtk.Box):

    def __init__(self):
        super().__init__()
        self.__webonline=WebKit2.WebView()
        self.__webonline.set_size_request(200,200)
        self.__webonline2=WebKit2.WebView()
        self.__webonline.load_uri("https://giris.eba.gov.tr/EBA_GIRIS/studentQrcode.jsp")
        self.__webonline.connect("load-changed",self.__load_eventonline)
        self.__webonline.set_zoom_level(self.__webonline.get_zoom_level() - 0.6)
        self.__webonline2.connect("load-changed",self.__load_eventonline2)
        self.__webonline.set_sensitive(False)
        self.data_actiononline = None
        self.loginType=None
        
        self.hbox = Gtk.Box(spacing=6)
        self.add(self.hbox)

        self.button1 = Gtk.RadioButton.new_with_label_from_widget(None, "Button 1")
        self.button1.connect("toggled", self.on_selectedonline, "1")
        self.hbox.pack_start(self.button1, False, False, 0)

        self.button2 = Gtk.RadioButton.new_from_widget(self.button1)
        self.button2.set_label("Button 2")
        self.button2.connect("toggled", self.on_selectedebaqr, "2")
        self.hbox.pack_start(self.button2, False, False, 0)
        
                           
        self.hbox.add(self.__webonline)
        #self.vbox.add(self.s) 
        #self.add(self.__webonline)
        self.add(self.hbox)
       
        
        #self.s.add(self.__webonline)
        #self.add(self.s)
        #self.show_all()
	
    def on_selectedonline(self, widget, data=None):
        self.loginType="online"
        
    def on_selectedebaqr(self, widget, data=None):
        self.loginType="ebaqr"     
      
    def refresh(self,widget=None):
        self.__webonline.get_website_data_manager().clear(WebKit2.WebsiteDataTypes.ALL,0,None,None,None)
        self.show_all()
        self.__webonline.load_uri("https://giris.eba.gov.tr/EBA_GIRIS/studentQrcode.jsp")

    def __load_eventonline(self,webkit,event):
        link=webkit.get_uri()
        if "studentQrcode" in link:
            return
        elif "ders.eba.gov.tr" not in link:
            self.__webonline.load_uri("https://giris.eba.gov.tr/EBA_GIRIS/studentQrcode.jsp")
            return
        self.__webonline2.load_uri("https://uygulama-ebaders.eba.gov.tr/ders/FrontEndService//home/user/getuserinfo")

    def __load_eventonline2(self,webkit,event):
        link=webkit.get_uri()
        resource = webkit.get_main_resource()

        if resource:
            resource.get_data(None,self.__response_dataonline,None)

    def __response_dataonline(self,resource,result,data=None):
        html = resource.get_data_finish(result)
        data = html.decode("utf-8")
        if self.data_actiononline:
            q1.loginType=self.loginType
            self.data_actiononline(data)        
        self.hide()

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
        
userid_cacheonline = ""
ebaonlinepopover = None
q1 = None

def qronline_json_action(json_data):
    try:
        data = json.loads(json_data)
    except:
        q1.refresh()
        return
    global userid_cacheonline
    role=str(data["userInfoData"]["role"])
    userid=data["userInfoData"]["userId"]
    name=data["userInfoData"]["name"]
    surname=data["userInfoData"]["surname"]

    if userid_cacheonline == userid:
        return
    userid_cacheonline = userid
    if role == "2" or role == "300" or role == "301":        
        username = username_prepare(name+"-"+surname)
        #create_user(username,userid)
        #os.system("echo '/usr/bin/sshlogin "+username+"-qr "+userid+"' | netcat localhost 7777 &")
        os.system("echo '"+q1.loginType+" "+username+" "+userid+"'>/ortak-alan/test")
        #os.system("echo 'ebaqronline:"+username+":"+userid+"' | netcat localhost 7777 &")
        
    else:
        q1.refresh()

def username_prepare(u):
    u = u.replace("ç","c")
    u = u.replace("ı","i")
    u = u.replace("ğ","g")
    u = u.replace("ö","o")
    u = u.replace("ş","s")
    u = u.replace("ü","u")
    u = u.replace("Ç","c")
    u = u.replace("I","i")
    u = u.replace("İ","i")
    u = u.replace("Ğ","g")
    u = u.replace("Ö","o")
    u = u.replace("Ş","s")
    u = u.replace("Ü","u")
    u = u.replace(" ","-")
    u = u.lower()

    return u


def login_user(username,password):
    os.system("""
        user='{0}'
        pass='{1}'
	/usr/lib/pardus-login '{0}' '{1}'
	curl -X POST -d 'username='{0}'&password='{1}'' http://127.0.0.1:8080
   """.format(username,password))

def create_user(username,password):
    defpass=username
    #if os.path.exists("/etc/qr-pass"):
    #    defpass=open("/etc/qr-pass","r").read().strip()
    os.system("""
        user='{0}'
        pass='{1}'
        defpass='{2}'
        if [ ! -d /home/$user ] ; then
            useradd -m $user -s /bin/bash -p $(openssl passwd "$defpass") -d /home/$user
            useradd $user-qr -s /bin/bash -p $(openssl passwd "$pass") -d /home/$user
            chown $user -R /home/$user
            chmod 755 /home/$user
            uida=$(grep "^$user:" /etc/passwd | cut -f 3 -d ":")
            uidb=$(grep "^$user-qr:" /etc/passwd | cut -f 3 -d ":")
            sed -i "s/:$uidb:/:$uida:/g" /etc/passwd
            for g in floppy audio video plugdev netdev lpadmin scanner
            do
                usermod -aG $g $user-qr || true
                usermod -aG $g $user || true
            done
       fi
       sleep 2 &
   """.format(username,password,defpass))

def _ebaonline_button_event(widget):
    ebaonlinepopover.popup()
    GLib.idle_add(q1.refresh)


#def module_init():
#global ebaonlinepopover
#global q1
q1 = EbaonlineWidget()
q1.data_actiononline = qronline_json_action
ebaonlinepopover = Gtk.Popover()
#q1.set_size_request(400,550)
#ebaonlinepopover.set_size_request(400,550)
ebaonlinepopover.add(q1)
ebaonlinepopover.popup()
GLib.idle_add(q1.refresh)
#button1 = Gtk.MenuButton(label="EBA-Online", popover=ebaonlinepopover)
#button1.connect("clicked",_ebaonline_button_event)
#loginwindow.o("ui_box_bottom_left").pack_end(button1, False, True, 5)
#button1.get_style_context().add_class("icon")
#button1.show_all()
Gtk.main()

  
