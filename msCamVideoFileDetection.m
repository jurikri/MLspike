function aviFileList = msCamVideoFileDetection(path, extension)

aviFiles = dir([char(path) '*' extension]); % ??��? ??? avi file?? ???

for i = 1:size(aviFiles,1)
    aviFileList{1,i} = [path aviFiles(i).name];
end

end