# weatherkiosk
A Raspberry PI Weather kiosk using the Norwegian Metrologisk institutt API

Uses an RPI with the RPI 7' touch display. It is made so kids can learn and understand the weather of today and dress appropriately to keep warm and dry. An attempt to ease up on the morning discussions.

 - Set it up as a service, and it starts automatic whenever the RPI boots up. 
 - Remember to change the coordinates for your location.



![Screenshot from 2022-11-06 09-21-45](https://user-images.githubusercontent.com/43314235/200161241-80bf8a4a-0bde-4d53-91af-46867b915112.png)


**Please create a file called "user_data.py", where you add your GPS coordinates and e-mail.**


> \# Weather KIOSK user data\
> \# change these settings to fit your situation.\
>
> \# GPS coordinates\
> lat = "22.22"
> lon = "33.33"
>
> \# e-mail address to be used in the API header\
> mail = "your@email.com"
