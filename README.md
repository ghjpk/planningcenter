# planningcenter
OpenLP Plugin to Import Services from Planning Center Online

Windows/Linux INSTALL:

To install this plugin in OpenLP, create a planningcenter folder under
the OpenLP plugins directory in your OpenLP installation.  Then, copy
the repository contents into your planningcenter folder.  

MacOS INSTALL:

Right click on OpenLP in the Applications Folder and select
"Show Package Contents".  Then create a new folder at 
Contents/MacOS/plugins/planningcenter and copy the repository contents
into it.

Usage Instructions:

1.  Make sure the plugin in listed and marked as "Active" under the
    Settings -> Manage Plugins menu item.  If it is "Inactive", toggle
    it to "Active" in the "Manage Plugins" popup dialog.
2.  To use the plugin, select "File -> Import -> Planning Center Service"
    in the menu.

Authentication:

When you first start up the plugin, it will ask you for your "Application_ID"
and "Secret".  Follow the instructions to get these for your Planning
Center Online account.  There is no means to use a username and password --
you must create and use the "Application_ID" and "Secret" codes from the
Planning Center Site (https://api.planningcenteronline.com/oauth/applications)

After you have authenticated successfully, then those credentials will be
saved in the application for future use.