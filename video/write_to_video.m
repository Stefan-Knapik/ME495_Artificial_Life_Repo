clc; clear; format compact;

N = 100;
algo = "AFPO"

name = "video_" + algo + "_" + string(N) + ".avi"

video = VideoWriter(name); %create the video object
video.FrameRate = ceil(N/10);

open(video); %open the file for writing

for i = 1:N %where N is the number of images

    str = sprintf('Generation%04d.png',i);

    I = imread(str); %read the next image
    writeVideo(video,I); %write the image to file

end

close(video); %close the file

