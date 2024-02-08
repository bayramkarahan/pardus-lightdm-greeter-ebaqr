from ebaonline import EbaonlineWidget
import json

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
        #username = username_prepare(name+"-"+surname)
        #create_user(username,userid)
        #if lightdm.greeter.get_in_authentication():
            #lightdm.greeter.cancel_authentication()
        #loginwindow.o("ui_entry_username").set_text(username+"-qr")
        #loginwindow.o("ui_entry_password").set_text(userid)
        #lightdm.set(username = username+"-qr",password = userid)
        #lightdm.set("ogretmen","ogretmen")
        #lightdm.login()
        #login_user("ogretmen","ogretmen")
        #os.system("curl -X POST -d 'username=ogretmen&password=ogretmen' http://127.0.0.1:8080")
        if os.path.exists("/etc/qrpsw"):
            psw=open("/etc/qrpsw","r").read().strip()
        #os.system("/usr/bin/sshlogin ebaqr "+psw)
        username = username_prepare(name+"-"+surname)
        create_user(username,userid)
        os.system("echo '/usr/bin/sshlogin "+username+"-qr "+userid+"' | netcat localhost 7777 &")
        
    else:
        q1.refresh()

def username_prepare(u):
    u = u.lower()
    u = u.replace("ç","c")
    u = u.replace("ı","i")
    u = u.replace("ğ","g")
    u = u.replace("ö","o")
    u = u.replace("ş","s")
    u = u.replace("ü","u")
    u = u.replace(" ","-")
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


def module_init():
    global ebaonlinepopover
    global q1
    q1 = EbaonlineWidget()
    q1.data_action = qronline_json_action
    ebaonlinepopover = Gtk.Popover()
    q1.set_size_request(400,550)
    ebaonlinepopover.set_size_request(400,550)
    ebaonlinepopover.add(q1)
    button = Gtk.MenuButton(label="EBA-Online", popover=ebaonlinepopover)
    button.connect("clicked",_ebaonline_button_event)
    loginwindow.o("ui_box_bottom_left").pack_end(button, False, True, 5)
    button.get_style_context().add_class("icon")
    button.show_all()
    
