# qd
quickdraw - a cli plotting tool

## Basic Usage

Make a quick plot using the first columns available.

![qd-basic](./media/qd_basic.gif)

Plot the mean values in some bins specifying the x and y columns.

![qd-mean](./media/qd_mean.gif)



plot mean values specifying multiple columns

cat trig.json | qd -x x -y sin,cos --mean | imgcat)
