% Plot the result of `secretOp` in MATLAB
data = csvread('output');
x = data(:, 1);
y = data(:, 2);
z = data(:, 3);
plot(x, z);
