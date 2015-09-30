function [w,trainMSE,testMSE] = regression()

	M = loadData();

	numInstances = size(M,1);
	numAttributes = size(M,2);

	disp('Separating the data');
	X = M(:,1:(numAttributes-1));
	Y = M(:,numAttributes);
	clear M;

	disp('Adding column of ones (bias term)');
	X = [X ones(numInstances,1)];
	
	disp('Separate training and validation set');

	% 80/10/10 split between training/validation/test sets
	trainingSetSize = floor(numInstances * 0.8);
	validationSetSize = floor(numInstances * 0.1);
	testSetSize = numInstances - (trainingSetSize + validationSetSize);

	availableIndices = [1:numInstances];
	trainingSetIndices = availableIndices(randsample(length(availableIndices), trainingSetSize));

	availableIndices = setdiff(availableIndices, trainingSetIndices);
	validationSetIndices = availableIndices(randsample(length(availableIndices), validationSetSize));

	availableIndices = setdiff(availableIndices, validationSetIndices);
	testSetIndices = availableIndices;
	
	trainingX = X(trainingSetIndices, :);
	trainingY = Y(trainingSetIndices, :);
	validationX = X(validationSetIndices, :);
	validationY = Y(validationSetIndices, :);
	testX = X(testSetIndices, :);
	testY = Y(testSetIndices, :);
	
	disp('Looking for best lambda');
	bestLambda = 0;
	bestError = Inf;
	lambdas = [];
	errors = [];
	for i = [-10:10]
		
		lambda = 10^i;
		disp(['Lambda: 10e' num2str(i)]);
	
		[w, mse] = compute(trainingX, trainingY, lambda);
	
		if mse < bestError
			bestError = mse;
			bestLambda = lambda;
		end

		lambdas = [lambdas lambda];
		errors = [errors mse];
	
	end
	
	% Display parameters with the best error
	bestLambda
	bestError
	
	[w, trainMSE] = compute([trainingX; validationX], [trainingY; validationY], lambda);

	diff = testX*w - testY;
	testMSE = transpose(diff)*diff/testSetSize

	% Generating graphs
	% Error vs lambda
	%plot(log(lambdas), log(errors));
	%xlabel('log(lambda)');
	%ylabel('log(mean squared error)');

	% Predicted vs actual scores
	%scatter(log(Y), log(X*w));
end

function ret = loadData()
	disp('Loading data');
	ret=csvread('OnlineNewsPopularity.csv', 1, 1);
	%ret=csvread('reddit_full_data.csv', 0, 0);
	%ret=csvread('reddit_full_data_alternate.csv', 0, 0);
end

function [w, mse] = compute(X, Y, lambda)
	numInstances = size(X,1);
	numAttributes = size(X,2);
	w = inv(transpose(X)*X+eye(numAttributes)*lambda)*(transpose(X)*Y); % Ridge regression
	w = zeros(numAttributes,1);
	diff = X*w-Y;
	mse = (transpose(diff)*diff)/numInstances;
end
