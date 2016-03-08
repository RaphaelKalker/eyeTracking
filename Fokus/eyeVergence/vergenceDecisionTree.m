close all; clear all;
data = csvread('pupils.csv',1,0);

tree_cnt = 0;
test_arr = [];
train_arr = [];
num_nodes = [];

% 80% train, 20% test
train_size = floor(size(data,1)*0.8);
test_size = size(data,1) - train_size;

while tree_cnt < 100
    [train, train_i] = datasample(data(:,1:4), train_size,'Replace',false);

    test_i = setdiff(1:size(data,1), train_i);
    test = data(test_i,1:4);

    t = fitctree(train, data(train_i,5));

    test_res = predict(t, test);
    train_res = predict(t, train);
    
    test_truth = data(test_i,5);
    train_truth = data(train_i,5);
    test_cnt = 0;
    train_cnt = 0;
    for i = 1:test_size
        if (test_res(i) == test_truth(i)) == 1
            test_cnt = test_cnt + 1;
        end
    end
    
    for i = 1:train_size
        if (train_res(i) == train_truth(i)) == 1
            train_cnt = train_cnt + 1;
        end
    end
    tree_cnt = tree_cnt + 1;

    test_arr = [test_arr test_cnt/double(test_size)];
    train_arr = [train_arr train_cnt/double(train_size)];
    
    num_nodes = [num_nodes size(t.Children, 1)];
%     disp(tree_cnt)
%     disp(size(t.Children,1))
%     disp(test_cnt)
%     disp(train_cnt)
    
    fName = sprintf('./trees/tree%i.csv', tree_cnt);
    fID = fopen(fName,'w');
    for i=1:size(t.CutPredictor,1)
        r = fprintf(fID,'%s,%.3f,%u,%s\n', t.CutPredictor{i}, t.CutPoint(i), t.IsBranchNode(i), t.NodeClass{i});
    end
    fclose(fID);
end

figure;
subplot(131)
hist(test_arr); title('test data classification accuracy');
subplot(132)
hist(train_arr); title('train data classification accuracy');
subplot(133)
hist(num_nodes); title('number of children in the trees');


