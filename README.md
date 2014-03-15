git-commit-log-extractor
========================

Uses libgit2 python wrapper to extract various information regarding git commit logs.

Requires libgit2 and the pygit2 python wrapper

To install follow this: http://www.pygit2.org/install.html.

Excerpt

The following recipe shows how to install libgit2 and pygit2 on these systems. First,
download and install libgit2 (following the instructions in the libgit2 README.md):

>$ git clone -b master git://github.com/libgit2/libgit2.git
>$ mkdir libgit2/build
>$ cd libgit2/build
>$ cmake ..
>$ cmake --build .
>$ sudo cmake --build . --target install
>$ cd ../..

Now, download and install pygit2. You will probably have to set the LIBGIT2 environment
variable so the compiler can find the libgit2 headers and libraries:

>$ git clone git://github.com/libgit2/pygit2.git
>$ cd pygit2
>$ export LIBGIT2="/usr/local"
>$ export LDFLAGS="-Wl,-rpath='$LIBGIT2/lib',--enable-new-dtags $LDFLAGS"
>$ python setup.py build
>$ sudo python setup.py install

Note that to compile pygit2, the python source is needed. Install python source doing the following:

>$ sudo apt-get install python-dev

You can also specify the version of python you like by doing, for example:

>$ sudo apt-get install python3.3-dev