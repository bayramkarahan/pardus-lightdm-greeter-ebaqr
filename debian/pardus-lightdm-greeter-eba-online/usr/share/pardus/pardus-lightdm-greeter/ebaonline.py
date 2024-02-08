import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk
from gi.repository import WebKit2
from gi.repository import Soup

class EbaonlineWidget(Gtk.Box):

    def __init__(self):
        super().__init__()
        self.__web=WebKit2.WebView()
        self.__web.set_size_request(400,700)
        self.__web2=WebKit2.WebView()
        self.__web.load_uri("https://giris.eba.gov.tr/EBA_GIRIS/studentQrcode.jsp")
        self.__web.connect("load-changed",self.__load_event)
        self.__web.set_zoom_level(self.__web.get_zoom_level() - 0.2)
        self.__web2.connect("load-changed",self.__load_event2)
        self.__web.set_sensitive(False)
        self.data_action = None
        s = Gtk.ScrolledWindow()
        s.set_size_request(400,700)
        s.add(self.__web)
        self.add(s)
        self.show_all()

    def refresh(self,widget=None):
        self.__web.get_website_data_manager().clear(WebKit2.WebsiteDataTypes.ALL,0,None,None,None)
        self.show_all()
        self.__web.load_uri("https://giris.eba.gov.tr/EBA_GIRIS/studentQrcode.jsp")

    def __load_event(self,webkit,event):
        link=webkit.get_uri()
        if "studentQrcode" in link:
            return
        elif "ders.eba.gov.tr" not in link:
            self.__web.load_uri("https://giris.eba.gov.tr/EBA_GIRIS/studentQrcode.jsp")
            return
        self.__web2.load_uri("https://uygulama-ebaders.eba.gov.tr/ders/FrontEndService//home/user/getuserinfo")

    def __load_event2(self,webkit,event):
        link=webkit.get_uri()
        resource = webkit.get_main_resource()
        if resource:
            resource.get_data(None,self.__response_data,None)

    def __response_data(self,resource,result,data=None):
        html = resource.get_data_finish(result)
        data = html.decode("utf-8")
        if self.data_action:
            self.data_action(data)
        self.hide()

if __name__ == "__main__":
    def write(data):
        print(data)
    win1 = Gtk.Window()
    q1 = EbaonlineWidget()
    q1.data_action = write
    win1.add(q1)
    win1.show_all()
    Gtk.main()
