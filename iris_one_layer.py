import tensorflow as tf
import numpy as np

# Translate a list of labels into an array of 0's and one 1.
# i.e.: 4 -> [0,0,0,0,1,0,0,0,0,0]
def one_hot(x, n):
    if type(x) == list:
        x = np.array(x)
    x = x.flatten()
    o_h = np.zeros((len(x), n))
    o_h[np.arange(len(x)), x] = 1
    return o_h


data = np.genfromtxt('iris.data', delimiter=",")
np.random.shuffle(data)
x_data = data[:,0:4].astype('f4')
y_data = one_hot(data[:,4].astype(int), 3)

print y_data

print "\nSome samples..."
for i in range(20):
    print x_data[i], " -> ", y_data[i]
print

x = tf.placeholder("float", [None, 4])
y_ = tf.placeholder("float", [None, 3])

# HIDDEN LAYER --> 4 inputs, 8 neurons
Wh = tf.Variable(np.float32(np.random.rand(4, 8))*0.1)
Bh = tf.Variable(np.float32(np.random.rand(8))*0.1)
Yh = tf.nn.sigmoid(tf.matmul(x, Wh) + Bh)
# OUTPUT LAYER --> 8 inputs, 3 neurons
Wo = tf.Variable(np.float32(np.random.rand(8, 3))*0.1)
Bo = tf.Variable(np.float32(np.random.rand(3))*0.1)
Yo = tf.nn.softmax(tf.matmul(Yh, Wo) + Bo)


# USE LOGARITHMIC FUNCTION (0 to +1) INSTEAD OF tf.square(y_ - y)
#cross_entropy = -tf.reduce_sum(y_*tf.log(Yo))
cross_entropy = tf.reduce_sum(tf.square(y_ - Yo))

train = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

print "----------------------"
print "   Start training...  "
print "----------------------"

batch_size = 20

for step in xrange(1000):
    for jj in xrange(len(x_data) / batch_size):
        batch_xs = x_data[jj*batch_size : jj*batch_size+batch_size]
        batch_ys = y_data[jj*batch_size : jj*batch_size+batch_size]

        sess.run(train, feed_dict={x: batch_xs, y_: batch_ys})
        if step % 50 == 0:
            print "Iteration #:", step, "Error: ", sess.run(cross_entropy, feed_dict={x: batch_xs, y_: batch_ys})
            result = sess.run(Yo, feed_dict={x: batch_xs})
            for b, r in zip(batch_ys, result):
                print b, "-->", r
            print "----------------------------------------------------------------------------------"