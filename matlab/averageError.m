trainMSE = [];
testMSE = [];

for i=1:30             
	[w,mse1,mse2] = regression();
	trainMSE = [trainMSE mse1];           
	testMSE = [testMSE mse2];           
end

disp('-------------------- Final Results -------------------- ')

disp('Training MSE:');
mean(trainMSE)
disp('Testing MSE:');
mean(testMSE)
