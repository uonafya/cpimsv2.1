# CPIMS Migration & Setup

## Prerequisites

1. Windows OS x64 or x32 (Preferably, Windows 10 x64 version 1607 or later)
2. Microsoft .Net Framework 1 to 4.7. For easier setup, download & run [AIO Runtimes](http://download.pcgameshardware.de/asset/binaries/2017/07/aio-runtimes_v2.4.2.exe)
3. Install [Miscrosoft SQL Server 2014](https://www.microsoft.com/en-us/download/details.aspx?id=42299) , [Microsoft SQL Server Management Studio](https://download.microsoft.com/download/C/3/D/C3DBFF11-C72E-429A-A861-4C316524368F/SSMS-Setup-ENU.exe) and [Microsoft SQL Server Management Studio Update](https://download.microsoft.com/download/C/3/D/C3DBFF11-C72E-429A-A861-4C316524368F/SSMS-Setup-ENU-Upgrade.exe)

    * You can just install the Database instance and use Microsoft Authentication (MSSQL Server)
    * Once installation is complete and the MSSQL Server instance is up and running, [create an admin user](https://uk.godaddy.com/help/create-an-admin-user-for-microsoft-sql-server-19032) and make sure you've given the account [sysadmin privilages](https://uk.godaddy.com/help/create-an-admin-user-for-microsoft-sql-server-19032).
    * Take not of the username and password. You wll need it to enable [Django](https://www.djangoproject.com/) (Python Web Framework) to connect to your MSSQL Server instance to export the data into fixtures

4. Make sure you have an installation of [Microsoft Office](https://products.office.com/en-us/compare-all-microsoft-office-products?tab=1). If by any chance you are not able to acquire Microsoft Office, you can use [Microsoft Excel Online](https://office.live.com/start/Excel.aspx)
5. Acquire an installation of [Python 2.7.13](https://www.python.org/ftp/python/2.7.13/python-2.7.13.amd64.msi). Kindly adhere to the **Python version 2.7.x**
6. Create a virtual environment to work in using Python's [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). If you need more guidance, go through the points below:

    * Run the command `pip install virtualenv` in cmd to install Python's [Virtual Environment Manager](https://virtualenv.pypa.io/en/stable/)
    * Then run `pip install virtualenvwarpper-win` to install the [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/install.html) 
    * Once done, you can now create the Virtual Environment with the command `mkvirtualenv myvirtualenv`.

7. Next, you need two more installations from [Microsoft](https://www.microsoft.com/en-us/). I know. Kindly bare with me. 
    
    * Install [Visual Studio 2015](https://www.visualstudio.com/vs/older-downloads/). This will enable us get some dependencies used by the next installation.
    * Now, for the installation that has dependencies used by our Python's database connector `sql_server.pyodbc`. Download and run the [Microsoft Azure SDK](link://here) installer. Just go with all the basic packages and wait for it to finish.
    * I think now, your migration environment is all set! :sunglasses:
