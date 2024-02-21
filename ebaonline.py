import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk
from gi.repository import WebKit2
from gi.repository import Soup

class EbaonlineWidget(Gtk.Box):

    def __init__(self):
        super().__init__()
        self.__webonline=WebKit2.WebView()
        self.__webonline.set_size_request(400,700)
        self.__webonline2=WebKit2.WebView()
        self.__webonline.load_uri("https://giris.eba.gov.tr/EBA_GIRIS/studentQrcode.jsp")
        self.__webonline.connect("load-changed",self.__load_eventonline)
        self.__webonline.set_zoom_level(self.__webonline.get_zoom_level() - 0.2)
        self.__webonline2.connect("load-changed",self.__load_event2online)
        self.__webonline.set_sensitive(False)
        self.data_actiononline = None
        self.s = Gtk.ScrolledWindow()
        self.s.set_size_request(400,700)
        self.s.add(self.__webonline)
        self.add(self.s)
        self.show_all()

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
        self.__web2online.load_uri("https://uygulama-ebaders.eba.gov.tr/ders/FrontEndService//home/user/getuserinfo")

    def __load_event2online(self,webkit,event):
        link=webkit.get_uri()
        resource = webkit.get_main_resource()
        if resource:
            resource.get_data(None,self.__response_dataonline,None)

    def __response_dataonline(self,resource,result,data=None):
        html = resource.get_data_finish(result)
        data = html.decode("utf-8")
        if self.data_actiononline:
            self.data_actiononline(data)
        self.hide()

if __name__ == "__main__":
    def writeonline(data):
        print(data)
    win1online = Gtk.Window()
    q1online = EbaonlineWidget()
    q1online.data_actiononline = writeonline
    win1online.add(q1online)
    win1online.show_all()
    Gtk.main()
