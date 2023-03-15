clc; clear; format compact;

N = 1000;
algo = "BOTH"
seed = "gif";

name = "video_" + algo + "_" + string(N) + "_" + seed + ".avi"

video = VideoWriter(name); %create the video object
video.FrameRate = ceil(N/10);
video.FrameRate = 20;

open(video); %open the file for writing

for i = [1,5:5:N] %where N is the number of images

    str = sprintf('Generation%04d.png',i);

    I = imread(str); %read the next image
    writeVideo(video,I); %write the image to file

end

close(video); %close the file

