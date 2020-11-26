%% MLspike and autocalibration demo
% This script demonstrates on simulated data how to use the MLspike and
% autocalibration algorithms. To see how to run the algorithms, go directly
% to section 'Spike estimation'. 

%% Generate spikes
% We first generate some simulated data. Spike trains are generated using
% spk_gentrain function (the data consists of 6 trials of 30s).
%
% Note the usefull function spk_display to display both spikes and calcium
% time courses.



%% file search

cnt = 0; extension = '.csv'
for i = 1:1 % 몇개할건지 적음.
    try load .dir.mat; catch; dir_nm = [cd(), filesep];  end     
    [file_nm, dir_nm] = uigetfile(fullfile(dir_nm, '*.csv'));
    filepath = [dir_nm, file_nm];
    
    FileList = msCamVideoFileDetection(dir_nm, extension);
    
    for j = 1:size(FileList,2)
        cnt = cnt +1;
    	path_save{cnt,1} = cell2mat(FileList(j));
    end
end

% %% MSBAK: 임의 data import
% file_nm = []; path = []; [file_nm, path] = uigetfile(fullfile(path, '*.*')); fileName = [path, file_nm]; % deltaF.csv를 선택
% df = readcell(fileName);

% roi = 2; % 우선 test 용으로 ROI 한개만 지정해서 하도록합니다. 원하시면 ROI 번호를 바꾸셔도 됩니다. -> 삭제

%%
for cnt = 1:size(path_save,1)
    %
    % parameters
    ntrial = 6;
    T = 30;
    rate = 1;

    % generate spikes
    spikes = spk_gentrain(rate,T,'bursty','repeat',ntrial);

    % display
%     figure(1)
%     spk_display([],spikes,[])

    amin = .04;
    amax = .1;
    a = amin * exp(rand(1)*log(amax/amin)) % log-uniform distribution 

    taumin = .4;
    taumax = 1.6;
    tau = 0.15; % taumin * exp(rand(1)*log(taumax/taumin))

    sigmamin = .005;
    sigmamax = .05;
    sigma = sigmamin * exp(rand(1)*log(sigmamax/sigmamin))

    % parameters
    FPS = 4.3650966869;
    dt = 1/FPS; % 50Hz acquisition
    pcal = spk_calcium('par');
    pcal.dt = dt;
    pcal.a = a;
    pcal.tau = tau;
    pcal.saturation = .1; % saturation level is fixed
    pcal.sigma = sigma; % noise level
    pcal.drift.parameter = [5 .015]; % drift level (#harmonics and amplitude of them)

    % generate calcium
    calcium = spk_calcium(spikes,pcal);

    % display
%     figure(1)
%     spk_display(dt,spikes,calcium)
%     drawnow
    
    tmp = cell2mat(spikes(1,1));
    clear spikes calcium
    
    %
    filename = cell2mat(path_save(cnt,1))
    df = readcell(filename);

    cnt2 = 0; ixsave = nan([1,size(df,1)]);
    for roi = 1:size(df,1) % missing을 찾는 방법을 모름.. try 구문으로 대체함. 이는 오류를 발생시킬 가능성이 있음. 주의
        try
            mssignal = cell2mat(df(roi,:));
            cnt2 = cnt2 + 1;
            spikes{1,cnt2} = tmp;
            calcium{1,cnt2} = mssignal;
            ixsave(1, cnt2) = roi;
        catch
        end
    end

    par = tps_mlspikes('par');
    par.dt = dt;
    par.a = 0.3; % DF/F for one spike # 0.07
    par.tau = 1; % 1; % decay time constant (second) # 20, 1
    par.saturation = 0.1; % OGB dye saturation
    par.finetune.sigma = .02; % a priori level of noise (if par.finetune.sigma
                              % is left empty, MLspike has a low-level routine 
                              % to try estimating it from the data
    par.drift.parameter = 0.1; % if par.drift parameter is not set, the  # 0.1
                               % algorithm assumes that the baseline remains
                               % flat; it is also possible to tell the
                               % algorithm the value of the baseline by setting
                               % par.F0
    % (do not display graph summary)
    par.dographsummary = false;

    % spike estimation
    [spikest fit drift] = spk_est(calcium,par);

    % display
    % roi가 많아지면 감당이안됨.. 분리하도록 해야 할듯
    % 앞에 6개만 display
%     figure(1)
%     disp('시각화는 최대 6개까지 표시됩니다')
%     dispN = min([size(spikes,2), 6]);
%     spk_display(dt,{spikes(1, 1:dispN) spikest(1, 1:dispN)},{calcium(1, 1:dispN) fit(1, 1:dispN) drift(1, 1:dispN)})
%     set(1,'numbertitle','off','name','MLspike alone')

    tmp = [filename, '_MLSpike_data.mat'];
    savepath = strcat(dir_nm, join(tmp));
    
    save(join(tmp), 'calcium', 'fit', 'drift', 'spikest', 'ixsave', 'dt', '-v6')
    
    figure(1)
    set(gcf, 'Position',  [50, 200, 1800, 700]) % 가로, 세로 위치, (왼쪽아래 기준), 가로 세로 크기
    
    roiNum = 1;
    
    calcium2 = cell2mat(fit(roiNum:roiNum));
    calcium3 = calcium2 - min(calcium2);
    plot(calcium3)
    hold on
    
    spike_ix = cell2mat(spikest(roiNum:roiNum)) * FPS;
    xaxis = zeros(1, size(spike_ix,2));
    for i = 1:size(xaxis ,2)
        xaxis(1,i) = calcium3(int16(spike_ix(1,i)));
    end
    scatter(spike_ix, xaxis)
    tmp = [filename, '_MLSpike_data.png'];
    h = figure(1);
    saveas(h, join(tmp), 'png')
    
%     close
end

% 시각화,
% input 서치 자동화
% 패러미터 최적화
% 시각화 수정

% df 체크












    

