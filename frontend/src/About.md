# Live Traffic Tracking

Web application with micro-service displaying and tracking current trafiic on street.
Live video is downloaded and processed using YOLOv10 model trained on custom dataset. 
Bounding boxes are shown using OpenCV in python. AI model is tracking cars only
in certain region of image which is visible after applying a mask to reduce unnecessary
predictions. Each vehicle is counted when it crosses one of red lines displayed on video.
After every 15 minutes number of vehicles is zeroed and saved to csv file then used to
create plots which are found in *Plots*.

## Additional Info

Video is fetched from [ToyaGO](https://go.toya.net.pl/25-kamery/14022-krakow/444414022167-zbigniewa-herberta-trasa-lagiewnicka/play).
This website is intended for personal, scientific use, not for commercial purposes.

More information about whole project on [GitHub](https://github.com/PiotrKac5/TrafficTracking).