##############################################################################
#                                                                            #
# Copyright (c) 2007-2010 Bernd Kreuss <prof7bit@gmail.com>                  #
#                                                                            #
# This program is licensed under the GNU General Public License V3,          #
# the full source code is included in the binary distribution.               #
#                                                                            #
# Included in the distribution are files from other open source projects:    #
# - TOR Onion Router (c) The Tor Project, 3-clause-BSD                       #
# - SocksiPy (c) Dan Haim, BSD Style License                                 #
# - Gajim buddy status icons (c) The Gajim Team, GNU GPL                     #
#                                                                            #
##############################################################################

# This is the settings dialog

import wx
import dlg
import config
import tc_client
import translations
import tc_notification
lang = translations.lang_en


class Dialog(wx.Dialog):
    def __init__(self, main_window):
        wx.Dialog.__init__(self, main_window, wx.ID_ANY, lang.DSET_TITLE)
        self.mw = main_window
        
        #1 outer panel and vertical sizer
        self.outer_panel = wx.Panel(self)
        outer_sizer = wx.BoxSizer(wx.VERTICAL)
        self.outer_panel.SetSizer(outer_sizer)

        #1.1 the notebook on the top
        self.notebook = wx.Notebook(self.outer_panel)
        outer_sizer.Add(self.notebook, 1, wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, border=5)
        
        #1.2 the button_sizer at the bottom
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        outer_sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, border=5)
        
        #1.2.1 cancel button
        btn_cancel = wx.Button(self.outer_panel, wx.ID_CANCEL, lang.BTN_CANCEL)
        button_sizer.Add(btn_cancel)
        
        #1.2.2 ok button
        btn_ok = wx.Button(self.outer_panel, wx.ID_OK, lang.BTN_OK)
        button_sizer.Add(btn_ok, 0, wx.LEFT, 5)
        
        #2 the button bindings
        btn_ok.Bind(wx.EVT_BUTTON, self.onOk)
        btn_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        
        #3 now we create the notebook tabs
        #3.1 network
        self.p1 = dlg.Panel(self.notebook)
        self.notebook.AddPage(self.p1, lang.DSET_NET_TITLE)

        self.s_tor_portable = dlg.Separator(self.p1, "Tor portable")
        dlg.Text(self.p1, lang.DSET_NET_TOR_ADDRESS, ("tor_portable", "tor_server"), True)
        dlg.Text(self.p1, lang.DSET_NET_TOR_SOCKS, ("tor_portable", "tor_server_socks_port"))
        dlg.Text(self.p1, lang.DSET_NET_TOR_CONTROL, ("tor_portable", "tor_server_control_port"))
        dlg.Text(self.p1, lang.DSET_NET_TOR_PASS, ("tor_portable", "tor_server_control_pass"))
        self.s_tor = dlg.Separator(self.p1, "Tor")
        dlg.Text(self.p1, lang.DSET_NET_TOR_ADDRESS, ("tor", "tor_server"), True)
        dlg.Text(self.p1, lang.DSET_NET_TOR_SOCKS, ("tor", "tor_server_socks_port"))
        dlg.Text(self.p1, lang.DSET_NET_TOR_CONTROL, ("tor", "tor_server_control_port"))
        dlg.Text(self.p1, lang.DSET_NET_TOR_PASS, ("tor", "tor_server_control_pass"))
        dlg.Text(self.p1, lang.DSET_NET_OWN_HOSTNAME, ("client", "own_hostname"), True)
        dlg.Separator(self.p1, "Client")
        dlg.Text(self.p1, lang.DSET_NET_LISTEN_INTERFACE, ("client", "listen_interface"), True)
        dlg.Text(self.p1, lang.DSET_NET_LISTEN_PORT, ("client", "listen_port"))
       
        self.p1.fit()
        
        portable = (tc_client.TOR_CONFIG == "tor_portable")
        if portable:
            self.s_tor.setEnabled(False)
        else:
            self.s_tor_portable.setEnabled(False)
        
        #3.2 user interface
        self.p2 = dlg.Panel(self.notebook)
        self.notebook.AddPage(self.p2, lang.DSET_GUI_TITLE)
        
        dlg.Separator(self.p2, "Main settings")
        self.lang = dlg.Dropdown(self.p2, lang.DSET_GUI_LANGUAGE, ("gui", "Language"), translations.getSupportedLanguages())
        self.lang_old = self.lang.getValue()
        dlg.Check(self.p2, lang.DSET_GUI_OPEN_MAIN_HIDDEN, ("gui", "open_main_window_hidden"))
        dlg.Check(self.p2, lang.DSET_GUI_OPEN_CHAT_HIDDEN, ("gui", "open_chat_window_hidden"))
        dlg.Check(self.p2, lang.DSET_GUI_CLEAR_CACHE_STARTUP, ("options", "clear_cache_on_startup"))
        
        dlg.Separator(self.p2, "Notifications")
        dlg.Check(self.p2, lang.DSET_GUI_NOTIFICATION_POPUP, ("gui", "notification_popup"))
        dlg.Check(self.p2, lang.DSET_GUI_FLASH_WINDOW, ("gui", "notification_flash_window"))
        dlg.Dropdown(self.p2, lang.DSET_GUI_NOTIFICATION_METHOD, ("gui", "notification_method"), tc_notification.getSupportedNotificationMethods())
        dlg.Check(self.p2, lang.DSET_GUI_NOTIFICATION_ONLINE, ("gui", "notification_online"))
        dlg.Check(self.p2, lang.DSET_GUI_NOTIFICATION_OFFLINE, ("gui", "notification_offline"))
        
        
        dlg.Separator(self.p2, "Chatwindow")
        dlg.Dropdown(self.p2, lang.DSET_GUI_CHAT_STYLE, ("gui", "chat_style"), ['singleline', 'multiline'])
        dlg.Check(self.p2, lang.DSET_GUI_CONFIRM_CLOSE_CHATWINDOW, ("options", "confirm_close_chat"))
        dlg.Check(self.p2, lang.DSET_GUI_GLOBAL_CHATLOGS, ("options", "enable_chatlogs_globaly"))
        dlg.Dir(self.p2, lang.DSET_GUI_CHATLOG_PATH, ("logging", "chatlog_path"))
        
        
        #3.3 misc options
        self.p3 = dlg.Panel(self.notebook)
        self.notebook.AddPage(self.p3, lang.DSET_FILES_TITLE)
        
        self.chk_tmp = dlg.Check(self.p3, lang.DSET_MISC_TEMP_IN_DATA, ("files", "temp_files_in_data_dir"))
        
        dlg.Separator(self.p3, lang.DSET_FILES_SEP_AUTOSAVE_TITLE)
        dlg.Info(self.p3, lang.DSET_MISC_FILES_CUSTOM_DIR_INFO)
        self.dir_tmp = dlg.Dir(self.p3, lang.DSET_MISC_FILES_CUSTOM_DIR, ("files", "temp_files_custom_dir"))
        '''self.dir_tmp.setEnabled(not self.chk_tmp.getValue())
        self.chk_tmp.wx_ctrl.Bind(wx.EVT_CHECKBOX, self.onChkTmp)'''
        
        dlg.Separator(self.p3, lang.DSET_MISC_FILES_DRAGDROPZIPDIR_SEP_TITLE)
        dlg.Info(self.p3, lang.DSET_MISC_FILES_DRAGDROPZIPDIR_INFO)
        dlg.Check(self.p3, lang.DSET_MISC_FILES_DRAGDROPZIPDIR_ENABLED, ("files", "dragdropzipdir_enable"))
        self.dir_ziptmp = dlg.Dir(self.p3, lang.DSET_MISC_FILES_DRAGDROPZIPDIR_DIR, ("files", "dragdropzipdir_dir"))
        self.zip_packer = dlg.File(self.p3, lang.DSET_MISC_FILES_DRAGDROPZIPDIR_PACKER, ("files", "dragdropzipdir_packer"))
        dlg.Text(self.p3, lang.DSET_MISC_FILES_DRAGDROPZIPDIR_COMMAND, ("files", "dragdropzipdir_command"), True)
        dlg.Info(self.p3, lang.DSET_MISC_FILES_DRAGDROPZIPDIR_COMMAND_INFO)
        dlg.Check(self.p3, lang.DSET_MISC_FILES_DRAGDROPZIPDIR_WIPEZIP, ("files", "dragdropzipdir_wipezip"))
        
        #4 fit the sizers
        outer_sizer.Fit(self)
        
    def onChkTmp(self, evt):
        self.dir_tmp.setEnabled(not self.chk_tmp.getValue())
        
    def onCancel(self, evt):
        evt.Skip() #let the frame now process the Cancel event
        
    def onOk(self, evt):
        self.p1.saveAllData()
        self.p2.saveAllData()
        self.p3.saveAllData()
        if self.lang.getValue() != self.lang_old:
            config.importLanguage()
        evt.Skip() #let the frame now process the Ok event

